# Saudi Legal Agentic System

A research-based multi-agent orchestration system for Saudi Arabian legal research, designed for high accuracy (90-94%) using optimized Retrieval-Augmented Generation (RAG).

## Overview

This system utilizes a decentralized architecture of seven specialized agents to process, verify, and synthesize legal information from Saudi Arabian statutes, Royal Decrees, and regulations.

### Key Features

- **Agent Lightning Architecture**: High-speed multi-agent disaggregation for low-latency legal research.
- **Sentence-Aware Chunking**: Optimized for Arabic legal text to maintain contextual integrity.
- **Parallel Multi-Agent Orchestration**: Asynchronous processing through QueryPlanner, Retriever, Verifier, Critic, and Synthesizer agents.
- **Verification Priority**: Strict policy-based generation where only 100% verified claims are included in final answers (90-94% accuracy target).
- **Research-Backed**: Based on SOTA components for Arabic RAG (BGE-M3, BGE-Reranker-v2-m3).

## Project Structure

- `saudi_legal_lightning.py`: **[LATEST]** Optimized high-speed orchestration engine using Agent Lightning principles.
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
