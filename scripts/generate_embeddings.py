"""
Embedding Generation Script
Generates OpenAI embeddings for knowledge base chunks and stores them in MongoDB.
"""
import asyncio
import os
from pathlib import Path
from datetime import datetime
from typing import List

# Add parent directory to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI package not installed. Install with: pip install openai")


class EmbeddingGenerator:
    """Generates embeddings for text content using OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        self.dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
        
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        if not self.client:
            print("⚠️ OpenAI client not available, using mock embeddings")
            return self._mock_embedding()
        
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
                dimensions=self.dimensions
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"  ⚠️ Error generating embedding: {e}")
            return self._mock_embedding()
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts in batch"""
        if not self.client:
            print("⚠️ OpenAI client not available, using mock embeddings")
            return [self._mock_embedding() for _ in texts]
        
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts,
                dimensions=self.dimensions
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"  ⚠️ Error generating batch embeddings: {e}")
            return [self._mock_embedding() for _ in texts]
    
    def _mock_embedding(self) -> List[float]:
        """Generate a mock embedding for testing without API key"""
        import random
        return [random.uniform(-1, 1) for _ in range(self.dimensions)]


async def get_database():
    """Connect to MongoDB and return database instance"""
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "coursecompanion")
    
    client = AsyncIOMotorClient(mongodb_uri)
    return client[db_name]


async def generate_knowledge_base_embeddings(db, generator: EmbeddingGenerator, batch_size: int = 10):
    """Generate embeddings for all knowledge base chunks"""
    print("🧠 Generating knowledge base embeddings...")
    
    # Get all chunks without embeddings
    cursor = db.knowledge_base.find({"embedding": None})
    chunks = await cursor.to_list(length=1000)
    
    if not chunks:
        print("  ℹ️ No chunks found without embeddings")
        return
    
    print(f"  Found {len(chunks)} chunks to process")
    
    # Process in batches
    total_processed = 0
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [chunk["content"] for chunk in batch]
        
        # Generate embeddings for batch
        embeddings = generator.generate_embeddings_batch(texts)
        
        # Update chunks with embeddings
        for chunk, embedding in zip(batch, embeddings):
            await db.knowledge_base.update_one(
                {"_id": chunk["_id"]},
                {
                    "$set": {
                        "embedding": embedding,
                        "embedding_model": generator.model,
                        "embedding_updated_at": datetime.utcnow()
                    }
                }
            )
        
        total_processed += len(batch)
        print(f"  ✓ Processed {total_processed}/{len(chunks)} chunks")
    
    print(f"  Total: {total_processed} embeddings generated")


async def generate_course_embeddings(db, generator: EmbeddingGenerator):
    """Generate embeddings for course descriptions (for semantic course search)"""
    print("📚 Generating course description embeddings...")
    
    # Get all courses without embeddings
    cursor = db.courses.find({"embedding": None})
    courses = await cursor.to_list(length=100)
    
    if not courses:
        print("  ℹ️ No courses found without embeddings")
        return
    
    print(f"  Found {len(courses)} courses to process")
    
    for course in courses:
        # Combine title and description for richer embedding
        text = f"{course['title']}: {course['description']}"
        
        embedding = generator.generate_embedding(text)
        
        await db.courses.update_one(
            {"_id": course["_id"]},
            {
                "$set": {
                    "embedding": embedding,
                    "embedding_model": generator.model,
                    "embedding_updated_at": datetime.utcnow()
                }
            }
        )
        
        print(f"  ✓ Generated embedding for: {course['title']}")
    
    print(f"  Total: {len(courses)} course embeddings generated")


async def verify_embeddings(db):
    """Verify that embeddings were generated correctly"""
    print("🔍 Verifying embeddings...")
    
    # Check knowledge base
    kb_with_embedding = await db.knowledge_base.count_documents({"embedding": {"$ne": None}})
    kb_total = await db.knowledge_base.count_documents({})
    print(f"  Knowledge base: {kb_with_embedding}/{kb_total} chunks have embeddings")
    
    # Check courses
    courses_with_embedding = await db.courses.count_documents({"embedding": {"$ne": None}})
    courses_total = await db.courses.count_documents({})
    print(f"  Courses: {courses_with_embedding}/{courses_total} courses have embeddings")
    
    # Sample embedding dimensions
    sample = await db.knowledge_base.find_one({"embedding": {"$ne": None}})
    if sample and sample.get("embedding"):
        print(f"  Embedding dimensions: {len(sample['embedding'])}")


async def setup_vector_search_index(db):
    """
    Print instructions for setting up MongoDB Atlas Vector Search index.
    The index must be created via Atlas UI or API.
    """
    print("\n📋 MongoDB Atlas Vector Search Index Setup")
    print("="*50)
    print("""
To enable semantic search, create a Vector Search index in MongoDB Atlas:

1. Go to your Atlas cluster → Search → Create Index
2. Select "JSON Editor" and use this configuration:

{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "course_id"
    }
  ]
}

3. Name the index: "course_content_index"
4. Select collection: knowledge_base

For course semantic search, create another index on the courses collection
with the same embedding configuration.
    """)


async def main():
    """Main embedding generation function"""
    print("\n" + "="*50)
    print("🔢 CourseCompanion Embedding Generator")
    print("="*50 + "\n")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ OPENAI_API_KEY not set in environment")
        print("  Embeddings will use mock data for testing")
        print("  Set OPENAI_API_KEY in .env file for real embeddings\n")
    
    try:
        db = await get_database()
        print(f"📦 Connected to database: {db.name}\n")
        
        # Initialize embedding generator
        generator = EmbeddingGenerator()
        print(f"🤖 Using model: {generator.model}")
        print(f"   Dimensions: {generator.dimensions}\n")
        
        # Generate embeddings
        await generate_knowledge_base_embeddings(db, generator)
        print()
        
        await generate_course_embeddings(db, generator)
        print()
        
        # Verify
        await verify_embeddings(db)
        print()
        
        # Vector search setup instructions
        await setup_vector_search_index(db)
        
        print("\n" + "="*50)
        print("✅ Embedding generation complete!")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during embedding generation: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())





