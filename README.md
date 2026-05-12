# Policy Pal

> Cited-answer RAG over policy, HR, and legal PDFs.

**Status:** 🚧 In development — part of a 3-week AI sprint building 5 production-grade POCs across RAG, multi-agent orchestration, and MCP.

## What it will do

Drop a folder of policy PDFs → ask natural-language questions → get answers with inline citations to the source document and section. Designed for HR, legal, and compliance teams that need answers they can trust and audit.

## Tech stack

- **LLM:** Claude Sonnet 4.5 / Opus 4.7 (Anthropic)
- **Embeddings:** OpenAI `text-embedding-3-small` + Voyage AI (comparison)
- **Vector DB:** Qdrant (local → cloud)
- **Retrieval:** Hybrid BM25 + dense, Cohere reranker
- **UI:** Streamlit
- **Eval:** Ragas (faithfulness, context precision, answer relevancy)

## Roadmap

- [x] **Day 1** — Environment, GitHub, hello tool-use loop
- [ ] **Day 2 AM** — Naive RAG v0 (fixed chunks, top-k, citations)
- [ ] **Day 2 PM** — Hybrid retrieval + reranker (v1)
- [ ] **Day 3** — Query rewriting, parent-doc retrieval, full eval harness (v2)
- [ ] **Stretch** — Slack bot wrapper, conversation memory

## Quickstart

```bash
git clone https://github.com/msnabeel96/policy-pal.git
cd policy-pal
uv sync
cp .env.example .env  # add your Anthropic key
uv run python hello_tools.py
```

## About this sprint

This is repo 1 of 5 in a 3-week sprint covering:
1. **Policy Pal** — RAG over documents *(this repo)*
2. **InboxIQ** — agentic RAG with multi-source retrieval
3. **ContractClerk** — multi-agent document workflow (LangGraph)
4. **DeskAgent** — personal productivity agent built on MCP
5. **ResearchOps** — full agentic research platform (capstone)

Follow along: [github.com/msnabeel96](https://github.com/msnabeel96)