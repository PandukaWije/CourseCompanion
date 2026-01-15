"""
Artifact Viewer Component - Display pre-made learning artifacts
"""
import streamlit as st
from typing import Optional
import sys
sys.path.append("..")

from utils.api_client import APIClient


# Mock artifact data - in production, these would be fetched from backend/storage
ARTIFACTS = {
    "xm-cloud-101": {
        "mindmap": {
            "title": "XM Cloud Architecture Mindmap",
            "description": "Visual overview of XM Cloud architecture and components",
            "type": "image",
            "preview": "🗺️ Interactive mindmap showing XM Cloud ecosystem",
            "available": True
        },
        "summary": {
            "title": "XM Cloud Quick Reference Guide",
            "description": "Comprehensive PDF summary of key concepts",
            "type": "pdf",
            "preview": "📄 12-page reference guide with code examples",
            "available": True
        },
        "slides": {
            "title": "XM Cloud Presentation Deck",
            "description": "Slide deck covering all course modules",
            "type": "slides",
            "preview": "📊 45 slides with diagrams and examples",
            "available": True
        },
        "cheatsheet": {
            "title": "JSS Component Cheatsheet",
            "description": "Quick reference for JSS component development",
            "type": "pdf",
            "preview": "📋 2-page cheatsheet with code snippets",
            "available": True
        }
    },
    "search-fundamentals": {
        "mindmap": {
            "title": "Search Architecture Mindmap",
            "description": "Visual overview of Sitecore Search components",
            "type": "image",
            "preview": "🗺️ Mindmap showing search flow and components",
            "available": True
        },
        "summary": {
            "title": "Search Configuration Guide",
            "description": "Step-by-step configuration reference",
            "type": "pdf",
            "preview": "📄 8-page configuration guide",
            "available": True
        },
        "slides": {
            "title": "Search Best Practices",
            "description": "Presentation on search optimization",
            "type": "slides",
            "preview": "📊 30 slides with performance tips",
            "available": True
        }
    },
    "content-hub-101": {
        "mindmap": {
            "title": "Content Hub Ecosystem",
            "description": "Visual map of Content Hub modules",
            "type": "image",
            "preview": "🗺️ DAM, CMP, and MRM relationships",
            "available": True
        },
        "summary": {
            "title": "Content Hub User Guide",
            "description": "Comprehensive feature overview",
            "type": "pdf",
            "preview": "📄 15-page user guide",
            "available": True
        },
        "slides": {
            "title": "Content Hub Implementation",
            "description": "Implementation best practices deck",
            "type": "slides",
            "preview": "📊 35 slides with workflows",
            "available": True
        },
        "workflow": {
            "title": "Workflow Templates",
            "description": "Pre-built workflow configurations",
            "type": "pdf",
            "preview": "📋 Common workflow patterns",
            "available": True
        }
    }
}


def get_artifact_icon(artifact_type: str) -> str:
    """Get icon for artifact type"""
    icons = {
        "mindmap": "🗺️",
        "summary": "📄",
        "slides": "📊",
        "cheatsheet": "📋",
        "workflow": "🔄",
        "image": "🖼️",
        "pdf": "📄"
    }
    return icons.get(artifact_type, "📎")


def render_artifact_card(course_id: str, artifact_key: str, artifact: dict):
    """Render a single artifact card"""
    icon = get_artifact_icon(artifact_key)
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {icon} {artifact['title']}")
            st.caption(artifact['description'])
            st.markdown(f"*{artifact['preview']}*")
        
        with col2:
            if artifact['available']:
                if st.button(
                    f"View {artifact_key.title()}", 
                    key=f"view_{course_id}_{artifact_key}",
                    use_container_width=True
                ):
                    st.session_state[f"viewing_artifact_{course_id}"] = artifact_key
                    st.rerun()
            else:
                st.button(
                    "Coming Soon",
                    key=f"soon_{course_id}_{artifact_key}",
                    disabled=True,
                    use_container_width=True
                )


def render_artifact_detail(course_id: str, artifact_key: str, artifact: dict):
    """Render detailed view of an artifact"""
    icon = get_artifact_icon(artifact_key)
    
    # Back button
    if st.button("← Back to Artifacts"):
        del st.session_state[f"viewing_artifact_{course_id}"]
        st.rerun()
    
    st.markdown(f"## {icon} {artifact['title']}")
    st.caption(artifact['description'])
    
    st.markdown("---")
    
    # Render based on type
    if artifact['type'] == 'image':
        render_mindmap_placeholder(course_id, artifact)
    elif artifact['type'] == 'pdf':
        render_pdf_placeholder(course_id, artifact)
    elif artifact['type'] == 'slides':
        render_slides_placeholder(course_id, artifact)
    else:
        st.info(f"Artifact type: {artifact['type']}")


