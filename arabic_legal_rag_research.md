# Research Findings: Arabic Legal RAG Optimization (Saudi Law)

## 1. Optimal Components for Arabic RAG (Based on Alsubhi et al., 2025)
- **Chunking Strategy**: **Sentence-aware chunking** consistently outperforms other methods (semantic, recursive, fixed-size) in context recall and answer relevancy for structured Arabic text.
- **Embedding Models**: 
    - **BGE-M3**: High performance across diverse domains.
    - **Multilingual-E5-large**: Excellent retrieval and generation scores.
    - **text-embedding-3-large**: Also noted as effective in other benchmarks (e.g., Islamic QA).
- **Reranker**: **bge-reranker-v2-m3** significantly boosts faithfulness, especially in complex retrieval scenarios.
- **LLM for Generation**: **Aya-8B** (by Cohere) is superior for Arabic answer generation within RAG frameworks compared to other models like StableLM.

## 2. Specialized Legal RAG Insights
- **Sharia & Legal Text**: Neural embeddings tuned with optimal hyperparameters produce satisfactory results for Sharia and Arabic legal texts.
- **Hybrid Approaches**: A two-step semantic text chunking method combining unsupervised semantic chunking with fine-tuned BERT embeddings is recommended for high precision.
- **Evaluation Framework**: Use **RAGAS** for measuring:
    - Context Precision
    - Context Recall
    - Answer Faithfulness
    - Answer Relevancy

## 3. Saudi Law Context
- Legal texts in Saudi Arabia are often dense and morphologically rich.
- Accuracy targets (90-94%) require high-quality retrieval (Precision@k) and rigorous verification to prevent hallucinations.
- Jurisdiction-specific references are mandatory.

## 4. Multi-Agent Orchestration Plan
- **QueryPlanner**: Breakdown complex Saudi legal queries into specific sub-tasks (e.g., search for Royal Decrees, search for Implementing Regulations).
- **Retriever**: Use BGE-M3 or Multilingual-E5-large with sentence-aware chunking.
- **Reranker**: Apply bge-reranker-v2-m3.
- **LegalExtractor**: Specialized in identifying statutes, case citations, and specific articles.
- **Verifier**: Cross-reference extracted claims with retrieved sources for factual consistency.
- **Critic**: Explicitly look for hallucinations or misinterpretations of Sharia-based laws.
- **Synthesizer**: Final JSON output with citations and jurisdiction.
