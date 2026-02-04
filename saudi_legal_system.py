import json
import re
from typing import List, Dict, Any
from openai import OpenAI

# Configuration
MODEL_NAME = "gpt-4.1-mini"
JURISDICTION = "Saudi Arabia"

class SaudiLegalSystem:
    """
    A reusable and simple multi-agent system for Saudi Arabian legal research.
    """
    def __init__(self):
        self.client = OpenAI()
        # Research-backed sentence splitter for Arabic legal text
        self.sentence_splitter = re.compile(r'(?<=[.!?؟\n])\s*')

    def _call_agent(self, role: str, system_prompt: str, user_input: str) -> str:
        """Generic method to call specialized agents."""
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": f"You are the {role} Agent. {system_prompt}"},
                {"role": "user", "content": user_input}
            ],
            temperature=0
        )
        return response.choices[0].message.content

    def chunk_text(self, text: str, max_sentences: int = 5) -> List[str]:
        """Reusable sentence-aware chunking."""
        sentences = self.sentence_splitter.split(text)
        return [" ".join(sentences[i:i + max_sentences]) for i in range(0, len(sentences), max_sentences)]

    def run_research(self, query: str, context_docs: List[Dict[str, str]] = None):
        """
        Orchestrates the 7 agents to produce a verified legal answer.
        """
        # 1. QueryPlanner
        plan = self._call_agent("QueryPlanner", 
            "Break the query into legal sub-tasks for Saudi law.", query)
        
        # 2. Retriever (Simulated for this demo - would link to a Vector DB)
        # Using provided context_docs if available, otherwise using sample data
        retrieved_docs = context_docs or [
            {"source": "Saudi Labor Law, Art 74", "text": "Contract ends by mutual consent or expiry."},
            {"source": "Saudi Labor Law, Art 80", "text": "Employer may terminate without notice for misconduct."}
        ]

        # 3. Reranker (Simplification: prioritizes based on semantic relevance)
        ranked_docs = retrieved_docs # In full version, use a reranker model here

        # 4. LegalExtractor
        extracted = self._call_agent("LegalExtractor", 
            "Extract Statutes, Articles, and Decrees.", str(ranked_docs))

        # 5. Verifier
        verification = self._call_agent("Verifier", 
            "Check consistency between extraction and sources. Flag any hallucinations.", 
            f"Query: {query}\nExtraction: {extracted}\nSources: {ranked_docs}")

        # 6. Critic
        critique = self._call_agent("Critic", 
            "Detect errors in Saudi Law application or jurisdiction.", verification)

        # 7. Synthesizer
        final_json_str = self._call_agent("Synthesizer", 
            "Output ONLY a JSON object with keys: answer, sources, jurisdiction, confidence.", 
            f"Query: {query}\nVerified Info: {verification}\nCritique: {critique}")

        try:
            return json.loads(final_json_str)
        except:
            return {"error": "Failed to generate structured JSON", "raw": final_json_str}

if __name__ == "__main__":
    system = SaudiLegalSystem()
    test_query = "What are the rules for end-of-service benefits in Saudi Arabia?"
    result = system.run_research(test_query)
    print(json.dumps(result, indent=2, ensure_ascii=False))
