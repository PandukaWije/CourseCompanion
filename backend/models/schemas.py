"""
Pydantic Schemas for MongoDB Documents
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


# ==================== User Models ====================

class UserProgress(BaseModel):
    """Progress tracking for a single course"""
    completed_modules: List[int] = []
    quiz_score: Optional[float] = None
    quiz_passed: bool = False
    notes: str = ""
    last_accessed: datetime = Field(default_factory=datetime.utcnow)


class UserProfile(BaseModel):
    """User profile information"""
    name: str
    email: Optional[str] = None
    role: Optional[str] = None  # developer, marketer, admin, etc.


class User(BaseModel):
    """User document schema"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    profile: UserProfile
    selected_courses: List[str] = []
    progress: Dict[str, UserProgress] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ==================== Course Models ====================

class CourseModule(BaseModel):
    """Course module information"""
    id: int
    title: str
    duration: str
    type: str = "video"  # video, text, quiz
    description: Optional[str] = None


class Course(BaseModel):
    """Course document schema"""
    id: Optional[str] = Field(default=None, alias="_id")
    course_id: str
    title: str
    description: str
    modules: List[CourseModule] = []
    prerequisites: List[str] = []
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    duration: str = ""
    topics: List[str] = []
    embedding: Optional[List[float]] = None  # For semantic search
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ==================== Knowledge Base Models ====================

class ChunkMetadata(BaseModel):
    """Metadata for a knowledge base chunk"""
    module: int
    timestamp: str = ""
    type: str = "text"  # text, transcript, summary
    topic: str = ""


class KnowledgeChunk(BaseModel):
    """Knowledge base chunk for RAG"""
    id: Optional[str] = Field(default=None, alias="_id")
    course_id: str
    chunk_id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: ChunkMetadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ==================== Conversation Models ====================

class Message(BaseModel):
    """Chat message"""
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sources: List[Dict] = []


class Conversation(BaseModel):
    """Conversation history document"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    course_id: Optional[str] = None  # None for discovery conversations
    session_id: str
    conversation_type: str = "chat"  # chat, discovery
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ==================== Quiz Models ====================

class QuizQuestion(BaseModel):
    """Quiz question"""
    id: str
    question: str
    options: List[str]
    correct: int  # Index of correct answer
    topic: str
    difficulty: str = "medium"  # easy, medium, hard


class Quiz(BaseModel):
    """Quiz document schema"""
    id: Optional[str] = Field(default=None, alias="_id")
    course_id: str
    title: str
    questions: List[QuizQuestion]
    time_limit_minutes: Optional[int] = None
    passing_score: float = 70.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class QuestionResult(BaseModel):
    """Result for a single question"""
    question_id: str
    user_answer: int
    correct_answer: int
    is_correct: bool
    topic: str


class TopicScore(BaseModel):
    """Score for a topic"""
    topic: str
    correct: int
    total: int
    percentage: float


class QuizResult(BaseModel):
    """Quiz result document"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    course_id: str
    quiz_id: str
    score: int
    total: int
    percentage: float
    passed: bool
    question_results: List[QuestionResult]
    topic_scores: List[TopicScore]
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ==================== Notes Models ====================

class Note(BaseModel):
    """User notes document"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    course_id: str
    content: str
    word_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ==================== Artifact Models ====================

class Artifact(BaseModel):
    """Learning artifact document"""
    id: Optional[str] = Field(default=None, alias="_id")
    artifact_id: str
    course_id: str
    title: str
    description: str
    artifact_type: str  # mindmap, summary, slides, cheatsheet
    file_type: str  # image, pdf, pptx
    url: Optional[str] = None
    content: Optional[str] = None  # For text-based artifacts
    available: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}





