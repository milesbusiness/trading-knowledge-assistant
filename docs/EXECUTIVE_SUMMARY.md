# Executive Summary — Trading Knowledge Assistant

## Business Problem

A trading firm's institutional knowledge is its competitive advantage. Risk frameworks, hedging playbooks, regulatory interpretations, and trading strategies represent years of accumulated expertise. Yet this knowledge is typically fragmented across shared drives, email chains, and the heads of senior staff.

The consequences are measurable:
- New analysts spend 3–6 months before they can operate independently
- Senior analysts answer the same questions repeatedly, consuming 30–60 minutes per day
- When experienced staff leave, their knowledge is lost and must be rebuilt from scratch
- Under market stress, analysts cannot quickly verify policies that govern their decisions

A firm with 20 analysts losing 30 minutes per day to avoidable knowledge searches loses approximately **€400K in productive capacity per year** (at blended analyst cost of €150K/year fully loaded).

## The Solution

The Trading Knowledge Assistant is a conversational AI system that indexes all of a firm's internal documents — playbooks, risk frameworks, regulatory summaries, trading strategies — and allows analysts to ask questions in plain English and receive instant, cited answers.

The system maintains a 10-turn conversational memory, enabling multi-turn dialogues that progressively build on prior answers, exactly as a conversation with a knowledgeable colleague would.

## How It Is Different From Document Search

**Traditional document search** returns a list of documents that may be relevant. The analyst must open each one, read through it, and synthesise the answer themselves.

**This system** reads the documents on the analyst's behalf and returns the direct answer with the specific page number cited. The analyst verifies rather than searches.

The difference for time-sensitive decisions — a risk limit query during volatile markets — is the difference between a 20-minute process and a 10-second one.

## Key Metrics

| Metric | Before | After |
|--------|--------|-------|
| Time to answer a policy question | 15–30 minutes | < 10 seconds |
| New analyst onboarding to operational | 3–6 months | 2–4 weeks |
| Senior analyst time spent on knowledge Q&A | 30–60 min/day | Near zero |
| Knowledge retained when senior staff leave | Lost with the person | Preserved in document index |
| Answer consistency across the desk | Variable | Uniform (single source) |

## Technology Architecture (Non-Technical Summary)

The system works in two phases:

**Phase 1 — Document ingestion (one-time per document):** When a document is uploaded, the system reads it, splits it into small sections, and creates a mathematical representation of the meaning of each section. These representations are stored in a searchable index.

**Phase 2 — Query answering (every conversation turn):** When an analyst asks a question, the system searches the index using both exact keyword matching and semantic meaning matching. It retrieves the most relevant sections, combines them with the conversation history, and asks GPT-4o to write a direct answer citing the exact source documents.

## Stakeholders

| Stakeholder | What They Gain |
|-------------|---------------|
| Junior Analysts | Instant access to policies without needing to ask senior colleagues |
| Senior Analysts | Significantly less time spent answering questions from junior staff |
| Compliance Officers | Single source of truth for regulatory interpretations; consistent answers |
| Head of Trading | Reduced onboarding cost; reduced risk of policy non-adherence |
| Chief Risk Officer | Confidence that risk limits are universally accessible and consistently applied |

## Investment and Return

| Item | Cost | Return |
|------|------|--------|
| Azure OpenAI (GPT-4o calls) | ~€200–€500/month at typical usage | — |
| Azure AI Search (Standard S1) | ~€250/month | — |
| Azure Blob Storage | < €50/month | — |
| **Total monthly running cost** | **~€500–€800/month** | — |
| Analyst productivity recovered | — | **€400K+/year** |
| Payback period | — | **< 2 weeks** |

## Regulatory Relevance

The system is built for the European financial services context:
- All data remains within Azure West Europe (GDPR-compliant data residency)
- Private endpoints prevent public internet access to document content
- Access control by session — each analyst sees only what they are authorised to access
- Full audit trail of queries logged to Azure Monitor

## Summary

The Trading Knowledge Assistant turns a firm's existing document library into an always-available expert that gives instant, cited answers. It reduces new analyst onboarding time by months, eliminates daily knowledge search friction, and preserves institutional knowledge regardless of staff turnover.

Running cost: less than €800 per month. Value delivered: significantly above €400,000 per year.

---

*Author: Dilip Kumar Jena | Technology: LangChain + FastAPI + Azure AI Search*
