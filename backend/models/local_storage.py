"""
Local Storage - JSON-based storage system replacing MongoDB
Uses JSON files for data persistence and FAISS for vector embeddings
"""
import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Storage directory paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "storage"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

# Storage file paths
USERS_FILE = DATA_DIR / "users.json"
COURSES_FILE = DATA_DIR / "courses.json"
KNOWLEDGE_BASE_FILE = DATA_DIR / "knowledge_base.json"
CONVERSATIONS_FILE = DATA_DIR / "conversations.json"
QUIZ_RESULTS_FILE = DATA_DIR / "quiz_results.json"
NOTES_FILE = DATA_DIR / "notes.json"
ARTIFACTS_FILE = DATA_DIR / "artifacts.json"


# ==================== Helper Functions ====================

def _load_json(file_path: Path) -> Dict:
    """Load JSON file, return empty dict if file doesn't exist"""
    if not file_path.exists():
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.warning(f"Failed to decode {file_path}, returning empty dict")
        return {}
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return {}


def _save_json(file_path: Path, data: Dict):
    """Save data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving to {file_path}: {e}")
        raise


# ==================== Initialization ====================

async def initialize_storage():
    """Initialize local storage system"""
    logger.info("Initializing local storage system...")
    
    # Create default storage files if they don't exist
    default_files = {
        USERS_FILE: {},
        COURSES_FILE: {},
        KNOWLEDGE_BASE_FILE: {},
        CONVERSATIONS_FILE: {},
        QUIZ_RESULTS_FILE: {},
        NOTES_FILE: {},
        ARTIFACTS_FILE: {}
    }
    
    for file_path, default_data in default_files.items():
        if not file_path.exists():
            _save_json(file_path, default_data)
            logger.info(f"Created {file_path.name}")
    
    logger.info("Local storage initialized successfully")


async def close_storage():
    """Close storage connections (no-op for local storage)"""
    logger.info("Storage closed")


# ==================== User Operations ====================

async def find_user(user_id: str) -> Optional[Dict]:
    """Find a user by user_id"""
    users = _load_json(USERS_FILE)
    return users.get(user_id)


async def create_user(user_data: Dict) -> str:
    """Create a new user"""
    users = _load_json(USERS_FILE)
    user_id = user_data.get("user_id")
    
    if not user_id:
        raise ValueError("user_id is required")
    
    users[user_id] = {
        **user_data,
        "created_at": datetime.utcnow().isoformat()
    }
    
    _save_json(USERS_FILE, users)
    return user_id


async def update_user(user_id: str, update_data: Dict) -> bool:
    """Update a user document"""
    users = _load_json(USERS_FILE)
    
    if user_id not in users:
        return False
    
    users[user_id].update({
        **update_data,
        "updated_at": datetime.utcnow().isoformat()
    })
    
    _save_json(USERS_FILE, users)
    return True


# ==================== Course Operations ====================

async def find_course(course_id: str) -> Optional[Dict]:
    """Find a course by course_id"""
    courses = _load_json(COURSES_FILE)
    return courses.get(course_id)


async def get_all_courses() -> List[Dict]:
    """Get all courses"""
    courses = _load_json(COURSES_FILE)
    return list(courses.values())


async def create_course(course_data: Dict) -> str:
    """Create a new course"""
    courses = _load_json(COURSES_FILE)
    course_id = course_data.get("course_id")
    
    if not course_id:
        raise ValueError("course_id is required")
    
    courses[course_id] = course_data
    _save_json(COURSES_FILE, courses)
    return course_id


# ==================== Knowledge Base Operations ====================

async def find_knowledge_chunks(course_id: str, limit: int = 10) -> List[Dict]:
    """Find knowledge base chunks for a course"""
    knowledge_base = _load_json(KNOWLEDGE_BASE_FILE)
    
    chunks = []
    for chunk_id, chunk in knowledge_base.items():
        if chunk.get("course_id") == course_id:
            chunks.append(chunk)
            if len(chunks) >= limit:
                break
    
    return chunks


async def save_knowledge_chunk(chunk_data: Dict) -> str:
    """Save a knowledge chunk"""
    knowledge_base = _load_json(KNOWLEDGE_BASE_FILE)
    chunk_id = chunk_data.get("chunk_id") or f"{chunk_data['course_id']}_{len(knowledge_base)}"
    
    chunk_data["chunk_id"] = chunk_id
    knowledge_base[chunk_id] = chunk_data
    
    _save_json(KNOWLEDGE_BASE_FILE, knowledge_base)
    return chunk_id


# ==================== Conversation Operations ====================

async def save_conversation(conversation_data: Dict) -> str:
    """Save a conversation"""
    conversations = _load_json(CONVERSATIONS_FILE)
    
    session_id = conversation_data.get("session_id")
    if not session_id:
        session_id = f"{conversation_data['user_id']}_{conversation_data['course_id']}_{datetime.utcnow().timestamp()}"
        conversation_data["session_id"] = session_id
    
    conversation_data["created_at"] = datetime.utcnow().isoformat()
    conversations[session_id] = conversation_data
    
    _save_json(CONVERSATIONS_FILE, conversations)
    return session_id


async def find_conversation(user_id: str, course_id: str = None, session_id: str = None) -> Optional[Dict]:
    """Find a conversation by user_id and optionally course_id or session_id"""
    conversations = _load_json(CONVERSATIONS_FILE)
    
    if session_id:
        return conversations.get(session_id)
    
    # Find most recent conversation for user and course
    matching_conversations = []
    for conv_id, conv in conversations.items():
        if conv.get("user_id") == user_id:
            if course_id is None or conv.get("course_id") == course_id:
                matching_conversations.append(conv)
    
    if matching_conversations:
        # Return most recent
        matching_conversations.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return matching_conversations[0]
    
    return None


# ==================== Quiz Results Operations ====================

async def save_quiz_result(result_data: Dict) -> str:
    """Save a quiz result"""
    results = _load_json(QUIZ_RESULTS_FILE)
    
    result_id = f"{result_data['user_id']}:{result_data['course_id']}"
    result_data["submitted_at"] = datetime.utcnow().isoformat()
    results[result_id] = result_data
    
    _save_json(QUIZ_RESULTS_FILE, results)
    return result_id


async def find_quiz_result(user_id: str, course_id: str) -> Optional[Dict]:
    """Find quiz result for a user and course"""
    results = _load_json(QUIZ_RESULTS_FILE)
    result_id = f"{user_id}:{course_id}"
    return results.get(result_id)


# ==================== Notes Operations ====================

async def save_note(user_id: str, course_id: str, content: str) -> bool:
    """Save or update user notes"""
    notes = _load_json(NOTES_FILE)
    note_id = f"{user_id}:{course_id}"
    
    notes[note_id] = {
        "user_id": user_id,
        "course_id": course_id,
        "content": content,
        "word_count": len(content.split()) if content else 0,
        "updated_at": datetime.utcnow().isoformat()
    }
    
    _save_json(NOTES_FILE, notes)
    return True


async def find_note(user_id: str, course_id: str) -> Optional[Dict]:
    """Find notes for a user and course"""
    notes = _load_json(NOTES_FILE)
    note_id = f"{user_id}:{course_id}"
    return notes.get(note_id)


# ==================== FAISS Vector Store (Prepared for future use) ====================

class FAISSVectorStore:
    """
    FAISS-based vector store for embeddings.
    Prepared for future embedding generation and similarity search.
    """
    
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.index = None
        self.documents = []
        
        try:
            import faiss
            self.faiss = faiss
        except ImportError:
            logger.warning("FAISS not installed. Vector search will not be available.")
            self.faiss = None
    
    def initialize_index(self):
        """Initialize FAISS index"""
        if self.faiss is None:
            return
        
        # Use L2 distance (can be changed to IP for cosine similarity with normalized vectors)
        self.index = self.faiss.IndexFlatL2(self.dimension)
        logger.info(f"FAISS index initialized with dimension {self.dimension}")
    
    def add_embeddings(self, embeddings: List[List[float]], documents: List[Dict]):
        """Add embeddings to the index"""
        if self.faiss is None or self.index is None:
            logger.warning("FAISS not available, skipping embedding addition")
            return
        
        import numpy as np
        embeddings_array = np.array(embeddings, dtype='float32')
        self.index.add(embeddings_array)
        self.documents.extend(documents)
        logger.info(f"Added {len(embeddings)} embeddings to index")
    
    def search(self, query_embedding: List[float], k: int = 5, course_id: str = None) -> List[Dict]:
        """Search for similar documents"""
        if self.faiss is None or self.index is None or self.index.ntotal == 0:
            logger.warning("FAISS not available or index empty")
            return []
        
        import numpy as np
        query_array = np.array([query_embedding], dtype='float32')
        distances, indices = self.index.search(query_array, min(k, self.index.ntotal))
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc["distance"] = float(distance)
                
                # Filter by course_id if provided
                if course_id is None or doc.get("course_id") == course_id:
                    results.append(doc)
        
        return results[:k]
    
    def save_index(self, index_name: str):
        """Save FAISS index to disk"""
        if self.faiss is None or self.index is None:
            return
        
        index_path = EMBEDDINGS_DIR / f"{index_name}.index"
        docs_path = EMBEDDINGS_DIR / f"{index_name}_docs.json"
        
        self.faiss.write_index(self.index, str(index_path))
        _save_json(docs_path, {"documents": self.documents})
        
        logger.info(f"Saved FAISS index to {index_path}")
    
    def load_index(self, index_name: str):
        """Load FAISS index from disk"""
        if self.faiss is None:
            return
        
        index_path = EMBEDDINGS_DIR / f"{index_name}.index"
        docs_path = EMBEDDINGS_DIR / f"{index_name}_docs.json"
        
        if index_path.exists():
            self.index = self.faiss.read_index(str(index_path))
            logger.info(f"Loaded FAISS index from {index_path}")
        
        if docs_path.exists():
            data = _load_json(docs_path)
            self.documents = data.get("documents", [])
            logger.info(f"Loaded {len(self.documents)} documents")


# Global FAISS store instance (initialized but not used until embeddings are generated)
vector_store = FAISSVectorStore()
