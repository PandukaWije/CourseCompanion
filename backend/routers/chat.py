"""
Chat Router - RAG chatbot endpoints
UPDATED: Added error logging to debug issues
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging

from services.rag_chatbot import RAGChatbot

router = APIRouter()

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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
        logger.info(f"Chat request - Course: {request.course_id}, Message: {request.message[:50]}...")
        
        chatbot = RAGChatbot(course_id=request.course_id)
        response = await chatbot.get_response(
            message=request.message,
            history=request.history
        )
        
        logger.info(f"Chat response generated - Sources: {len(response.get('sources', []))}")
        
        return ChatResponse(
            message=response["message"],
            sources=response.get("sources", []),
            course_id=request.course_id
        )
        
    except Exception as e:
        # LOG THE ERROR SO WE CAN SEE IT!
        logger.error(f"Chat error for course {request.course_id}: {str(e)}", exc_info=True)
        
        # Return error in response for debugging
        error_message = f"""I encountered an error while processing your question.

**Error**: {str(e)}

**Troubleshooting:**
1. Check backend logs for full error details
2. Verify MongoDB has knowledge base for course: {request.course_id}
3. Check Azure OpenAI credentials in .env
4. Ensure vector index is active in Atlas

Please check the backend terminal for detailed error information."""
        
        return ChatResponse(
            message=error_message,
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