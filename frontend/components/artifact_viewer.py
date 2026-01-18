"""
Artifact Viewer Component - Display pre-made learning artifacts
Loads artifacts from files in data/artifacts/ directory
"""
import streamlit as st
from typing import Optional
import json
import os
from pathlib import Path

# Get the base path for artifacts
BASE_DIR = Path(__file__).parent.parent.parent
ARTIFACTS_DIR = BASE_DIR / "data" / "artifacts"


def get_artifact_path(course_id: str, artifact_type: str) -> Path:
    """Get the path to an artifact file"""
    paths = {
        "mindmap": ARTIFACTS_DIR / "mindmaps" / f"{course_id}_mindmap.md",
        "slides": ARTIFACTS_DIR / "slides" / f"{course_id}_slides.json",
        "summary": ARTIFACTS_DIR / "summaries" / f"{course_id}_summary.md",
        "summary_json": ARTIFACTS_DIR / "summaries" / f"{course_id}_summary.json",
        "cheatsheet": ARTIFACTS_DIR / "summaries" / f"{course_id}_cheatsheet.pdf",
    }
    return paths.get(artifact_type, Path())


def load_artifact_file(course_id: str, artifact_type: str) -> Optional[str]:
    """Load artifact content from file"""
    path = get_artifact_path(course_id, artifact_type)
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def load_json_artifact(course_id: str, artifact_type: str) -> Optional[dict]:
    """Load JSON artifact from file"""
    path = get_artifact_path(course_id, artifact_type)
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def check_artifact_availability(course_id: str) -> dict:
    """Check which artifacts are available for a course"""
    return {
        "mindmap": get_artifact_path(course_id, "mindmap").exists(),
        "slides": get_artifact_path(course_id, "slides").exists(),
        "summary": get_artifact_path(course_id, "summary").exists(),
        "summary_json": get_artifact_path(course_id, "summary_json").exists(),
    }


