"""
Sidebar Component - Extracted from app.py
Consistent navigation across all pages using the same design as app.py
"""
import streamlit as st


def render_app_sidebar():
    """
    Render sidebar exactly as it appears in app.py
    """
    st.sidebar.title("📚 CourseCompanion")
    st.sidebar.markdown("---")
    
    # Display user info if available
    if st.session_state.get("user_id"):
        st.sidebar.success(f"👤 User: {st.session_state.user_id}")
        if st.session_state.get("selected_courses"):
            st.sidebar.info(f"📖 Enrolled: {len(st.session_state.selected_courses)} courses")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Navigation")
    st.sidebar.markdown("""
    - 🏠 **Landing** - Start here
    - 🔍 **Discovery** - Find your courses
    - 📖 **Learning** - Study & Chat
    - 🧪 **Quiz** - Test yourself
    - 📊 **Results** - See your progress
    """)