"""Learning Unit Generator - Creates complete learning units from a single prompt."""
from typing import Dict, Any, Optional
from app.llm_providers import LLMProvider, LLMFactory
from app.services import EducationalService
from app.config import settings
import re


class LearningUnitGenerator:
    """Generates complete learning units with explanations, quizzes, practice, and study plans."""

    def __init__(self, provider: Optional[LLMProvider] = None):
        """Initialize the learning unit generator."""
        if provider is None:
            provider_name = settings.default_llm_provider
            self.provider = LLMFactory.create_provider(provider_name)
        else:
            self.provider = provider

        self.service = EducationalService(provider=self.provider)

    async def generate_learning_unit(self, user_prompt: str) -> Dict[str, Any]:
        """Generate a complete learning unit from a user's natural language prompt.

        Args:
            user_prompt: Natural language description of what the user wants to learn

        Returns:
            Dictionary containing:
                - topic: Extracted topic
                - level: Detected difficulty level
                - explanation: Detailed explanation
                - quiz: Generated quiz with questions
                - practice: Practice problems
                - study_plan: Structured study plan
                - validation: Content validation metadata
                - provider: LLM provider used
        """
        # Step 1: Analyze the user prompt to extract topic, level, and intent
        analysis = await self._analyze_prompt(user_prompt)

        topic = analysis['topic']
        level = analysis['level']
        duration_weeks = analysis.get('duration_weeks', 2)

        # Step 2: Generate the learning unit components in parallel where possible
        # We'll generate them sequentially but could optimize with asyncio.gather

        # Generate explanation with validation
        explanation_result = await self.service.explain_concept(
            concept=topic,
            level=level
        )
        explanation = explanation_result['explanation']
        validation = explanation_result['validation']

        # Generate quiz
        quiz = await self.service.generate_quiz(
            topic=topic,
            num_questions=5,
            difficulty=self._map_level_to_difficulty(level)
        )

        # Generate practice problems
        practice = await self.service.practice_problems(
            topic=topic,
            num_problems=3,
            difficulty=self._map_level_to_difficulty(level)
        )

        # Generate study plan
        study_plan = await self.service.generate_study_plan(
            subject=topic,
            duration_weeks=duration_weeks,
            hours_per_week=5
        )

        # Combine everything into a complete learning unit
        learning_unit = {
            "topic": topic,
            "level": level,
            "explanation": explanation,
            "quiz": quiz,
            "practice": practice,
            "study_plan": study_plan,
            "validation": validation,
            "provider": self.provider.get_provider_name()
        }

        return learning_unit

    async def _analyze_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """Analyze user prompt to extract topic, level, and other parameters.

        Args:
            user_prompt: User's natural language request

        Returns:
            Dictionary with extracted parameters
        """
        # Use LLM to intelligently parse the user's request
        system_prompt = """You are an educational assistant that analyzes student requests.
Extract the following information from the student's request:
1. Main topic they want to learn
2. Difficulty level (beginner/intermediate/advanced)
3. Duration if specified (in weeks)
4. Any specific focus areas

Return ONLY a JSON object with this structure:
{
    "topic": "main topic",
    "level": "beginner/intermediate/advanced",
    "duration_weeks": 2,
    "focus_areas": ["area1", "area2"]
}"""

        prompt = f"""Analyze this learning request and extract the key information:

"{user_prompt}"

Return the JSON analysis."""

        try:
            response = await self.provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=500
            )

            # Extract JSON from response
            response = response.strip()
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()

            import json
            analysis = json.loads(response)

            # Validate and set defaults
            if 'topic' not in analysis or not analysis['topic']:
                # Fallback: try to extract topic from prompt
                analysis['topic'] = self._extract_topic_fallback(user_prompt)

            if 'level' not in analysis:
                analysis['level'] = 'intermediate'

            if 'duration_weeks' not in analysis:
                analysis['duration_weeks'] = 2

            return analysis

        except Exception as e:
            # Fallback to simple extraction if LLM fails
            return {
                "topic": self._extract_topic_fallback(user_prompt),
                "level": self._detect_level_fallback(user_prompt),
                "duration_weeks": self._extract_duration_fallback(user_prompt)
            }

    def _extract_topic_fallback(self, user_prompt: str) -> str:
        """Extract topic using simple heuristics as fallback."""
        # Remove common phrases
        text = user_prompt.lower()
        text = re.sub(r'(אני רוצה ללמוד|תכין לי|אני צריך ללמוד|לימוד על|תלמד אותי|יחידת לימוד)', '', text)
        text = re.sub(r'(i want to learn|teach me|learn about|study|learning unit)', '', text)

        # Take first meaningful phrase
        words = text.strip().split()
        if len(words) > 0:
            # Take up to first 5 words as topic
            return ' '.join(words[:5])

        return "General Topic"

    def _detect_level_fallback(self, user_prompt: str) -> str:
        """Detect difficulty level using keywords."""
        text = user_prompt.lower()

        beginner_keywords = ['beginner', 'basic', 'intro', 'בסיסי', 'למתחילים', 'מתחיל', 'פשוט']
        advanced_keywords = ['advanced', 'expert', 'מתקדם', 'מומחה', 'גבוה']

        if any(keyword in text for keyword in beginner_keywords):
            return 'beginner'
        elif any(keyword in text for keyword in advanced_keywords):
            return 'advanced'
        else:
            return 'intermediate'

    def _extract_duration_fallback(self, user_prompt: str) -> int:
        """Extract duration in weeks using regex."""
        # Look for patterns like "2 weeks", "שבועיים", etc.
        weeks_match = re.search(r'(\d+)\s*(weeks?|שבועות?)', user_prompt.lower())
        if weeks_match:
            return int(weeks_match.group(1))

        # Default to 2 weeks
        return 2

    def _map_level_to_difficulty(self, level: str) -> str:
        """Map educational level to quiz difficulty."""
        mapping = {
            'beginner': 'easy',
            'intermediate': 'medium',
            'advanced': 'hard'
        }
        return mapping.get(level.lower(), 'medium')
