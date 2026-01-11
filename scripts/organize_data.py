"""
CourseCompanion - Data Organization Script
Organizes your Course Companion Data into the proper project structure
Based on actual scan of your data folder
"""
import os
import shutil
import json
from pathlib import Path
from datetime import datetime

# ============== CONFIGURATION ==============
SOURCE_DIR = r"C:\Users\AR Kamaldeen\Downloads\Course Companion Data"
PROJECT_DIR = r"C:\Users\AR Kamaldeen\Desktop\CourseCompanion"
DEST_DATA_DIR = os.path.join(PROJECT_DIR, "data")

# Course ID mapping (proper format: lowercase-with-hyphens-number)
COURSE_MAPPING = {
    "Course 1 - C++": {
        "course_id": "cpp-fundamentals-101",
        "title": "C++ Fundamentals",
        "description": "Complete C++ programming course from basics to advanced concepts",
        "difficulty": "Beginner",
        "duration": "6 hours",
        "topics": ["programming", "cpp", "object-oriented", "fundamentals"],
        "keywords": ["c++", "programming", "oop", "syntax", "data structures"]
    },
    "Course 2  - Kubernetes": {
        "course_id": "kubernetes-fundamentals-101",
        "title": "Kubernetes Fundamentals",
        "description": "Learn container orchestration with Kubernetes from scratch",
        "difficulty": "Intermediate",
        "duration": "5 hours",
        "topics": ["kubernetes", "containers", "devops", "orchestration"],
        "keywords": ["kubernetes", "k8s", "docker", "containers", "deployment"]
    },
    "Course 3 - C": {
        "course_id": "c-programming-101",
        "title": "C Programming Fundamentals",
        "description": "Master C programming language fundamentals and best practices",
        "difficulty": "Beginner",
        "duration": "4 hours",
        "topics": ["programming", "c-language", "systems-programming", "fundamentals"],
        "keywords": ["c", "programming", "systems", "pointers", "memory management"]
    }
}

# ============================================


def create_directory_structure():
    """Create the complete directory structure in the project"""
    print("\n" + "="*70)
    print("📁 CREATING DIRECTORY STRUCTURE")
    print("="*70 + "\n")
    
    base_data = Path(DEST_DATA_DIR)
    
    # Create base directories
    directories = [
        "raw",
        "courses/knowledge_base",
        "quizzes",
        "artifacts/mindmaps",
        "artifacts/summaries",
        "artifacts/slides",
        "ui-designs"
    ]
    
    for dir_path in directories:
        full_path = base_data / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {dir_path}/")
    
    # Create course-specific directories
    for course_info in COURSE_MAPPING.values():
        course_id = course_info['course_id']
        
        course_dirs = [
            f"raw/{course_id}/videos",
            f"raw/{course_id}/transcripts",
            f"raw/{course_id}/documents",
            f"raw/{course_id}/urls"
        ]
        
        for dir_path in course_dirs:
            full_path = base_data / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
        
        print(f"  ✓ raw/{course_id}/ (with subdirectories)")
    
    print("\n✅ Directory structure created!")


