"""
CourseCompanion Database Models
"""
from .schemas import (
    User, Course, KnowledgeChunk, Conversation,
    Quiz, QuizResult, Note, Artifact
)
from .database import (
    connect_to_mongo, close_mongo_connection, get_database,
    users_collection, courses_collection, knowledge_base_collection,
    conversations_collection, quizzes_collection, quiz_results_collection,
    notes_collection
)

__all__ = [
    # Schemas
    "User", "Course", "KnowledgeChunk", "Conversation",
    "Quiz", "QuizResult", "Note", "Artifact",
    # Database
    "connect_to_mongo", "close_mongo_connection", "get_database",
    "users_collection", "courses_collection", "knowledge_base_collection",
    "conversations_collection", "quizzes_collection", "quiz_results_collection",
    "notes_collection"
]





