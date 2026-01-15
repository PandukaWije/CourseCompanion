"""
Discovery Agent - LangGraph-based course recommendation agent
"""
from typing import List, Dict, Any, Optional, TypedDict
from enum import Enum
import os
from pathlib import Path
import sys

# Add backend to path for config import
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

try:
    from config import settings
except ImportError:
    settings = None

# LangGraph imports - these will be used when LangGraph is installed
# from langgraph.graph import StateGraph, END
# from langchain_openai import ChatOpenAI, AzureChatOpenAI
# from langchain.prompts import ChatPromptTemplate


class ConversationState(Enum):
    """States for the discovery conversation"""
    GREETING = "greeting"
    ASSESS_ROLE = "assess_role"
    ASSESS_SKILLS = "assess_skills"
    ASSESS_GOALS = "assess_goals"
    RECOMMEND = "recommend"
    COMPLETE = "complete"


class DiscoveryState(TypedDict):
    """State for the discovery agent"""
    messages: List[Dict]
    user_role: Optional[str]
    skill_level: Optional[str]
    interests: List[str]
    goals: List[str]
    recommended_courses: List[Dict]
    current_state: str
    turn_count: int


class DiscoveryAgent:
    """
    LangGraph-based agent for course discovery and recommendation.
    
    This agent:
    1. Greets the user
    2. Assesses their role (developer, marketer, etc.)
    3. Understands their skill level
    4. Gathers their learning goals
    5. Recommends appropriate courses
    """
    
    def __init__(self):
        self.max_turns = 5
        self.courses = self._load_courses()
        
        # In production, initialize LangChain/LangGraph components with Azure OpenAI
        # if settings and settings.USE_AZURE_OPENAI:
        #     self.llm = AzureChatOpenAI(
        #         azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        #         api_key=settings.AZURE_OPENAI_API_KEY,
        #         api_version=settings.AZURE_OPENAI_API_VERSION,
        #         deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        #         temperature=0.7
        #     )
        # else:
        #     self.llm = ChatOpenAI(model=settings.OPENAI_MODEL)
        # 
        # self.workflow = self._build_workflow()
    
    def _load_courses(self) -> List[Dict]:
        """Load available courses for recommendation"""
        return [
            {
                "course_id": "xm-cloud-101",
                "title": "XM Cloud Fundamentals",
                "keywords": ["developer", "technical", "headless", "cms", "react", "nextjs", "architecture"],
                "difficulty": "beginner",
                "roles": ["developer", "architect", "technical"],
                "description": "Learn the basics of XM Cloud architecture and implementation"
            },
            {
                "course_id": "search-fundamentals",
                "title": "Sitecore Search Fundamentals",
                "keywords": ["search", "indexing", "optimization", "technical", "performance"],
                "difficulty": "intermediate",
                "roles": ["developer", "architect", "admin"],
                "description": "Master Sitecore Search configuration and optimization"
            },
            {
                "course_id": "content-hub-101",
                "title": "Content Hub Basics",
                "keywords": ["content", "marketing", "dam", "assets", "workflow", "digital", "media"],
                "difficulty": "beginner",
                "roles": ["marketer", "content author", "admin", "content", "marketing"],
                "description": "Introduction to Sitecore Content Hub DAM and CMP"
            }
        ]
    
    def _analyze_message(self, message: str) -> Dict[str, Any]:
        """Analyze user message for role, skills, and interests"""
        message_lower = message.lower()
        
        analysis = {
            "detected_role": None,
            "detected_skills": [],
            "detected_interests": [],
            "should_recommend": False
        }
        
        # Role detection
        role_keywords = {
            "developer": ["developer", "dev", "engineer", "programmer", "code", "coding", "technical"],
            "marketer": ["marketing", "marketer", "content", "campaign", "digital marketing"],
            "architect": ["architect", "design", "system", "infrastructure"],
            "admin": ["admin", "administrator", "manage", "configuration"],
            "content_author": ["author", "writer", "content creator", "editor"]
        }
        
        for role, keywords in role_keywords.items():
            if any(kw in message_lower for kw in keywords):
                analysis["detected_role"] = role
                break
        
        # Interest detection
        interest_keywords = {
            "headless": ["headless", "api", "decoupled"],
            "search": ["search", "find", "index", "query"],
            "content": ["content", "dam", "asset", "media"],
            "development": ["develop", "build", "create", "component"],
            "workflow": ["workflow", "process", "automation"]
        }
        
        for interest, keywords in interest_keywords.items():
            if any(kw in message_lower for kw in keywords):
                analysis["detected_interests"].append(interest)
        
        # Check if enough info to recommend
        if analysis["detected_role"] or len(analysis["detected_interests"]) >= 2:
            analysis["should_recommend"] = True
        
        return analysis
    
    def _match_courses(self, role: Optional[str], interests: List[str]) -> List[Dict]:
        """Match courses based on user profile"""
        scored_courses = []
        
        for course in self.courses:
            score = 0
            reason_parts = []
            
            # Role matching
            if role and role in course["roles"]:
                score += 3
                reason_parts.append(f"great for {role}s")
            
            # Interest matching
            for interest in interests:
                if interest in course["keywords"]:
                    score += 2
                    reason_parts.append(f"covers {interest}")
            
            # Keyword matching
            for keyword in course["keywords"]:
                if keyword in " ".join(interests).lower():
                    score += 1
            
            if score > 0:
                reason = ", ".join(reason_parts[:2]) if reason_parts else "recommended based on your profile"
                scored_courses.append({
                    "course_id": course["course_id"],
                    "title": course["title"],
                    "score": score,
                    "reason": reason.capitalize()
                })
        
        # Sort by score and return top 3
        scored_courses.sort(key=lambda x: x["score"], reverse=True)
        return scored_courses[:3]
    
    async def process_message(
        self,
        message: str,
        history: List[Dict]
    ) -> Dict[str, Any]:
        """
        Process a user message and return appropriate response.
        
        In production, this would use LangGraph for state management
        and GPT-4 for response generation.
        """
        turn_count = len([m for m in history if m.get("role") == "user"])
        analysis = self._analyze_message(message)
        
        # Collect all detected info from history and current message
        all_interests = analysis["detected_interests"]
        detected_role = analysis["detected_role"]
        
        # Check history for additional context
        for msg in history:
            if msg.get("role") == "user":
                hist_analysis = self._analyze_message(msg.get("content", ""))
                if hist_analysis["detected_role"] and not detected_role:
                    detected_role = hist_analysis["detected_role"]
                all_interests.extend(hist_analysis["detected_interests"])
        
        all_interests = list(set(all_interests))  # Remove duplicates
        
        # Determine if we should recommend
        should_recommend = (
            analysis["should_recommend"] or 
            turn_count >= 2 or 
            len(all_interests) >= 2
        )
        
        if should_recommend:
            # Generate recommendations
            recommendations = self._match_courses(detected_role, all_interests)
            
            if recommendations:
                response_message = self._generate_recommendation_message(
                    recommendations, detected_role, all_interests
                )
                
                return {
                    "message": response_message,
                    "has_recommendations": True,
                    "recommended_courses": recommendations,
                    "conversation_complete": True
                }
        
        # Continue conversation
        response_message = self._generate_followup_message(
            detected_role, all_interests, turn_count
        )
        
        return {
            "message": response_message,
            "has_recommendations": False,
            "recommended_courses": [],
            "conversation_complete": False
        }
    
    def _generate_recommendation_message(
        self,
        recommendations: List[Dict],
        role: Optional[str],
        interests: List[str]
    ) -> str:
        """Generate a message presenting course recommendations"""
        role_text = f"as a {role}" if role else ""
        interest_text = f"interested in {', '.join(interests)}" if interests else ""
        
        profile_description = " ".join(filter(None, [role_text, interest_text]))
        
        message = f"""Based on what you've shared{' ' + profile_description if profile_description else ''}, I've found some perfect courses for you!

🎯 **Here are my recommendations:**

"""
        
        for i, course in enumerate(recommendations, 1):
            message += f"""**{i}. {course['title']}**
   _{course['reason']}_

"""
        
        message += """These courses will give you a solid foundation. Select the ones that interest you most to get started!

Would you like more details about any of these courses, or are you ready to begin?"""
        
        return message
    
    def _generate_followup_message(
        self,
        role: Optional[str],
        interests: List[str],
        turn_count: int
    ) -> str:
        """Generate a follow-up question to gather more information"""
        
        if not role:
            return """That's helpful! To give you the best recommendations, could you tell me a bit more about:

- **Your role**: Are you a developer, marketer, content author, or administrator?
- **Your experience**: Are you new to Sitecore products or looking to level up existing skills?

This helps me match you with the right courses! 🎯"""
        
        if not interests:
            return f"""Great to know you're a {role}! 

What specific areas are you most interested in learning about?

For example:
- 🏗️ **Architecture & Development** - Building with modern frameworks
- 🔍 **Search & Discovery** - Content findability and optimization  
- 📦 **Content Management** - Digital assets and workflows
- ⚡ **Performance** - Speed and optimization

What catches your attention?"""
        
        return """Thanks for sharing! I think I have enough information to suggest some courses.

Let me find the best matches for your learning goals... 🔍"""
    
    # Production LangGraph workflow with Azure OpenAI (commented for reference)
    """
    def _build_workflow(self) -> StateGraph:
        '''Build the LangGraph workflow with Azure OpenAI'''
        from langgraph.graph import StateGraph, END
        from langchain_openai import AzureChatOpenAI
        
        # Initialize Azure OpenAI
        llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.7
        )
        
        workflow = StateGraph(DiscoveryState)
        
        # Add nodes
        workflow.add_node("greet", self._greet_user)
        workflow.add_node("assess_role", self._assess_role)
        workflow.add_node("assess_skills", self._assess_skills)
        workflow.add_node("assess_goals", self._assess_goals)
        workflow.add_node("recommend", self._recommend_courses)
        
        # Add edges
        workflow.add_edge("greet", "assess_role")
        workflow.add_conditional_edges(
            "assess_role",
            self._should_continue,
            {
                "continue": "assess_skills",
                "recommend": "recommend"
            }
        )
        workflow.add_conditional_edges(
            "assess_skills",
            self._should_continue,
            {
                "continue": "assess_goals",
                "recommend": "recommend"
            }
        )
        workflow.add_edge("assess_goals", "recommend")
        workflow.add_edge("recommend", END)
        
        workflow.set_entry_point("greet")
        
        return workflow.compile()
    """



