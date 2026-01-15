"""
Notepad Component - Course-specific note taking
"""
import streamlit as st
from typing import Optional
import sys
sys.path.append("..")

from utils.api_client import APIClient


def init_notepad_state(course_id: str):
    """Initialize notepad state for a specific course"""
    if "notes" not in st.session_state:
        st.session_state.notes = {}
    
    if course_id not in st.session_state.notes:
        st.session_state.notes[course_id] = ""


def save_notes(course_id: str, content: str, user_id: str = "demo_user"):
    """Save notes to backend"""
    api = APIClient()
    try:
        api.save_notes(user_id=user_id, course_id=course_id, content=content)
        return True
    except Exception:
        # For demo, just save to session state
        return True


def load_notes(course_id: str, user_id: str = "demo_user") -> str:
    """Load notes from backend"""
    api = APIClient()
    try:
        response = api.get_notes(user_id=user_id, course_id=course_id)
        return response.get("content", "")
    except Exception:
        # Return from session state for demo
        return st.session_state.notes.get(course_id, "")


def render_notepad(course_id: str):
    """Render the notepad interface"""
    init_notepad_state(course_id)
    
    st.markdown("### 📝 Course Notes")
    st.caption("Take notes while learning. Notes are automatically saved.")
    
    # Note-taking tips
    with st.expander("💡 Note-Taking Tips"):
        st.markdown("""
        - Use **Markdown** for formatting
        - Add `#` for headings
        - Use `-` for bullet points
        - Use `**text**` for bold
        - Use `` `code` `` for code snippets
        """)
    
    st.markdown("---")
    
    # Course name for display
    course_names = {
        "xm-cloud-101": "XM Cloud Fundamentals",
        "search-fundamentals": "Sitecore Search Fundamentals",
        "content-hub-101": "Content Hub Basics"
    }
    course_name = course_names.get(course_id, course_id)
    
    # Notes text area
    notes_content = st.text_area(
        f"Notes for {course_name}",
        value=st.session_state.notes.get(course_id, ""),
        height=400,
        key=f"notepad_{course_id}",
        placeholder=f"""Start taking notes for {course_name}...

# Key Concepts

## Topic 1
- Point 1
- Point 2

## Questions to Review
- Question 1?

---
Notes added from chat will appear here automatically.
"""
    )
    
    # Update session state
    st.session_state.notes[course_id] = notes_content
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Notes", key=f"save_notes_{course_id}", use_container_width=True):
            if save_notes(course_id, notes_content):
                st.success("Notes saved!")
            else:
                st.error("Failed to save notes")
    
    with col2:
        if st.button("🔄 Refresh", key=f"refresh_notes_{course_id}", use_container_width=True):
            loaded_notes = load_notes(course_id)
            st.session_state.notes[course_id] = loaded_notes
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear Notes", key=f"clear_notes_{course_id}", use_container_width=True):
            st.session_state.notes[course_id] = ""
            st.rerun()
    
    st.markdown("---")
    
    # Notes preview
    with st.expander("📖 Preview Notes (Rendered Markdown)"):
        if notes_content:
            st.markdown(notes_content)
        else:
            st.info("Start typing to see your notes rendered here.")
    
    # Word count
    word_count = len(notes_content.split()) if notes_content else 0
    char_count = len(notes_content) if notes_content else 0
    st.caption(f"📊 {word_count} words | {char_count} characters")
    
    st.markdown("---")
    
    # Quick templates
    st.markdown("#### 📋 Quick Templates")
    
    template_col1, template_col2 = st.columns(2)
    
    with template_col1:
        if st.button("📝 Add Heading", key=f"template_heading_{course_id}"):
            st.session_state.notes[course_id] += "\n\n# New Section\n"
            st.rerun()
        
        if st.button("✅ Add Checklist", key=f"template_checklist_{course_id}"):
            st.session_state.notes[course_id] += "\n\n## Checklist\n- [ ] Item 1\n- [ ] Item 2\n- [ ] Item 3\n"
            st.rerun()
    
    with template_col2:
        if st.button("❓ Add Question", key=f"template_question_{course_id}"):
            st.session_state.notes[course_id] += "\n\n**Question:** \n**Answer:** \n"
            st.rerun()
        
        if st.button("💡 Add Key Concept", key=f"template_concept_{course_id}"):
            st.session_state.notes[course_id] += "\n\n### Key Concept\n> Important: \n\n"
            st.rerun()





