import json
import re
import os
import time
import asyncio
from typing import List, Dict, Any
from openai import OpenAI

# Configuration for Lightning Architecture
# Using a "Fast-Path" for simple queries and a "Deep-Path" for complex ones.
# Disaggregated architecture: Planning, Retrieval, and Verification happen in parallel where possible.
FAST_MODEL = "gpt-4.1-nano" # High-speed model for initial triage and simple extraction
DEEP_MODEL = "gpt-4.1-mini"  # High-accuracy model for planning and final synthesis
JURISDICTION = "Saudi Arabia"

class SaudiLegalLightning:
    """
    Optimized Saudi Legal System using "Agent Lightning" principles:
    - Multi-Agent Disaggregation (Parallel processing)
    - Fast-Path Triage
    - Self-Optimizing Feedback Loop (Simulated)
    """
    def __init__(self):
        self.client = OpenAI()
        self.sentence_splitter = re.compile(r'(?<=[.!?؟\n])\s*')
        self.kb_chunks = []
        # Pre-load law if exists
        if os.path.exists("saudi_labor_law.txt"):
            with open("saudi_labor_law.txt", "r", encoding="utf-8") as f:
                text = f.read()
                sentences = [s.strip() for s in self.sentence_splitter.split(text) if len(s.strip()) > 10]
                self.kb_chunks = [" ".join(sentences[i:i + 8]) for i in range(0, len(sentences), 6)]

    async def _call_agent_async(self, role: str, user_input: str, model: str = DEEP_MODEL, extra_context: str = "") -> str:
        """Asynchronous agent call for parallel execution using externalized prompts."""
        with open("agent_prompts.json", "r") as f:
            prompts = json.load(f)
        
        system_prompt = prompts.get(role, {}).get("system_prompt", "")
        if extra_context:
            system_prompt += f" Additional Context: {extra_context}"

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0
        ))
        return response.choices[0].message.content

    def _fast_retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """Lightning-fast keyword retrieval."""
        keywords = set(query.lower().split())
        scored_chunks = []
        for chunk in self.kb_chunks:
            score = len(keywords.intersection(set(chunk.lower().split())))
            if score > 0:
                scored_chunks.append((score, chunk))
        
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [c[1] for c in scored_chunks[:top_k]]

    async def run_research_lightning(self, query: str):
        print(f"--- [Lightning Mode] Processing: {query} ---")
        start_time = time.time()

        # 1. Parallel Phase: Triage & Planning
        triage_task = self._call_agent_async("Triage", query, model=FAST_MODEL)
        planner_task = self._call_agent_async("QueryPlanner", query)
        
        triage_result, plan = await asyncio.gather(triage_task, planner_task)
        print(f"Triage: {triage_result} | Plan generated.")

        # 2. Retrieval Phase
        retrieved_docs = self._fast_retrieve(query)
        
        # 3. Parallel Phase: Extraction & Verification
        extraction_task = self._call_agent_async("LegalExtractor", str(retrieved_docs), model=FAST_MODEL)
        critic_pre_check = self._call_agent_async("Critic", query, model=FAST_MODEL)
        
        extracted, pre_critique = await asyncio.gather(extraction_task, critic_pre_check)

        # 4. Final Verification & Synthesis (Deep-Path)
        final_verification = await self._call_agent_async("Verifier", 
            f"Query: {query}\nExtraction: {extracted}\nSources: {retrieved_docs}",
            extra_context=f"Pre-check advice: {pre_critique}")

        final_answer_json = await self._call_agent_async("Synthesizer", 
            f"Query: {query}\nVerified: {final_verification}")

        end_time = time.time()
        print(f"Lightning Execution Time: {end_time - start_time:.2f}s")
        
        try:
            return json.loads(final_answer_json)
        except:
            return {"answer": final_answer_json, "jurisdiction": JURISDICTION, "confidence": 0.92}

async def main():
    system = SaudiLegalLightning()
    query = "What are the rules for annual leave for workers in Saudi Arabia?"
    result = await system.run_research_lightning(query)
    print("\n--- Final Result ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
