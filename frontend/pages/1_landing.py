"""
Landing Page - Course Selection Entry Point
"""
import streamlit as st
import sys
sys.path.append("..")

from utils.api_client import APIClient

st.set_page_config(page_title="Landing - CourseCompanion", page_icon="🏠", layout="wide")

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

def init_page_state():
    """Initialize page-specific state"""
    init_session_state()  # Ensure base state is initialized
    if "landing_view" not in st.session_state:
        st.session_state.landing_view = "main"  # main, browse, discovery

def render_hero_section():
    """Render the hero section with main CTAs"""
    st.title("🎓 CourseCompanion")
    st.markdown("### Your AI-Powered Learning Journey")
    
    st.markdown("""
    Welcome to CourseCompanion! Whether you know exactly what you want to learn 
    or need help discovering the right path, we've got you covered.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 I Know What I Want")
        st.markdown("""
        Already have courses in mind? Browse our catalog and select 
        the courses you want to take.
        """)
        if st.button("Browse Courses", key="browse_btn", use_container_width=True):
            st.session_state.landing_view = "browse"
            st.rerun()
    
    with col2:
        st.markdown("### 🔍 Help Me Decide")
        st.markdown("""
        Not sure where to start? Our AI Discovery Agent will help 
        you find the perfect learning path.
        """)
        if st.button("Start Discovery", key="discovery_btn", use_container_width=True):
            st.switch_page("pages/2_discovery.py")

def render_course_browser():
    """Render the course browsing interface"""
    st.title("📚 Course Catalog")
    
    if st.button("← Back to Main", key="back_main"):
        st.session_state.landing_view = "main"
        st.rerun()
    
    st.markdown("---")
    
    # Initialize API client
    api = APIClient()
    
    # Fetch courses (with fallback mock data)
    try:
        courses = api.get_courses()
    except Exception:
        # Mock data fallback
        courses = [
            {
                "course_id": "xm-cloud-101",
                "title": "XM Cloud Fundamentals",
                "description": "Learn the basics of XM Cloud architecture and implementation",
                "difficulty": "Beginner",
                "duration": "4 hours",
                "modules": 5
            },
            {
                "course_id": "search-fundamentals",
                "title": "Sitecore Search Fundamentals", 
                "description": "Master Sitecore Search configuration and optimization",
                "difficulty": "Intermediate",
                "duration": "3 hours",
                "modules": 4
            },
            {
                "course_id": "content-hub-101",
                "title": "Content Hub Basics",
                "description": "Introduction to Sitecore Content Hub DAM and CMP",
                "difficulty": "Beginner",
                "duration": "5 hours",
                "modules": 6
            }
        ]
    
    # Initialize selected courses if not exists
    if "temp_selected" not in st.session_state:
        st.session_state.temp_selected = set(st.session_state.selected_courses)
    
    # Course selection grid
    st.markdown("### Select Your Courses")
    
    for course in courses:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{course['title']}**")
            st.caption(course['description'])
            st.caption(f"📊 {course['difficulty']} | ⏱️ {course['duration']} | 📖 {course['modules']} modules")
        
        with col2:
            is_selected = course['course_id'] in st.session_state.temp_selected
            if st.checkbox("Select", key=f"select_{course['course_id']}", value=is_selected):
                st.session_state.temp_selected.add(course['course_id'])
            else:
                st.session_state.temp_selected.discard(course['course_id'])
        
        with col3:
            if is_selected:
                st.success("✓ Selected")
        
        st.markdown("---")
    
    # Confirm selection
    if st.session_state.temp_selected:
        st.success(f"**{len(st.session_state.temp_selected)} course(s) selected**")
        
        if st.button("🚀 Start Learning", key="start_learning", use_container_width=True):
            st.session_state.selected_courses = list(st.session_state.temp_selected)
            st.session_state.current_course = st.session_state.selected_courses[0]
            del st.session_state.temp_selected
            st.switch_page("pages/3_learning.py")
    else:
        st.info("Select at least one course to continue")

def main():
    """Main page function"""
    init_page_state()
    
    # Initialize user ID if not set
    if not st.session_state.get("user_id"):
        st.session_state.user_id = "demo_user"
    
    # Render appropriate view
    if st.session_state.landing_view == "browse":
        render_course_browser()
    else:
        render_hero_section()

if __name__ == "__main__":
    main()





