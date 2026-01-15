"""
Artifacts Router - Learning artifact retrieval endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class Artifact(BaseModel):
    """Model for an artifact"""
    artifact_id: str
    title: str
    description: str
    artifact_type: str  # mindmap, summary, slides, cheatsheet
    file_type: str  # image, pdf, pptx
    url: Optional[str] = None
    available: bool = True


class ArtifactListResponse(BaseModel):
    """Response model for artifact list"""
    course_id: str
    artifacts: List[Artifact]


# Static artifact data (in production, fetch from MongoDB/storage)
ARTIFACTS_DATA = {
    "xm-cloud-101": [
        Artifact(
            artifact_id="xm-mindmap-1",
            title="XM Cloud Architecture Mindmap",
            description="Visual overview of XM Cloud architecture and components",
            artifact_type="mindmap",
            file_type="image",
            url="/static/artifacts/xm-cloud-101/mindmap.png",
            available=True
        ),
        Artifact(
            artifact_id="xm-summary-1",
            title="XM Cloud Quick Reference Guide",
            description="Comprehensive PDF summary of key concepts",
            artifact_type="summary",
            file_type="pdf",
            url="/static/artifacts/xm-cloud-101/summary.pdf",
            available=True
        ),
        Artifact(
            artifact_id="xm-slides-1",
            title="XM Cloud Presentation Deck",
            description="Slide deck covering all course modules",
            artifact_type="slides",
            file_type="pptx",
            url="/static/artifacts/xm-cloud-101/slides.pptx",
            available=True
        ),
        Artifact(
            artifact_id="xm-cheatsheet-1",
            title="JSS Component Cheatsheet",
            description="Quick reference for JSS component development",
            artifact_type="cheatsheet",
            file_type="pdf",
            url="/static/artifacts/xm-cloud-101/cheatsheet.pdf",
            available=True
        )
    ],
    "search-fundamentals": [
        Artifact(
            artifact_id="search-mindmap-1",
            title="Search Architecture Mindmap",
            description="Visual overview of Sitecore Search components",
            artifact_type="mindmap",
            file_type="image",
            url="/static/artifacts/search-fundamentals/mindmap.png",
            available=True
        ),
        Artifact(
            artifact_id="search-summary-1",
            title="Search Configuration Guide",
            description="Step-by-step configuration reference",
            artifact_type="summary",
            file_type="pdf",
            url="/static/artifacts/search-fundamentals/summary.pdf",
            available=True
        ),
        Artifact(
            artifact_id="search-slides-1",
            title="Search Best Practices",
            description="Presentation on search optimization",
            artifact_type="slides",
            file_type="pptx",
            url="/static/artifacts/search-fundamentals/slides.pptx",
            available=True
        )
    ],
    "content-hub-101": [
        Artifact(
            artifact_id="ch-mindmap-1",
            title="Content Hub Ecosystem",
            description="Visual map of Content Hub modules",
            artifact_type="mindmap",
            file_type="image",
            url="/static/artifacts/content-hub-101/mindmap.png",
            available=True
        ),
        Artifact(
            artifact_id="ch-summary-1",
            title="Content Hub User Guide",
            description="Comprehensive feature overview",
            artifact_type="summary",
            file_type="pdf",
            url="/static/artifacts/content-hub-101/summary.pdf",
            available=True
        ),
        Artifact(
            artifact_id="ch-slides-1",
            title="Content Hub Implementation",
            description="Implementation best practices deck",
            artifact_type="slides",
            file_type="pptx",
            url="/static/artifacts/content-hub-101/slides.pptx",
            available=True
        ),
        Artifact(
            artifact_id="ch-workflow-1",
            title="Workflow Templates",
            description="Pre-built workflow configurations",
            artifact_type="workflow",
            file_type="pdf",
            url="/static/artifacts/content-hub-101/workflows.pdf",
            available=True
        )
    ]
}


@router.get("/artifacts/{course_id}", response_model=ArtifactListResponse)
async def list_artifacts(course_id: str):
    """
    List all artifacts available for a course.
    """
    if course_id not in ARTIFACTS_DATA:
        return ArtifactListResponse(
            course_id=course_id,
            artifacts=[]
        )
    
    return ArtifactListResponse(
        course_id=course_id,
        artifacts=ARTIFACTS_DATA[course_id]
    )


@router.get("/artifacts/{course_id}/{artifact_type}", response_model=Artifact)
async def get_artifact(course_id: str, artifact_type: str):
    """
    Get a specific artifact by course ID and type.
    
    artifact_type can be: mindmap, summary, slides, cheatsheet, workflow
    """
    if course_id not in ARTIFACTS_DATA:
        raise HTTPException(status_code=404, detail="Course not found")
    
    artifacts = ARTIFACTS_DATA[course_id]
    
    for artifact in artifacts:
        if artifact.artifact_type == artifact_type:
            return artifact
    
    raise HTTPException(
        status_code=404, 
        detail=f"Artifact type '{artifact_type}' not found for course '{course_id}'"
    )


@router.get("/artifacts/{course_id}/by-id/{artifact_id}", response_model=Artifact)
async def get_artifact_by_id(course_id: str, artifact_id: str):
    """
    Get a specific artifact by its ID.
    """
    if course_id not in ARTIFACTS_DATA:
        raise HTTPException(status_code=404, detail="Course not found")
    
    artifacts = ARTIFACTS_DATA[course_id]
    
    for artifact in artifacts:
        if artifact.artifact_id == artifact_id:
            return artifact
    
    raise HTTPException(
        status_code=404,
        detail=f"Artifact '{artifact_id}' not found"
    )


@router.get("/artifacts/types")
async def get_artifact_types():
    """
    Get list of available artifact types.
    """
    return {
        "types": [
            {"id": "mindmap", "name": "Mind Map", "icon": "🗺️", "file_type": "image"},
            {"id": "summary", "name": "Summary", "icon": "📄", "file_type": "pdf"},
            {"id": "slides", "name": "Slides", "icon": "📊", "file_type": "pptx"},
            {"id": "cheatsheet", "name": "Cheat Sheet", "icon": "📋", "file_type": "pdf"},
            {"id": "workflow", "name": "Workflow", "icon": "🔄", "file_type": "pdf"}
        ]
    }





