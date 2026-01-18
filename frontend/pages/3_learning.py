"""
Learning Environment Page - Content, Chat, Notes, and Artifacts
"""
import streamlit as st
import sys
sys.path.append("..")

from utils.api_client import APIClient
from components.chatbot import render_chatbot
from components.notepad import render_notepad
from components.artifact_viewer import render_artifact_viewer

st.set_page_config(page_title="Learning - CourseCompanion", page_icon="📖", layout="wide")

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "user_id": None,
        "selected_courses": [],
        "current_course": None,
        "discovery_messages": [],
        "chat_messages": {},
        "notes": {},
        "quiz_results": {},
        "authenticated": False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def init_learning_state():
    """Initialize learning-specific state"""
    init_session_state()  # Ensure base state is initialized
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = {}
    if "notes" not in st.session_state:
        st.session_state.notes = {}

def check_enrollment():
    """Check if user has selected courses"""
    if not st.session_state.get("selected_courses"):
        st.warning("⚠️ You haven't selected any courses yet!")
        st.markdown("Please go to the Landing page to select courses or use the Discovery agent.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📚 Browse Courses"):
                st.switch_page("pages/1_landing.py")
        with col2:
            if st.button("🔍 Discover Courses"):
                st.switch_page("pages/2_discovery.py")
        return False
    return True

def render_course_selector():
    """Render course selection dropdown"""
    courses = st.session_state.selected_courses
    
    # Get course titles (mock data for now)
    course_titles = {
        "xm-cloud-101": "XM Cloud Fundamentals",
        "search-fundamentals": "Sitecore Search Fundamentals",
        "content-hub-101": "Content Hub Basics"
    }
    
    options = [course_titles.get(c, c) for c in courses]
    
    selected_idx = st.selectbox(
        "📖 Current Course",
        range(len(options)),
        format_func=lambda x: options[x],
        key="course_selector"
    )
    
    st.session_state.current_course = courses[selected_idx]
    return courses[selected_idx]

def render_content_tab(course_id: str):
    """Render the course content tab"""
    st.markdown("### 📺 Course Content")
    
    # Mock course content
    course_content = {
        "xm-cloud-101": {
            "title": "XM Cloud Fundamentals",
            "modules": [
                {"id": 1, "title": "Introduction to XM Cloud", "duration": "15 min", "type": "video"},
                {"id": 2, "title": "Architecture Overview", "duration": "20 min", "type": "video"},
                {"id": 3, "title": "Setting Up Your Environment", "duration": "25 min", "type": "video"},
                {"id": 4, "title": "Component Development", "duration": "30 min", "type": "video"},
                {"id": 5, "title": "Deployment & Publishing", "duration": "20 min", "type": "video"}
            ]
        },
        "search-fundamentals": {
            "title": "Sitecore Search Fundamentals",
            "modules": [
                {"id": 1, "title": "Search Architecture", "duration": "20 min", "type": "video"},
                {"id": 2, "title": "Indexing Strategies", "duration": "25 min", "type": "video"},
                {"id": 3, "title": "Query Optimization", "duration": "20 min", "type": "video"},
                {"id": 4, "title": "Faceted Search", "duration": "15 min", "type": "video"}
            ]
        },
        "content-hub-101": {
            "title": "Content Hub Basics",
            "modules": [
                {"id": 1, "title": "Content Hub Overview", "duration": "15 min", "type": "video"},
                {"id": 2, "title": "Asset Management", "duration": "25 min", "type": "video"},
                {"id": 3, "title": "Content Operations", "duration": "20 min", "type": "video"},
                {"id": 4, "title": "Integration Patterns", "duration": "30 min", "type": "video"},
                {"id": 5, "title": "Workflows & Approvals", "duration": "20 min", "type": "video"},
                {"id": 6, "title": "Reporting & Analytics", "duration": "15 min", "type": "video"}
            ]
        }
    }
    
    content = course_content.get(course_id, {"title": course_id, "modules": []})
    
    # Module list
    st.markdown(f"#### {content['title']}")
    
    for module in content.get("modules", []):
        with st.expander(f"📹 Module {module['id']}: {module['title']} ({module['duration']})"):
            # Video placeholder
            st.markdown("---")
            st.markdown("🎬 **Video Player**")
            st.info("Video content would be displayed here. In production, this would be an embedded video player.")
            
            # Placeholder video controls
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("⏮️ -30s", key=f"rewind_{course_id}_{module['id']}")
            with col2:
                st.button("▶️ Play", key=f"play_{course_id}_{module['id']}")
            with col3:
                st.button("⏭️ +30s", key=f"forward_{course_id}_{module['id']}")
            
            st.markdown("---")
            
            # Quick actions
            if st.button("💡 Explain this section", key=f"explain_{course_id}_{module['id']}"):
                st.session_state[f"explain_request_{course_id}"] = f"Explain Module {module['id']}: {module['title']}"
                st.info("Switch to the Chat tab to see the explanation!")

def render_sidebar(course_id: str):
    """Render learning page sidebar"""
    with st.sidebar:
        st.markdown("### 📊 Progress")
        
        # Mock progress
        progress = 0.35
        st.progress(progress)
        st.caption(f"{int(progress * 100)}% complete")
        
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("📝 Take Quiz", use_container_width=True):
            st.switch_page("pages/4_quiz.py")
        
        if st.button("📊 View Results", use_container_width=True):
            st.switch_page("pages/5_results.py")
        
        st.markdown("---")
        st.markdown("### 📚 My Courses")
        
        for course in st.session_state.selected_courses:
            course_names = {
                "xm-cloud-101": "XM Cloud Fundamentals",
                "search-fundamentals": "Search Fundamentals",
                "content-hub-101": "Content Hub Basics"
            }
            name = course_names.get(course, course)
            if course == course_id:
                st.markdown(f"**▶️ {name}**")
            else:
                st.markdown(f"○ {name}")

def main():
    """Main page function"""
    init_learning_state()
    
    st.title("📖 Learning Environment")
    
    if not check_enrollment():
        return
    
    # Course selector
    course_id = render_course_selector()
    
    st.markdown("---")
    
    # Render sidebar
    render_sidebar(course_id)
    
    # Main content tabs
    tab_content, tab_chat, tab_notes, tab_artifacts = st.tabs([
        "📺 Content", "💬 AI Chat", "📝 Notes", "🎨 Artifacts"
    ])
    
    with tab_content:
        render_content_tab(course_id)
    
    with tab_chat:
        render_chatbot(course_id)
    
    with tab_notes:
        render_notepad(course_id)
    
    with tab_artifacts:
        render_artifact_viewer(course_id)

if __name__ == "__main__":
    main()