# Artifact metadata
ARTIFACTS = {
    "xm-cloud-101": {
        "mindmap": {
            "title": "XM Cloud Architecture Mindmap",
            "description": "Visual overview of XM Cloud architecture and components using Mermaid diagrams",
            "type": "mermaid",
            "preview": "🗺️ Interactive mindmap showing XM Cloud ecosystem with multiple views",
        },
        "summary": {
            "title": "XM Cloud Quick Reference Guide",
            "description": "Comprehensive markdown summary of key concepts",
            "type": "markdown",
            "preview": "📄 Complete reference guide with code examples and architecture diagrams",
        },
        "slides": {
            "title": "XM Cloud Presentation Deck",
            "description": "18-slide deck covering all course modules",
            "type": "slides",
            "preview": "📊 Full presentation with code examples and diagrams",
        },
        "cheatsheet": {
            "title": "JSS Component Cheatsheet",
            "description": "Quick reference for JSS component development",
            "type": "pdf",
            "preview": "📋 2-page cheatsheet with code snippets",
        }
    },
    "search-fundamentals": {
        "mindmap": {
            "title": "Search Architecture Mindmap",
            "description": "Visual overview of Sitecore Search components",
            "type": "image",
            "preview": "🗺️ Mindmap showing search flow and components",
        },
        "summary": {
            "title": "Search Configuration Guide",
            "description": "Step-by-step configuration reference",
            "type": "pdf",
            "preview": "📄 8-page configuration guide",
        },
        "slides": {
            "title": "Search Best Practices",
            "description": "Presentation on search optimization",
            "type": "slides",
            "preview": "📊 30 slides with performance tips",
        }
    },
    "content-hub-101": {
        "mindmap": {
            "title": "Content Hub Ecosystem",
            "description": "Visual map of Content Hub modules",
            "type": "image",
            "preview": "🗺️ DAM, CMP, and MRM relationships",
        },
        "summary": {
            "title": "Content Hub User Guide",
            "description": "Comprehensive feature overview",
            "type": "pdf",
            "preview": "📄 15-page user guide",
        },
        "slides": {
            "title": "Content Hub Implementation",
            "description": "Implementation best practices deck",
            "type": "slides",
            "preview": "📊 35 slides with workflows",
        },
        "workflow": {
            "title": "Workflow Templates",
            "description": "Pre-built workflow configurations",
            "type": "pdf",
            "preview": "📋 Common workflow patterns",
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
        "pdf": "📄",
        "mermaid": "🗺️",
        "markdown": "📝"
    }
    return icons.get(artifact_type, "📎")


def render_artifact_card(course_id: str, artifact_key: str, artifact: dict, available: bool):
    """Render a single artifact card"""
    icon = get_artifact_icon(artifact_key)
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {icon} {artifact['title']}")
            st.caption(artifact['description'])
            st.markdown(f"*{artifact['preview']}*")
            if available:
                st.success("✅ Available", icon="✅")
            else:
                st.warning("⏳ Coming Soon", icon="⏳")
        
        with col2:
            if available:
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
    if artifact_key == 'mindmap':
        render_mindmap(course_id, artifact)
    elif artifact_key == 'summary':
        render_summary(course_id, artifact)
    elif artifact_key == 'slides':
        render_slides(course_id, artifact)
    else:
        st.info(f"Artifact type: {artifact['type']}")


def render_mermaid(mermaid_code: str, height: int = 800, diagram_id: str = "diagram"):
    """Render a Mermaid diagram using mermaid.ink service (renders as image)"""
    import streamlit.components.v1 as components
    import base64
    import urllib.parse
    
    # Clean the mermaid code
    mermaid_code = mermaid_code.strip()
    
    # Encode for mermaid.ink URL
    encoded = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
    
    # Use mermaid.ink to render as SVG
    img_url = f"https://mermaid.ink/svg/{encoded}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                background: #f8f9fa;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                min-height: 100%;
            }}
            .diagram-container {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                max-width: 100%;
                overflow: auto;
            }}
            .diagram-container img {{
                max-width: 100%;
                height: auto;
                display: block;
            }}
            .error {{
                color: #e53e3e;
                padding: 20px;
                text-align: center;
            }}
            .loading {{
                color: #718096;
                padding: 40px;
                text-align: center;
                font-size: 16px;
            }}
        </style>
    </head>
    <body>
        <div class="diagram-container">
            <img 
                src="{img_url}" 
                alt="Mermaid Diagram" 
                onerror="this.parentElement.innerHTML='<div class=error>Failed to load diagram. Try refreshing.</div>'"
                onload="this.style.opacity=1"
                style="opacity: 0; transition: opacity 0.3s;"
            />
        </div>
    </body>
    </html>
    """
    
    components.html(html_content, height=height, scrolling=True)


def extract_mermaid_diagrams(content: str) -> list:
    """Extract mermaid diagram code blocks from markdown content"""
    import re
    # Match ```mermaid ... ``` blocks
    pattern = r'```mermaid\s*\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    return matches


def render_mindmap(course_id: str, artifact: dict):
    """Render mindmap from file - DEBUG MODE: Show code only"""
    st.markdown("### 🗺️ Visual Diagrams")
    
    content = load_artifact_file(course_id, "mindmap")
    
    if content:
        # Extract mermaid diagrams
        diagrams = extract_mermaid_diagrams(content)
        
        if diagrams:
            # Create tabs for different diagram views
            diagram_names = [
                "🌐 Platform Overview",
                "🏗️ Architecture Flow", 
                "🧩 Core Components",
                "🔧 Development Flow",
                "🚀 Deployment Pipeline"
            ]
            
            st.info(f"📊 **{len(diagrams)} diagrams found** - Showing Mermaid code for debugging")
            
            # Only show as many tabs as we have diagrams
            tabs = st.tabs(diagram_names[:len(diagrams)])
            
            for i, (tab, diagram) in enumerate(zip(tabs, diagrams)):
                with tab:
                    st.markdown(f"**Diagram {i+1}: {diagram_names[i]}**")
                    st.markdown("---")
                    # Show the mermaid code
                    st.code(diagram.strip(), language="text")
                    st.markdown("---")
                    # Create proper mermaid.live URL
                    # mermaid.live expects a JSON object: {"code": "...", "mermaid": {"theme": "default"}}
                    import json
                    import base64
                    import zlib
                    
                    mermaid_state = {
                        "code": diagram.strip(),
                        "mermaid": {"theme": "default"},
                        "autoSync": True,
                        "updateDiagram": True
                    }
                    json_str = json.dumps(mermaid_state)
                    # Pako compression (zlib) then base64
                    compressed = zlib.compress(json_str.encode('utf-8'), level=9)
                    encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
                    mermaid_live_url = f"https://mermaid.live/edit#pako:{encoded}"
                    
                    st.markdown(f"[🔗 Test this diagram in Mermaid Live Editor]({mermaid_live_url})")
        else:
            st.warning("No mermaid code blocks found in the file")
            st.markdown(content)
        
        # Download button
        st.markdown("---")
        st.download_button(
            "📥 Download Diagrams (Markdown)",
            data=content,
            file_name=f"{course_id}_mindmap.md",
            mime="text/markdown",
            use_container_width=True
        )
    else:
        # Fallback placeholder
        st.info("Mindmap file not found. Showing placeholder...")
        render_mindmap_placeholder(course_id)


def render_mindmap_placeholder(course_id: str):
    """Render placeholder mindmap"""
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
   └─────────┘            └─────────────┘          └───────────┘
```
        """
    }
    
    st.code(mindmaps.get(course_id, "Mindmap not available"), language=None)


