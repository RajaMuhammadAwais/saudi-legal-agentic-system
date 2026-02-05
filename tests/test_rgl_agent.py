import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from saudi_legal_system_rgl import SaudiLegalSystemRGL

def test_rgl_flow():
    print("Initializing RGL Test...")
    system = SaudiLegalSystemRGL()
    
    # Ingest data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'saudi_labor_law.txt')
    system.ingest_document(data_path)
    
    # Test Query
    query = "What are the working hour limits during Ramadan for Muslim workers?"
    result = system.run_research(query)
    
    print("\n--- RGL Evaluation ---")
    adherence = result.get("rgl_metrics", {}).get("adherence_score", 0)
    print(f"RGL Adherence Score: {adherence * 100}%")
    
    if adherence == 1.0:
        print("SUCCESS: All agents followed the RGL 'Think-Answer' protocol.")
    else:
        print("PARTIAL SUCCESS: Some agents skipped the RGL protocol.")
        
    print("\n--- Thinking Process Sample (Synthesizer) ---")
    print(result.get("rgl_metrics", {}).get("thinking_steps", {}).get("synthesizer", "No thinking recorded."))
    
    print("\n--- Final Answer ---")
    print(result.get("answer", "No answer generated."))

if __name__ == "__main__":
    test_rgl_flow()
