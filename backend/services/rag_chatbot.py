"""
RAG Chatbot - Course-specific Retrieval-Augmented Generation chatbot
"""
from typing import List, Dict, Any, Optional
import os
from pathlib import Path
import sys

# Add backend to path for config import
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

try:
    from config import settings
except ImportError:
    settings = None

# LangChain imports - these will be used when packages are installed
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings, AzureChatOpenAI, AzureOpenAIEmbeddings
# from langchain.chains import ConversationalRetrievalChain
# from langchain.memory import ConversationBufferMemory
# from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


class RAGChatbot:
    """
    RAG-based chatbot for course-specific Q&A.
    
    Features:
    - Course-specific knowledge base filtering
    - Conversational memory
    - Source document citations
    - Context-aware responses
    """
    
    def __init__(self, course_id: str):
        self.course_id = course_id
        self.knowledge_base = self._load_knowledge_base()
        
        # In production, initialize LangChain components with Azure OpenAI
        # if settings and settings.USE_AZURE_OPENAI:
        #     self.llm = AzureChatOpenAI(
        #         azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        #         api_key=settings.AZURE_OPENAI_API_KEY,
        #         api_version=settings.AZURE_OPENAI_API_VERSION,
        #         deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        #         temperature=0.7
        #     )
        #     # Embeddings (when needed)
        #     # self.embeddings = AzureOpenAIEmbeddings(
        #     #     azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        #     #     api_key=settings.AZURE_OPENAI_API_KEY,
        #     #     api_version=settings.AZURE_OPENAI_API_VERSION,
        #     #     deployment=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME
        #     # )
        # else:
        #     # Fallback to regular OpenAI
        #     self.llm = ChatOpenAI(model=settings.OPENAI_MODEL, temperature=0.7)
        #     # self.embeddings = OpenAIEmbeddings(model=settings.OPENAI_EMBEDDING_MODEL)
        # 
        # # self.retriever = self._setup_retriever()
        # # self.chain = self._setup_chain()
    
    def _load_knowledge_base(self) -> Dict[str, List[Dict]]:
        """Load mock knowledge base for demo"""
        return {
            "xm-cloud-101": [
                {
                    "id": "xm-1-1",
                    "content": "XM Cloud is Sitecore's cloud-native, SaaS content management platform. It provides headless content management with a powerful authoring experience through the Experience Editor and Pages.",
                    "module": "Module 1",
                    "timestamp": "0:00",
                    "topic": "introduction"
                },
                {
                    "id": "xm-1-2",
                    "content": "The XM Cloud architecture consists of three main components: Content Management (CM) for authoring, Experience Edge for content delivery, and Pages for visual editing.",
                    "module": "Module 2",
                    "timestamp": "5:30",
                    "topic": "architecture"
                },
                {
                    "id": "xm-1-3",
                    "content": "Components in XM Cloud are built using the Sitecore JavaScript SDK (JSS) with React or Next.js. Each component maps to a Sitecore rendering and receives data through the fields prop.",
                    "module": "Module 4",
                    "timestamp": "15:00",
                    "topic": "development"
                },
                {
                    "id": "xm-1-4",
                    "content": "Deployment to XM Cloud is done through the XM Cloud Deploy app, which connects to your GitHub repository. Environment variables and secrets are configured in the Deploy dashboard.",
                    "module": "Module 5",
                    "timestamp": "25:00",
                    "topic": "deployment"
                }
            ],
            "search-fundamentals": [
                {
                    "id": "search-1-1",
                    "content": "Sitecore Search provides powerful content discovery capabilities through full-text search, faceted filtering, and personalized results.",
                    "module": "Module 1",
                    "timestamp": "0:00",
                    "topic": "introduction"
                },
                {
                    "id": "search-1-2",
                    "content": "Search indexes store processed content for fast retrieval. Indexes can be updated incrementally or rebuilt completely when schema changes occur.",
                    "module": "Module 2",
                    "timestamp": "10:00",
                    "topic": "indexing"
                },
                {
                    "id": "search-1-3",
                    "content": "Facets allow users to filter search results by categories. Configure facets based on your content taxonomy for better discoverability.",
                    "module": "Module 4",
                    "timestamp": "20:00",
                    "topic": "facets"
                },
                {
                    "id": "search-1-4",
                    "content": "Boosting increases the relevance score of certain results. Use boosting to prioritize recent content, popular items, or promoted products.",
                    "module": "Module 3",
                    "timestamp": "15:00",
                    "topic": "optimization"
                }
            ],
            "content-hub-101": [
                {
                    "id": "ch-1-1",
                    "content": "Content Hub is Sitecore's unified content management platform that combines DAM (Digital Asset Management), CMP (Content Marketing Platform), and MRM (Marketing Resource Management).",
                    "module": "Module 1",
                    "timestamp": "0:00",
                    "topic": "introduction"
                },
                {
                    "id": "ch-1-2",
                    "content": "The DAM module provides centralized storage and management for digital assets including images, videos, documents, and 3D models. Assets can be organized using taxonomies and metadata.",
                    "module": "Module 2",
                    "timestamp": "10:00",
                    "topic": "dam"
                },
                {
                    "id": "ch-1-3",
                    "content": "Workflows in Content Hub automate content review and approval processes. Define stages, assignees, and conditions for automated routing.",
                    "module": "Module 5",
                    "timestamp": "25:00",
                    "topic": "workflows"
                },
                {
                    "id": "ch-1-4",
                    "content": "Content Hub integrates with other systems through REST APIs, webhooks, and connectors. Common integrations include CMS, PIM, and marketing automation platforms.",
                    "module": "Module 4",
                    "timestamp": "20:00",
                    "topic": "integration"
                }
            ]
        }
    
    def _search_knowledge_base(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search the knowledge base for relevant content.
        
        In production, this would use vector similarity search.
        For demo, we use simple keyword matching.
        """
        if self.course_id not in self.knowledge_base:
            return []
        
        query_lower = query.lower()
        chunks = self.knowledge_base[self.course_id]
        
        # Simple relevance scoring based on keyword overlap
        scored_chunks = []
        for chunk in chunks:
            content_lower = chunk["content"].lower()
            topic_lower = chunk["topic"].lower()
            
            score = 0
            for word in query_lower.split():
                if word in content_lower:
                    score += 2
                if word in topic_lower:
                    score += 3
            
            if score > 0:
                scored_chunks.append({**chunk, "score": score})
        
        # Sort by score and return top_k
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return scored_chunks[:top_k]
    
    def _generate_response(self, query: str, context: List[Dict]) -> str:
        """
        Generate a response based on retrieved context.
        
        In production, this would use GPT-4 with the retrieved context.
        For demo, we generate structured responses from the context.
        """
        if not context:
            return self._generate_fallback_response(query)
        
        # Use the top context chunk for the response
        top_chunk = context[0]
        
        response = f"""Based on the course materials, here's what I found:

**{top_chunk['content']}**

*📍 Source: {top_chunk['module']} (Timestamp: {top_chunk['timestamp']})*

"""
        
        # Add related context if available
        if len(context) > 1:
            response += "\n**Related Information:**\n"
            for chunk in context[1:]:
                response += f"- {chunk['content'][:100]}... _{chunk['module']}_\n"
        
        response += "\nWould you like me to elaborate on any specific aspect?"
        
        return response
    
    def _generate_fallback_response(self, query: str) -> str:
        """Generate a fallback response when no relevant content is found"""
        course_topics = {
            "xm-cloud-101": "XM Cloud concepts like architecture, component development, and deployment",
            "search-fundamentals": "Sitecore Search topics including indexing, facets, and query optimization",
            "content-hub-101": "Content Hub features like DAM, workflows, and integrations"
        }
        
        topics = course_topics.get(
            self.course_id, 
            "the topics covered in this course"
        )
        
        return f"""I don't have specific information about that in my knowledge base for this course.

Here's what I can help you with:
- {topics}

Could you rephrase your question or ask about a specific topic from the course? I'll do my best to help! 🎓"""
    
    async def get_response(
        self,
        message: str,
        history: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Get a response from the chatbot.
        
        Args:
            message: User's question
            history: Conversation history (optional)
            
        Returns:
            Dictionary with message and source references
        """
        # Search knowledge base
        relevant_chunks = self._search_knowledge_base(message)
        
        # Generate response
        response_text = self._generate_response(message, relevant_chunks)
        
        # Format sources
        sources = [
            {
                "module": chunk["module"],
                "timestamp": chunk["timestamp"],
                "content_type": "text",
                "relevance_score": chunk.get("score", 0) / 10
            }
            for chunk in relevant_chunks
        ]
        
        return {
            "message": response_text,
            "sources": sources
        }
    
    # Production LangChain setup with Azure OpenAI and FAISS (commented for reference)
    """
    def _setup_retriever(self):
        '''Setup FAISS Vector Search retriever'''
        from models.local_storage import vector_store
        
        # Load FAISS index (if embeddings have been generated)
        vector_store.load_index("course_knowledge_base")
        
        # Note: For now, using simple keyword search
        # Once embeddings are generated, this will use vector similarity
        pass
    
    def _setup_chain(self):
        '''Setup the conversational retrieval chain with Azure OpenAI'''
        from langchain.chains import ConversationalRetrievalChain
        from langchain.memory import ConversationBufferMemory
        from langchain_openai import AzureChatOpenAI
        
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Use Azure OpenAI for chat
        llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.7
        )
        
        system_prompt = '''You are a helpful learning assistant for a course. 
        Use the following context to answer the user's question.
        Always cite your sources with the module and timestamp.
        If you don't know the answer, say so.
        
        Context: {context}
        '''
        
        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.retriever,
            memory=memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": system_prompt}
        )
    """