def render_summary(course_id: str, artifact: dict):
    """Render summary from file"""
    st.markdown("### 📄 Course Summary")
    
    # Try to load markdown summary
    content = load_artifact_file(course_id, "summary")
    
    if content:
        # Add tabs for different views
        tab1, tab2 = st.tabs(["📖 Full Summary", "📊 Structured View"])
        
        with tab1:
            st.markdown(content)
        
        with tab2:
            # Try to load JSON summary for structured view
            json_content = load_json_artifact(course_id, "summary_json")
            if json_content:
                render_structured_summary(json_content)
            else:
                st.info("Structured view not available")
        
        # Download buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download Summary (Markdown)",
                data=content,
                file_name=f"{course_id}_summary.md",
                mime="text/markdown"
            )
        with col2:
            if json_content:
                st.download_button(
                    "📥 Download Summary (JSON)",
                    data=json.dumps(json_content, indent=2),
                    file_name=f"{course_id}_summary.json",
                    mime="application/json"
                )
    else:
        # Fallback placeholder
        st.info("Summary file not found. Showing placeholder...")
        render_pdf_placeholder(course_id, artifact)


def render_structured_summary(data: dict):
    """Render structured JSON summary"""
    # Executive Summary
    st.markdown("#### Executive Summary")
    st.info(data.get("executive_summary", ""))
    
    # Learning Objectives
    st.markdown("#### 🎯 Learning Objectives")
    for obj in data.get("learning_objectives", []):
        st.markdown(f"- {obj}")
    
    # Chapters
    st.markdown("#### 📚 Chapters")
    for chapter in data.get("chapters", []):
        with st.expander(f"Chapter {chapter['chapter_id']}: {chapter['title']}"):
            for section in chapter.get("sections", []):
                st.markdown(f"**{section['title']}**")
                st.write(section.get("content", ""))
                if section.get("key_points"):
                    for point in section["key_points"]:
                        st.markdown(f"  • {point}")
                if section.get("code_example"):
                    st.code(
                        section["code_example"]["code"],
                        language=section["code_example"].get("language", "text")
                    )
    
    # Key Takeaways
    st.markdown("#### 🔑 Key Takeaways")
    for takeaway in data.get("key_takeaways", []):
        st.success(f"✅ {takeaway}")
    
    # Glossary
    if data.get("glossary"):
        st.markdown("#### 📖 Glossary")
        glossary_data = {item["term"]: item["definition"] for item in data["glossary"]}
        for term, definition in glossary_data.items():
            st.markdown(f"**{term}**: {definition}")


def render_pdf_placeholder(course_id: str, artifact: dict):
    """Render PDF placeholder"""
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

