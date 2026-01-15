"""
MongoDB Database Connection and Collection Management
"""
import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)

# Global database client and database instances
_client: Optional[AsyncIOMotorClient] = None
_database: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo():
    """
    Connect to MongoDB Atlas.
    
    Uses environment variables:
    - MONGODB_URI: MongoDB connection string
    - MONGODB_DB_NAME: Database name
    """
    global _client, _database
    
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "coursecompanion")
    
    try:
        _client = AsyncIOMotorClient(mongodb_uri)
        _database = _client[db_name]
        
        # Test connection
        await _client.admin.command("ping")
        logger.info(f"Connected to MongoDB: {db_name}")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close the MongoDB connection"""
    global _client, _database
    
    if _client:
        _client.close()
        _client = None
        _database = None
        logger.info("Closed MongoDB connection")


def get_database() -> AsyncIOMotorDatabase:
    """Get the database instance"""
    if _database is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo first.")
    return _database


async def create_indexes():
    """Create necessary indexes for collections"""
    db = get_database()
    
    # Users collection indexes
    await db.users.create_index("user_id", unique=True)
    
    # Courses collection indexes
    await db.courses.create_index("course_id", unique=True)
    
    # Knowledge base collection indexes
    await db.knowledge_base.create_index("course_id")
    await db.knowledge_base.create_index("chunk_id", unique=True)
    # Note: Vector search index must be created via Atlas UI or API
    
    # Conversations collection indexes
    await db.conversations.create_index([("user_id", 1), ("course_id", 1)])
    await db.conversations.create_index("session_id")
    
    # Quiz results collection indexes
    await db.quiz_results.create_index([("user_id", 1), ("course_id", 1)])
    
    # Notes collection indexes
    await db.notes.create_index([("user_id", 1), ("course_id", 1)], unique=True)
    
    logger.info("Created database indexes")


# ==================== Collection Accessors ====================

def users_collection():
    """Get the users collection"""
    return get_database().users


def courses_collection():
    """Get the courses collection"""
    return get_database().courses


def knowledge_base_collection():
    """Get the knowledge base collection"""
    return get_database().knowledge_base


def conversations_collection():
    """Get the conversations collection"""
    return get_database().conversations


def quizzes_collection():
    """Get the quizzes collection"""
    return get_database().quizzes


def quiz_results_collection():
    """Get the quiz results collection"""
    return get_database().quiz_results


def notes_collection():
    """Get the notes collection"""
    return get_database().notes


def artifacts_collection():
    """Get the artifacts collection"""
    return get_database().artifacts


# ==================== CRUD Helpers ====================

async def find_user(user_id: str) -> Optional[dict]:
    """Find a user by user_id"""
    return await users_collection().find_one({"user_id": user_id})


async def create_user(user_data: dict) -> str:
    """Create a new user"""
    result = await users_collection().insert_one(user_data)
    return str(result.inserted_id)


async def update_user(user_id: str, update_data: dict) -> bool:
    """Update a user document"""
    result = await users_collection().update_one(
        {"user_id": user_id},
        {"$set": update_data}
    )
    return result.modified_count > 0


async def find_course(course_id: str) -> Optional[dict]:
    """Find a course by course_id"""
    return await courses_collection().find_one({"course_id": course_id})


async def get_all_courses() -> list:
    """Get all courses"""
    cursor = courses_collection().find({})
    return await cursor.to_list(length=100)


async def find_knowledge_chunks(course_id: str, limit: int = 10) -> list:
    """Find knowledge base chunks for a course"""
    cursor = knowledge_base_collection().find({"course_id": course_id}).limit(limit)
    return await cursor.to_list(length=limit)


async def save_conversation(conversation_data: dict) -> str:
    """Save a conversation"""
    result = await conversations_collection().insert_one(conversation_data)
    return str(result.inserted_id)


async def find_conversation(user_id: str, course_id: str = None, session_id: str = None) -> Optional[dict]:
    """Find a conversation by user_id and optionally course_id or session_id"""
    query = {"user_id": user_id}
    if course_id:
        query["course_id"] = course_id
    if session_id:
        query["session_id"] = session_id
    return await conversations_collection().find_one(query)


async def save_quiz_result(result_data: dict) -> str:
    """Save a quiz result"""
    result = await quiz_results_collection().insert_one(result_data)
    return str(result.inserted_id)


async def find_quiz_result(user_id: str, course_id: str) -> Optional[dict]:
    """Find quiz result for a user and course"""
    return await quiz_results_collection().find_one({
        "user_id": user_id,
        "course_id": course_id
    })


async def save_note(user_id: str, course_id: str, content: str) -> bool:
    """Save or update user notes"""
    result = await notes_collection().update_one(
        {"user_id": user_id, "course_id": course_id},
        {
            "$set": {
                "content": content,
                "word_count": len(content.split()) if content else 0,
                "updated_at": __import__("datetime").datetime.utcnow()
            },
            "$setOnInsert": {
                "created_at": __import__("datetime").datetime.utcnow()
            }
        },
        upsert=True
    )
    return result.acknowledged


async def find_note(user_id: str, course_id: str) -> Optional[dict]:
    """Find notes for a user and course"""
    return await notes_collection().find_one({
        "user_id": user_id,
        "course_id": course_id
    })



