import json
from saudi_legal_system import SaudiLegalSystem

def run_tests():
    system = SaudiLegalSystem()
    
    queries = [
        "What are the mandatory requirements for a valid employment contract under Saudi Labor Law?",
        "Explain the regulations regarding working hours and overtime compensation in Saudi Arabia.",
        "What is the legal procedure for an employer to terminate a contract due to employee misconduct (Article 80)?"
    ]
    
    results = []
    for query in queries:
        print(f"Executing Query: {query}")
        result = system.run_research(query)
        results.append(result)
        print("Done.\n")
    
    with open("test_query_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return results

if __name__ == "__main__":
    run_tests()