def copy_course_files():
    """Copy files from source to organized project structure"""
    print("\n" + "="*70)
    print("📦 COPYING COURSE FILES")
    print("="*70 + "\n")
    
    source = Path(SOURCE_DIR)
    dest = Path(DEST_DATA_DIR)
    
    files_copied = 0
    
    for source_course, course_info in COURSE_MAPPING.items():
        course_id = course_info['course_id']
        source_course_path = source / source_course
        
        if not source_course_path.exists():
            print(f"  ⚠️  Course not found: {source_course}")
            continue
        
        print(f"\n📚 Processing: {course_info['title']}")
        print(f"   Course ID: {course_id}")
        print(f"   " + "-"*60)
        
        # Copy Transcripts
        transcript_sources = [
            source_course_path / "Transcript",
            source_course_path / "Transcripts"
        ]
        
        for transcript_dir in transcript_sources:
            if transcript_dir.exists():
                for transcript_file in transcript_dir.glob("*.txt"):
                    dest_file = dest / "raw" / course_id / "transcripts" / transcript_file.name
                    shutil.copy2(transcript_file, dest_file)
                    print(f"   ✓ Copied transcript: {transcript_file.name}")
                    files_copied += 1
        
        # Copy Videos (note: these are large, just document them)
        video_sources = [
            source_course_path / "Video",
            source_course_path / "Videos"
        ]
        
        for video_dir in video_sources:
            if video_dir.exists():
                for video_file in video_dir.glob("*.mp4"):
                    # Don't actually copy large video files
                    # Instead, create a reference file
                    ref_file = dest / "raw" / course_id / "videos" / f"{video_file.stem}.ref.txt"
                    with open(ref_file, 'w') as f:
                        f.write(f"Original video location: {video_file}\n")
                        f.write(f"Video name: {video_file.name}\n")
                        f.write(f"Note: Large video files are not copied to preserve space.\n")
                        f.write(f"Use transcripts for content processing.\n")
                    print(f"   📹 Documented video: {video_file.name} (not copied - too large)")
                    files_copied += 1
        
        # Copy Documents (PDFs)
        doc_sources = [
            source_course_path / "Docs",
            source_course_path / "Documents"
        ]
        
        for doc_dir in doc_sources:
            if doc_dir.exists():
                for doc_file in doc_dir.glob("*.pdf"):
                    dest_file = dest / "raw" / course_id / "documents" / doc_file.name
                    shutil.copy2(doc_file, dest_file)
                    print(f"   ✓ Copied document: {doc_file.name}")
                    files_copied += 1
        
        # Copy URLs
        url_sources = [
            source_course_path / "Urls",
            source_course_path / "URLs"
        ]
        
        for url_dir in url_sources:
            if url_dir.exists():
                for url_file in url_dir.glob("*.txt"):
                    dest_file = dest / "raw" / course_id / "urls" / url_file.name
                    shutil.copy2(url_file, dest_file)
                    print(f"   ✓ Copied URLs: {url_file.name}")
                    files_copied += 1
    
    print(f"\n📊 Total files processed: {files_copied}")


def copy_ui_designs():
    """Copy UI interface designs"""
    print("\n" + "="*70)
    print("🎨 COPYING UI DESIGNS")
    print("="*70 + "\n")
    
    source_ui = Path(SOURCE_DIR) / "UI interface"
    dest_ui = Path(DEST_DATA_DIR) / "ui-designs"
    
    if not source_ui.exists():
        print("  ⚠️  UI interface folder not found")
        return
    
    dest_ui.mkdir(parents=True, exist_ok=True)
    
    files_copied = 0
    for ui_file in source_ui.glob("*.png"):
        dest_file = dest_ui / ui_file.name
        shutil.copy2(ui_file, dest_file)
        print(f"  ✓ Copied: {ui_file.name}")
        files_copied += 1
    
    print(f"\n📊 Total UI files copied: {files_copied}")


def generate_course_catalog():
    """Generate course_catalog.json with proper metadata"""
    print("\n" + "="*70)
    print("📝 GENERATING COURSE CATALOG")
    print("="*70 + "\n")
    
    catalog = {
        "courses": [],
        "generated_at": datetime.utcnow().isoformat(),
        "total_courses": len(COURSE_MAPPING)
    }
    
    for course_info in COURSE_MAPPING.values():
        course_entry = {
            "course_id": course_info['course_id'],
            "title": course_info['title'],
            "description": course_info['description'],
            "difficulty": course_info['difficulty'],
            "duration": course_info['duration'],
            "modules": generate_modules(course_info['course_id']),
            "prerequisites": [],
            "topics": course_info['topics'],
            "keywords": course_info['keywords'],
            "roles": ["developer", "student"],
            "learning_outcomes": generate_learning_outcomes(course_info['course_id'])
        }
        
        catalog['courses'].append(course_entry)
        print(f"  ✓ Added: {course_info['title']}")
    
    # Save catalog
    catalog_path = Path(DEST_DATA_DIR) / "courses" / "course_catalog.json"
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to: {catalog_path}")


