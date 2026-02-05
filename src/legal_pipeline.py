import os
import json
import re
from typing import List, Dict
from openai import OpenAI

# Initialize OpenAI client (configured to use gpt-4.1-mini/nano for processing)
# Note: For real embedding models like BGE-M3, we would typically use sentence-transformers.
# In this, we will simulate the pipeline logic.
client = OpenAI()

class SaudiLegalPipeline:
    def __init__(self, embedding_model="bge-m3"):
        self.embedding_model = embedding_model
        # Pre-compiled regex for Arabic sentence splitting
        # Splits by period, exclamation, or question mark followed by space or newline
        self.sentence_splitter = re.compile(r'(?<=[.!?؟\n])\s*')

    def sentence_aware_chunking(self, text: str, max_sentences_per_chunk: int = 5, overlap: int = 1) -> List[str]:
        """
        Implements sentence-aware chunking as recommended by research for Arabic legal texts.
        """
        sentences = self.sentence_splitter.split(text)
        chunks = []
        
        for i in range(0, len(sentences), max_sentences_per_chunk - overlap):
            chunk = " ".join(sentences[i:i + max_sentences_per_chunk])
            if chunk.strip():
                chunks.append(chunk.strip())
            if i + max_sentences_per_chunk >= len(sentences):
                break
                
        return chunks

    def get_embeddings(self, chunks: List[str]) -> List[List[float]]:
        """
        Simulates getting embeddings from a model like BGE-M3.
        In a real environment, this would call a local model or a specialized API.
        """
        # Placeholder for actual embedding logic
        # For demonstration, we'll return mock vectors
        return [[0.1] * 1024 for _ in chunks]

    def process_document(self, doc_path: str):
        """
        Full ingestion pipeline: Read -> Chunk -> Embed
        """
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chunks = self.sentence_aware_chunking(content)
        embeddings = self.get_embeddings(chunks)
        
        return {
            "source": doc_path,
            "chunks": chunks,
            "embeddings": embeddings
        }

# Example usage
if __name__ == "__main__":
    # Create a sample Saudi legal text for testing
    sample_text = """
    المادة الأولى: يهدف هذا النظام إلى تنظيم العلاقة بين صاحب العمل والعامل.
    المادة الثانية: يجب أن يكون عقد العمل مكتوباً وباللغة العربية.
    المادة الثالثة: تحدد ساعات العمل بثماني ساعات في اليوم الواحد.
    المادة الرابعة: يستحق العامل إجازة سنوية لا تقل عن واحد وعشرين يوماً.
    """
    with open("sample_law.txt", "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    pipeline = SaudiLegalPipeline()
    result = pipeline.process_document("sample_law.txt")
    
    print(f"Processed {len(result['chunks'])} chunks from document.")
    for idx, chunk in enumerate(result['chunks']):
        print(f"Chunk {idx+1}: {chunk[:50]}...")
