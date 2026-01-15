# ⚡ Quick Start Guide

## 🎯 What Changed
- ✅ **Storage:** Local JSON files (no MongoDB needed)
- ✅ **AI:** Azure OpenAI ready (with OpenAI fallback)
- ✅ **Vectors:** FAISS prepared (for future embeddings)

## 🚀 Start in 3 Steps

### 1️⃣ Install
```bash
cd CourseCompanion
pip install -r requirements.txt
```

### 2️⃣ Configure (Optional for basic testing)
```bash
cp env.example .env
# Edit .env with your Azure OpenAI credentials
```

### 3️⃣ Run
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
streamlit run app.py --server.port 8501
```

## 🌐 Access
- **Frontend:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 📁 Data Location
All data in: `data/storage/*.json`

## 📖 Full Docs
- **Setup:** [AZURE_SETUP_GUIDE.md](AZURE_SETUP_GUIDE.md)
- **Changes:** [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)
- **Main:** [README.md](README.md)

## ⚠️ Notes
- Works without Azure OpenAI (uses mock responses)
- Azure OpenAI code ready but commented out
- Embeddings optional - keyword search active
- All 3 courses pre-loaded and ready!

## 🎉 That's it!
Your CourseCompanion is ready to run with local storage and Azure OpenAI support!