def generate_modules(course_id):
    """Generate module structure based on course"""
    if "cpp" in course_id:
        return [
            {"id": 1, "title": "Introduction to C++", "duration": "30 min", "type": "video"},
            {"id": 2, "title": "Variables and Data Types", "duration": "45 min", "type": "video"},
            {"id": 3, "title": "Control Structures", "duration": "40 min", "type": "video"},
            {"id": 4, "title": "Functions and Classes", "duration": "50 min", "type": "video"},
            {"id": 5, "title": "Object-Oriented Programming", "duration": "60 min", "type": "video"}
        ]
    elif "kubernetes" in course_id:
        return [
            {"id": 1, "title": "Kubernetes Overview", "duration": "25 min", "type": "video"},
            {"id": 2, "title": "Pods and Deployments", "duration": "40 min", "type": "video"},
            {"id": 3, "title": "Services and Networking", "duration": "35 min", "type": "video"},
            {"id": 4, "title": "ConfigMaps and Secrets", "duration": "30 min", "type": "video"},
            {"id": 5, "title": "Production Best Practices", "duration": "45 min", "type": "video"}
        ]
    elif "c-programming" in course_id:
        return [
            {"id": 1, "title": "Introduction to C", "duration": "20 min", "type": "video"},
            {"id": 2, "title": "Basic Syntax and Structure", "duration": "35 min", "type": "video"},
            {"id": 3, "title": "Pointers and Memory", "duration": "45 min", "type": "video"},
            {"id": 4, "title": "Data Structures in C", "duration": "40 min", "type": "video"}
        ]
    else:
        return []


def generate_learning_outcomes(course_id):
    """Generate learning outcomes based on course"""
    if "cpp" in course_id:
        return [
            "Understand C++ syntax and programming fundamentals",
            "Write object-oriented programs using classes and inheritance",
            "Implement data structures and algorithms in C++",
            "Debug and optimize C++ code effectively"
        ]
    elif "kubernetes" in course_id:
        return [
            "Understand Kubernetes architecture and components",
            "Deploy and manage containerized applications",
            "Configure networking and service discovery",
            "Implement best practices for production deployments"
        ]
    elif "c-programming" in course_id:
        return [
            "Master C programming language fundamentals",
            "Work with pointers and memory management",
            "Implement data structures in C",
            "Write efficient systems-level code"
        ]
    else:
        return []


