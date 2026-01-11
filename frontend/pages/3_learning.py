"""
Learning Environment Page - Clean 2-Column Layout
"""
import streamlit as st
import sys
sys.path.append("..")

from utils.api_client import APIClient
from utils.css_loader import load_css

from components.chatbot import init_chat_state, add_to_notes, get_mock_response
from components.sidebar import render_app_sidebar

# Page configuration
st.set_page_config(
    page_title="Learning - CourseCompanion",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
load_css()

def init_learning_state():
    """Initialize session state"""
    defaults = {
        "chat_messages": {},
        "notes": {},
        "quick_notes": {},
        "current_course": None,
        "current_module": 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_chat_header():
    """Render chat header"""
    course_id = st.session_state.current_course
    
    course_titles = {
        "xm-cloud-101": "XM Cloud Fundamentals",
        "search-fundamentals": "Sitecore Search Fundamentals",
        "content-hub-101": "Content Hub Basics"
    }
    
    current_module = st.session_state.current_module
    course_name = course_titles.get(course_id, "Course")
    
    st.markdown(f"""
    <div class="chat-header">
        <h2>💬 AI Learning Assistant</h2>
        <p>{course_name} · Module {current_module + 1}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")


def render_chat_messages():
    """Render chat messages"""
    course_id = st.session_state.current_course
    init_chat_state(course_id)
    
    messages = st.session_state.chat_messages.get(course_id, [])
    
    if not messages:
        initial_msg = {
            "role": "assistant",
            "content": f"""👋 **Welcome! I'm your AI Learning Assistant.**

I'm here to help you master this course. I can:

• **📚 Explain concepts** in detail
• **🔍 Answer questions** about the material
• **💡 Clarify confusing topics**
• **🎯 Provide examples** to illustrate ideas
• **📝 Summarize key points** from modules

**Current Module:** Module {st.session_state.current_module + 1}

What would you like to learn about?"""
        }
        st.session_state.chat_messages[course_id] = [initial_msg]
        messages = [initial_msg]
    
    # Render messages
    for idx, message in enumerate(messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Action buttons for assistant messages
            if message["role"] == "assistant" and idx > 0:
                col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
                
                with col1:
                    if st.button("📝", key=f"note_{idx}", help="Add to notes"):
                        add_to_notes(message["content"], course_id)
                        st.toast("✅ Added to notes!", icon="📝")
                
                with col2:
                    if st.button("🔖", key=f"bookmark_{idx}", help="Bookmark"):
                        st.toast("✅ Bookmarked!", icon="🔖")
                
                with col3:
                    if st.button("📋", key=f"copy_{idx}", help="Copy"):
                        st.toast("✅ Copied!", icon="📋")


def render_chat_input():
    """Render chat input"""
    course_id = st.session_state.current_course
    
    # Suggested prompts for new conversations
    if len(st.session_state.chat_messages.get(course_id, [])) <= 1:
        st.markdown("---")
        st.markdown("#### 💡 Try asking:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📚 Explain module", key="prompt_explain", use_container_width=True):
                process_message("Can you explain the key concepts from this module?", course_id)
        
        with col2:
            if st.button("🎯 Give examples", key="prompt_examples", use_container_width=True):
                process_message("Can you give me practical examples?", course_id)
        
        with col3:
            if st.button("❓ Quiz me", key="prompt_quiz", use_container_width=True):
                process_message("Can you quiz me on this content?", course_id)
    
    # Chat input
    if prompt := st.chat_input("Ask anything about the course...", key=f"chat_input_{course_id}"):
        process_message(prompt, course_id)


def process_message(prompt: str, course_id: str):
    """Process user message"""
    # Add user message
    st.session_state.chat_messages[course_id].append({
        "role": "user",
        "content": prompt
    })
    
    # Get AI response
    api = APIClient()
    try:
        response = api.chat(course_id=course_id, message=prompt)
        assistant_content = response.get("message", "I couldn't process that request.")
    except Exception:
        response = get_mock_response(prompt, course_id)
        assistant_content = response["message"]
    
    # Add assistant response
    st.session_state.chat_messages[course_id].append({
        "role": "assistant",
        "content": assistant_content
    })
    
    st.rerun()


def render_artifacts():
    """Render artifacts section"""
    st.markdown('<div class="studio-section">', unsafe_allow_html=True)
    st.markdown("### 🎨 Learning Artifacts")
    
    course_id = st.session_state.current_course
    
    artifacts = {
        "xm-cloud-101": [
            {"icon": "🗺️", "title": "Architecture Mindmap", "size": "1.2 MB"},
            {"icon": "📄", "title": "Quick Reference", "size": "450 KB"},
            {"icon": "📊", "title": "Slide Deck", "size": "2.8 MB"}
        ],
        "search-fundamentals": [
            {"icon": "🗺️", "title": "Search Flow Diagram", "size": "980 KB"},
            {"icon": "📄", "title": "Config Guide", "size": "520 KB"},
            {"icon": "📊", "title": "Best Practices", "size": "1.9 MB"}
        ],
        "content-hub-101": [
            {"icon": "🗺️", "title": "Ecosystem Map", "size": "1.5 MB"},
            {"icon": "📄", "title": "User Guide", "size": "780 KB"},
            {"icon": "📊", "title": "Implementation Deck", "size": "3.2 MB"}
        ]
    }
    
    course_artifacts = artifacts.get(course_id, [])
    
    for artifact in course_artifacts:
        st.markdown(f"""
        <div class="artifact-card">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 28px;">{artifact['icon']}</span>
                <div style="flex: 1;">
                    <div style="font-weight: 600; font-size: 15px; color: #E0E0E0;">{artifact['title']}</div>
                    <div style="font-size: 12px; color: #999; margin-top: 4px;">{artifact['size']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"📥 Download {artifact['title']}", key=f"artifact_{artifact['title']}", use_container_width=True):
            st.toast(f"Downloading {artifact['title']}...", icon="📥")
    
    st.markdown("---")
    
    # Generate buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Generate Mindmap", key="gen_mindmap", use_container_width=True):
            st.toast("Generating mindmap...", icon="🗺️")
    
    with col2:
        if st.button("➕ Generate Summary", key="gen_summary", use_container_width=True):
            st.toast("Generating summary...", icon="📄")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_notes():
    """Render notes section"""
    st.markdown('<div class="studio-section">', unsafe_allow_html=True)
    st.markdown("### 📝 Course Notes")
    
    course_id = st.session_state.current_course
    
    if "quick_notes" not in st.session_state:
        st.session_state.quick_notes = {}
    
    if course_id not in st.session_state.quick_notes:
        st.session_state.quick_notes[course_id] = ""
    
    note = st.text_area(
        "Notes",
        value=st.session_state.quick_notes.get(course_id, ""),
        height=300,
        placeholder="• Key point 1\n• Key point 2\n• Question to review\n\nYour notes here...",
        key=f"quick_note_{course_id}"
    )
    
    st.session_state.quick_notes[course_id] = note
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Notes", key="save_note", use_container_width=True):
            st.toast("✅ Notes saved!", icon="💾")
    
    with col2:
        if st.button("🗑️ Clear Notes", key="clear_notes", use_container_width=True):
            st.session_state.quick_notes[course_id] = ""
            st.rerun()
    
    word_count = len(note.split()) if note else 0
    st.caption(f"📊 {word_count} words")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_studio_panel():
    """Render studio panel with Artifacts and Notes"""
    tab1, tab2 = st.tabs(["🎨 Artifacts", "📝 Notes"])
    
    with tab1:
        render_artifacts()
    
    with tab2:
        render_notes()


def main():
    """Main application"""
    init_learning_state()
    
    # Check if course is selected
    if not st.session_state.get("current_course"):
        st.error("❌ No course selected!")
        st.info("Please select a course from the Discovery page first.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Go to Discovery", use_container_width=True):
                st.switch_page("pages/2_discovery.py")
        with col2:
            if st.button("🏠 Go to Landing", use_container_width=True):
                st.switch_page("pages/1_landing.py")
        return
    
    # Render app sidebar
    render_app_sidebar()
    
    # Main layout - 2 columns
    col_chat, col_studio = st.columns([2.5, 1.2], gap="medium")
    
    # Chat column
    with col_chat:
        render_chat_header()
        render_chat_messages()
        render_chat_input()
    
    # Studio column
    with col_studio:
        render_studio_panel()


if __name__ == "__main__":
    main()