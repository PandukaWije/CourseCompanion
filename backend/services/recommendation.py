"""
Recommendation Engine - Generate personalized learning recommendations
"""
from typing import List, Dict, Any, Optional


class RecommendationEngine:
    """
    Engine for generating personalized learning recommendations
    based on quiz results and learning progress.
    
    Features:
    - Topic-based weakness identification
    - Module and artifact recommendations
    - Priority-based sorting
    """
    
    def __init__(self):
        self.course_resources = self._load_course_resources()
    
    def _load_course_resources(self) -> Dict[str, Dict]:
        """Load course-specific resources for recommendations"""
        return {
            "xm-cloud-101": {
                "topics": {
                    "fundamentals": {
                        "module": "Module 1: Introduction to XM Cloud",
                        "artifact": "mindmap",
                        "tip": "Review the core concepts and architecture overview",
                        "resources": [
                            "Watch the introduction video",
                            "Review the architecture diagram",
                            "Complete the hands-on exercise"
                        ]
                    },
                    "development": {
                        "module": "Module 4: Component Development",
                        "artifact": "cheatsheet",
                        "tip": "Practice creating components with the JSS SDK",
                        "resources": [
                            "Follow the component tutorial",
                            "Review the JSS documentation",
                            "Build a sample component"
                        ]
                    },
                    "architecture": {
                        "module": "Module 2: Architecture Overview",
                        "artifact": "mindmap",
                        "tip": "Study the headless architecture diagram",
                        "resources": [
                            "Review the system diagram",
                            "Understand the data flow",
                            "Learn about Experience Edge"
                        ]
                    },
                    "deployment": {
                        "module": "Module 5: Deployment & Publishing",
                        "artifact": "summary",
                        "tip": "Follow the deployment checklist step by step",
                        "resources": [
                            "Set up your GitHub repository",
                            "Configure environment variables",
                            "Practice with the Deploy app"
                        ]
                    }
                }
            },
            "search-fundamentals": {
                "topics": {
                    "indexing": {
                        "module": "Module 1 & 2: Search Architecture & Indexing",
                        "artifact": "mindmap",
                        "tip": "Understand when and how to rebuild indexes",
                        "resources": [
                            "Learn about index structures",
                            "Practice index configuration",
                            "Understand incremental vs full rebuild"
                        ]
                    },
                    "facets": {
                        "module": "Module 4: Faceted Search",
                        "artifact": "slides",
                        "tip": "Practice creating facet configurations",
                        "resources": [
                            "Review facet types",
                            "Configure custom facets",
                            "Implement facet UI"
                        ]
                    },
                    "optimization": {
                        "module": "Module 3: Query Optimization",
                        "artifact": "summary",
                        "tip": "Learn about boosting and relevance tuning",
                        "resources": [
                            "Study relevance scoring",
                            "Implement boosting rules",
                            "Test query performance"
                        ]
                    }
                }
            },
            "content-hub-101": {
                "topics": {
                    "dam": {
                        "module": "Module 2: Asset Management",
                        "artifact": "mindmap",
                        "tip": "Explore different asset types and metadata",
                        "resources": [
                            "Upload and organize assets",
                            "Configure metadata schemas",
                            "Learn about renditions"
                        ]
                    },
                    "cmp": {
                        "module": "Module 3: Content Operations",
                        "artifact": "slides",
                        "tip": "Understand the content lifecycle",
                        "resources": [
                            "Create content items",
                            "Set up taxonomies",
                            "Learn about content types"
                        ]
                    },
                    "workflows": {
                        "module": "Module 5: Workflows & Approvals",
                        "artifact": "workflow",
                        "tip": "Practice creating approval workflows",
                        "resources": [
                            "Design workflow stages",
                            "Configure notifications",
                            "Test approval processes"
                        ]
                    },
                    "integration": {
                        "module": "Module 4: Integration Patterns",
                        "artifact": "slides",
                        "tip": "Review API documentation and examples",
                        "resources": [
                            "Study the REST API",
                            "Implement webhooks",
                            "Build a sample integration"
                        ]
                    }
                }
            }
        }
    
    def generate_recommendations(
        self,
        course_id: str,
        topic_scores: Dict[str, Dict],
        threshold: float = 70.0
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on quiz topic scores.
        
        Args:
            course_id: Course identifier
            topic_scores: Dictionary mapping topics to score dictionaries
            threshold: Score percentage below which topics are recommended
            
        Returns:
            List of recommendations sorted by priority
        """
        recommendations = []
        course_resources = self.course_resources.get(course_id, {})
        topic_resources = course_resources.get("topics", {})
        
        for topic, scores in topic_scores.items():
            percentage = scores.get("percentage", 0)
            if isinstance(percentage, (int, float)):
                pass
            else:
                total = scores.get("total", 1)
                correct = scores.get("correct", 0)
                percentage = (correct / total * 100) if total > 0 else 0
            
            # Only recommend for topics below threshold
            if percentage < threshold:
                resource = topic_resources.get(topic, self._default_resource(topic))
                
                # Determine priority based on score
                if percentage < 40:
                    priority = "high"
                elif percentage < 60:
                    priority = "medium"
                else:
                    priority = "low"
                
                recommendations.append({
                    "topic": topic,
                    "score": percentage,
                    "priority": priority,
                    "module": resource.get("module", f"Review {topic} section"),
                    "artifact": resource.get("artifact", "summary"),
                    "tip": resource.get("tip", f"Focus on {topic} concepts"),
                    "resources": resource.get("resources", [])
                })
        
        # Sort by score (lowest first) and then by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(
            key=lambda x: (priority_order.get(x["priority"], 3), x["score"])
        )
        
        return recommendations
    
    def _default_resource(self, topic: str) -> Dict[str, Any]:
        """Generate default resource for unknown topics"""
        topic_title = topic.replace("_", " ").title()
        return {
            "module": f"Review {topic_title} section",
            "artifact": "summary",
            "tip": f"Focus on {topic_title.lower()} concepts",
            "resources": [
                f"Review {topic_title.lower()} materials",
                "Practice with examples",
                "Take notes on key concepts"
            ]
        }
    
    def get_next_steps(
        self,
        course_id: str,
        quiz_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get suggested next steps based on quiz results.
        
        Args:
            course_id: Course identifier
            quiz_results: Quiz results including score and topic breakdown
            
        Returns:
            Dictionary with next steps and suggestions
        """
        percentage = quiz_results.get("percentage", 0)
        passed = quiz_results.get("passed", False)
        
        if passed and percentage >= 90:
            return {
                "status": "excellent",
                "message": "🎉 Excellent work! You've mastered this course!",
                "next_steps": [
                    "Consider taking an advanced course",
                    "Help others learn by sharing your knowledge",
                    "Apply your skills in a real project"
                ],
                "badge": "gold"
            }
        elif passed:
            return {
                "status": "passed",
                "message": "✅ Great job! You've passed the course!",
                "next_steps": [
                    "Review the recommended topics to strengthen weak areas",
                    "Try the practical exercises",
                    "Move on to the next course in the learning path"
                ],
                "badge": "silver"
            }
        elif percentage >= 50:
            return {
                "status": "almost",
                "message": "📚 Almost there! A little more study and you'll pass!",
                "next_steps": [
                    "Focus on the high-priority topics below",
                    "Review the course materials",
                    "Retake the quiz when ready"
                ],
                "badge": None
            }
        else:
            return {
                "status": "needs_work",
                "message": "📖 Keep learning! Review the materials and try again.",
                "next_steps": [
                    "Start with the fundamentals",
                    "Watch all course videos",
                    "Take notes and use the artifacts",
                    "Practice with the chatbot"
                ],
                "badge": None
            }
    
    def get_learning_path(
        self,
        completed_courses: List[str],
        quiz_scores: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """
        Suggest next courses based on completed courses and performance.
        
        Args:
            completed_courses: List of completed course IDs
            quiz_scores: Dictionary mapping course_id to quiz score percentage
            
        Returns:
            List of suggested next courses with reasons
        """
        all_courses = [
            {"id": "xm-cloud-101", "title": "XM Cloud Fundamentals", "prereqs": []},
            {"id": "search-fundamentals", "title": "Search Fundamentals", "prereqs": ["xm-cloud-101"]},
            {"id": "content-hub-101", "title": "Content Hub Basics", "prereqs": []},
        ]
        
        suggestions = []
        
        for course in all_courses:
            if course["id"] in completed_courses:
                continue
            
            # Check prerequisites
            prereqs_met = all(p in completed_courses for p in course["prereqs"])
            
            if prereqs_met:
                suggestions.append({
                    "course_id": course["id"],
                    "title": course["title"],
                    "reason": "Prerequisites completed" if course["prereqs"] else "Great starting point",
                    "recommended": True
                })
        
        return suggestions





