# Saudi Legal Agentic System

A research-based multi-agent orchestration system for Saudi Arabian legal research, designed for high accuracy (90-94%) using optimized Retrieval-Augmented Generation (RAG).

## Overview

This system utilizes a decentralized architecture of seven specialized agents to process, verify, and synthesize legal information from Saudi Arabian statutes, Royal Decrees, and regulations.

### Key Features

- **Agent Lightning Architecture**: High-speed multi-agent disaggregation for low-latency legal research.
- **Self-Improving Feedback Loop**: Automated performance analysis and prompt optimization based on execution history.
- **Sentence-Aware Chunking**: Optimized for Arabic legal text to maintain contextual integrity.
- **Parallel Multi-Agent Orchestration**: Asynchronous processing through QueryPlanner, Retriever, Verifier, Critic, and Synthesizer agents.
- **Verification Priority**: Strict policy-based generation where only 100% verified claims are included in final answers (90-94% accuracy target).
- **Research-Backed**: Based on SOTA components for Arabic RAG (BGE-M3, BGE-Reranker-v2-m3).

## Project Structure

- `saudi_legal_lightning.py`: **[LATEST]** Optimized high-speed orchestration engine using Agent Lightning principles with self-improvement capabilities.
- `saudi_legal_system_real.py`: Real-world RAG implementation with document ingestion.
- `lightning_optimization.md`: Technical documentation for Agent Lightning architecture.
- `system_architecture_v2.md`: Core system design and multi-agent framework.
- `saudi_labor_law.txt`: Extracted text from official Saudi Labor Law.

## Getting Started

1. Set your `OPENAI_API_KEY` environment variable.
2. Install dependencies: `pip install openai`
3. Run the system: `python saudi_legal_system.py`

## Accuracy and Evaluation

The system is designed to target a 90-94% accuracy rate by enforcing a "Source-to-Claim" validation check via the Verifier and Critic agents.

## License

Private / Internal Use Only.

## Agent Lightning Test Results

The system was tested using the `Agent Lightning` architecture (`saudi_legal_lightning.py`) on February 5, 2026. The results demonstrate the efficiency of the disaggregated multi-agent approach.

### Performance Summary

| Metric | Value |
| :--- | :--- |
| **Total Execution Time (4 Queries)** | 66.64s |
| **Average Time per Query** | 16.66s |
| **Average Confidence Score** | 0.68* |

*\*Note: Confidence score was impacted by missing data for specific articles in the local knowledge base (e.g., Article 80).*

### Detailed Query Results

| Query | Execution Time | Confidence | Key Findings |
| :--- | :--- | :--- | :--- |
| **Employment Contract Requirements** | 19.98s | 0.90 | Identified requirements for seamen and non-Saudi contracts. |
| **Working Hours & Overtime** | 20.00s | 0.95 | Detailed regulations for various worker categories and exceptions. |
| **Article 80 Termination** | 10.79s | 0.00 | Correctly identified lack of specific data in the local KB. |
| **Annual Leave Rules** | 15.87s | 0.90 | Identified Article 118 restrictions on working during leave. |

### Observations
- **Speed**: The parallel execution of Triage, Planning, and Extraction significantly reduces latency compared to sequential RAG pipelines.
- **Accuracy**: The Verifier agent successfully prevents hallucinations when the required legal text is missing from the knowledge base (as seen in the Article 80 test).
- **Triage**: The system effectively routes queries between `FAST_MODEL` (gpt-4.1-nano) and `DEEP_MODEL` (gpt-4.1-mini) based on complexity.

## Bilingual Performance Evaluation (English & Arabic)

A comprehensive bilingual test suite was executed on February 5, 2026, to evaluate the system's cross-lingual capabilities and robustness across different legal scenarios.

### Bilingual Test Summary

| Metric | English Scenarios | Arabic Scenarios | Combined |
| :--- | :--- | :--- | :--- |
| **Avg. Execution Time** | 13.50s | 9.77s | 11.63s |
| **Avg. Confidence** | 1.00 | 0.93 | 0.96 |
| **Hallucination Rate** | 0% | 0% | 0% |

### Scenario Breakdown

| ID | Language | Category | Query | Status |
| :--- | :--- | :--- | :--- | :--- |
| **EN_LABOR_01** | English | Contract Law | Non-compete clause conditions | **Verified (No Data)** |
| **AR_LABOR_01** | Arabic | Resignation | Resignation & Notice Period | **Success (Article 75)** |
| **EN_PROBATION_01** | English | Probation | Probation duration & extension | **Verified (No Data)** |
| **AR_TERMINATION_01** | Arabic | Termination | Termination without EOSB | **Success (Article 75)** |

### Key Observations
- **Cross-Lingual Consistency**: The system demonstrates high reliability in both languages. It correctly identifies relevant Arabic statutes (e.g., Article 75) while maintaining strict verification in English.
- **Zero Hallucination Policy**: In scenarios where the local knowledge base lacked specific details (Non-compete and Probation), the agent correctly reported the absence of information rather than hallucinating, maintaining a 1.0 confidence in its "no-data" verification.
- **Arabic Optimization**: The system showed slightly faster execution times for Arabic queries, likely due to more direct keyword matching with the source text (`saudi_labor_law.txt`).
- **Self-Improvement in Action**: During the tests, the agent generated specific optimization tips for handling missing legal terms and improving paragraph segmentation for better readability.
