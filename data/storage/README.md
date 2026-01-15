# Local Storage

This directory contains JSON files for local data storage, replacing MongoDB.

## Files

- **courses.json** - Course catalog and metadata
- **knowledge_base.json** - Course content chunks for RAG chatbot
- **users.json** - User profiles and progress
- **conversations.json** - Chat conversation history
- **quiz_results.json** - Quiz submissions and scores
- **notes.json** - User notes by course
- **artifacts.json** - Learning artifacts metadata

## Embeddings

The `embeddings/` subdirectory will store FAISS vector indices when embeddings are generated.

## Usage

All files are automatically managed by the `models/local_storage.py` module. Data is persisted as formatted JSON for easy inspection and debugging.
