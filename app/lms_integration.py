"""LMS Integration Service - Submits learning results to external LMS."""
import httpx
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from app.config import settings

# Configure logging
logger = logging.getLogger("lms_integration")
logger.setLevel(logging.INFO)


class LMSIntegration:
    """Handles integration with external Learning Management System."""

    def __init__(self):
        """Initialize LMS integration."""
        self.api_url = settings.lms_api_url
        self.api_key = settings.lms_api_key
        self.timeout = settings.lms_timeout
        self.enabled = settings.enable_lms_integration

    async def submit_quiz_results(
        self,
        student_id: str,
        guide_name: str,
        quiz_data: Dict[str, Any],
        quiz_answers: List[Dict[str, Any]],
        score: float,
        total_questions: int,
        page_url: str = "",
        guide_chapter: str = "",
        guide_section: str = "",
        guide_task: str = "השלמת מבחן"
    ) -> Dict[str, Any]:
        """Submit quiz results to LMS.

        Args:
            student_id: Student identifier
            guide_name: Name of the learning guide/unit
            quiz_data: Original quiz data
            quiz_answers: Student's answers
            score: Student's score (0-100)
            total_questions: Total number of questions
            page_url: URL of the page
            guide_chapter: Chapter name
            guide_section: Section name
            guide_task: Task description

        Returns:
            Dictionary with success status and LMS response
        """
        if not self.enabled:
            logger.warning("LMS integration is disabled")
            return {
                "success": True,
                "message": "LMS integration disabled - results not submitted",
                "lms_disabled": True
            }

        # Prepare quiz results data
        quiz_results = {
            "score": score,
            "total_questions": total_questions,
            "correct_answers": sum(1 for ans in quiz_answers if ans.get("is_correct", False)),
            "wrong_answers": sum(1 for ans in quiz_answers if not ans.get("is_correct", False)),
            "completion_time": datetime.now().isoformat(),
            "questions": [
                {
                    "question_number": ans.get("question_number", i + 1),
                    "question": ans.get("question", ""),
                    "student_answer": ans.get("student_answer", ""),
                    "correct_answer": ans.get("correct_answer", ""),
                    "is_correct": ans.get("is_correct", False)
                }
                for i, ans in enumerate(quiz_answers)
            ]
        }

        # Prepare submission data in LMS format
        submission_data = {
            "student_id": student_id,
            "guide_name": guide_name,
            "guide_chapter": guide_chapter or f"פרק - {quiz_data.get('topic', 'כללי')}",
            "guide_section": guide_section or f"רמת קושי: {quiz_data.get('difficulty', 'בינונית')}",
            "guide_task": guide_task,
            "page_url": page_url or "EduGenius Learning Platform",
            "form_data": {
                "quiz_topic": quiz_data.get("topic", ""),
                "quiz_difficulty": quiz_data.get("difficulty", ""),
                "score": score,
                "score_percentage": f"{score}%",
                "total_questions": total_questions,
                "correct_answers": quiz_results["correct_answers"],
                "wrong_answers": quiz_results["wrong_answers"],
                "completion_date": quiz_results["completion_time"],
                "provider": quiz_data.get("provider", ""),
                "validation_confidence": quiz_data.get("validation", {}).get("confidence_level", ""),
                "detailed_results": quiz_results
            }
        }

        try:
            # Submit to LMS API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                headers = {
                    "Content-Type": "application/json"
                }

                # Add API key if configured
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"

                response = await client.post(
                    self.api_url,
                    json=submission_data,
                    headers=headers
                )

                response.raise_for_status()
                result = response.json()

                logger.info(f"Successfully submitted quiz results to LMS for student {student_id}")

                return {
                    "success": True,
                    "message": "תוצאות המבחן נשלחו בהצלחה למערכת הלמידה",
                    "lms_response": result,
                    "submission_id": result.get("id", ""),
                    "links": result.get("links", {})
                }

        except httpx.TimeoutException:
            logger.error(f"Timeout submitting to LMS for student {student_id}")
            return {
                "success": False,
                "error": "חריגת זמן בשליחה למערכת הלמידה. נסה שוב מאוחר יותר.",
                "error_type": "timeout"
            }

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error submitting to LMS: {e.response.status_code}")
            return {
                "success": False,
                "error": f"שגיאה בשליחה למערכת הלמידה (קוד {e.response.status_code})",
                "error_type": "http_error",
                "status_code": e.response.status_code
            }

        except Exception as e:
            logger.error(f"Error submitting to LMS: {str(e)}")
            return {
                "success": False,
                "error": f"שגיאה בשליחה למערכת הלמידה: {str(e)}",
                "error_type": "unknown"
            }

    def calculate_quiz_score(
        self,
        quiz_answers: List[Dict[str, Any]],
        quiz_questions: List[Dict[str, Any]]
    ) -> tuple[float, List[Dict[str, Any]]]:
        """Calculate quiz score and detailed results.

        Args:
            quiz_answers: Student's submitted answers
            quiz_questions: Original quiz questions

        Returns:
            Tuple of (score_percentage, detailed_answers)
        """
        if not quiz_questions or not quiz_answers:
            return 0.0, []

        detailed_answers = []
        correct_count = 0

        for i, answer in enumerate(quiz_answers):
            question_data = quiz_questions[i] if i < len(quiz_questions) else {}

            student_answer = answer.get("answer", "")
            correct_answer = question_data.get("correct_answer", "")

            # Normalize answers for comparison (remove "A) ", "B) " etc.)
            student_answer_normalized = student_answer.strip().upper()
            if student_answer_normalized and len(student_answer_normalized) >= 1:
                student_answer_normalized = student_answer_normalized[0]

            correct_answer_normalized = correct_answer.strip().upper()
            if correct_answer_normalized and len(correct_answer_normalized) >= 1:
                correct_answer_normalized = correct_answer_normalized[0]

            is_correct = student_answer_normalized == correct_answer_normalized

            if is_correct:
                correct_count += 1

            detailed_answers.append({
                "question_number": i + 1,
                "question": question_data.get("question", ""),
                "student_answer": student_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": question_data.get("explanation", "")
            })

        score_percentage = (correct_count / len(quiz_questions)) * 100 if quiz_questions else 0

        return round(score_percentage, 2), detailed_answers


# Global LMS integration instance
lms_integration = LMSIntegration()
