"""
Notes Router - User notes CRUD endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class NoteContent(BaseModel):
    """Request model for note content"""
    content: str


class NoteResponse(BaseModel):
    """Response model for notes"""
    user_id: str
    course_id: str
    content: str
    last_updated: str
    word_count: int


# In-memory storage for demo (replace with MongoDB in production)
notes_storage: dict = {}


def get_storage_key(user_id: str, course_id: str) -> str:
    """Generate storage key for notes"""
    return f"{user_id}:{course_id}"


@router.get("/notes/{user_id}/{course_id}", response_model=NoteResponse)
async def get_notes(user_id: str, course_id: str):
    """
    Get notes for a specific user and course.
    """
    key = get_storage_key(user_id, course_id)
    
    if key not in notes_storage:
        # Return empty notes
        return NoteResponse(
            user_id=user_id,
            course_id=course_id,
            content="",
            last_updated=datetime.utcnow().isoformat(),
            word_count=0
        )
    
    note = notes_storage[key]
    return NoteResponse(
        user_id=user_id,
        course_id=course_id,
        content=note["content"],
        last_updated=note["last_updated"],
        word_count=len(note["content"].split()) if note["content"] else 0
    )


@router.post("/notes/{user_id}/{course_id}", response_model=NoteResponse)
async def create_notes(user_id: str, course_id: str, note: NoteContent):
    """
    Create or replace notes for a specific user and course.
    """
    key = get_storage_key(user_id, course_id)
    
    notes_storage[key] = {
        "content": note.content,
        "last_updated": datetime.utcnow().isoformat()
    }
    
    return NoteResponse(
        user_id=user_id,
        course_id=course_id,
        content=note.content,
        last_updated=notes_storage[key]["last_updated"],
        word_count=len(note.content.split()) if note.content else 0
    )


@router.put("/notes/{user_id}/{course_id}", response_model=NoteResponse)
async def update_notes(user_id: str, course_id: str, note: NoteContent):
    """
    Update notes for a specific user and course.
    """
    key = get_storage_key(user_id, course_id)
    
    notes_storage[key] = {
        "content": note.content,
        "last_updated": datetime.utcnow().isoformat()
    }
    
    return NoteResponse(
        user_id=user_id,
        course_id=course_id,
        content=note.content,
        last_updated=notes_storage[key]["last_updated"],
        word_count=len(note.content.split()) if note.content else 0
    )


@router.delete("/notes/{user_id}/{course_id}")
async def delete_notes(user_id: str, course_id: str):
    """
    Delete notes for a specific user and course.
    """
    key = get_storage_key(user_id, course_id)
    
    if key in notes_storage:
        del notes_storage[key]
    
    return {
        "status": "deleted",
        "user_id": user_id,
        "course_id": course_id
    }


@router.get("/notes/{user_id}")
async def get_all_user_notes(user_id: str):
    """
    Get all notes for a specific user across all courses.
    """
    user_notes = []
    
    for key, note in notes_storage.items():
        if key.startswith(f"{user_id}:"):
            course_id = key.split(":")[1]
            user_notes.append({
                "course_id": course_id,
                "content": note["content"],
                "last_updated": note["last_updated"],
                "word_count": len(note["content"].split()) if note["content"] else 0
            })
    
    return {
        "user_id": user_id,
        "notes": user_notes
    }





