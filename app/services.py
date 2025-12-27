"""Educational services using LLM providers."""
from typing import Dict, List, Any, Optional
from app.llm_providers import LLMProvider, LLMFactory
from app.config import settings
import json


class EducationalService:
    """Service class for educational features."""

    def __init__(self, provider: Optional[LLMProvider] = None):
        """Initialize the educational service with an LLM provider."""
        if provider is None:
            provider_name = settings.default_llm_provider
            self.provider = LLMFactory.create_provider(provider_name)
        else:
            self.provider = provider

    async def generate_quiz(self, topic: str, num_questions: int = 5,
                          difficulty: str = "medium") -> Dict[str, Any]:
        """Generate a quiz on a given topic."""
        system_prompt = """You are an expert educational content creator.
Generate quizzes in valid JSON format only. Do not include any additional text or explanation.
The JSON must have this exact structure:
{
    "topic": "topic name",
    "difficulty": "easy/medium/hard",
    "questions": [
        {
            "question": "question text",
            "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
            "correct_answer": "A",
            "explanation": "why this is correct"
        }
    ]
}"""

        prompt = f"""Create a {difficulty} level quiz about "{topic}" with exactly {num_questions} multiple choice questions.
Each question should have 4 options (A, B, C, D).
Return ONLY valid JSON with no additional text."""

        try:
            response = await self.provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )

            # Try to extract JSON from response
            response = response.strip()
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()

            quiz_data = json.loads(response)
            quiz_data["provider"] = self.provider.get_provider_name()
            return quiz_data

        except json.JSONDecodeError as e:
            # If JSON parsing fails, return a structured error
            return {
                "topic": topic,
                "difficulty": difficulty,
                "error": "Failed to parse quiz data",
                "provider": self.provider.get_provider_name(),
                "questions": []
            }
        except Exception as e:
            raise Exception(f"Error generating quiz: {str(e)}")

    async def explain_concept(self, concept: str, level: str = "intermediate") -> str:
        """Explain a concept at the specified level."""
        system_prompt = f"""You are an expert educator. Explain concepts clearly and effectively
for {level} level students. Use examples, analogies, and structured explanations."""

        prompt = f"""Explain the concept of "{concept}" in a clear and engaging way.
Include:
1. A simple definition
2. Key points or characteristics
3. Real-world examples or applications
4. Common misconceptions (if any)

Keep the explanation suitable for {level} level students."""

        try:
            explanation = await self.provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            return explanation
        except Exception as e:
            raise Exception(f"Error explaining concept: {str(e)}")

    async def generate_study_plan(self, subject: str, duration_weeks: int = 4,
                                 hours_per_week: int = 5) -> Dict[str, Any]:
        """Generate a personalized study plan."""
        system_prompt = """You are an expert educational planner. Create realistic and
effective study plans in valid JSON format."""

        prompt = f"""Create a {duration_weeks}-week study plan for learning "{subject}".
The student can dedicate {hours_per_week} hours per week.

Return a JSON object with this structure:
{{
    "subject": "subject name",
    "duration_weeks": {duration_weeks},
    "hours_per_week": {hours_per_week},
    "weeks": [
        {{
            "week": 1,
            "focus": "week focus area",
            "topics": ["topic1", "topic2"],
            "activities": ["activity1", "activity2"],
            "goals": ["goal1", "goal2"]
        }}
    ],
    "resources": ["resource1", "resource2"],
    "tips": ["tip1", "tip2"]
}}

Return ONLY valid JSON."""

        try:
            response = await self.provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=3000
            )

            # Try to extract JSON from response
            response = response.strip()
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()

            plan_data = json.loads(response)
            plan_data["provider"] = self.provider.get_provider_name()
            return plan_data

        except json.JSONDecodeError:
            return {
                "subject": subject,
                "duration_weeks": duration_weeks,
                "hours_per_week": hours_per_week,
                "error": "Failed to parse study plan",
                "provider": self.provider.get_provider_name(),
                "weeks": []
            }
        except Exception as e:
            raise Exception(f"Error generating study plan: {str(e)}")

    async def get_homework_help(self, question: str, subject: Optional[str] = None) -> str:
        """Provide homework help and guidance."""
        system_prompt = """You are a helpful tutor. Guide students to understand problems
rather than just giving answers. Use the Socratic method when appropriate."""

        subject_context = f" (Subject: {subject})" if subject else ""
        prompt = f"""A student needs help with this question{subject_context}:

"{question}"

Provide guidance that:
1. Helps them understand the concept
2. Breaks down the problem into steps
3. Gives hints rather than direct answers
4. Encourages critical thinking
5. Provides a final answer only after explanation"""

        try:
            help_text = await self.provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=2000
            )
            return help_text
        except Exception as e:
            raise Exception(f"Error providing homework help: {str(e)}")

    async def practice_problems(self, topic: str, num_problems: int = 3,
                              difficulty: str = "medium") -> List[Dict[str, str]]:
        """Generate practice problems for a topic."""
        system_prompt = """You are an expert educator creating practice problems.
Return valid JSON format only."""

        prompt = f"""Create {num_problems} {difficulty} practice problems about "{topic}".

Return a JSON array with this structure:
[
    {{
        "problem": "problem statement",
        "hints": ["hint1", "hint2"],
        "solution": "detailed solution",
        "difficulty": "{difficulty}"
    }}
]

Return ONLY valid JSON array."""

        try:
            response = await self.provider.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=2500
            )

            # Try to extract JSON from response
            response = response.strip()
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()

            problems = json.loads(response)
            return problems if isinstance(problems, list) else []

        except json.JSONDecodeError:
            return []
        except Exception as e:
            raise Exception(f"Error generating practice problems: {str(e)}")
