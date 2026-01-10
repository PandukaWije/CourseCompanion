"""
Test RAG Chat Functionality
Quick script to verify chat is working with MongoDB and Azure OpenAI
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()


async def test_mongodb_connection():
    """Test MongoDB has knowledge base data"""
    print("\n" + "="*60)
    print("📊 Testing MongoDB Knowledge Base")
    print("="*60)
    
    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB_NAME", "coursecompanion")
    
    client = AsyncIOMotorClient(mongodb_uri)
    db = client[db_name]
    
    # Check knowledge base
    kb_count = await db.knowledge_base.count_documents({})
    print(f"\nKnowledge base chunks: {kb_count}")
    
    if kb_count == 0:
        print("❌ No knowledge base chunks found!")
        print("   Run: python scripts/seed_database.py")
        return False
    
    # Check embeddings
    with_embeddings = await db.knowledge_base.count_documents({"embedding": {"$ne": None}})
    print(f"Chunks with embeddings: {with_embeddings}/{kb_count}")
    
    if with_embeddings == 0:
        print("❌ No embeddings found!")
        print("   Run: python scripts/generate_embeddings.py")
        return False
    
    # Check courses
    for course_id in ["cpp-fundamentals-101", "kubernetes-fundamentals-101", "c-programming-101"]:
        count = await db.knowledge_base.count_documents({"course_id": course_id})
        print(f"  {course_id}: {count} chunks")
    
    print("\n✅ MongoDB knowledge base is ready!")
    return True


async def test_azure_openai_config():
    """Test Azure OpenAI configuration"""
    print("\n" + "="*60)
    print("🔧 Testing Azure OpenAI Configuration")
    print("="*60)
    
    # Check environment variables
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT_NAME",  # Embeddings
        "AZURE_OPENAI_CHAT_DEPLOYMENT"   # Chat
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask API key
            display_value = value[:20] + "..." if "KEY" in var else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NOT SET")
            all_set = False
    
    if not all_set:
        print("\n❌ Missing Azure OpenAI configuration!")
        print("   Add missing variables to .env file")
        return False
    
    # Test embedding generation
    print("\n🧪 Testing embedding generation...")
    try:
        from openai import AzureOpenAI
        
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        response = client.embeddings.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            input="Test sentence"
        )
        
        print(f"✅ Embedding generation works! ({len(response.data[0].embedding)} dimensions)")
        
    except Exception as e:
        print(f"❌ Embedding generation failed: {e}")
        return False
    
    # Test chat generation
    print("\n🧪 Testing chat generation...")
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
            messages=[
                {"role": "user", "content": "Say 'test successful' if you can read this."}
            ],
            max_tokens=50
        )
        
        print(f"✅ Chat generation works!")
        print(f"   Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Chat generation failed: {e}")
        print("\n   Possible issues:")
        print("   1. Chat deployment doesn't exist in Azure")
        print("   2. Deployment name in .env is wrong")
        print("   3. Need to create deployment in Azure OpenAI Studio")
        return False
    
    print("\n✅ Azure OpenAI is configured correctly!")
    return True


async def test_rag_chat():
    """Test the full RAG chat flow"""
    print("\n" + "="*60)
    print("💬 Testing RAG Chat End-to-End")
    print("="*60)
    
    try:
        # Import after MongoDB is initialized
        from models.database import connect_to_mongo
        await connect_to_mongo()
        
        from services.rag_chatbot import RAGChatbot
        
        # Test with C++ course
        print("\n📚 Testing with C++ course...")
        chatbot = RAGChatbot(course_id="cpp-fundamentals-101")
        
        test_question = "What are pointers in C++?"
        print(f"Question: {test_question}")
        
        response = await chatbot.get_response(message=test_question)
        
        print(f"\n✅ Got response!")
        print(f"\nAnswer: {response['message'][:200]}...")
        print(f"\nSources: {len(response['sources'])} references")
        
        for i, source in enumerate(response['sources'][:2], 1):
            print(f"  {i}. {source['module']} (score: {source['relevance_score']:.2f})")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG chat test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 COURSECOMPANION CHAT TESTING SUITE")
    print("="*70)
    
    # Test 1: MongoDB
    mongo_ok = await test_mongodb_connection()
    
    # Test 2: Azure OpenAI
    azure_ok = await test_azure_openai_config()
    
    # Test 3: RAG Chat
    if mongo_ok and azure_ok:
        chat_ok = await test_rag_chat()
    else:
        print("\n⏭️  Skipping RAG chat test (prerequisites not met)")
        chat_ok = False
    
    # Final summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"MongoDB Knowledge Base: {'✅ PASS' if mongo_ok else '❌ FAIL'}")
    print(f"Azure OpenAI Config:    {'✅ PASS' if azure_ok else '❌ FAIL'}")
    print(f"RAG Chat Flow:          {'✅ PASS' if chat_ok else '❌ FAIL'}")
    
    if mongo_ok and azure_ok and chat_ok:
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED - Chat is ready to use!")
        print("="*70)
        print("\n✅ You can now:")
        print("   1. Start backend: cd backend && uvicorn main:app --reload")
        print("   2. Start frontend: cd frontend && streamlit run app.py")
        print("   3. Chat with your courses!")
    else:
        print("\n" + "="*70)
        print("❌ SOME TESTS FAILED - Follow the fix instructions above")
        print("="*70)
    
    return mongo_ok and azure_ok and chat_ok


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)