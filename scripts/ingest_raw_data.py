"""
Raw Data Ingestion Script V2
Processes transcripts, PDFs, URLs, and documents into knowledge base chunks
Optimized for CourseCompanion data structure
"""
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Optional dependencies - install if needed
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("ℹ️  PyPDF2 not installed. PDFs will be skipped.")
    print("   Install with: pip install PyPDF2\n")

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("ℹ️  LangChain not installed. Using simple chunking.")
    print("   Install with: pip install langchain\n")


class ContentProcessor:
    """Process various content types into knowledge base chunks"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if LANGCHAIN_AVAILABLE:
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
        else:
            self.text_splitter = None
    
    def process_transcript(self, transcript_path: Path, course_id: str, module_num: int = 1) -> List[Dict]:
        """Process a video transcript"""
        print(f"  📝 Processing transcript: {transcript_path.name}")
        
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                print(f"     ⚠️  Empty transcript")
                return []
            
            chunks = self._chunk_text(content)
            chunk_docs = []
            
            for i, chunk_text in enumerate(chunks):
                chunk_id = self._generate_chunk_id(course_id, transcript_path.name, i)
                chunk_docs.append({
                    "chunk_id": chunk_id,
                    "content": chunk_text,
                    "metadata": {
                        "source": transcript_path.name,
                        "source_type": "transcript",
                        "module": f"Module {module_num}",
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                })
            
            print(f"     ✓ Generated {len(chunk_docs)} chunks")
            return chunk_docs
            
        except Exception as e:
            print(f"     ⚠️  Error: {e}")
            return []
    
    def process_pdf(self, pdf_path: Path, course_id: str, module_num: int = 1) -> List[Dict]:
        """Process a PDF document"""
        print(f"  📄 Processing PDF: {pdf_path.name}")
        
        if not PDF_AVAILABLE:
            print(f"     ⚠️  PyPDF2 not installed, skipping")
            return []
        
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n\n=== Page {page_num + 1}/{total_pages} ===\n\n{page_text}"
            
            if not text.strip():
                print(f"     ⚠️  No text extracted from PDF")
                return []
            
            chunks = self._chunk_text(text)
            chunk_docs = []
            
            for i, chunk_text in enumerate(chunks):
                chunk_id = self._generate_chunk_id(course_id, pdf_path.name, i)
                chunk_docs.append({
                    "chunk_id": chunk_id,
                    "content": chunk_text,
                    "metadata": {
                        "source": pdf_path.name,
                        "source_type": "pdf",
                        "module": f"Module {module_num}",
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                })
            
            print(f"     ✓ Generated {len(chunk_docs)} chunks from {total_pages} pages")
            return chunk_docs
            
        except Exception as e:
            print(f"     ⚠️  Error: {e}")
            return []
    
    def process_urls(self, urls_path: Path, course_id: str) -> List[Dict]:
        """Process URL list file"""
        print(f"  🔗 Processing URLs: {urls_path.name}")
        
        try:
            with open(urls_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and line.strip().startswith('http')]
            
            if not urls:
                print(f"     ⚠️  No valid URLs found")
                return []
            
            # Create a reference chunk for URLs
            url_content = "External Resources:\n\n"
            for i, url in enumerate(urls, 1):
                url_content += f"{i}. {url}\n"
            
            chunk_id = self._generate_chunk_id(course_id, "urls", 0)
            chunk_doc = {
                "chunk_id": chunk_id,
                "content": url_content,
                "metadata": {
                    "source": urls_path.name,
                    "source_type": "urls",
                    "module": "External Resources",
                    "url_count": len(urls),
                    "urls": urls
                }
            }
            
            print(f"     ✓ Processed {len(urls)} URLs")
            return [chunk_doc]
            
        except Exception as e:
            print(f"     ⚠️  Error: {e}")
            return []
    
    def process_text_file(self, text_path: Path, course_id: str, module_num: int = 1) -> List[Dict]:
        """Process a text file"""
        print(f"  📝 Processing text file: {text_path.name}")
        
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                print(f"     ⚠️  Empty file")
                return []
            
            chunks = self._chunk_text(content)
            chunk_docs = []
            
            for i, chunk_text in enumerate(chunks):
                chunk_id = self._generate_chunk_id(course_id, text_path.name, i)
                chunk_docs.append({
                    "chunk_id": chunk_id,
                    "content": chunk_text,
                    "metadata": {
                        "source": text_path.name,
                        "source_type": "document",
                        "module": f"Module {module_num}",
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                })
            
            print(f"     ✓ Generated {len(chunk_docs)} chunks")
            return chunk_docs
            
        except Exception as e:
            print(f"     ⚠️  Error: {e}")
            return []
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        if not text.strip():
            return []
        
        if self.text_splitter:
            return self.text_splitter.split_text(text)
        else:
            # Simple sentence-based chunking
            return self._simple_chunk(text)
    
    def _simple_chunk(self, text: str) -> List[str]:
        """Simple chunking fallback"""
        chunks = []
        sentences = text.replace('\n', ' ').split('. ')
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(current_chunk) + len(sentence) + 2 <= self.chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _generate_chunk_id(self, course_id: str, source: str, index: int) -> str:
        """Generate unique chunk ID"""
        unique_string = f"{course_id}_{source}_{index}"
        return hashlib.md5(unique_string.encode()).hexdigest()


def process_course(course_dir: Path, course_id: str, processor: ContentProcessor) -> Dict:
    """Process all content for a course"""
    print(f"\n📚 Processing Course: {course_id}")
    print("=" * 70)
    
    all_chunks = []
    module_num = 1
    
    # Process transcripts
    transcript_dir = course_dir / "transcripts"
    if transcript_dir.exists():
        print("\n📝 Transcripts:")
        for transcript_file in sorted(transcript_dir.glob("*.txt")):
            chunks = processor.process_transcript(transcript_file, course_id, module_num)
            all_chunks.extend(chunks)
            if chunks:
                module_num += 1
    
    # Process documents/PDFs
    docs_dir = course_dir / "documents"
    if docs_dir.exists():
        print("\n📄 Documents:")
        for pdf_file in sorted(docs_dir.glob("*.pdf")):
            chunks = processor.process_pdf(pdf_file, course_id, module_num)
            all_chunks.extend(chunks)
            if chunks:
                module_num += 1
        
        # Process text documents
        for txt_file in sorted(docs_dir.glob("*.txt")):
            chunks = processor.process_text_file(txt_file, course_id, module_num)
            all_chunks.extend(chunks)
            if chunks:
                module_num += 1
    
    # Process URLs
    urls_dir = course_dir / "urls"
    if urls_dir.exists():
        print("\n🔗 URLs:")
        for url_file in urls_dir.glob("*.txt"):
            chunks = processor.process_urls(url_file, course_id)
            all_chunks.extend(chunks)
    
    return {
        "course_id": course_id,
        "total_chunks": len(all_chunks),
        "chunks": all_chunks,
        "processed_at": datetime.utcnow().isoformat()
    }


def save_knowledge_base(kb_data: Dict, output_dir: Path):
    """Save knowledge base to JSON"""
    course_id = kb_data["course_id"]
    output_file = output_dir / f"{course_id}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved: {output_file.relative_to(output_file.parent.parent)}")
    print(f"   Total chunks: {kb_data['total_chunks']}")


def main():
    """Main ingestion function"""
    print("\n" + "="*70)
    print("📥 COURSECOMPANION DATA INGESTION")
    print("="*70 + "\n")
    
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    raw_data_dir = project_root / "data" / "raw"
    output_dir = project_root / "data" / "courses" / "knowledge_base"
    
    if not raw_data_dir.exists():
        print(f"❌ Raw data directory not found: {raw_data_dir}")
        print("\n💡 Run organize_data.py first to set up the structure")
        return
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize processor
    processor = ContentProcessor(chunk_size=1000, chunk_overlap=200)
    
    print(f"📂 Source: {raw_data_dir}")
    print(f"📂 Output: {output_dir}\n")
    
    # Process each course
    courses_processed = 0
    total_chunks = 0
    
    for course_dir in sorted(raw_data_dir.iterdir()):
        if course_dir.is_dir() and not course_dir.name.startswith('.'):
            course_id = course_dir.name
            
            # Process course
            kb_data = process_course(course_dir, course_id, processor)
            
            if kb_data["total_chunks"] > 0:
                save_knowledge_base(kb_data, output_dir)
                courses_processed += 1
                total_chunks += kb_data["total_chunks"]
            else:
                print(f"  ⚠️  No content processed for {course_id}")
    
    print("\n" + "="*70)
    print("✅ INGESTION COMPLETE!")
    print("="*70)
    print(f"\n📊 Summary:")
    print(f"   Courses processed: {courses_processed}")
    print(f"   Total chunks: {total_chunks}")
    print(f"   Output: {output_dir}")
    
    print("\n🎯 Next Steps:")
    print("   1. Review generated JSON files in data/courses/knowledge_base/")
    print("   2. Run: python scripts/seed_database.py")
    print("   3. Run: python scripts/generate_embeddings.py")


if __name__ == "__main__":
    main()