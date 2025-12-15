"""FastAPI routes for skill agents."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Import main agent with unified skills
from main_agents import main_agent

# Request Models
class GlossaryRequest(BaseModel):
    """Request model for glossary skill."""
    term: str = Field(..., min_length=1, max_length=200, description="Technical term to define")


class DiagramRequest(BaseModel):
    """Request model for diagram skill."""
    topic: str = Field(..., min_length=1, max_length=200, description="Topic to diagram")


class TranslateRequest(BaseModel):
    """Request model for translation skill."""
    text: str = Field(..., min_length=1, max_length=1000, description="English text to translate")


class ExercisesRequest(BaseModel):
    """Request model for exercises skill."""
    chapter: str = Field(..., min_length=1, max_length=5000, description="Chapter content or topic")


# Response Models
class SkillResponse(BaseModel):
    """Success response model for all skills."""
    result: str = Field(..., description="Generated output from the skill")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")


# Create router with prefix
skills_router = APIRouter(prefix="/api/skills", tags=["skills"])


# Use main_agent's unified skills object
@skills_router.post("/glossary", response_model=SkillResponse)
async def generate_glossary(request: GlossaryRequest):
    """Generate a glossary definition for a technical term."""
    try:
        result = main_agent.skills.glossary.run(query=request.term)
        return SkillResponse(result=result["response"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@skills_router.post("/diagram", response_model=SkillResponse)
async def generate_diagram(request: DiagramRequest):
    """Generate an ASCII diagram for a topic."""
    try:
        result = main_agent.skills.diagrams.run(query=request.topic)
        return SkillResponse(result=result["response"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@skills_router.post("/translate", response_model=SkillResponse)
async def translate_to_urdu(request: TranslateRequest):
    """Translate English text to Urdu."""
    try:
        result = main_agent.skills.translate.run(query=request.text)
        return SkillResponse(result=result["response"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@skills_router.post("/exercises", response_model=SkillResponse)
async def generate_exercises(request: ExercisesRequest):
    """Generate practice exercises from chapter content."""
    try:
        result = main_agent.skills.exercises.run(query=request.chapter)
        return SkillResponse(result=result["response"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
