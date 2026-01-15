"""
Quiz Router - Quiz and assessment endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

from services.quiz_service import QuizService
from services.recommendation import RecommendationEngine

router = APIRouter()


class QuizQuestion(BaseModel):
    """Model for a quiz question"""
    id: str
    question: str
    options: List[str]
    topic: str


class QuizResponse(BaseModel):
    """Response model for quiz questions"""
    course_id: str
    title: str
    questions: List[QuizQuestion]
    time_limit_minutes: Optional[int] = None


class QuizSubmission(BaseModel):
    """Request model for quiz submission"""
    user_id: str
    course_id: str
    answers: Dict[str, int]  # question_id -> selected option index


class TopicScore(BaseModel):
    """Model for topic-level score"""
    topic: str
    correct: int
    total: int
    percentage: float


class Recommendation(BaseModel):
    """Model for a recommendation"""
    topic: str
    score: float
    priority: str
    module: str
    artifact: str
    tip: str


class QuizResultResponse(BaseModel):
    """Response model for quiz results"""
    user_id: str
    course_id: str
    score: int
    total: int
    percentage: float
    passed: bool
    topic_scores: List[TopicScore]
    recommendations: List[Recommendation]
    submitted_at: str


# In-memory storage for results (replace with MongoDB in production)
results_storage: dict = {}


@router.get("/quiz/{course_id}", response_model=QuizResponse)
async def get_quiz(course_id: str):
    """
    Get quiz questions for a specific course.
    """
    quiz_service = QuizService()
    questions = quiz_service.get_questions(course_id)
    
    if not questions:
        raise HTTPException(status_code=404, detail="Quiz not found for this course")
    
    course_titles = {
        "xm-cloud-101": "XM Cloud Fundamentals Quiz",
        "search-fundamentals": "Sitecore Search Fundamentals Quiz",
        "content-hub-101": "Content Hub Basics Quiz"
    }
    
    return QuizResponse(
        course_id=course_id,
        title=course_titles.get(course_id, f"{course_id} Quiz"),
        questions=[
            QuizQuestion(
                id=q["id"],
                question=q["question"],
                options=q["options"],
                topic=q["topic"]
            )
            for q in questions
        ],
        time_limit_minutes=30
    )


@router.post("/quiz/submit", response_model=QuizResultResponse)
async def submit_quiz(submission: QuizSubmission):
    """
    Submit quiz answers and get results with recommendations.
    """
    quiz_service = QuizService()
    recommendation_engine = RecommendationEngine()
    
    # Get questions for scoring
    questions = quiz_service.get_questions(submission.course_id)
    
    if not questions:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Score the quiz
    score = 0
    topic_scores = {}
    
    for question in questions:
        q_id = question["id"]
        user_answer = submission.answers.get(q_id, -1)
        is_correct = user_answer == question["correct"]
        
        if is_correct:
            score += 1
        
        topic = question["topic"]
        if topic not in topic_scores:
            topic_scores[topic] = {"correct": 0, "total": 0}
        topic_scores[topic]["total"] += 1
        if is_correct:
            topic_scores[topic]["correct"] += 1
    
    total = len(questions)
    percentage = (score / total * 100) if total > 0 else 0
    passed = percentage >= 70
    
    # Convert topic scores to response format
    topic_score_list = [
        TopicScore(
            topic=topic,
            correct=scores["correct"],
            total=scores["total"],
            percentage=(scores["correct"] / scores["total"] * 100) if scores["total"] > 0 else 0
        )
        for topic, scores in topic_scores.items()
    ]
    
    # Generate recommendations
    recommendations = recommendation_engine.generate_recommendations(
        course_id=submission.course_id,
        topic_scores=topic_scores
    )
    
    recommendation_list = [
        Recommendation(
            topic=rec["topic"],
            score=rec["score"],
            priority=rec["priority"],
            module=rec["module"],
            artifact=rec["artifact"],
            tip=rec["tip"]
        )
        for rec in recommendations
    ]
    
    # Store results
    result = QuizResultResponse(
        user_id=submission.user_id,
        course_id=submission.course_id,
        score=score,
        total=total,
        percentage=percentage,
        passed=passed,
        topic_scores=topic_score_list,
        recommendations=recommendation_list,
        submitted_at=datetime.utcnow().isoformat()
    )
    
    # Save to storage
    storage_key = f"{submission.user_id}:{submission.course_id}"
    results_storage[storage_key] = result.model_dump()
    
    return result


@router.get("/results/{user_id}/{course_id}", response_model=QuizResultResponse)
async def get_results(user_id: str, course_id: str):
    """
    Get quiz results for a specific user and course.
    """
    storage_key = f"{user_id}:{course_id}"
    
    if storage_key not in results_storage:
        raise HTTPException(status_code=404, detail="Results not found")
    
    return QuizResultResponse(**results_storage[storage_key])


@router.get("/results/{user_id}")
async def get_all_results(user_id: str):
    """
    Get all quiz results for a specific user.
    """
    user_results = []
    
    for key, result in results_storage.items():
        if key.startswith(f"{user_id}:"):
            user_results.append(result)
    
    return {
        "user_id": user_id,
        "results": user_results
    }