def render_mindmap_placeholder(course_id: str, artifact: dict):
    """Render mindmap placeholder"""
    st.markdown("### 🗺️ Mindmap View")
    
    # Placeholder mindmap using markdown
    mindmaps = {
        "xm-cloud-101": """
```
                        ┌─────────────────┐
                        │   XM Cloud      │
                        │   Platform      │
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   ┌────┴────┐            ┌──────┴──────┐          ┌─────┴─────┐
   │ Content │            │    Edge     │          │   Pages   │
   │   API   │            │   Delivery  │          │  Editor   │
   └────┬────┘            └──────┬──────┘          └─────┬─────┘
        │                        │                       │
   ┌────┴────┐            ┌──────┴──────┐          ┌─────┴─────┐
   │ GraphQL │            │     CDN     │          │ Experience│
   │  REST   │            │   Caching   │          │  Editor   │
   └─────────┘            └─────────────┘          └───────────┘
```
        """,
        "search-fundamentals": """
```
                        ┌─────────────────┐
                        │ Sitecore Search │
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   ┌────┴────┐            ┌──────┴──────┐          ┌─────┴─────┐
   │  Index  │            │   Query     │          │  Results  │
   │ Service │            │  Processing │          │  Ranking  │
   └────┬────┘            └──────┬──────┘          └─────┬─────┘
        │                        │                       │
   ┌────┴────┐            ┌──────┴──────┐          ┌─────┴─────┐
   │ Crawlers│            │   Facets    │          │ Relevance │
   │ Triggers│            │  Filtering  │          │  Boosting │
   └─────────┘            └─────────────┘          └───────────┘
```
        """,
        "content-hub-101": """
```
                        ┌─────────────────┐
                        │  Content Hub    │
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   ┌────┴────┐            ┌──────┴──────┐          ┌─────┴─────┐
   │   DAM   │            │     CMP     │          │    MRM    │
   │ Assets  │            │  Marketing  │          │ Resources │
   └────┬────┘            └──────┬──────┘          └─────┬─────┘
        │                        │                       │
   ┌────┴────┐            ┌──────┴──────┐          ┌─────┴─────┐
   │ Storage │            │  Workflows  │          │  Projects │
   │Metadata │            │  Campaigns  │          │  Planning │
   └─────────┘            └─────────────┘          └───────────┘
```
        """
    }
    
    st.code(mindmaps.get(course_id, "Mindmap not available"), language=None)
    
    st.info("💡 In production, this would be an interactive mindmap image or embedded diagram.")
    
    # Download placeholder
    st.download_button(
        "📥 Download Mindmap (PNG)",
        data="Placeholder mindmap data",
        file_name=f"{course_id}_mindmap.txt",
        mime="text/plain"
    )


def render_pdf_placeholder(course_id: str, artifact: dict):
    """Render PDF placeholder"""
    st.markdown("### 📄 Document Preview")
    
    # Course summaries
    summaries = {
        "xm-cloud-101": """
## XM Cloud Quick Reference Guide

### Chapter 1: Introduction
XM Cloud is Sitecore's cloud-native, SaaS content management platform...

### Chapter 2: Architecture
- **Content Management**: Cloud-hosted authoring environment
- **Experience Edge**: Content delivery via CDN
- **Pages**: Visual page building and editing

### Chapter 3: Development
```javascript
// Sample JSS Component
import { Text, RichText } from '@sitecore-jss/sitecore-jss-nextjs';

const MyComponent = ({ fields }) => (
  <div>
    <Text field={fields.title} />
    <RichText field={fields.body} />
  </div>
);
```

### Chapter 4: Deployment
- Connect to GitHub repository
- Configure environment variables
- Deploy via XM Cloud Deploy app

---
*Full document available for download*
        """,
        "search-fundamentals": """
## Search Configuration Guide

### Index Configuration
1. Create source connection
2. Define field mappings
3. Configure crawl schedule

### Query Optimization
- Use faceted search for filtering
- Implement boosting for relevance
- Enable synonyms for better matching

---
*Full document available for download*
        """,
        "content-hub-101": """
## Content Hub User Guide

### Getting Started
1. Navigate to your Content Hub instance
2. Configure user permissions
3. Set up taxonomy

### Asset Management
- Upload assets via drag-and-drop
- Add metadata and tags
- Create collections

### Workflows
- Define approval stages
- Configure notifications
- Set up automated actions

---
*Full document available for download*
        """
    }
    
    st.markdown(summaries.get(course_id, "Summary not available"))
    
    st.markdown("---")
    
    # Download placeholder
    st.download_button(
        "📥 Download Full PDF",
        data=summaries.get(course_id, ""),
        file_name=f"{course_id}_summary.txt",
        mime="text/plain"
    )