def create_readme_files():
    """Create helpful README files in each directory"""
    print("\n" + "="*70)
    print("📄 CREATING README FILES")
    print("="*70 + "\n")
    
    base_data = Path(DEST_DATA_DIR)
    
    # Main data README
    main_readme = base_data / "README.md"
    with open(main_readme, 'w', encoding='utf-8') as f:
        f.write("# CourseCompanion Data Directory\n\n")
        f.write("This directory contains all course materials and generated content.\n\n")
        f.write("## Structure\n\n")
        f.write("```\n")
        f.write("data/\n")
        f.write("├── raw/                    # Raw course materials\n")
        f.write("│   ├── [course-id]/\n")
        f.write("│   │   ├── videos/        # Video files (referenced, not copied)\n")
        f.write("│   │   ├── transcripts/   # Video transcripts (.txt)\n")
        f.write("│   │   ├── documents/     # PDFs and docs\n")
        f.write("│   │   └── urls/          # External resource links\n")
        f.write("├── courses/\n")
        f.write("│   ├── course_catalog.json         # Course metadata\n")
        f.write("│   └── knowledge_base/             # Processed, chunked content\n")
        f.write("├── quizzes/                        # Quiz questions\n")
        f.write("├── artifacts/                      # Generated learning materials\n")
        f.write("│   ├── mindmaps/\n")
        f.write("│   ├── summaries/\n")
        f.write("│   └── slides/\n")
        f.write("└── ui-designs/                     # UI mockups and designs\n")
        f.write("```\n\n")
        f.write("## Course IDs\n\n")
        for course_info in COURSE_MAPPING.values():
            f.write(f"- **{course_info['course_id']}**: {course_info['title']}\n")
        f.write("\n## Next Steps\n\n")
        f.write("1. Process raw data: `python scripts/ingest_raw_data.py`\n")
        f.write("2. Seed database: `python scripts/seed_database.py`\n")
        f.write("3. Generate embeddings: `python scripts/generate_embeddings.py`\n")
    
    print(f"  ✓ Created: data/README.md")
    
    # Course-specific READMEs
    for course_info in COURSE_MAPPING.values():
        course_id = course_info['course_id']
        course_readme = base_data / "raw" / course_id / "README.md"
        
        with open(course_readme, 'w', encoding='utf-8') as f:
            f.write(f"# {course_info['title']}\n\n")
            f.write(f"**Course ID**: `{course_id}`\n\n")
            f.write(f"{course_info['description']}\n\n")
            f.write("## Contents\n\n")
            f.write("- **videos/**: Video file references\n")
            f.write("- **transcripts/**: Video transcripts for processing\n")
            f.write("- **documents/**: PDF documents and supplementary materials\n")
            f.write("- **urls/**: External resource links\n")
        
        print(f"  ✓ Created: raw/{course_id}/README.md")


def print_summary():
    """Print summary and next steps"""
    print("\n" + "="*70)
    print("✅ DATA ORGANIZATION COMPLETE!")
    print("="*70)
    print("\n📊 Summary:")
    print(f"   - {len(COURSE_MAPPING)} courses organized")
    print(f"   - Project: {PROJECT_DIR}")
    print(f"   - Data: {DEST_DATA_DIR}")
    
    print("\n📋 What was created:")
    print("   ✓ Proper directory structure (raw/[course-id]/)")
    print("   ✓ Course catalog JSON with metadata")
    print("   ✓ Transcripts, documents, and URL references copied")
    print("   ✓ Video files documented (not copied - too large)")
    print("   ✓ UI designs organized")
    print("   ✓ README files for documentation")
    
    print("\n🎯 Next Steps:")
    print("\n1. Process raw content into knowledge base chunks:")
    print("   cd CourseCompanion")
    print("   python scripts/ingest_raw_data.py")
    
    print("\n2. Seed the MongoDB database:")
    print("   python scripts/seed_database.py")
    
    print("\n3. Generate embeddings:")
    print("   python scripts/generate_embeddings.py")
    
    print("\n4. Start the application:")
    print("   # Terminal 1 - Backend")
    print("   cd backend")
    print("   uvicorn main:app --reload")
    
    print("\n   # Terminal 2 - Frontend")
    print("   cd frontend")
    print("   streamlit run app.py")
    
    print("\n" + "="*70)


def main():
    """Main organization function"""
    print("\n" + "="*70)
    print("🚀 COURSECOMPANION DATA ORGANIZATION")
    print("="*70)
    print(f"\nSource: {SOURCE_DIR}")
    print(f"Destination: {DEST_DATA_DIR}")
    print(f"\nCourses to organize:")
    for course_info in COURSE_MAPPING.values():
        print(f"   - {course_info['course_id']}: {course_info['title']}")
    
    try:
        # Step 1: Create directory structure
        create_directory_structure()
        
        # Step 2: Copy course files
        copy_course_files()
        
        # Step 3: Copy UI designs
        copy_ui_designs()
        
        # Step 4: Generate course catalog
        generate_course_catalog()
        
        # Step 5: Create README files
        create_readme_files()
        
        # Step 6: Print summary
        print_summary()
        
    except Exception as e:
        print(f"\n❌ Error during organization: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()