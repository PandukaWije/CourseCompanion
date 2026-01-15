"""
Database Seeding Script
Populates MongoDB with initial course data, quizzes, and knowledge base chunks.
"""
import asyncio
import json
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def get_database():
    """Connect to MongoDB and return database instance"""
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "coursecompanion")
    
    client = AsyncIOMotorClient(mongodb_uri)
    return client[db_name]


async def seed_courses(db):
    """Seed courses collection"""
    print("📚 Seeding courses...")
    
    # Load course catalog
    catalog_path = Path(__file__).parent.parent / "data" / "courses" / "course_catalog.json"
    
    with open(catalog_path, "r") as f:
        catalog = json.load(f)
    
    courses = catalog.get("courses", [])
    
    # Clear existing courses
    await db.courses.delete_many({})
    
    # Insert courses
    for course in courses:
        course["created_at"] = datetime.utcnow()
        await db.courses.insert_one(course)
        print(f"  ✓ Added course: {course['title']}")
    
    print(f"  Total: {len(courses)} courses seeded")


async def seed_knowledge_base(db):
    """Seed knowledge base collection with course content chunks"""
    print("🧠 Seeding knowledge base...")
    
    knowledge_base_dir = Path(__file__).parent.parent / "data" / "courses" / "knowledge_base"
    
    # Clear existing knowledge base
    await db.knowledge_base.delete_many({})
    
    total_chunks = 0
    
    # Process each knowledge base file
    for kb_file in knowledge_base_dir.glob("*.json"):
        with open(kb_file, "r") as f:
            kb_data = json.load(f)
        
        course_id = kb_data.get("course_id")
        chunks = kb_data.get("chunks", [])
        
        for chunk in chunks:
            chunk_doc = {
                "course_id": course_id,
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "metadata": chunk["metadata"],
                "embedding": None,  # Will be added by generate_embeddings.py
                "created_at": datetime.utcnow()
            }
            await db.knowledge_base.insert_one(chunk_doc)
            total_chunks += 1
        
        print(f"  ✓ Added {len(chunks)} chunks for: {course_id}")
    
    print(f"  Total: {total_chunks} chunks seeded")


async def seed_quizzes(db):
    """Seed quizzes collection"""
    print("📝 Seeding quizzes...")
    
    quiz_path = Path(__file__).parent.parent / "data" / "quizzes" / "quiz_questions.json"
    
    with open(quiz_path, "r") as f:
        quiz_data = json.load(f)
    
    quizzes = quiz_data.get("quizzes", {})
    
    # Clear existing quizzes
    await db.quizzes.delete_many({})
    
    # Insert quizzes
    for course_id, quiz in quizzes.items():
        quiz_doc = {
            "course_id": course_id,
            "title": quiz["title"],
            "passing_score": quiz["passing_score"],
            "time_limit_minutes": quiz["time_limit_minutes"],
            "questions": quiz["questions"],
            "created_at": datetime.utcnow()
        }
        await db.quizzes.insert_one(quiz_doc)
        print(f"  ✓ Added quiz: {quiz['title']} ({len(quiz['questions'])} questions)")
    
    print(f"  Total: {len(quizzes)} quizzes seeded")


async def seed_demo_user(db):
    """Seed a demo user for testing"""
    print("👤 Seeding demo user...")
    
    # Clear existing demo user
    await db.users.delete_one({"user_id": "demo_user"})
    
    demo_user = {
        "user_id": "demo_user",
        "profile": {
            "name": "Demo User",
            "email": "demo@example.com",
            "role": "developer"
        },
        "selected_courses": [],
        "progress": {},
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await db.users.insert_one(demo_user)
    print("  ✓ Added demo user")


async def create_indexes(db):
    """Create necessary database indexes"""
    print("🔧 Creating indexes...")
    
    # Users collection
    await db.users.create_index("user_id", unique=True)
    print("  ✓ users.user_id index")
    
    # Courses collection
    await db.courses.create_index("course_id", unique=True)
    print("  ✓ courses.course_id index")
    
    # Knowledge base collection
    await db.knowledge_base.create_index("course_id")
    await db.knowledge_base.create_index("chunk_id", unique=True)
    print("  ✓ knowledge_base indexes")
    
    # Quizzes collection
    await db.quizzes.create_index("course_id", unique=True)
    print("  ✓ quizzes.course_id index")
    
    # Quiz results collection
    await db.quiz_results.create_index([("user_id", 1), ("course_id", 1)])
    print("  ✓ quiz_results composite index")
    
    # Notes collection
    await db.notes.create_index([("user_id", 1), ("course_id", 1)], unique=True)
    print("  ✓ notes composite index")
    
    # Conversations collection
    await db.conversations.create_index([("user_id", 1), ("course_id", 1)])
    await db.conversations.create_index("session_id")
    print("  ✓ conversations indexes")


async def main():
    """Main seeding function"""
    print("\n" + "="*50)
    print("🌱 CourseCompanion Database Seeder")
    print("="*50 + "\n")
    
    try:
        db = await get_database()
        print(f"📦 Connected to database: {db.name}\n")
        
        # Run seeding functions
        await seed_courses(db)
        print()
        
        await seed_knowledge_base(db)
        print()
        
        await seed_quizzes(db)
        print()
        
        await seed_demo_user(db)
        print()
        
        await create_indexes(db)
        print()
        
        print("="*50)
        print("✅ Database seeding complete!")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())





