import json
import re
import os
import time
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from a local .env file (if present)
load_dotenv()

# Configuration for Lightning Architecture
FAST_MODEL = "gpt-4.1-nano" # High-speed model for initial triage and simple extraction
DEEP_MODEL = "gpt-4.1-mini"  # High-accuracy model for planning and final synthesis
JURISDICTION = "Saudi Arabia"

class SaudiLegalLightning:
    """
    Optimized Saudi Legal System using "Agent Lightning" principles with Self-Improvement:
    - Multi-Agent Disaggregation (Parallel processing)
    - Fast-Path Triage
    - Self-Optimizing Feedback Loop: Evaluates its own performance and adjusts prompts/strategy.
    - Memory-Augmented Reasoning: Stores successful patterns for future queries.
    """
    def __init__(self, feedback_file: str = "agent_feedback_loop.json"):
        self.client = OpenAI()
        self.sentence_splitter = re.compile(r'(?<=[.!?؟\n])\s*')
        self.kb_chunks = []
        self.feedback_file = feedback_file
        self.performance_history = self._load_feedback()
        
        # Pre-load law if exists
        if os.path.exists("saudi_labor_law.txt"):
            with open("saudi_labor_law.txt", "r", encoding="utf-8") as f:
                text = f.read()
                sentences = [s.strip() for s in self.sentence_splitter.split(text) if len(s.strip()) > 10]
                self.kb_chunks = [" ".join(sentences[i:i + 8]) for i in range(0, len(sentences), 6)]

    def _load_feedback(self) -> List[Dict]:
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_feedback(self):
        with open(self.feedback_file, "w") as f:
            json.dump(self.performance_history, f, indent=2)

    async def _call_agent_async(self, role: str, user_input: str, model: str = DEEP_MODEL, extra_context: str = "") -> str:
        """Asynchronous agent call for parallel execution using externalized prompts."""
        with open("agent_prompts.json", "r") as f:
            prompts = json.load(f)
        
        system_prompt = prompts.get(role, {}).get("system_prompt", "")
        
        # Self-Improvement: Inject learned optimizations if available
        optimizations = self._get_relevant_optimizations(role)
        if optimizations:
            system_prompt += f"\nLearned Optimizations: {optimizations}"
            
        if extra_context:
            system_prompt += f"\nAdditional Context: {extra_context}"

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

    def _get_relevant_optimizations(self, role: str) -> str:
        """Retrieve successful patterns for a specific agent role."""
        relevant = [h for h in self.performance_history if h.get("role") == role and h.get("score", 0) > 0.8]
        if not relevant:
            return ""
        # Return the latest successful tip
        return relevant[-1].get("optimization_tip", "")

    def _fast_retrieve(self, query: str, top_k: int = 8) -> List[str]:
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
        print(f"--- [Lightning Mode + Self-Improvement] Processing: {query} ---")
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
        execution_time = end_time - start_time
        print(f"Lightning Execution Time: {execution_time:.2f}s")
        
        try:
            result = json.loads(final_answer_json)
        except:
            result = {"answer": final_answer_json, "jurisdiction": JURISDICTION, "confidence": 0.92}

        # 5. Self-Improvement Phase: Evaluate and Learn
        await self._perform_self_improvement(query, result, execution_time)
        
        return result

    async def _perform_self_improvement(self, query: str, result: Dict, execution_time: float):
        """Analyze the result and store feedback for future optimization."""
        print("--- [Self-Improvement] Analyzing performance... ---")
        
        eval_prompt = f"""
        Analyze the following legal agent response for query: "{query}"
        Response: {json.dumps(result)}
        Execution Time: {execution_time}s
        
        Identify one specific 'optimization_tip' for the 'Synthesizer' or 'LegalExtractor' to improve accuracy or speed.
        Provide a 'score' from 0.0 to 1.0 based on clarity and source attribution.
        Output ONLY JSON.
        """
        
        eval_response = await self._call_agent_async("Critic", eval_prompt, model=DEEP_MODEL)
        try:
            # Clean potential markdown
            clean_json = re.search(r'\{.*\}', eval_response, re.DOTALL).group()
            feedback = json.loads(clean_json)
            feedback["timestamp"] = time.time()
            feedback["query"] = query
            
            # For this demo, we'll attribute feedback to the Synthesizer
            feedback["role"] = "Synthesizer" 
            
            self.performance_history.append(feedback)
            self._save_feedback()
            print(f"Self-Improvement: Learned new tip - {feedback.get('optimization_tip')}")
        except Exception as e:
            print(f"Self-Improvement: Failed to parse feedback. {e}")

async def main():
    system = SaudiLegalLightning()
    query = "What are the rules for annual leave for workers in Saudi Arabia?"
    result = await system.run_research_lightning(query)
    print("\n--- Final Result ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
