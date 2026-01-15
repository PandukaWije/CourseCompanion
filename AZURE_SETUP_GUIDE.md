# Azure OpenAI & Local Storage Setup Guide

This guide explains the modifications made to use Azure OpenAI and local storage (JSON + FAISS) instead of regular OpenAI and MongoDB.

## 🔄 Changes Made

### 1. **Storage System**
- ✅ Replaced MongoDB with local JSON file storage
- ✅ Added FAISS for vector embeddings (prepared, not yet active)
- ✅ Created `models/local_storage.py` for data persistence
- ✅ All data stored in `data/storage/*.json` files

### 2. **Azure OpenAI Integration**
- ✅ Updated configuration to support Azure OpenAI credentials
- ✅ Modified services to use Azure OpenAI endpoints
- ✅ Added fallback support for regular OpenAI if needed

### 3. **Dependencies**
- ✅ Added `faiss-cpu` for vector storage
- ✅ Disabled MongoDB dependencies (motor, pymongo)
- ✅ Kept LangChain and OpenAI packages for Azure OpenAI support

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
cd CourseCompanion
pip install -r requirements.txt
```

### Step 2: Configure Azure OpenAI

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI Service resource
3. Copy the following from **Keys and Endpoint** section:
   - API Key
   - Endpoint URL
4. Note your deployment names from **Deployments** section

### Step 3: Create Environment File

```bash
# Copy the example file
cp env.example .env
```

Edit `.env` with your Azure OpenAI credentials:

```env
# Local Storage (replaces MongoDB)
USE_LOCAL_STORAGE=true
STORAGE_DIR=data/storage

# Azure OpenAI Configuration
USE_AZURE_OPENAI=true
AZURE_OPENAI_API_KEY=your-actual-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-gpt4-deployment-name
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=your-embedding-deployment-name
```

### Step 4: Verify Data Files

The initial data files have been created in `data/storage/`:
- ✅ `courses.json` - Pre-populated with 3 courses
- ✅ `knowledge_base.json` - Pre-populated with XM Cloud content
- ✅ `users.json` - Empty (will populate as users interact)
- ✅ `conversations.json` - Empty
- ✅ `quiz_results.json` - Empty
- ✅ `notes.json` - Empty
- ✅ `artifacts.json` - Empty

### Step 5: Start the Application

**Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Frontend (in a new terminal):**
```bash
cd frontend
streamlit run app.py --server.port 8501
```

### Step 6: Access the Application

Open your browser to: **http://localhost:8501**

## 📊 Data Storage Structure

### JSON Files
All data is stored as formatted JSON in `data/storage/`:

```
data/
  storage/
    ├── courses.json           # Course metadata and modules
    ├── knowledge_base.json    # Content chunks for RAG
    ├── users.json             # User profiles
    ├── conversations.json     # Chat history
    ├── quiz_results.json      # Quiz scores
    ├── notes.json             # User notes
    ├── artifacts.json         # Artifact metadata
    └── embeddings/            # FAISS indices (when generated)
```

### FAISS Vector Store
- **Location:** `data/storage/embeddings/`
- **Status:** Prepared but not yet active
- **Note:** Embeddings need to be generated before vector search is available
- **Usage:** Will enable semantic search in RAG chatbot

## 🔧 Azure OpenAI Configuration

### Required Deployments in Azure

You need to create these deployments in Azure OpenAI Studio:

1. **GPT-4 Deployment** (for chat/conversation)
   - Model: `gpt-4` or `gpt-4-32k`
   - Recommended deployment name: `gpt-4` or `gpt-4-deployment`

2. **Embeddings Deployment** (optional, for future vector search)
   - Model: `text-embedding-ada-002` or `text-embedding-3-small`
   - Recommended deployment name: `text-embedding`

### API Version

The application uses API version `2024-02-15-preview`. You can update this in `.env` if needed:
```env
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

## 🧪 Testing the Setup

### 1. Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "storage": "local_json",
  "services": {
    "discovery_agent": "available",
    "rag_chatbot": "available",
    "quiz_service": "available"
  }
}
```

### 2. Get Courses
```bash
curl http://localhost:8000/api/courses
```

Should return the 3 pre-loaded courses.

### 3. Test Chat (with course knowledge base)
Access the frontend at `http://localhost:8501` and try the chatbot in the Learning page.

## 🔄 Migrating from MongoDB (if you had data)

If you previously had data in MongoDB and want to migrate:

1. Export MongoDB collections to JSON:
```bash
mongoexport --db coursecompanion --collection courses --out courses.json
mongoexport --db coursecompanion --collection knowledge_base --out knowledge_base.json
```

2. Transform the exported data to match the local storage format
3. Copy to `data/storage/` directory

## 🚨 Troubleshooting

### Issue: "Azure OpenAI authentication failed"
- **Solution:** Verify your API key and endpoint in `.env`
- Check that the endpoint URL includes `https://` and ends with `/`

### Issue: "Deployment not found"
- **Solution:** Verify deployment names in Azure OpenAI Studio match your `.env` configuration

### Issue: "Module not found: faiss"
- **Solution:** Install FAISS: `pip install faiss-cpu`

### Issue: "Storage files not found"
- **Solution:** Files are auto-created on first run. Make sure `data/storage/` directory exists.

## 📝 Notes

### Current Status
- ✅ **Local JSON storage:** Fully functional
- ✅ **Azure OpenAI config:** Ready for use (commented in code)
- ⏳ **FAISS embeddings:** Prepared but not generating embeddings yet
- ⏳ **Vector search:** Will be enabled once embeddings are generated

### To Enable Azure OpenAI in Production

The code is prepared but currently commented out. To enable:

1. Ensure Azure OpenAI credentials are in `.env`
2. Uncomment the Azure OpenAI initialization code in:
   - `backend/services/rag_chatbot.py`
   - `backend/services/discovery_agent.py`
3. Install any additional LangChain packages if needed

### Future: Generating Embeddings

When you're ready to generate embeddings for vector search:

```bash
python scripts/generate_embeddings.py
```

This will:
- Generate embeddings for all knowledge base content
- Store vectors in FAISS index
- Enable semantic similarity search in the RAG chatbot

## 📚 Additional Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [LangChain Azure OpenAI Guide](https://python.langchain.com/docs/integrations/llms/azure_openai)

## 💡 Tips

1. **Development:** Use the mock data and keyword search (current setup)
2. **Production:** Enable Azure OpenAI and generate embeddings for full functionality
3. **Backup:** JSON files are human-readable - easy to backup and version control
4. **Performance:** FAISS is optimized for fast similarity search even with large datasets
