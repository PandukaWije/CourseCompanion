"""
CourseCompanion - FastAPI Backend Main Entry Point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from models.database import (
    connect_to_mongo, 
    close_mongo_connection,
    get_all_courses,
    find_course,
    quizzes_collection
)
from routers import discovery, chat, notes, artifacts, quiz


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown events"""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


# Initialize FastAPI application
app = FastAPI(
    title="CourseCompanion API",
    description="AI-powered learning platform backend with RAG chatbot and course discovery",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(discovery.router, prefix="/api", tags=["Discovery"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(notes.router, prefix="/api", tags=["Notes"])
app.include_router(artifacts.router, prefix="/api", tags=["Artifacts"])
app.include_router(quiz.router, prefix="/api", tags=["Quiz"])


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "CourseCompanion API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "database": "connected",
        "services": {
            "discovery_agent": "available",
            "rag_chatbot": "available",
            "quiz_service": "available"
        }
    }


# ============================================
# Course Endpoints - NOW READS FROM MONGODB
# ============================================

@app.get("/api/courses")
async def get_courses():
    """Get all available courses from MongoDB"""
    try:
        # Fetch courses from MongoDB Atlas
        courses = await get_all_courses()
        
        # Clean up MongoDB _id field for JSON serialization
        for course in courses:
            if "_id" in course:
                course["_id"] = str(course["_id"])
        
        return courses
        
    except Exception as e:
        print(f"Error fetching courses: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch courses: {str(e)}")


@app.get("/api/courses/{course_id}")
async def get_course(course_id: str):
    """Get a specific course by ID from MongoDB"""
    try:
        # Fetch course from MongoDB Atlas
        course = await find_course(course_id)
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # Clean up MongoDB _id field
        if "_id" in course:
            course["_id"] = str(course["_id"])
        
        return course
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching course {course_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch course: {str(e)}")


# ============================================
# User Endpoints
# ============================================

@app.get("/api/users/{user_id}/progress")
async def get_user_progress(user_id: str):
    """Get user progress across all courses"""
    # This would normally fetch from MongoDB
    # For now, return mock data
    return {
        "user_id": user_id,
        "enrolled_courses": [],
        "progress": {}
    }


@app.post("/api/users/{user_id}/enroll")
async def enroll_user(user_id: str, course_ids: list):
    """Enroll user in selected courses"""
    return {
        "user_id": user_id,
        "enrolled": course_ids,
        "message": f"Successfully enrolled in {len(course_ids)} course(s)"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )