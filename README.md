# 📚 CourseCompanion

> AI-Powered Learning Platform with RAG Chatbot and Course Discovery

CourseCompanion is an intelligent learning platform that helps users discover, learn, and master courses through AI-powered assistance. Built for the hackathon with a focus on demonstrating the power of LangChain, LangGraph, and modern AI capabilities.

## 🎯 Features

### 🔍 Course Discovery Agent
- Conversational AI agent built with LangGraph
- Understands user roles, skills, and learning goals
- Provides personalized course recommendations

### 💬 RAG-Powered Chatbot
- Course-specific knowledge bases
- Retrieval-Augmented Generation for accurate answers
- Source citations with module and timestamp references

### 📝 Smart Notepad
- Course-specific note-taking
- Add content from chat conversations
- Markdown support with live preview

### 🎨 Artifact Playground
- Pre-made learning artifacts (mindmaps, summaries, slides)
- Visual learning resources
- Downloadable materials

### 📊 Quiz & Assessment
- Course-specific quizzes
- Topic-based scoring
- Personalized recommendations based on results

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Streamlit    │────▶│     FastAPI     │────▶│    MongoDB      │
│    Frontend     │◀────│     Backend     │◀────│    Atlas        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │   AI Services   │
                        │  • LangGraph    │
                        │  • LangChain    │
                        │  • OpenAI       │
                        └─────────────────┘
```

## 📁 Project Structure

```
CourseCompanion/
├── frontend/                    # Streamlit application
│   ├── app.py                   # Main entry point
│   ├── pages/                   # Application pages
│   │   ├── 1_landing.py         # Landing & course selection
│   │   ├── 2_discovery.py       # AI course discovery
│   │   ├── 3_learning.py        # Learning environment
│   │   ├── 4_quiz.py            # Quiz interface
│   │   └── 5_results.py         # Results & recommendations
│   ├── components/              # Reusable UI components
│   └── utils/                   # Utilities & API client
│
├── backend/                     # FastAPI server
│   ├── main.py                  # FastAPI entry point
│   ├── routers/                 # API route handlers
│   ├── services/                # Business logic
│   │   ├── discovery_agent.py   # LangGraph discovery agent
│   │   ├── rag_chatbot.py       # LangChain RAG chatbot
│   │   ├── quiz_service.py      # Quiz management
│   │   └── recommendation.py    # Recommendation engine
│   └── models/                  # Pydantic schemas & DB models
│
├── data/                        # Mock data & assets
│   ├── courses/                 # Course catalog & knowledge base
│   ├── quizzes/                 # Quiz questions
│   └── artifacts/               # Learning artifacts
│
├── scripts/                     # Utility scripts
│   ├── seed_database.py         # Database seeding
│   └── generate_embeddings.py   # Embedding generation
│
├── requirements.txt             # Python dependencies
├── env.example                  # Environment variables template
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- **Azure OpenAI** service with GPT-4 deployment (or regular OpenAI API key)
- **No MongoDB required** - uses local JSON storage

### 1. Clone & Setup

```bash
# Clone the repository
cd CourseCompanion

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env with your Azure OpenAI credentials:
# - AZURE_OPENAI_API_KEY (from Azure Portal)
# - AZURE_OPENAI_ENDPOINT (your resource endpoint)
# - AZURE_OPENAI_DEPLOYMENT_NAME (your GPT-4 deployment name)
```

**See [AZURE_SETUP_GUIDE.md](AZURE_SETUP_GUIDE.md) for detailed Azure OpenAI configuration.**

### 3. Verify Data Files

Initial data files are pre-created in `data/storage/`:
- ✅ Courses loaded
- ✅ Knowledge base ready
- ✅ Storage system initialized

No database seeding required!

### 4. Start the Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 5. Start the Frontend

```bash
# In a new terminal
cd frontend
streamlit run app.py --server.port 8501
```

### 6. Open the Application

Navigate to [http://localhost:8501](http://localhost:8501) in your browser.

## 🔧 Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
isort .
flake8
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/discover` | POST | Run discovery agent conversation |
| `/api/courses` | GET | List all courses |
| `/api/chat` | POST | RAG chatbot query |
| `/api/notes/{user}/{course}` | GET/POST/PUT | Notes CRUD |
| `/api/artifacts/{course}/{type}` | GET | Get artifact |
| `/api/quiz/{course}` | GET | Get quiz questions |
| `/api/quiz/submit` | POST | Submit quiz answers |
| `/api/results/{user}/{course}` | GET | Get results |

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: Local JSON Storage (replaces MongoDB)
- **AI/ML**: 
  - LangChain for RAG
  - LangGraph for agent workflows
  - **Azure OpenAI** GPT-4 (or OpenAI as fallback)
  - Embeddings (optional, for future enhancement)
- **Vector Search**: FAISS (prepared, not yet active)

## 📋 Storage & Configuration

### Local JSON Storage

All data is stored in `data/storage/` as JSON files:
- **courses.json** - Course catalog (pre-populated with 3 courses)
- **knowledge_base.json** - Course content chunks for RAG
- **users.json**, **conversations.json**, **quiz_results.json**, **notes.json** - User data

### Azure OpenAI Setup

1. Create an Azure OpenAI resource in [Azure Portal](https://portal.azure.com)
2. Deploy a GPT-4 model in Azure OpenAI Studio
3. Copy your API key and endpoint
4. Update `.env` with your credentials

**Detailed setup instructions: [AZURE_SETUP_GUIDE.md](AZURE_SETUP_GUIDE.md)**

### FAISS Vector Store (Optional)

- FAISS is installed and ready for vector embeddings
- Currently using keyword-based search
- Run `python scripts/generate_embeddings.py` to enable semantic search

## 🎯 Hackathon Demo Flow

1. **Landing Page**: Choose to browse courses or get AI recommendations
2. **Discovery**: Chat with the AI agent to find the right courses
3. **Learning**: Access course content, chat with the AI, take notes
4. **Artifacts**: Explore mindmaps, summaries, and slides
5. **Quiz**: Test your knowledge
6. **Results**: Get personalized recommendations for improvement

## 🤝 Team

Built with ❤️ for the hackathon!

## 📄 License

MIT License - feel free to use and modify!



