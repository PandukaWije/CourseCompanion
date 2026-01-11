"""
CourseCompanion - Main Streamlit Application Entry Point
"""
import streamlit as st
from utils.css_loader import load_css

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="CourseCompanion",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "user_id": None,
        "selected_courses": [],
        "current_course": None,
        "discovery_messages": [],
        "chat_messages": {},  # course_id -> messages
        "notes": {},  # course_id -> note content
        "quiz_results": {},  # course_id -> results
        "authenticated": False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    """Main application entry point"""
    init_session_state()
    
    # Try to load CSS (might not exist yet)
    try:
        load_css()
    except FileNotFoundError:
        pass
    
    # Sidebar navigation
    st.sidebar.title("📚 CourseCompanion")
    st.sidebar.markdown("---")
    
    # Display user info if available
    if st.session_state.user_id:
        st.sidebar.success(f"👤 User: {st.session_state.user_id}")
        if st.session_state.selected_courses:
            st.sidebar.info(f"📖 Enrolled: {len(st.session_state.selected_courses)} courses")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Navigation")
    st.sidebar.markdown("""
    - 🏠 **Landing** - Start here
    - 🔍 **Discovery** - Find your courses
    - 📖 **Learning** - Study & Chat
    - 📝 **Quiz** - Test yourself
    - 📊 **Results** - See your progress
    """)
    
    # Main content area - shows landing page by default
    st.title("Welcome to CourseCompanion! 🎓")
    st.markdown("""
    ### Your AI-Powered Learning Journey Starts Here
    
    Use the sidebar to navigate through the application, or use the pages in the navigation menu.
    
    **Quick Start:**
    1. Visit the **Landing** page to begin
    2. Use **Discovery** to find the right courses for you
    3. Start **Learning** with AI assistance
    4. Take a **Quiz** to test your knowledge
    5. View your **Results** and recommendations
    """)

if __name__ == "__main__":
    main()

