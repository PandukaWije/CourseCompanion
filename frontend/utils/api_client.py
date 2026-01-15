"""
API Client - FastAPI Backend Communication
"""
import os
import requests
from typing import Optional, List, Dict, Any


class APIClient:
    """Client for communicating with the FastAPI backend"""
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize the API client
        
        Args:
            base_url: Base URL for the API. Defaults to environment variable or localhost.
        """
        self.base_url = base_url or os.getenv("API_BASE_URL", "http://localhost:8000")
        self.timeout = 30
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an HTTP request to the API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            JSON response as dictionary
            
        Raises:
            requests.exceptions.RequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        
        return response.json()
    
    # ===== Discovery Endpoints =====
    
    def discover_courses(self, message: str, history: List[Dict] = None) -> Dict[str, Any]:
        """Send message to discovery agent
        
        Args:
            message: User message
            history: Conversation history
            
        Returns:
            Agent response with message and optional recommendations
        """
        return self._request(
            "POST",
            "/api/discover",
            json={
                "message": message,
                "history": history or []
            }
        )
    
    # ===== Course Endpoints =====
    
    def get_courses(self) -> List[Dict[str, Any]]:
        """Get all available courses
        
        Returns:
            List of course objects
        """
        return self._request("GET", "/api/courses")
    
    def get_course(self, course_id: str) -> Dict[str, Any]:
        """Get a specific course by ID
        
        Args:
            course_id: Course identifier
            
        Returns:
            Course details
        """
        return self._request("GET", f"/api/courses/{course_id}")
    
    # ===== Chat Endpoints =====
    
    def chat(self, course_id: str, message: str, history: List[Dict] = None) -> Dict[str, Any]:
        """Send message to course-specific RAG chatbot
        
        Args:
            course_id: Course identifier for knowledge base filtering
            message: User message
            history: Conversation history
            
        Returns:
            Chatbot response with message and sources
        """
        return self._request(
            "POST",
            "/api/chat",
            json={
                "course_id": course_id,
                "message": message,
                "history": history or []
            }
        )
    
    # ===== Notes Endpoints =====
    
    def get_notes(self, user_id: str, course_id: str) -> Dict[str, Any]:
        """Get notes for a specific user and course
        
        Args:
            user_id: User identifier
            course_id: Course identifier
            
        Returns:
            Notes content
        """
        return self._request("GET", f"/api/notes/{user_id}/{course_id}")
    
    def save_notes(self, user_id: str, course_id: str, content: str) -> Dict[str, Any]:
        """Save notes for a specific user and course
        
        Args:
            user_id: User identifier
            course_id: Course identifier
            content: Notes content
            
        Returns:
            Save confirmation
        """
        return self._request(
            "POST",
            f"/api/notes/{user_id}/{course_id}",
            json={"content": content}
        )
    
    def update_notes(self, user_id: str, course_id: str, content: str) -> Dict[str, Any]:
        """Update notes for a specific user and course
        
        Args:
            user_id: User identifier
            course_id: Course identifier
            content: Updated notes content
            
        Returns:
            Update confirmation
        """
        return self._request(
            "PUT",
            f"/api/notes/{user_id}/{course_id}",
            json={"content": content}
        )
    
    # ===== Artifact Endpoints =====
    
    def get_artifact(self, course_id: str, artifact_type: str) -> Dict[str, Any]:
        """Get a specific artifact for a course
        
        Args:
            course_id: Course identifier
            artifact_type: Type of artifact (mindmap, summary, slides)
            
        Returns:
            Artifact data/URL
        """
        return self._request("GET", f"/api/artifacts/{course_id}/{artifact_type}")
    
    def list_artifacts(self, course_id: str) -> List[Dict[str, Any]]:
        """List all artifacts for a course
        
        Args:
            course_id: Course identifier
            
        Returns:
            List of available artifacts
        """
        return self._request("GET", f"/api/artifacts/{course_id}")
    
    # ===== Quiz Endpoints =====
    
    def get_quiz(self, course_id: str) -> Dict[str, Any]:
        """Get quiz questions for a course
        
        Args:
            course_id: Course identifier
            
        Returns:
            Quiz questions and metadata
        """
        return self._request("GET", f"/api/quiz/{course_id}")
    
    def submit_quiz(
        self, 
        user_id: str, 
        course_id: str, 
        answers: Dict[str, int]
    ) -> Dict[str, Any]:
        """Submit quiz answers for scoring
        
        Args:
            user_id: User identifier
            course_id: Course identifier
            answers: Dictionary mapping question_id to selected answer index
            
        Returns:
            Quiz results with score and recommendations
        """
        return self._request(
            "POST",
            "/api/quiz/submit",
            json={
                "user_id": user_id,
                "course_id": course_id,
                "answers": answers
            }
        )
    
    # ===== Results Endpoints =====
    
    def get_results(self, user_id: str, course_id: str) -> Dict[str, Any]:
        """Get quiz results and recommendations for a user
        
        Args:
            user_id: User identifier
            course_id: Course identifier
            
        Returns:
            Results with score, topic breakdown, and recommendations
        """
        return self._request("GET", f"/api/results/{user_id}/{course_id}")
    
    # ===== User Endpoints =====
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Get overall user progress across all courses
        
        Args:
            user_id: User identifier
            
        Returns:
            Progress data for all enrolled courses
        """
        return self._request("GET", f"/api/users/{user_id}/progress")
    
    def enroll_courses(self, user_id: str, course_ids: List[str]) -> Dict[str, Any]:
        """Enroll user in selected courses
        
        Args:
            user_id: User identifier
            course_ids: List of course identifiers to enroll in
            
        Returns:
            Enrollment confirmation
        """
        return self._request(
            "POST",
            f"/api/users/{user_id}/enroll",
            json={"course_ids": course_ids}
        )
    
    # ===== Health Check =====
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status
        
        Returns:
            Health status information
        """
        return self._request("GET", "/health")





