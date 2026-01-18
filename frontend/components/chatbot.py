"""
RAG Chatbot Component - Course-specific AI assistant
"""
import streamlit as st
from typing import Optional
import sys
sys.path.append("..")

from utils.api_client import APIClient


def init_chat_state(course_id: str):
    """Initialize chat state for a specific course"""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = {}
    
    if course_id not in st.session_state.chat_messages:
        st.session_state.chat_messages[course_id] = [
            {
                "role": "assistant",
                "content": f"""👋 Hi! I'm your AI learning assistant for this course.

I have access to all the course materials and can help you with:
- 📚 Explaining concepts from the course
- 🔍 Finding specific information
- 💡 Answering your questions
- 🎯 Clarifying confusing topics

What would you like to learn about?"""
            }
        ]


def add_to_notes(content: str, course_id: str):
    """Add content to the notepad"""
    if "notes" not in st.session_state:
        st.session_state.notes = {}
    
    if course_id not in st.session_state.notes:
        st.session_state.notes[course_id] = ""
    
    # Add timestamp and content
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M")
    
    st.session_state.notes[course_id] += f"\n\n--- Added from chat at {timestamp} ---\n{content}"


def get_mock_response(message: str, course_id: str) -> dict:
    """Generate mock response for demo purposes"""
    message_lower = message.lower()
    
    # Course-specific mock responses
    responses = {
        "xm-cloud-101": {
            "default": """Based on the XM Cloud course materials, I can help explain that concept!

**XM Cloud** is Sitecore's modern, cloud-native content management platform. It enables headless content delivery with a powerful authoring experience.

Key points:
- 🏗️ **Architecture**: Fully SaaS-based, no infrastructure management needed
- 🔗 **Headless**: Content API delivers to any frontend
- ⚡ **Modern Stack**: Works with Next.js, React, and other frameworks
- 📝 **Experience Editor**: Visual editing capabilities

Would you like me to elaborate on any specific aspect?

*Source: Module 1 - Introduction to XM Cloud*""",
            "component": """Great question about components in XM Cloud!

**Components in XM Cloud** are built using the Sitecore JavaScript SDK (JSS):

```jsx
// Example Component
const HeroBanner = ({ fields }) => {
  return (
    <div className="hero">
      <h1>{fields.title?.value}</h1>
      <p>{fields.description?.value}</p>
    </div>
  );
};
```

Key concepts:
- 📦 Components map to Sitecore renderings
- 🔄 Data comes through `fields` prop
- 🎨 Style with CSS modules or styled-components
- ✏️ Editable in Experience Editor

*Source: Module 4 - Component Development*"""
        },
        "search-fundamentals": {
            "default": """I can help with Sitecore Search concepts!

**Sitecore Search** provides powerful content discovery capabilities:

Key features:
- 🔍 **Full-text search** across all content
- 📊 **Faceted filtering** for refined results
- ⚡ **Real-time indexing** for fresh content
- 🎯 **Relevance tuning** for better results

What specific aspect would you like to explore?

*Source: Module 1 - Search Architecture*""",
            "index": """Let me explain **indexing** in Sitecore Search:

**Index** = A searchable database of your content

When content changes:
1. 📝 Content is updated in CMS
2. 🔄 Change triggers indexing
3. 📊 Content is processed and stored
4. ✅ Index is updated

**Rebuild vs. Update:**
- **Update**: Single item changes
- **Rebuild**: Full reindex of all content

*Source: Module 2 - Indexing Strategies*"""
        },
        "content-hub-101": {
            "default": """I can help explain Content Hub concepts!

**Sitecore Content Hub** is a unified content platform:

- 🖼️ **DAM**: Digital Asset Management
- 📝 **CMP**: Content Marketing Platform
- 🔄 **MRM**: Marketing Resource Management

Key benefits:
- Central asset repository
- Workflow automation
- Brand consistency
- Multi-channel distribution

What would you like to know more about?

*Source: Module 1 - Content Hub Overview*""",
            "workflow": """Great question about **Workflows** in Content Hub!

Workflows automate content processes:

```
Draft → Review → Approve → Publish
  ↓       ↓        ↓         ↓
Author  Reviewer  Manager   System
```

Key features:
- ✅ Multi-stage approval
- 📧 Email notifications
- ⏰ SLA tracking
- 🔐 Permission-based actions

*Source: Module 5 - Workflows & Approvals*"""
        }
    }
    
    course_responses = responses.get(course_id, responses["xm-cloud-101"])
    
    # Check for specific keywords
    if any(word in message_lower for word in ["component", "jsx", "react"]):
        return {"message": course_responses.get("component", course_responses["default"]), "sources": ["Module 4"]}
    elif any(word in message_lower for word in ["index", "indexing", "rebuild"]):
        return {"message": course_responses.get("index", course_responses["default"]), "sources": ["Module 2"]}
    elif any(word in message_lower for word in ["workflow", "approval", "review"]):
        return {"message": course_responses.get("workflow", course_responses["default"]), "sources": ["Module 5"]}
    else:
        return {"message": course_responses["default"], "sources": ["Course Materials"]}


def render_chatbot(course_id: str):
    """Render the RAG chatbot interface"""
    init_chat_state(course_id)
    
    st.markdown("### 💬 AI Learning Assistant")
    st.caption("Ask questions about the course content")
    
    # Check for explain request from content tab
    explain_key = f"explain_request_{course_id}"
    if explain_key in st.session_state and st.session_state[explain_key]:
        # Auto-add the explain request as a message
        st.session_state.chat_messages[course_id].append({
            "role": "user",
            "content": st.session_state[explain_key]
        })
        del st.session_state[explain_key]
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.chat_messages[course_id]):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Add "Add to Notes" button for assistant messages
                if message["role"] == "assistant" and i > 0:
                    if st.button("📝 Add to Notes", key=f"add_note_{course_id}_{i}"):
                        add_to_notes(message["content"], course_id)
                        st.success("Added to notes!")
    
    # Chat input (st.chat_input can't be used inside tabs)
    with st.form(key=f"chat_form_{course_id}", clear_on_submit=True):
        prompt = st.text_input("Ask a question about the course...", key=f"chat_input_{course_id}")
        submitted = st.form_submit_button("Send")

    if submitted and prompt.strip():
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
            # Use mock response for demo
            response = get_mock_response(prompt, course_id)
            assistant_content = response["message"]
        
        # Add assistant response
        st.session_state.chat_messages[course_id].append({
            "role": "assistant",
            "content": assistant_content
        })
        
        st.rerun()
    
    # Clear chat button
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", key=f"clear_chat_{course_id}"):
        st.session_state.chat_messages[course_id] = [
            st.session_state.chat_messages[course_id][0]  # Keep initial greeting
        ]
        st.rerun()





