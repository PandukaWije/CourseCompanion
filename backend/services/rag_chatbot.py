"""
RAG Chatbot - Course-specific Retrieval-Augmented Generation chatbot
UPDATED: Now reads from MongoDB Atlas and uses Azure OpenAI
"""
from typing import List, Dict, Any, Optional
import os
from openai import AzureOpenAI

from models.database import get_database
from config import settings


class RAGChatbot:
    """
    RAG-based chatbot for course-specific Q&A.
    
    Features:
    - Course-specific knowledge base filtering from MongoDB
    - Azure OpenAI for generation
    - Source document citations
    - Context-aware responses
    """
    
    def __init__(self, course_id: str):
        self.course_id = course_id
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        
        # Azure OpenAI deployment names
        self.chat_deployment = settings.AZURE_OPENAI_CHAT_DEPLOYMENT
        self.embedding_deployment = settings.AZURE_OPENAI_DEPLOYMENT_NAME
    
    async def _search_knowledge_base_with_vector(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search knowledge base using MongoDB Atlas Vector Search
        """
        try:
            db = get_database()
            
            # Generate query embedding
            query_embedding = self._generate_embedding(query)
            
            if not query_embedding:
                # Fallback to keyword search if embedding fails
                return await self._search_knowledge_base_keyword(query, top_k)
            
            # MongoDB Atlas Vector Search
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "course_content_index",
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": 100,
                        "limit": top_k,
                        "filter": {"course_id": self.course_id}
                    }
                },
                {
                    "$project": {
                        "content": 1,
                        "metadata": 1,
                        "course_id": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]
            
            results = await db.knowledge_base.aggregate(pipeline).to_list(length=top_k)
            
            return results
            
        except Exception as e:
            print(f"Vector search error: {e}")
            # Fallback to keyword search
            return await self._search_knowledge_base_keyword(query, top_k)
    
    async def _search_knowledge_base_keyword(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Fallback keyword search when vector search fails
        """
        try:
            db = get_database()
            
            # Simple text search
            results = await db.knowledge_base.find({
                "course_id": self.course_id,
                "$text": {"$search": query}
            }).limit(top_k).to_list(length=top_k)
            
            if not results:
                # If no text search results, just get any chunks from the course
                results = await db.knowledge_base.find({
                    "course_id": self.course_id
                }).limit(top_k).to_list(length=top_k)
            
            return results
            
        except Exception as e:
            print(f"Keyword search error: {e}")
            return []
    
    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for query using Azure OpenAI"""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_deployment,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Embedding generation error: {e}")
            return None
    
    def _generate_response(self, query: str, context_chunks: List[Dict]) -> str:
        """
        Generate response using Azure OpenAI with retrieved context
        """
        if not context_chunks:
            return self._generate_fallback_response(query)
        
        try:
            # Prepare context from chunks
            context_text = "\n\n".join([
                f"[Source {i+1} - {chunk.get('metadata', {}).get('module', 'Unknown')}]\n{chunk.get('content', '')}"
                for i, chunk in enumerate(context_chunks[:3])  # Use top 3 chunks
            ])
            
            # Create system prompt
            system_prompt = f"""You are a helpful learning assistant for a programming course.
Use the following context from the course materials to answer the student's question.
Always be clear, educational, and provide examples when helpful.
If the context doesn't contain the answer, say so politely and suggest what you can help with.

Context from course materials:
{context_text}
"""
            
            # Generate response using Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.chat_deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Response generation error: {e}")
            # Fallback: use first chunk directly
            if context_chunks:
                return f"Based on the course materials:\n\n{context_chunks[0].get('content', '')}\n\nWould you like me to explain this further?"
            return self._generate_fallback_response(query)
    
    def _generate_fallback_response(self, query: str) -> str:
        """Generate a fallback response when no relevant content is found"""
        return f"""I don't have specific information about that in the course materials I have access to.

Could you try:
- Rephrasing your question
- Asking about a specific topic from the course
- Breaking down your question into smaller parts

I'm here to help with your learning! 📚"""
    
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
        try:
            # Search knowledge base (vector search with keyword fallback)
            relevant_chunks = await self._search_knowledge_base_with_vector(message)
            
            # Generate response
            response_text = self._generate_response(message, relevant_chunks)
            
            # Format sources
            sources = []
            for chunk in relevant_chunks:
                metadata = chunk.get("metadata", {})
                sources.append({
                    "module": metadata.get("module", "Unknown"),
                    "timestamp": metadata.get("timestamp", ""),
                    "content_type": metadata.get("source_type", "text"),
                    "relevance_score": chunk.get("score", 0.8)
                })
            
            return {
                "message": response_text,
                "sources": sources[:3]  # Return top 3 sources
            }
            
        except Exception as e:
            print(f"RAG chatbot error: {e}")
            return {
                "message": self._generate_fallback_response(message),
                "sources": []
            }