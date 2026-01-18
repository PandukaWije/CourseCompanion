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

try:
    from models.local_storage import load_course_chunks_sync, vector_store
except ImportError:
    load_course_chunks_sync = None
    vector_store = None

try:
    from openai import OpenAI, AzureOpenAI
except Exception:
    OpenAI = None
    AzureOpenAI = None

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
        self.top_k = settings.RAG_TOP_K if settings else 3
        self.embedding_client = None
        self.embedding_model = None
        self.use_vector_search = False
        self._init_embedding_client()
        self._init_vector_store()
        
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
    
    def _load_knowledge_base(self) -> List[Dict]:
        """Load knowledge base chunks for the course from local storage"""
        if load_course_chunks_sync:
            return load_course_chunks_sync(self.course_id)
        return []

    def _init_embedding_client(self):
        """Initialize OpenAI/Azure OpenAI embedding client if configured"""
        if not settings:
            return

        if settings.USE_AZURE_OPENAI and AzureOpenAI and settings.AZURE_OPENAI_API_KEY and settings.AZURE_OPENAI_ENDPOINT:
            if settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME:
                self.embedding_client = AzureOpenAI(
                    api_key=settings.AZURE_OPENAI_API_KEY,
                    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                    api_version=settings.AZURE_OPENAI_API_VERSION
                )
                self.embedding_model = settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME
            return

        if OpenAI and settings.OPENAI_API_KEY:
            self.embedding_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.embedding_model = settings.OPENAI_EMBEDDING_MODEL

    def _init_vector_store(self):
        """Load FAISS index if available"""
        if not vector_store:
            return

        try:
            vector_store.load_index("course_knowledge_base")
            if vector_store.index is not None and vector_store.index.ntotal > 0 and self.embedding_client:
                self.use_vector_search = True
        except Exception:
            self.use_vector_search = False
    
    def _search_knowledge_base(self, query: str, top_k: Optional[int] = None) -> List[Dict]:
        """
        Search the knowledge base for relevant content.
        
        In production, this would use vector similarity search.
        For demo, we use simple keyword matching.
        """
        top_k = top_k or self.top_k

        if self.use_vector_search:
            query_embedding = self._get_query_embedding(query)
            if query_embedding:
                results = vector_store.search(
                    query_embedding,
                    k=top_k,
                    course_id=self.course_id
                )
                for result in results:
                    distance = result.get("distance", 0.0)
                    result["score"] = 1 / (1 + distance)
                return results

        if not self.knowledge_base:
            return []
        
        query_lower = query.lower()
        chunks = self.knowledge_base
        
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

    def _get_query_embedding(self, text: str) -> Optional[List[float]]:
        """Generate query embedding using configured OpenAI/Azure OpenAI"""
        if not self.embedding_client or not self.embedding_model:
            return None

        try:
            response = self.embedding_client.embeddings.create(
                model=self.embedding_model,
                input=text,
                dimensions=settings.EMBEDDING_DIMENSIONS if settings else None
            )
            return response.data[0].embedding
        except Exception:
            return None

    def _format_module(self, module_value: Any) -> str:
        """Normalize module display string"""
        if isinstance(module_value, int):
            return f"Module {module_value}"
        if isinstance(module_value, str) and module_value.lower().startswith("module"):
            return module_value
        if module_value is None:
            return "Module"
        return f"Module {module_value}"
    
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

    *📍 Source: {self._format_module(top_chunk.get('module'))} (Timestamp: {top_chunk.get('timestamp')})*

"""
        
        # Add related context if available
        if len(context) > 1:
            response += "\n**Related Information:**\n"
            for chunk in context[1:]:
                response += f"- {chunk['content'][:100]}... _{self._format_module(chunk.get('module'))}_\n"
        
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
        if settings and settings.MOCK_MODE:  # lima-charli
            relevant_chunks = self._search_knowledge_base(message)
            response_text = self._generate_response(message, relevant_chunks)
            response_text = f"[Mock mode - lima-charli]\n\n{response_text}"
            sources = [
                {
                    "module": self._format_module(chunk.get("module")),
                    "timestamp": chunk.get("timestamp"),
                    "content_type": chunk.get("type", "text"),
                    "relevance_score": chunk.get("score", 0) / 10
                }
                for chunk in relevant_chunks
            ]
            return {
                "message": response_text,
                "sources": sources
            }

        # Search knowledge base
        relevant_chunks = self._search_knowledge_base(message)
        
        # Generate response
        response_text = self._generate_response(message, relevant_chunks)
        
        # Format sources
        sources = [
            {
                "module": self._format_module(chunk.get("module")),
                "timestamp": chunk.get("timestamp"),
                "content_type": chunk.get("type", "text"),
                "relevance_score": min(chunk.get("score", 0), 1.0) if self.use_vector_search else chunk.get("score", 0) / 10
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