def render_slides_placeholder(course_id: str, artifact: dict):
    """Render slides placeholder"""
    st.markdown("### 📊 Presentation Slides")
    
    # Mock slides
    slides = {
        "xm-cloud-101": [
            {"title": "Welcome to XM Cloud", "content": "Your journey to modern content management"},
            {"title": "What is XM Cloud?", "content": "Cloud-native, headless CMS platform"},
            {"title": "Key Features", "content": "• SaaS delivery\n• Headless architecture\n• Visual editing"},
            {"title": "Architecture Overview", "content": "Content API → Edge → Frontend"},
            {"title": "Getting Started", "content": "1. Create project\n2. Clone starter\n3. Deploy"}
        ],
        "search-fundamentals": [
            {"title": "Sitecore Search", "content": "Powerful content discovery"},
            {"title": "How Search Works", "content": "Index → Query → Results"},
            {"title": "Configuration", "content": "• Sources\n• Fields\n• Widgets"}
        ],
        "content-hub-101": [
            {"title": "Content Hub", "content": "Unified content management"},
            {"title": "DAM Features", "content": "Asset storage and organization"},
            {"title": "CMP Overview", "content": "Content marketing workflows"}
        ]
    }
    
    course_slides = slides.get(course_id, [{"title": "Slides", "content": "Coming soon"}])
    
    # Slide navigation
    if f"slide_index_{course_id}" not in st.session_state:
        st.session_state[f"slide_index_{course_id}"] = 0
    
    current_slide = st.session_state[f"slide_index_{course_id}"]
    slide = course_slides[current_slide]
    
    # Slide display
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 10px;
        color: white;
        min-height: 200px;
    ">
        <h2 style="color: white; margin-bottom: 20px;">{slide['title']}</h2>
        <p style="font-size: 18px; white-space: pre-line;">{slide['content']}</p>
        <p style="position: absolute; bottom: 10px; right: 20px; opacity: 0.7;">
            Slide {current_slide + 1} of {len(course_slides)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("◀️ Previous", disabled=(current_slide == 0)):
            st.session_state[f"slide_index_{course_id}"] -= 1
            st.rerun()
    
    with col2:
        st.markdown(f"<center>Slide {current_slide + 1} / {len(course_slides)}</center>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Next ▶️", disabled=(current_slide >= len(course_slides) - 1)):
            st.session_state[f"slide_index_{course_id}"] += 1
            st.rerun()
    
    st.markdown("---")
    
    # Download placeholder
    st.download_button(
        "📥 Download Slides (PPTX)",
        data="Placeholder slides data",
        file_name=f"{course_id}_slides.txt",
        mime="text/plain"
    )


def render_artifact_viewer(course_id: str):
    """Render the artifact viewer interface"""
    st.markdown("### 🎨 Learning Artifacts")
    st.caption("Access mindmaps, summaries, and slide decks for this course")
    
    # Get artifacts for this course
    course_artifacts = ARTIFACTS.get(course_id, {})
    
    if not course_artifacts:
        st.info("No artifacts available for this course yet.")
        return
    
    # Check if viewing a specific artifact
    viewing_key = f"viewing_artifact_{course_id}"
    if viewing_key in st.session_state:
        artifact_key = st.session_state[viewing_key]
        artifact = course_artifacts.get(artifact_key)
        if artifact:
            render_artifact_detail(course_id, artifact_key, artifact)
            return
    
    st.markdown("---")
    
    # List all artifacts
    st.markdown("#### 📦 Available Artifacts")
    
    for artifact_key, artifact in course_artifacts.items():
        render_artifact_card(course_id, artifact_key, artifact)
        st.markdown("---")
    
    # Generation placeholder
    st.markdown("#### 🤖 AI-Generated Artifacts")
    st.info("💡 In a full implementation, you could generate custom artifacts based on your notes and chat history.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🗺️ Generate Custom Mindmap", disabled=True, help="Coming in future version")
    with col2:
        st.button("📝 Generate Study Guide", disabled=True, help="Coming in future version")





