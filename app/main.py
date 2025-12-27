"""Main FastAPI application for EduGenius."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import os

from app.config import settings
from app.llm_providers import LLMFactory
from app.services import EducationalService

# Create FastAPI app
app = FastAPI(
    title="EduGenius",
    description="AI-Powered Educational Assistant with DeepSeek, OpenAI, and Anthropic support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_path), name="static")


# Pydantic models for request validation
class QuizRequest(BaseModel):
    topic: str = Field(..., description="The topic for the quiz")
    num_questions: int = Field(5, ge=1, le=20, description="Number of questions")
    difficulty: str = Field("medium", pattern="^(easy|medium|hard)$")
    provider: Optional[str] = Field(None, pattern="^(openai|anthropic|deepseek)$")


class ConceptRequest(BaseModel):
    concept: str = Field(..., description="The concept to explain")
    level: str = Field("intermediate", pattern="^(beginner|intermediate|advanced)$")
    provider: Optional[str] = Field(None, pattern="^(openai|anthropic|deepseek)$")


class StudyPlanRequest(BaseModel):
    subject: str = Field(..., description="The subject to study")
    duration_weeks: int = Field(4, ge=1, le=52, description="Duration in weeks")
    hours_per_week: int = Field(5, ge=1, le=40, description="Hours per week")
    provider: Optional[str] = Field(None, pattern="^(openai|anthropic|deepseek)$")


class HomeworkRequest(BaseModel):
    question: str = Field(..., description="The homework question")
    subject: Optional[str] = Field(None, description="The subject area")
    provider: Optional[str] = Field(None, pattern="^(openai|anthropic|deepseek)$")


class PracticeRequest(BaseModel):
    topic: str = Field(..., description="The topic for practice problems")
    num_problems: int = Field(3, ge=1, le=10, description="Number of problems")
    difficulty: str = Field("medium", pattern="^(easy|medium|hard)$")
    provider: Optional[str] = Field(None, pattern="^(openai|anthropic|deepseek)$")


# Helper function to get service with specified provider
def get_service(provider_name: Optional[str] = None) -> EducationalService:
    """Get educational service with optional provider override."""
    if provider_name:
        provider = LLMFactory.create_provider(provider_name)
        return EducationalService(provider=provider)
    return EducationalService()


# API Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page."""
    html_file = os.path.join(static_path, "index.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="""
    <html>
        <head><title>EduGenius</title></head>
        <body>
            <h1>EduGenius API is running!</h1>
            <p>Visit <a href="/docs">/docs</a> for API documentation.</p>
        </body>
    </html>
    """)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    available_providers = LLMFactory.get_available_providers()
    return {
        "status": "healthy",
        "version": "1.0.0",
        "providers": available_providers,
        "default_provider": settings.default_llm_provider
    }


@app.get("/api/providers")
async def get_providers():
    """Get available LLM providers."""
    providers = LLMFactory.get_available_providers()
    return {
        "providers": providers,
        "default": settings.default_llm_provider
    }


@app.post("/api/quiz")
async def generate_quiz(request: QuizRequest):
    """Generate a quiz on a given topic."""
    try:
        service = get_service(request.provider)
        quiz = await service.generate_quiz(
            topic=request.topic,
            num_questions=request.num_questions,
            difficulty=request.difficulty
        )
        return quiz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")


@app.post("/api/explain")
async def explain_concept(request: ConceptRequest):
    """Explain a concept with content validation."""
    try:
        service = get_service(request.provider)
        result = await service.explain_concept(
            concept=request.concept,
            level=request.level
        )
        return {
            "concept": request.concept,
            "level": request.level,
            "explanation": result["explanation"],
            "provider": service.provider.get_provider_name(),
            "validation": result["validation"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error explaining concept: {str(e)}")


@app.post("/api/study-plan")
async def create_study_plan(request: StudyPlanRequest):
    """Generate a personalized study plan."""
    try:
        service = get_service(request.provider)
        plan = await service.generate_study_plan(
            subject=request.subject,
            duration_weeks=request.duration_weeks,
            hours_per_week=request.hours_per_week
        )
        return plan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating study plan: {str(e)}")


@app.post("/api/homework-help")
async def homework_help(request: HomeworkRequest):
    """Get homework help."""
    try:
        service = get_service(request.provider)
        help_text = await service.get_homework_help(
            question=request.question,
            subject=request.subject
        )
        return {
            "question": request.question,
            "subject": request.subject,
            "help": help_text,
            "provider": service.provider.get_provider_name()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error providing homework help: {str(e)}")


@app.post("/api/practice")
async def generate_practice(request: PracticeRequest):
    """Generate practice problems."""
    try:
        service = get_service(request.provider)
        problems = await service.practice_problems(
            topic=request.topic,
            num_problems=request.num_problems,
            difficulty=request.difficulty
        )
        return {
            "topic": request.topic,
            "difficulty": request.difficulty,
            "problems": problems,
            "provider": service.provider.get_provider_name()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating practice problems: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
