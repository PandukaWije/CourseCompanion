"""
Landing Page - Course Selection Entry Point
"""
import streamlit as st
import sys
sys.path.append("..")

from utils.api_client import APIClient
from utils.css_loader import load_css
from components.sidebar import render_app_sidebar

st.set_page_config(page_title="Landing - CourseCompanion", page_icon="🏠", layout="wide")

# Load CSS
load_css()

def init_page_state():
    """Initialize page-specific state"""
    if "landing_view" not in st.session_state:
        st.session_state.landing_view = "main"
    
    if not st.session_state.get("user_id"):
        st.session_state.user_id = "demo_user"

def render_hero_section():
    """Render the hero section with main CTAs"""
    st.markdown("""
    <div class="custom-header">
        <h1>🎓 CourseCompanion</h1>
        <p>Your AI-Powered Learning Journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Welcome to CourseCompanion! Whether you know exactly what you want to learn 
    or need help discovering the right path, we've got you covered.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🎯 I Know What I Want</h3>
            <p>Already have courses in mind? Browse our catalog and select the courses you want to take.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Browse Courses", key="browse_btn", use_container_width=True):
            st.session_state.landing_view = "browse"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🔍 Help Me Decide</h3>
            <p>Not sure where to start? Our AI Discovery Agent will help you find the perfect learning path.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        st.error("Failed to load courses from the server.")
    
    # Initialize selected courses
    if "temp_selected" not in st.session_state:
        st.session_state.temp_selected = set(st.session_state.get("selected_courses", []))
    
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
    
    # Render sidebar
    render_app_sidebar()
    
    # Render appropriate view
    if st.session_state.landing_view == "browse":
        render_course_browser()
    else:
        render_hero_section()

if __name__ == "__main__":
    main()