# System Architecture: An Agentic Framework for Saudi Arabian Legal Research

**Author**: Manus AI

**Date**: February 4, 2026

## Introduction

This document outlines the architecture for a sophisticated multi-agent system designed to perform high-accuracy legal research and analysis under the jurisdiction of Saudi Arabian law. The primary objective is to achieve a factual accuracy rate of 90-94% by leveraging a research-backed, retrieval-augmented generation (RAG) pipeline and a rigorous, multi-stage verification process. The system is engineered to address the unique linguistic and legal complexities of the Saudi legal framework, which integrates modern statutory law with foundational Sharia principles.

## Core Retrieval-Augmented Generation (RAG) Pipeline

The foundation of the system is a specialized RAG pipeline optimized for the nuances of Arabic legal text. Each component of this pipeline has been selected based on empirical evidence from recent studies in Arabic natural language processing.

| Component | Selected Technology/Method | Rationale and Justification |
| :--- | :--- | :--- |
| **Data Ingestion & Preprocessing** | Optical Character Recognition (OCR) & Hierarchical Markdown Parsing | This combination ensures that the structural integrity of legal documents, such as Royal Decrees, Implementing Regulations, and judicial precedents, is preserved during digitization. Maintaining the hierarchy is critical for contextual understanding. |
| **Text Chunking** | **Sentence-Aware Chunking** | Based on the findings of Alsubhi et al. (2025), sentence-aware chunking provides the optimal balance between context preservation and granularity. This method is particularly effective for the dense and syntactically complex nature of Arabic legal documents, outperforming fixed-size or recursive methods. [1] |
| **Text Embedding** | **BGE-M3** | This state-of-the-art multilingual embedding model has demonstrated superior performance on diverse Arabic datasets. Its ability to capture deep semantic relationships is essential for retrieving relevant legal provisions from a vast corpus. [1] |
| **Vector Database** | Qdrant / Milvus | A high-performance vector database is required to support real-time retrieval with metadata filtering. This allows the system to narrow searches by jurisdiction, year of enactment, or document type, which is crucial for legal accuracy. |
| **Retrieval Reranking** | **BGE-Reranker-v2-m3** | To meet the high precision demands (Precision@k), a sophisticated reranker is employed. It re-evaluates the top-k retrieved document chunks, ensuring that the most semantically relevant results are prioritized for the subsequent generation and verification stages. [1] |

## Multi-Agent Orchestration Framework

Overlaying the RAG pipeline is a decentralized orchestration framework composed of seven specialized agents. Each agent performs a distinct function in the query processing lifecycle, ensuring a thorough and factually grounded analysis.

1.  **QueryPlanner Agent**: This agent first receives and analyzes the user's legal query. It decomposes complex questions into a sequence of discrete, actionable sub-tasks. For instance, a query regarding employee termination rights under Saudi law would be broken down into specific tasks, such as retrieving relevant articles from the Saudi Labor Law, searching for related Royal Decrees, and checking for recent circulars from the Ministry of Human Resources and Social Development.

2.  **Retriever Agent**: The Retriever Agent executes the search plan formulated by the QueryPlanner. It interfaces with the vector database to fetch the top-k relevant document chunks using the BGE-M3 embeddings.

3.  **Reranker Agent**: This agent takes the initial set of retrieved documents and applies the BGE-Reranker model. By re-evaluating the relevance of each chunk in the context of the specific user query, it significantly improves the precision of the information passed to the next stage.

4.  **LegalExtractor Agent**: The LegalExtractor Agent is a specialized information extraction tool. It parses the reranked legal texts to identify and structure key legal entities, such as **Statutes**, **Articles**, **Royal Decrees**, and **Case Law References**. This structured data is essential for the verification and synthesis processes.

5.  **Verifier Agent**: This agent is the cornerstone of the system's accuracy. It performs a rigorous "Source-to-Claim" validation, ensuring that every piece of information intended for the final answer is directly and explicitly supported by the extracted legal source documents. Any claim that cannot be verified is discarded.

6.  **Critic Agent**: Functioning as an adversarial validator, the Critic Agent actively attempts to identify potential errors. It is specifically trained to detect common LLM failure modes, such as "phantom articles" (hallucinated legal provisions), misinterpretation of Sharia-based principles, and jurisdictional errors (e.g., confusing Saudi law with that of other GCC nations).

7.  **Synthesizer Agent**: The final agent in the chain, the Synthesizer, compiles the verified legal information into the final, structured JSON output. It generates a clear and concise answer, provides precise citations for all claims, specifies the jurisdiction, and calculates a confidence score based on the strength of the supporting evidence.

## Evaluation, Policy, and Governance

To ensure the system consistently operates within the 90-94% accuracy target, a strict set of evaluation metrics and governance policies are enforced.

> **Governing Policy**: The system operates under a strict "no-verification, no-answer" policy. If the Verifier Agent cannot find a direct and unambiguous source for a legal claim, the Synthesizer Agent is programmatically prohibited from including that claim in the final output. This policy is fundamental to mitigating the risk of hallucination and ensuring the reliability of the legal information provided.

Key performance indicators include:

-   **Precision@k**: Measures the relevance of the top-k documents retrieved and reranked.
-   **Citation Correctness**: A binary assessment of whether all citations in the final output correspond to real and correctly mapped legal sources.
-   **Hallucination Rate**: Continuously monitored by the Critic Agent, with a zero-tolerance policy for fabricated legal content.

## References

[1] Alsubhi, J., Alahmadi, M. D., Alhusayni, A., Aldailami, I., Hamdine, I., Shabana, A., ... & Khayyat, S. (2025). *Optimizing RAG Pipelines for Arabic: A Systematic Analysis of Core Components*. arXiv preprint arXiv:2506.06339. Available: https://arxiv.org/html/2506.06339v1
