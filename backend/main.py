"""
CourseCompanion - FastAPI Backend Main Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from models.local_storage import initialize_storage, close_storage
from routers import discovery, chat, notes, artifacts, quiz


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown events"""
    # Startup
    await initialize_storage()
    yield
    # Shutdown
    await close_storage()


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
        "storage": "local_json",
        "services": {
            "discovery_agent": "available",
            "rag_chatbot": "available",
            "quiz_service": "available"
        }
    }


# Course endpoints (simple CRUD - not in separate router for simplicity)
@app.get("/api/courses")
async def get_courses():
    """Get all available courses"""
    # Mock data - in production, fetch from MongoDB
    return [
        {
            "course_id": "xm-cloud-101",
            "title": "XM Cloud Fundamentals",
            "description": "Learn the basics of XM Cloud architecture and implementation",
            "difficulty": "Beginner",
            "duration": "4 hours",
            "modules": 5,
            "topics": ["architecture", "development", "deployment"]
        },
        {
            "course_id": "search-fundamentals",
            "title": "Sitecore Search Fundamentals",
            "description": "Master Sitecore Search configuration and optimization",
            "difficulty": "Intermediate",
            "duration": "3 hours",
            "modules": 4,
            "topics": ["indexing", "facets", "optimization"]
        },
        {
            "course_id": "content-hub-101",
            "title": "Content Hub Basics",
            "description": "Introduction to Sitecore Content Hub DAM and CMP",
            "difficulty": "Beginner",
            "duration": "5 hours",
            "modules": 6,
            "topics": ["dam", "cmp", "workflows", "integration"]
        }
    ]


@app.get("/api/courses/{course_id}")
async def get_course(course_id: str):
    """Get a specific course by ID"""
    courses = {
        "xm-cloud-101": {
            "course_id": "xm-cloud-101",
            "title": "XM Cloud Fundamentals",
            "description": "Learn the basics of XM Cloud architecture and implementation",
            "difficulty": "Beginner",
            "duration": "4 hours",
            "modules": [
                {"id": 1, "title": "Introduction to XM Cloud", "duration": "15 min"},
                {"id": 2, "title": "Architecture Overview", "duration": "20 min"},
                {"id": 3, "title": "Setting Up Your Environment", "duration": "25 min"},
                {"id": 4, "title": "Component Development", "duration": "30 min"},
                {"id": 5, "title": "Deployment & Publishing", "duration": "20 min"}
            ]
        },
        "search-fundamentals": {
            "course_id": "search-fundamentals",
            "title": "Sitecore Search Fundamentals",
            "description": "Master Sitecore Search configuration and optimization",
            "difficulty": "Intermediate",
            "duration": "3 hours",
            "modules": [
                {"id": 1, "title": "Search Architecture", "duration": "20 min"},
                {"id": 2, "title": "Indexing Strategies", "duration": "25 min"},
                {"id": 3, "title": "Query Optimization", "duration": "20 min"},
                {"id": 4, "title": "Faceted Search", "duration": "15 min"}
            ]
        },
        "content-hub-101": {
            "course_id": "content-hub-101",
            "title": "Content Hub Basics",
            "description": "Introduction to Sitecore Content Hub DAM and CMP",
            "difficulty": "Beginner",
            "duration": "5 hours",
            "modules": [
                {"id": 1, "title": "Content Hub Overview", "duration": "15 min"},
                {"id": 2, "title": "Asset Management", "duration": "25 min"},
                {"id": 3, "title": "Content Operations", "duration": "20 min"},
                {"id": 4, "title": "Integration Patterns", "duration": "30 min"},
                {"id": 5, "title": "Workflows & Approvals", "duration": "20 min"},
                {"id": 6, "title": "Reporting & Analytics", "duration": "15 min"}
            ]
        }
    }
    
    if course_id not in courses:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Course not found")
    
    return courses[course_id]


# User endpoints
@app.get("/api/users/{user_id}/progress")
async def get_user_progress(user_id: str):
    """Get user progress across all courses"""
    # Mock data
    return {
        "user_id": user_id,
        "enrolled_courses": ["xm-cloud-101", "search-fundamentals"],
        "progress": {
            "xm-cloud-101": {
                "completed_modules": [1, 2],
                "quiz_score": None,
                "last_accessed": "2024-01-15T10:30:00Z"
            },
            "search-fundamentals": {
                "completed_modules": [1],
                "quiz_score": None,
                "last_accessed": "2024-01-14T15:45:00Z"
            }
        }
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



