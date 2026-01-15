"""
Course Discovery Page - AI-Powered Course Recommendation
"""
import streamlit as st
import sys
sys.path.append("..")

from utils.api_client import APIClient

st.set_page_config(page_title="Discovery - CourseCompanion", page_icon="🔍", layout="wide")

def init_discovery_state():
    """Initialize discovery-specific state"""
    if "discovery_messages" not in st.session_state:
        st.session_state.discovery_messages = []
    if "discovery_complete" not in st.session_state:
        st.session_state.discovery_complete = False
    if "recommended_courses" not in st.session_state:
        st.session_state.recommended_courses = []

def render_chat_interface():
    """Render the discovery chat interface"""
    st.title("🔍 Course Discovery Agent")
    st.markdown("""
    I'm here to help you find the perfect courses! Tell me about yourself, 
    your role, experience level, and what you'd like to learn.
    """)
    
    st.markdown("---")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.discovery_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # If this message contains recommendations, show selection UI
                if message.get("has_recommendations") and message["role"] == "assistant":
                    render_course_recommendations(message.get("courses", []))
    
    # Initial greeting if no messages
    if not st.session_state.discovery_messages:
        initial_message = {
            "role": "assistant",
            "content": """👋 Hello! I'm your Course Discovery Agent.

I'll help you find the perfect learning path. Let me ask you a few questions:

**To get started, tell me:**
1. What is your current role? (e.g., Developer, Marketer, Content Author)
2. What's your experience level with Sitecore products?
3. What are you hoping to achieve or learn?

Feel free to share as much or as little as you'd like!"""
        }
        st.session_state.discovery_messages.append(initial_message)
        st.rerun()
    
    # Chat input
    if not st.session_state.discovery_complete:
        if prompt := st.chat_input("Tell me about yourself and what you want to learn..."):
            # Add user message
            st.session_state.discovery_messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Get AI response
            api = APIClient()
            try:
                response = api.discover_courses(
                    message=prompt,
                    history=st.session_state.discovery_messages[:-1]
                )
                
                assistant_message = {
                    "role": "assistant",
                    "content": response.get("message", ""),
                    "has_recommendations": response.get("has_recommendations", False),
                    "courses": response.get("recommended_courses", [])
                }
                
                if response.get("has_recommendations"):
                    st.session_state.recommended_courses = response.get("recommended_courses", [])
                    st.session_state.discovery_complete = True
                
            except Exception as e:
                # Fallback response for demo
                assistant_message = generate_fallback_response(prompt)
            
            st.session_state.discovery_messages.append(assistant_message)
            st.rerun()

def generate_fallback_response(user_input: str) -> dict:
    """Generate fallback response when API is unavailable"""
    user_lower = user_input.lower()
    
    # Simple keyword matching for demo
    if any(word in user_lower for word in ["developer", "technical", "code", "api"]):
        return {
            "role": "assistant",
            "content": """Based on what you've shared, I can see you have a technical background! 

For developers looking to work with Sitecore products, I recommend starting with:

🎯 **Recommended Courses for You:**""",
            "has_recommendations": True,
            "courses": [
                {
                    "course_id": "xm-cloud-101",
                    "title": "XM Cloud Fundamentals",
                    "reason": "Essential for understanding the modern Sitecore architecture"
                },
                {
                    "course_id": "search-fundamentals", 
                    "title": "Sitecore Search Fundamentals",
                    "reason": "Great for implementing search functionality"
                }
            ]
        }
    elif any(word in user_lower for word in ["marketing", "content", "author", "editor"]):
        return {
            "role": "assistant",
            "content": """It sounds like you're focused on content and marketing!

For content professionals, these courses will help you get the most out of Sitecore:

🎯 **Recommended Courses for You:**""",
            "has_recommendations": True,
            "courses": [
                {
                    "course_id": "content-hub-101",
                    "title": "Content Hub Basics",
                    "reason": "Perfect for managing digital assets and content"
                },
                {
                    "course_id": "xm-cloud-101",
                    "title": "XM Cloud Fundamentals", 
                    "reason": "Understanding the platform you'll be creating content for"
                }
            ]
        }
    else:
        # Continue conversation
        return {
            "role": "assistant",
            "content": """Thanks for sharing! To give you better recommendations, could you tell me more about:

- **Your primary goal**: Are you looking to build, manage content, or analyze data?
- **Your timeline**: Do you need to learn quickly for a project, or is this for long-term growth?
- **Your interests**: Any specific Sitecore products you've heard about?

The more I know, the better I can match you with the right courses! 🎯""",
            "has_recommendations": False,
            "courses": []
        }

def render_course_recommendations(courses: list):
    """Render course recommendation cards with selection"""
    if not courses:
        return
    
    st.markdown("---")
    
    # Initialize temp selection
    if "discovery_selected" not in st.session_state:
        st.session_state.discovery_selected = set()
    
    for course in courses:
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"**📖 {course['title']}**")
            st.caption(course.get('reason', ''))
        
        with col2:
            if st.checkbox("Select", key=f"disc_{course['course_id']}"):
                st.session_state.discovery_selected.add(course['course_id'])
            else:
                st.session_state.discovery_selected.discard(course['course_id'])
    
    st.markdown("---")
    
    if st.session_state.discovery_selected:
        if st.button("✅ Enroll in Selected Courses", use_container_width=True):
            st.session_state.selected_courses = list(st.session_state.discovery_selected)
            st.session_state.current_course = st.session_state.selected_courses[0]
            st.success("🎉 Enrolled successfully! Redirecting to learning environment...")
            st.switch_page("pages/3_learning.py")

def render_sidebar():
    """Render discovery page sidebar"""
    with st.sidebar:
        st.markdown("### 💡 Discovery Tips")
        st.markdown("""
        - Be specific about your role
        - Mention your experience level
        - Share your learning goals
        - Ask questions if unsure
        """)
        
        st.markdown("---")
        
        if st.button("🔄 Start Over"):
            st.session_state.discovery_messages = []
            st.session_state.discovery_complete = False
            st.session_state.recommended_courses = []
            if "discovery_selected" in st.session_state:
                del st.session_state.discovery_selected
            st.rerun()
        
        if st.button("📚 Browse Courses Instead"):
            st.switch_page("pages/1_landing.py")

def main():
    """Main page function"""
    init_discovery_state()
    render_sidebar()
    render_chat_interface()

if __name__ == "__main__":
    main()





