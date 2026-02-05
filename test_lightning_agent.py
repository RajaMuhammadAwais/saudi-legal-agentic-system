import json
import asyncio
import time
from saudi_legal_lightning import SaudiLegalLightning

async def run_lightning_tests():
    system = SaudiLegalLightning()
    
    queries = [
        "What are the mandatory requirements for a valid employment contract under Saudi Labor Law?",
        "Explain the regulations regarding working hours and overtime compensation in Saudi Arabia.",
        "What is the legal procedure for an employer to terminate a contract due to employee misconduct (Article 80)?",
        "What are the rules for annual leave for workers in Saudi Arabia?"
    ]
    
    results = []
    total_start_time = time.time()
    
    for query in queries:
        print(f"Executing Lightning Query: {query}")
        start_time = time.time()
        result = await system.run_research_lightning(query)
        end_time = time.time()
        
        execution_time = end_time - start_time
        result['query'] = query
        result['execution_time'] = f"{execution_time:.2f}s"
        
        results.append(result)
        print(f"Done in {execution_time:.2f}s.\n")
    
    total_end_time = time.time()
    summary = {
        "total_execution_time": f"{total_end_time - total_start_time:.2f}s",
        "average_time_per_query": f"{(total_end_time - total_start_time) / len(queries):.2f}s",
        "results": results
    }
    
    with open("lightning_test_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"All tests completed. Total time: {total_end_time - total_start_time:.2f}s")
    return summary

if __name__ == "__main__":
    asyncio.run(run_lightning_tests())
