import json
import asyncio
import time
from saudi_legal_lightning import SaudiLegalLightning

async def run_bilingual_tests():
    system = SaudiLegalLightning(feedback_file="bilingual_feedback.json")
    
    # Diverse scenarios in English and Arabic
    scenarios = [
        {
            "id": "EN_LABOR_01",
            "language": "English",
            "query": "What are the specific conditions for a valid non-compete clause in a Saudi employment contract?",
            "category": "Contract Law"
        },
        {
            "id": "AR_LABOR_01",
            "language": "Arabic",
            "query": "ما هي شروط الاستقالة في نظام العمل السعودي وما هي مدة الإخطار المطلوبة؟",
            "category": "Resignation/Notice Period"
        },
        {
            "id": "EN_PROBATION_01",
            "language": "English",
            "query": "Explain the rules regarding the probation period duration and extension under the Saudi Labor Law.",
            "category": "Probation"
        },
        {
            "id": "AR_TERMINATION_01",
            "language": "Arabic",
            "query": "هل يحق لصاحب العمل فصل الموظف دون مكافأة نهاية الخدمة؟ وما هي الحالات التي تسمح بذلك؟",
            "category": "Termination/EOSB"
        }
    ]
    
    test_results = []
    print(f"--- Starting Bilingual Test Suite ({len(scenarios)} scenarios) ---")
    
    for scenario in scenarios:
        print(f"\n[Scenario {scenario['id']}] Language: {scenario['language']}")
        print(f"Query: {scenario['query']}")
        
        start_time = time.time()
        result = await system.run_research_lightning(scenario['query'])
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        test_entry = {
            "scenario_id": scenario['id'],
            "language": scenario['language'],
            "category": scenario['category'],
            "query": scenario['query'],
            "execution_time": f"{execution_time:.2f}s",
            "result": result
        }
        
        test_results.append(test_entry)
        print(f"Completed in {execution_time:.2f}s with confidence {result.get('confidence', 'N/A')}")

    summary = {
        "test_date": "2026-02-05",
        "total_scenarios": len(scenarios),
        "results": test_results
    }
    
    with open("bilingual_test_results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n--- All tests completed. Results saved to bilingual_test_results.json ---")

if __name__ == "__main__":
    asyncio.run(run_bilingual_tests())
