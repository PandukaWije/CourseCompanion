"""
Discovery Router - Course recommendation agent endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

from services.discovery_agent import DiscoveryAgent

router = APIRouter()


class DiscoveryRequest(BaseModel):
    """Request model for discovery endpoint"""
    message: str
    history: List[Dict] = []


class CourseRecommendation(BaseModel):
    """Model for course recommendation"""
    course_id: str
    title: str
    reason: str


class DiscoveryResponse(BaseModel):
    """Response model for discovery endpoint"""
    message: str
    has_recommendations: bool = False
    recommended_courses: List[CourseRecommendation] = []
    conversation_complete: bool = False


@router.post("/discover", response_model=DiscoveryResponse)
async def discover_courses(request: DiscoveryRequest):
    """
    Run the discovery agent to recommend courses based on user conversation.
    
    The agent will:
    1. Gather information about the user's role and experience
    2. Understand their learning goals
    3. Recommend appropriate courses
    """
    try:
        agent = DiscoveryAgent()
        response = await agent.process_message(
            message=request.message,
            history=request.history
        )
        return response
    except Exception as e:
        # Fallback response for demo
        return DiscoveryResponse(
            message=f"I understand you're looking to learn more. Could you tell me about your current role and what specific skills you'd like to develop?",
            has_recommendations=False,
            recommended_courses=[],
            conversation_complete=False
        )


@router.post("/discover/reset")
async def reset_discovery():
    """Reset the discovery conversation"""
    return {"status": "reset", "message": "Discovery conversation has been reset"}


@router.get("/discover/courses")
async def get_recommendable_courses():
    """Get list of courses available for recommendation"""
    return [
        {
            "course_id": "xm-cloud-101",
            "title": "XM Cloud Fundamentals",
            "keywords": ["developer", "technical", "headless", "cms", "react", "nextjs"],
            "difficulty": "beginner",
            "roles": ["developer", "architect"]
        },
        {
            "course_id": "search-fundamentals",
            "title": "Sitecore Search Fundamentals",
            "keywords": ["search", "indexing", "optimization", "technical"],
            "difficulty": "intermediate",
            "roles": ["developer", "architect", "admin"]
        },
        {
            "course_id": "content-hub-101",
            "title": "Content Hub Basics",
            "keywords": ["content", "marketing", "dam", "assets", "workflow"],
            "difficulty": "beginner",
            "roles": ["marketer", "content author", "admin"]
        }
    ]



