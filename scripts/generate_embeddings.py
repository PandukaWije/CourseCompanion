"""
Embedding Generation Script
Generates embeddings for knowledge base chunks and stores them in local JSON storage.
Optionally builds a FAISS vector index for semantic search.
"""
import asyncio
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict

import sys
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from dotenv import load_dotenv

from models.local_storage import (
    load_knowledge_base_map_sync,
    save_knowledge_base_map_sync,
    load_courses_map_sync,
    save_courses_map_sync,
    vector_store
)

# Load environment variables
load_dotenv()

# Check for OpenAI
try:
    from openai import OpenAI, AzureOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None
    AzureOpenAI = None
    print("⚠️ OpenAI package not installed. Install with: pip install openai")


class EmbeddingGenerator:
    """Generates embeddings for text content using OpenAI"""
    
    def __init__(self):
        self.use_azure = os.getenv("USE_AZURE_OPENAI", "").lower() in {"1", "true", "yes"}
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        self.dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))

        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.azure_embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

        if OPENAI_AVAILABLE and self.use_azure and self.azure_api_key and self.azure_endpoint and self.azure_embedding_deployment:
            self.client = AzureOpenAI(
                api_key=self.azure_api_key,
                azure_endpoint=self.azure_endpoint,
                api_version=self.azure_api_version
            )
            self.model = self.azure_embedding_deployment
        elif OPENAI_AVAILABLE and self.api_key:
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


def generate_knowledge_base_embeddings(generator: EmbeddingGenerator, batch_size: int = 10):
    """Generate embeddings for all knowledge base chunks"""
    print("🧠 Generating knowledge base embeddings...")
    knowledge_base = load_knowledge_base_map_sync()
    chunks = [chunk for chunk in knowledge_base.values() if not chunk.get("embedding")]

    if not chunks:
        print("  ℹ️ No chunks found without embeddings")
        return

    print(f"  Found {len(chunks)} chunks to process")

    total_processed = 0

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [chunk["content"] for chunk in batch]

        embeddings = generator.generate_embeddings_batch(texts)

        for chunk, embedding in zip(batch, embeddings):
            chunk["embedding"] = embedding
            chunk["embedding_model"] = generator.model
            chunk["embedding_updated_at"] = datetime.utcnow().isoformat()

        total_processed += len(batch)
        print(f"  ✓ Processed {total_processed}/{len(chunks)} chunks")

    save_knowledge_base_map_sync(knowledge_base)
    print(f"  Total: {total_processed} embeddings generated")


def generate_course_embeddings(generator: EmbeddingGenerator):
    """Generate embeddings for course descriptions (for semantic course search)"""
    print("📚 Generating course description embeddings...")
    courses = load_courses_map_sync()
    course_list = [course for course in courses.values() if not course.get("embedding")]

    if not course_list:
        print("  ℹ️ No courses found without embeddings")
        return

    print(f"  Found {len(course_list)} courses to process")

    for course in course_list:
        text = f"{course['title']}: {course['description']}"
        embedding = generator.generate_embedding(text)
        course["embedding"] = embedding
        course["embedding_model"] = generator.model
        course["embedding_updated_at"] = datetime.utcnow().isoformat()
        print(f"  ✓ Generated embedding for: {course['title']}")

    save_courses_map_sync(courses)
    print(f"  Total: {len(course_list)} course embeddings generated")


def verify_embeddings():
    """Verify that embeddings were generated correctly"""
    print("🔍 Verifying embeddings...")
    knowledge_base = load_knowledge_base_map_sync()
    courses = load_courses_map_sync()

    kb_with_embedding = len([c for c in knowledge_base.values() if c.get("embedding")])
    kb_total = len(knowledge_base)
    print(f"  Knowledge base: {kb_with_embedding}/{kb_total} chunks have embeddings")

    courses_with_embedding = len([c for c in courses.values() if c.get("embedding")])
    courses_total = len(courses)
    print(f"  Courses: {courses_with_embedding}/{courses_total} courses have embeddings")

    sample = next((c for c in knowledge_base.values() if c.get("embedding")), None)
    if sample and sample.get("embedding"):
        print(f"  Embedding dimensions: {len(sample['embedding'])}")


def build_faiss_index():
    """Build and save FAISS index from local knowledge base embeddings"""
    print("🧭 Building FAISS index...")
    knowledge_base = load_knowledge_base_map_sync()
    chunks = [chunk for chunk in knowledge_base.values() if chunk.get("embedding")]

    if not chunks:
        print("  ℹ️ No embedded chunks found. Skipping FAISS index.")
        return

    embeddings = [chunk["embedding"] for chunk in chunks]
    documents = [
        {
            "chunk_id": chunk.get("chunk_id"),
            "course_id": chunk.get("course_id"),
            "content": chunk.get("content"),
            "module": chunk.get("module"),
            "timestamp": chunk.get("timestamp"),
            "type": chunk.get("type"),
            "topic": chunk.get("topic")
        }
        for chunk in chunks
    ]

    vector_store.initialize_index()
    vector_store.add_embeddings(embeddings, documents)
    vector_store.save_index("course_knowledge_base")
    print("  ✓ FAISS index saved")


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
        generator = EmbeddingGenerator()
        print(f"🤖 Using model: {generator.model}")
        print(f"   Dimensions: {generator.dimensions}\n")

        generate_knowledge_base_embeddings(generator)
        print()

        generate_course_embeddings(generator)
        print()

        verify_embeddings()
        print()

        build_faiss_index()

        print("\n" + "="*50)
        print("✅ Embedding generation complete!")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n❌ Error during embedding generation: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())





