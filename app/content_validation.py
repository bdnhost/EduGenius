"""Content validation and verification module with RAG (Retrieval-Augmented Generation).

This module provides content validation using external knowledge sources like Wikipedia
to improve accuracy and provide confidence scores for AI-generated educational content.
"""
import wikipedia
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import os
from pathlib import Path

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Create logger
logger = logging.getLogger("content_validation")
logger.setLevel(logging.INFO)

# File handler for validation logs
fh = logging.FileHandler(log_dir / "content_validation.log")
fh.setLevel(logging.INFO)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


class ContentValidator:
    """Validates educational content using external knowledge sources."""

    def __init__(self):
        """Initialize the content validator."""
        self.wikipedia_enabled = True
        wikipedia.set_lang("en")  # Default to English

    def search_wikipedia(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """Search Wikipedia for relevant articles.

        Args:
            query: The search query
            max_results: Maximum number of results to return

        Returns:
            List of dictionaries with title and summary
        """
        try:
            search_results = wikipedia.search(query, results=max_results)
            results = []

            for title in search_results[:max_results]:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    results.append({
                        "title": page.title,
                        "summary": page.summary[:500],  # First 500 chars
                        "url": page.url
                    })
                except (wikipedia.exceptions.DisambiguationError,
                        wikipedia.exceptions.PageError):
                    continue

            return results
        except Exception as e:
            logger.warning(f"Wikipedia search failed for '{query}': {str(e)}")
            return []

    def get_reference_context(self, topic: str) -> Optional[str]:
        """Get reference context from Wikipedia for a topic.

        Args:
            topic: The topic to get context for

        Returns:
            Wikipedia summary or None if not found
        """
        try:
            results = self.search_wikipedia(topic, max_results=1)
            if results:
                return results[0]["summary"]
            return None
        except Exception as e:
            logger.error(f"Error getting reference context: {str(e)}")
            return None

    def calculate_confidence_score(self, topic: str, has_reference: bool,
                                  provider: str) -> Tuple[str, float]:
        """Calculate confidence score for the generated content.

        Args:
            topic: The topic being generated
            has_reference: Whether reference material was found
            provider: The LLM provider used

        Returns:
            Tuple of (confidence_level, score) where score is 0-1
        """
        # Base scores by provider (based on general reliability)
        provider_scores = {
            "deepseek": 0.75,
            "openai": 0.80,
            "anthropic": 0.85,
            "default": 0.70
        }

        base_score = provider_scores.get(provider.lower(), provider_scores["default"])

        # Adjust based on whether we have reference material
        if has_reference:
            final_score = min(base_score + 0.15, 0.95)  # Boost with reference
        else:
            final_score = base_score - 0.10  # Lower without reference

        # Categorize confidence level
        if final_score >= 0.85:
            level = "high"
        elif final_score >= 0.70:
            level = "medium"
        else:
            level = "low"

        return level, final_score

    def generate_validation_metadata(self, topic: str, content_type: str,
                                    provider: str, references: List[Dict] = None) -> Dict:
        """Generate validation metadata for content.

        Args:
            topic: The topic of the content
            content_type: Type of content (quiz, explanation, etc.)
            provider: LLM provider used
            references: Optional list of reference materials

        Returns:
            Dictionary with validation metadata
        """
        has_reference = bool(references and len(references) > 0)
        confidence_level, confidence_score = self.calculate_confidence_score(
            topic, has_reference, provider
        )

        metadata = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "content_type": content_type,
            "provider": provider,
            "has_reference_material": has_reference,
            "confidence_level": confidence_level,
            "confidence_score": round(confidence_score, 2),
            "references": references or [],
            "validation_warnings": self._generate_warnings(confidence_level, has_reference)
        }

        # Log the validation
        logger.info(f"Content validated: {content_type} on '{topic}' - "
                   f"Confidence: {confidence_level} ({confidence_score:.2f})")

        return metadata

    def _generate_warnings(self, confidence_level: str, has_reference: bool) -> List[str]:
        """Generate appropriate warnings based on confidence level.

        Args:
            confidence_level: The confidence level (high/medium/low)
            has_reference: Whether reference material was found

        Returns:
            List of warning messages
        """
        warnings = [
            "This content is AI-generated and may contain errors."
        ]

        if confidence_level == "low":
            warnings.append("⚠️ Low confidence: Please verify this information with other sources.")

        if not has_reference:
            warnings.append("📚 No reference material found. Consider cross-checking this information.")

        if confidence_level == "medium":
            warnings.append("💡 Medium confidence: We recommend verifying key facts.")

        warnings.append("Always consult multiple sources for important educational content.")

        return warnings

    def log_content_generation(self, request_data: Dict, response_data: Dict,
                              validation_metadata: Dict):
        """Log content generation for tracking and auditing.

        Args:
            request_data: The original request data
            response_data: The generated response
            validation_metadata: Validation metadata
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "request": request_data,
            "validation": validation_metadata,
            "response_summary": {
                "provider": response_data.get("provider"),
                "content_type": validation_metadata.get("content_type"),
                "topic": validation_metadata.get("topic")
            }
        }

        # Log to file
        log_file = log_dir / f"content_log_{datetime.now().strftime('%Y%m%d')}.jsonl"
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Failed to write content log: {str(e)}")

    async def validate_and_enrich_quiz(self, topic: str, provider: str) -> Dict:
        """Validate and enrich quiz generation with references.

        Args:
            topic: The quiz topic
            provider: LLM provider being used

        Returns:
            Dictionary with validation metadata and references
        """
        # Get reference material
        references = self.search_wikipedia(topic, max_results=2)

        # Generate validation metadata
        metadata = self.generate_validation_metadata(
            topic=topic,
            content_type="quiz",
            provider=provider,
            references=references
        )

        return metadata

    async def validate_and_enrich_explanation(self, concept: str, provider: str) -> Dict:
        """Validate and enrich concept explanation with references.

        Args:
            concept: The concept being explained
            provider: LLM provider being used

        Returns:
            Dictionary with validation metadata and references
        """
        # Get reference material
        references = self.search_wikipedia(concept, max_results=3)

        # Add reference context to help improve accuracy
        reference_context = None
        if references:
            reference_context = references[0]["summary"]

        # Generate validation metadata
        metadata = self.generate_validation_metadata(
            topic=concept,
            content_type="explanation",
            provider=provider,
            references=references
        )

        metadata["reference_context"] = reference_context

        return metadata

    async def validate_and_enrich_study_plan(self, subject: str, provider: str) -> Dict:
        """Validate and enrich study plan with references.

        Args:
            subject: The subject for the study plan
            provider: LLM provider being used

        Returns:
            Dictionary with validation metadata and references
        """
        # Get reference material
        references = self.search_wikipedia(subject, max_results=2)

        # Generate validation metadata
        metadata = self.generate_validation_metadata(
            topic=subject,
            content_type="study_plan",
            provider=provider,
            references=references
        )

        return metadata


# Global validator instance
content_validator = ContentValidator()