---
*Full document available for download*
        """
    }
    
    st.markdown(summaries.get(course_id, "Summary not available"))


def render_slides(course_id: str, artifact: dict):
    """Render slides from JSON file"""
    st.markdown("### 📊 Presentation Slides")
    
    # Try to load slides from file
    slides_data = load_json_artifact(course_id, "slides")
    
    if slides_data:
        # Get all slides from all modules
        all_slides = []
        for module in slides_data.get("modules", []):
            for slide in module.get("slides", []):
                slide["module_title"] = module["title"]
                all_slides.append(slide)
        
        if not all_slides:
            st.warning("No slides found in the presentation")
            return
        
        # Slide navigation state
        if f"slide_index_{course_id}" not in st.session_state:
            st.session_state[f"slide_index_{course_id}"] = 0
        
        current_idx = st.session_state[f"slide_index_{course_id}"]
        slide = all_slides[current_idx]
        
        # Module indicator
        st.caption(f"Module: {slide.get('module_title', 'Unknown')}")
        
        # Slide display
        slide_html = f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 15px;
            color: white;
            min-height: 300px;
            position: relative;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        ">
            <h2 style="color: white; margin-bottom: 20px; font-size: 28px;">{slide['title']}</h2>
            <p style="font-size: 18px; margin-bottom: 20px; opacity: 0.9;">{slide.get('content', '')}</p>
        """
        
        # Add bullets
        if slide.get('bullets'):
            slide_html += '<ul style="font-size: 16px; line-height: 1.8;">'
            for bullet in slide['bullets']:
                slide_html += f'<li style="margin-bottom: 8px;">{bullet}</li>'
            slide_html += '</ul>'
        
        # Add code if present
        if slide.get('code'):
            code = slide['code']
            # Escape HTML entities in code snippet
            import html
            escaped_code = html.escape(code.get('snippet', ''))
            slide_html += f"""
            <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin-top: 15px;">
                <pre style="margin: 0;"><code style="color: #ffd700; font-family: 'Courier New', monospace; white-space: pre-wrap; font-size: 13px; line-height: 1.5;">{escaped_code}</code></pre>
            </div>
            """
        
        # Slide number
        slide_html += f"""
            <p style="position: absolute; bottom: 15px; right: 20px; opacity: 0.7; font-size: 14px;">
                Slide {current_idx + 1} of {len(all_slides)}
            </p>
        </div>
        """
        
        # Use components.html for reliable HTML rendering
        import streamlit.components.v1 as components
        components.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            </style>
        </head>
        <body>
            {slide_html}
        </body>
        </html>
        """, height=400, scrolling=False)
        
        # Navigation
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("◀️ Previous", disabled=(current_idx == 0), use_container_width=True):
                st.session_state[f"slide_index_{course_id}"] -= 1
                st.rerun()
        
        with col2:
            # Slide selector
            selected = st.selectbox(
                "Jump to slide",
                options=range(len(all_slides)),
                index=current_idx,
                format_func=lambda x: f"Slide {x+1}: {all_slides[x]['title'][:30]}...",
                label_visibility="collapsed"
            )
            if selected != current_idx:
                st.session_state[f"slide_index_{course_id}"] = selected
                st.rerun()
        
        with col3:
            if st.button("Next ▶️", disabled=(current_idx >= len(all_slides) - 1), use_container_width=True):
                st.session_state[f"slide_index_{course_id}"] += 1
                st.rerun()
        
        # Speaker notes
        if slide.get('notes'):
            with st.expander("📝 Speaker Notes"):
                st.write(slide['notes'])
        
        # Download button
        st.markdown("---")
        st.download_button(
            "📥 Download Slides (JSON)",
            data=json.dumps(slides_data, indent=2),
            file_name=f"{course_id}_slides.json",
            mime="application/json"
        )
    else:
        # Fallback to placeholder
        st.info("Slides file not found. Showing placeholder...")
        render_slides_placeholder(course_id, artifact)


def render_slides_placeholder(course_id: str, artifact: dict):
    """Render slides placeholder"""
    slides = {
        "xm-cloud-101": [
            {"title": "Welcome to XM Cloud", "content": "Your journey to modern content management"},
            {"title": "What is XM Cloud?", "content": "Cloud-native, headless CMS platform"},
            {"title": "Key Features", "content": "• SaaS delivery\n• Headless architecture\n• Visual editing"},
        ],
        "search-fundamentals": [
            {"title": "Sitecore Search", "content": "Powerful content discovery"},
            {"title": "How Search Works", "content": "Index → Query → Results"},
        ],
        "content-hub-101": [
            {"title": "Content Hub", "content": "Unified content management"},
            {"title": "DAM Features", "content": "Asset storage and organization"},
        ]
    }
    
    course_slides = slides.get(course_id, [{"title": "Slides", "content": "Coming soon"}])
    
    if f"slide_index_{course_id}" not in st.session_state:
        st.session_state[f"slide_index_{course_id}"] = 0
    
    current_slide = st.session_state[f"slide_index_{course_id}"]
    slide = course_slides[current_slide]
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 10px;
        color: white;
        min-height: 200px;
    ">
        <h2 style="color: white;">{slide['title']}</h2>
        <p style="font-size: 18px; white-space: pre-line;">{slide['content']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("◀️ Prev", disabled=(current_slide == 0)):
            st.session_state[f"slide_index_{course_id}"] -= 1
            st.rerun()
    with col3:
        if st.button("Next ▶️", disabled=(current_slide >= len(course_slides) - 1)):
            st.session_state[f"slide_index_{course_id}"] += 1
            st.rerun()


def render_artifact_viewer(course_id: str):
    """Render the artifact viewer interface"""
    st.markdown("### 🎨 Learning Artifacts")
    st.caption("Access mindmaps, summaries, and slide decks for this course")
    
    # Get artifacts for this course
    course_artifacts = ARTIFACTS.get(course_id, {})
    
    if not course_artifacts:
        st.info("No artifacts available for this course yet.")
        return
    
    # Check artifact availability from files
    availability = check_artifact_availability(course_id)
    
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
        is_available = availability.get(artifact_key, False) or availability.get(f"{artifact_key}_json", False)
        render_artifact_card(course_id, artifact_key, artifact, is_available)
        st.markdown("---")
    
    # Stats
    available_count = sum(1 for k in ["mindmap", "slides", "summary"] if availability.get(k, False))
    total_count = len(course_artifacts)
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
    ">
        <strong>📊 Artifact Status:</strong> {available_count} of {total_count} artifacts loaded from files
    </div>
    """, unsafe_allow_html=True)
