import json
import re
import os
import numpy as np
from typing import List, Dict, Any, Tuple
from openai import OpenAI

# Configuration
MODEL_NAME = "gpt-4.1-mini"
JURISDICTION = "Saudi Arabia"

class SaudiLegalSystemRGL:
    """
    A Reinforcement Learning with Guided Logic (RGL) implementation 
    of the Saudi Legal Agentic System.
    
    This system uses a 'Think-Answer' pattern and a rule-based feedback loop
    to simulate reinforcement learning dynamics for legal reasoning.
    """
    def __init__(self):
        self.client = OpenAI()
        self.sentence_splitter = re.compile(r'(?<=[.!?؟\n])\s*')
        self.kb_chunks = []
        self.kb_embeddings = []
        
        # RGL System Prompt Template
        self.rgl_system_prompt = (
            "You are a specialized Saudi Legal Agent. "
            "You MUST follow the Reinforcement Learning with Guided Logic (RGL) protocol:\n"
            "1. First, THINK about the legal reasoning process within <think> </think> tags.\n"
            "2. Reflect on the specific Articles and Statutes provided in the context.\n"
            "3. Verify your own reasoning for any jurisdictional errors or hallucinations.\n"
            "4. Finally, provide your structured output within <answer> </answer> tags.\n"
            "Strict adherence to the <think> and <answer> format is required for reward optimization."
        )

    def _call_rgl_agent(self, role: str, task_prompt: str, user_input: str) -> Tuple[str, str, float]:
        """
        Calls an agent using the RGL protocol and calculates a format reward.
        """
        full_system_prompt = f"{self.rgl_system_prompt}\n\nRole: {role} Agent\nTask: {task_prompt}"
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": full_system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0
        )
        
        content = response.choices[0].message.content
        
        # Extract think and answer blocks
        think_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
        answer_match = re.search(r'<answer>(.*?)</answer>', content, re.DOTALL)
        
        think_content = think_match.group(1).strip() if think_match else ""
        answer_content = answer_match.group(1).strip() if answer_match else content
        
        # Calculate Format Reward (RGL Principle)
        format_reward = 1.0 if (think_match and answer_match) else 0.0
        if not think_match:
            print(f"Warning: {role} Agent failed RGL 'think' format.")
        
        return think_content, answer_content, format_reward

    def chunk_text(self, text: str, max_sentences: int = 8) -> List[str]:
        sentences = self.sentence_splitter.split(text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        chunks = []
        for i in range(0, len(sentences), max_sentences - 2):
            chunk = " ".join(sentences[i:i + max_sentences])
            if chunk:
                chunks.append(chunk)
        return chunks

    def ingest_document(self, file_path: str):
        if not os.path.exists(file_path):
            # Fallback for relative paths in different directories
            alt_path = os.path.join(os.path.dirname(__file__), "..", "data", os.path.basename(file_path))
            if os.path.exists(alt_path):
                file_path = alt_path
            else:
                print(f"Error: {file_path} not found.")
                return

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        self.kb_chunks.extend(self.chunk_text(text))
        print(f"Ingested {len(self.kb_chunks)} chunks for RGL Knowledge Base.")

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, str]]:
        keywords = query.lower().split()
        scores = []
        for chunk in self.kb_chunks:
            score = sum(1 for kw in keywords if kw in chunk.lower())
            scores.append(score)
        
        top_indices = np.argsort(scores)[-top_k:][::-1]
        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                results.append({"text": self.kb_chunks[idx], "score": float(scores[idx])})
        return results

    def run_research(self, query: str):
        print(f"\n--- Starting RGL Research for: {query} ---")
        
        # 1. QueryPlanner (RGL)
        think_p, plan, r_p = self._call_rgl_agent("QueryPlanner", 
            "Break the query into legal search tasks for Saudi Labor Law.", query)
        
        # 2. Retriever
        retrieved_docs = self.retrieve(query)
        
        # 3. LegalExtractor (RGL)
        think_e, extracted, r_e = self._call_rgl_agent("LegalExtractor", 
            "Extract specific Article numbers and legal rules from the context.", str(retrieved_docs))
        
        # 4. Verifier (RGL - Acts as the 'Logic Guide')
        # The Verifier provides the 'Answer Reward' signal in this simulation
        think_v, verification, r_v = self._call_rgl_agent("Verifier", 
            "Verify the extracted rules against the source text. Be adversarial.", 
            f"Query: {query}\nExtraction: {extracted}\nSources: {retrieved_docs}")
        
        # 5. Synthesizer (RGL)
        think_s, final_json_str, r_s = self._call_rgl_agent("Synthesizer", 
            "Output a JSON object with: answer, sources, jurisdiction, confidence.", 
            f"Query: {query}\nVerified Info: {verification}")

        # Calculate Total RGL Adherence Score
        total_reward = (r_p + r_e + r_v + r_s) / 4.0
        
        try:
            result = json.loads(final_json_str)
            result["rgl_metrics"] = {
                "adherence_score": total_reward,
                "thinking_steps": {
                    "planner": think_p[:100] + "...",
                    "extractor": think_e[:100] + "...",
                    "verifier": think_v[:100] + "...",
                    "synthesizer": think_s[:100] + "..."
                }
            }
            return result
        except:
            return {
                "answer": final_json_str, 
                "rgl_metrics": {"adherence_score": total_reward},
                "jurisdiction": JURISDICTION
            }

if __name__ == "__main__":
    system = SaudiLegalSystemRGL()
    # Path adjustment for local execution
    data_path = "data/saudi_labor_law.txt"
    if not os.path.exists(data_path):
        data_path = "../data/saudi_labor_law.txt"
        
    system.ingest_document(data_path)
    
    test_query = "What are the rules for end-of-service benefits if I resign after 5 years?"
    result = system.run_research(test_query)
    print("\n--- Final RGL Result ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))
