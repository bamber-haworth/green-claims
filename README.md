# 🌿 GreenCheck
An AI-powered tool for validating environmental claims against open regulatory standards.
Built as a learning project to explore how LLMs can make complex, unstructured policy documents easier to find, understand, and act on.

## What it does
Companies make a lot of environmental claims. "Carbon neutral." "Sustainably sourced." "Net zero by 2030." Some are substantiated. Many aren't.
GreenCheck lets you paste any green claim and validates it against a curated corpus of open regulatory and policy documents — returning a structured verdict, the relevant standard, and exactly what the regulation actually requires.

## Why I built this
I'm interested in the intersection of AI, open data, and policy — specifically how NLP and LLMs can unlock insight from documents that are technically public but practically inaccessible. Most people can't read 200 pages of EU regulatory guidance to check whether a claim on a shampoo bottle is legitimate. This is a small attempt to close that gap.
The problem structure maps directly onto challenges I find compelling: unstructured documents, professional-grade information needs, and the question of how to surface the right insight at the right moment for a non-expert user.

## The corpus
Rather than scraping everything, I curated a small set of high-quality, authoritative sources. Curation decisions matter as much as retrieval — garbage in, garbage out.
* EU Green Claims Directive (2024 draft) - 
Sets the incoming legal standard for environmental claims in Europe
* CMA Green Claims Code (UK) - 
The UK regulator's practical guidance on what makes a claim legitimate
* FCA Anti-Greenwashing Guidance - 
Applies to financial products and sustainability-linked instruments
* Science Based Targets initiative (SBTi) criteria - 
The dominant standard for corporate net zero and emissions targets


## How it works

You paste a claim
The corpus is passed to Gemini 2.0 Flash alongside a structured prompt
The model returns a JSON verdict: substantiated / partially substantiated / unsubstantiated / misleading, with confidence level, the relevant standard, what the regulation actually says, red flags, and what would make the claim valid
The UI surfaces this in plain English

No vector database at this scale — the full corpus fits comfortably within Gemini's context window, which also means retrieval is deterministic rather than dependent on embedding quality.

## Stack

* Python / Streamlit — UI
* Gemini — LLM (free tier via Google AI Studio)
* Plain text corpus — no database, no embeddings at this scale


Running it locally:

`bashgit clone https://github.com/bamber-haworth/green-claims`
`cd greencheck`
`pip install streamlit google-genai`
`export GEMINI_API_KEY=your_key_here`
`streamlit run app.py`

## Limitations (and what I'd do next)
This is a v0 built to learn, not a production tool. Limitations:

* Corpus is small and static — claims outside the scope of these documents will get weaker verdicts. A production version would need a much wider, regularly updated corpus.
* No chunking or retrieval — stuffing the full corpus into context works at this scale but doesn't scale. A proper RAG pipeline with a vector store (Pinecone, pgvector) and smarter chunking would improve both quality and cost.
* LLMs hallucinate — the model is instructed to cite specific language but can still confabulate. Every verdict should be verified against the source.
* Not legal advice — this is a research and learning tool, not a compliance product.

If I were building v2:

* Proper ingestion pipeline for new documents (PDF → chunk → embed → store)
* Source citation with page references
* Claim history and comparison across multiple products
* API endpoint so it could be embedded in other tools


Acknowledgements
Regulatory documents sourced from the EU Commission, UK CMA, FCA, IPCC, SBTi, and GRI. All open access. Built with Claude.
