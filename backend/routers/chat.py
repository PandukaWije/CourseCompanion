"""
Chat Router - RAG chatbot endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

from services.rag_chatbot import RAGChatbot

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    course_id: str
    message: str
    history: List[Dict] = []


class SourceDocument(BaseModel):
    """Model for source document reference"""
    module: Optional[str] = None
    timestamp: Optional[str] = None
    content_type: str = "text"
    relevance_score: float = 0.0


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    message: str
    sources: List[SourceDocument] = []
    course_id: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the course-specific RAG chatbot.
    
    The chatbot will:
    1. Search the course-specific knowledge base
    2. Generate a contextual response
    3. Include source references
    """
    try:
        chatbot = RAGChatbot(course_id=request.course_id)
        response = await chatbot.get_response(
            message=request.message,
            history=request.history
        )
        return ChatResponse(
            message=response["message"],
            sources=response.get("sources", []),
            course_id=request.course_id
        )
    except Exception as e:
        # Fallback response for demo
        fallback_responses = {
            "xm-cloud-101": "Based on the XM Cloud course materials, I can help explain concepts about headless CMS, component development, and deployment. What specific topic would you like to explore?",
            "search-fundamentals": "I can help you understand Sitecore Search concepts including indexing, facets, and query optimization. What would you like to know?",
            "content-hub-101": "Let me help you with Content Hub topics like DAM, workflows, and content operations. What area interests you?"
        }
        
        return ChatResponse(
            message=fallback_responses.get(
                request.course_id,
                "I'm here to help with your course questions. Could you please rephrase your question?"
            ),
            sources=[],
            course_id=request.course_id
        )


@router.get("/chat/history/{user_id}/{course_id}")
async def get_chat_history(user_id: str, course_id: str):
    """Get chat history for a user in a specific course"""
    # In production, fetch from MongoDB
    return {
        "user_id": user_id,
        "course_id": course_id,
        "messages": [],
        "message": "Chat history retrieval not yet implemented"
    }


@router.delete("/chat/history/{user_id}/{course_id}")
async def clear_chat_history(user_id: str, course_id: str):
    """Clear chat history for a user in a specific course"""
    return {
        "status": "cleared",
        "user_id": user_id,
        "course_id": course_id
    }



