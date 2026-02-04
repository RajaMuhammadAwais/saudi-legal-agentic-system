# Saudi Legal Agentic System

A research-based multi-agent orchestration system for Saudi Arabian legal research, designed for high accuracy (90-94%) using optimized Retrieval-Augmented Generation (RAG).

## Overview

This system utilizes a decentralized architecture of seven specialized agents to process, verify, and synthesize legal information from Saudi Arabian statutes, Royal Decrees, and regulations.

### Key Features

- **Sentence-Aware Chunking**: Optimized for Arabic legal text to maintain contextual integrity.
- **Multi-Agent Orchestration**: Sequential processing through QueryPlanner, Retriever, Reranker, LegalExtractor, Verifier, Critic, and Synthesizer agents.
- **Verification Priority**: Strict policy-based generation where only 100% verified claims are included in final answers.
- **Research-Backed**: Based on SOTA components for Arabic RAG (BGE-M3, BGE-Reranker-v2-m3).

## Project Structure

- `saudi_legal_system.py`: Main orchestration engine and agent logic.
- `legal_pipeline.py`: Data ingestion and chunking pipeline.
- `system_architecture_v2.md`: Detailed technical documentation.
- `arabic_legal_rag_research.md`: Summary of research findings.

## Getting Started

1. Set your `OPENAI_API_KEY` environment variable.
2. Install dependencies: `pip install openai`
3. Run the system: `python saudi_legal_system.py`

## Accuracy and Evaluation

The system is designed to target a 90-94% accuracy rate by enforcing a "Source-to-Claim" validation check via the Verifier and Critic agents.

## License

Private / Internal Use Only.
