"""
Quiz Service - Quiz question management and scoring
"""
from typing import List, Dict, Any, Optional


class QuizService:
    """
    Service for managing quiz questions and scoring.
    
    Features:
    - Course-specific quiz retrieval
    - Topic-based question organization
    - Scoring with topic breakdown
    """
    
    def __init__(self):
        self.quizzes = self._load_quizzes()
    
    def _load_quizzes(self) -> Dict[str, List[Dict]]:
        """Load quiz questions for all courses"""
        return {
            "xm-cloud-101": [
                {
                    "id": "xm-q1",
                    "question": "What is the primary purpose of XM Cloud?",
                    "options": [
                        "Database management",
                        "Headless content management and delivery",
                        "Email marketing",
                        "Customer relationship management"
                    ],
                    "correct": 1,
                    "topic": "fundamentals",
                    "difficulty": "easy"
                },
                {
                    "id": "xm-q2",
                    "question": "Which framework is commonly used with XM Cloud for frontend development?",
                    "options": [
                        "Angular only",
                        "Vue.js only",
                        "Next.js with JSS",
                        "PHP"
                    ],
                    "correct": 2,
                    "topic": "development",
                    "difficulty": "medium"
                },
                {
                    "id": "xm-q3",
                    "question": "What does 'headless' mean in the context of XM Cloud?",
                    "options": [
                        "No user interface at all",
                        "Content is separated from presentation",
                        "Only works without a database",
                        "Requires no authentication"
                    ],
                    "correct": 1,
                    "topic": "architecture",
                    "difficulty": "easy"
                },
                {
                    "id": "xm-q4",
                    "question": "How are components typically created in XM Cloud?",
                    "options": [
                        "Only through the UI",
                        "Using SQL scripts",
                        "As React/Next.js components with Sitecore integration",
                        "Through XML configuration only"
                    ],
                    "correct": 2,
                    "topic": "development",
                    "difficulty": "medium"
                },
                {
                    "id": "xm-q5",
                    "question": "What is the deployment model for XM Cloud?",
                    "options": [
                        "On-premise only",
                        "SaaS (Software as a Service)",
                        "Self-hosted required",
                        "Desktop application"
                    ],
                    "correct": 1,
                    "topic": "deployment",
                    "difficulty": "easy"
                }
            ],
            "search-fundamentals": [
                {
                    "id": "search-q1",
                    "question": "What is the primary function of an index in Sitecore Search?",
                    "options": [
                        "Store user passwords",
                        "Enable fast content retrieval",
                        "Manage user sessions",
                        "Handle authentication"
                    ],
                    "correct": 1,
                    "topic": "indexing",
                    "difficulty": "easy"
                },
                {
                    "id": "search-q2",
                    "question": "What are facets in search?",
                    "options": [
                        "Error messages",
                        "Categories for filtering search results",
                        "Database tables",
                        "User permissions"
                    ],
                    "correct": 1,
                    "topic": "facets",
                    "difficulty": "easy"
                },
                {
                    "id": "search-q3",
                    "question": "What is boosting in search queries?",
                    "options": [
                        "Making searches slower",
                        "Increasing relevance of certain results",
                        "Removing results",
                        "Encrypting queries"
                    ],
                    "correct": 1,
                    "topic": "optimization",
                    "difficulty": "medium"
                },
                {
                    "id": "search-q4",
                    "question": "When should you rebuild a search index?",
                    "options": [
                        "Never",
                        "After significant content changes or schema updates",
                        "Every minute",
                        "Only on weekends"
                    ],
                    "correct": 1,
                    "topic": "indexing",
                    "difficulty": "medium"
                }
            ],
            "content-hub-101": [
                {
                    "id": "ch-q1",
                    "question": "What is the primary use case for Content Hub DAM?",
                    "options": [
                        "Code deployment",
                        "Digital asset management",
                        "User authentication",
                        "Email sending"
                    ],
                    "correct": 1,
                    "topic": "dam",
                    "difficulty": "easy"
                },
                {
                    "id": "ch-q2",
                    "question": "What does CMP stand for in Content Hub?",
                    "options": [
                        "Code Management Platform",
                        "Content Marketing Platform",
                        "Customer Management Portal",
                        "Central Media Player"
                    ],
                    "correct": 1,
                    "topic": "cmp",
                    "difficulty": "easy"
                },
                {
                    "id": "ch-q3",
                    "question": "How do workflows help in Content Hub?",
                    "options": [
                        "They slow down processes",
                        "They automate content review and approval processes",
                        "They delete content automatically",
                        "They prevent any changes"
                    ],
                    "correct": 1,
                    "topic": "workflows",
                    "difficulty": "medium"
                },
                {
                    "id": "ch-q4",
                    "question": "What types of assets can Content Hub manage?",
                    "options": [
                        "Only images",
                        "Only videos",
                        "Multiple asset types including images, videos, documents",
                        "Only PDFs"
                    ],
                    "correct": 2,
                    "topic": "dam",
                    "difficulty": "easy"
                },
                {
                    "id": "ch-q5",
                    "question": "What is the benefit of Content Hub's integration capabilities?",
                    "options": [
                        "It cannot integrate with other systems",
                        "It enables connection with other marketing and content tools",
                        "It only works standalone",
                        "Integration removes all features"
                    ],
                    "correct": 1,
                    "topic": "integration",
                    "difficulty": "medium"
                }
            ]
        }
    
    def get_questions(self, course_id: str) -> List[Dict]:
        """
        Get quiz questions for a specific course.
        
        Args:
            course_id: Course identifier
            
        Returns:
            List of question dictionaries
        """
        return self.quizzes.get(course_id, [])
    
    def get_questions_by_topic(self, course_id: str, topic: str) -> List[Dict]:
        """
        Get quiz questions for a specific topic within a course.
        
        Args:
            course_id: Course identifier
            topic: Topic name
            
        Returns:
            List of questions for the topic
        """
        questions = self.get_questions(course_id)
        return [q for q in questions if q["topic"] == topic]
    
    def get_topics(self, course_id: str) -> List[str]:
        """
        Get all topics covered in a course quiz.
        
        Args:
            course_id: Course identifier
            
        Returns:
            List of unique topic names
        """
        questions = self.get_questions(course_id)
        return list(set(q["topic"] for q in questions))
    
    def score_quiz(
        self,
        course_id: str,
        answers: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Score a quiz submission.
        
        Args:
            course_id: Course identifier
            answers: Dictionary mapping question_id to selected answer index
            
        Returns:
            Scoring results with total score and topic breakdown
        """
        questions = self.get_questions(course_id)
        
        if not questions:
            return {
                "error": "Quiz not found",
                "score": 0,
                "total": 0,
                "percentage": 0,
                "topic_scores": {}
            }
        
        score = 0
        topic_scores = {}
        question_results = []
        
        for question in questions:
            q_id = question["id"]
            topic = question["topic"]
            user_answer = answers.get(q_id, -1)
            is_correct = user_answer == question["correct"]
            
            # Track score
            if is_correct:
                score += 1
            
            # Track topic scores
            if topic not in topic_scores:
                topic_scores[topic] = {"correct": 0, "total": 0}
            topic_scores[topic]["total"] += 1
            if is_correct:
                topic_scores[topic]["correct"] += 1
            
            # Track question results
            question_results.append({
                "question_id": q_id,
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": question["correct"],
                "is_correct": is_correct,
                "topic": topic
            })
        
        total = len(questions)
        percentage = (score / total * 100) if total > 0 else 0
        
        # Calculate topic percentages
        for topic, scores in topic_scores.items():
            scores["percentage"] = (
                scores["correct"] / scores["total"] * 100 
                if scores["total"] > 0 else 0
            )
        
        return {
            "score": score,
            "total": total,
            "percentage": percentage,
            "passed": percentage >= 70,
            "topic_scores": topic_scores,
            "question_results": question_results
        }
    
    def get_question_count(self, course_id: str) -> int:
        """Get the number of questions in a course quiz"""
        return len(self.get_questions(course_id))
    
    def validate_answers(
        self,
        course_id: str,
        answers: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Validate that all questions have been answered.
        
        Args:
            course_id: Course identifier
            answers: Dictionary mapping question_id to selected answer index
            
        Returns:
            Validation result with missing questions if any
        """
        questions = self.get_questions(course_id)
        question_ids = {q["id"] for q in questions}
        answered_ids = set(answers.keys())
        
        missing = question_ids - answered_ids
        
        return {
            "valid": len(missing) == 0,
            "total_questions": len(questions),
            "answered": len(answered_ids),
            "missing_questions": list(missing)
        }





