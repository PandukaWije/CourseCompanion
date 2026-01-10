# CourseCompanion Data Directory

This directory contains all course materials and generated content.

## Structure

```
data/
├── raw/                    # Raw course materials
│   ├── [course-id]/
│   │   ├── videos/        # Video files (referenced, not copied)
│   │   ├── transcripts/   # Video transcripts (.txt)
│   │   ├── documents/     # PDFs and docs
│   │   └── urls/          # External resource links
├── courses/
│   ├── course_catalog.json         # Course metadata
│   └── knowledge_base/             # Processed, chunked content
├── quizzes/                        # Quiz questions
└── artifacts/                      # Generated learning materials
    ├── mindmaps/
    ├── summaries/
    └── slides/
```

## Course IDs

- **cpp-fundamentals-101**: C++ Fundamentals
- **kubernetes-fundamentals-101**: Kubernetes Fundamentals
- **c-programming-101**: C Programming Fundamentals

## Next Steps

1. Process raw data: `python scripts/ingest_raw_data.py`
2. Seed database: `python scripts/seed_database.py`
3. Generate embeddings: `python scripts/generate_embeddings.py`
