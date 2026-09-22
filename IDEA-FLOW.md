# بيان — Bayan

## IDEA-FLOW: Canonical Product Idea & Vision Document

> **Purpose of this document:**  
> Preserve the complete product idea, reasoning, architecture direction, UX philosophy, POC scope, constraints, and future extensibility so that any developer or AI reading it later can understand exactly what Bayan is supposed to be.

---

## Table of Contents

1. [Product Identity](#1-product-identity)
2. [The Core Idea](#2-the-core-idea)
3. [Natural Language First](#3-natural-language-first)
4. [POC Scope](#4-poc-scope)
5. [No Internet Search in the POC](#5-no-internet-search-in-the-poc)
6. [Why the Limited POC Is Okay](#6-why-the-limited-poc-is-okay)
7. [Extensibility](#7-extensibility)
8. [MCP Philosophy](#8-mcp-philosophy)
9. [Initial Tool Set](#9-initial-tool-set)
10. [Quran Audio](#10-quran-audio)
11. [Evidence-First Architecture](#11-evidence-first-architecture)
12. [Cards](#12-cards)
13. [Sources & References UI](#13-sources--references-ui)
14. [Evidence View — "Why This Answer?"](#14-evidence-view--why-this-answer)
15. [Agent vs. Evidence — The Most Important Visual Distinction](#15-agent-vs-evidence--the-most-important-visual-distinction)
16. [The Agent Must Not Generate UI](#16-the-agent-must-not-generate-ui)
17. [Guardrails](#17-guardrails)
18. ["لا أعلم" Is a Success State](#18-لا-أعلم-is-a-success-state)
19. [Retrieval Philosophy](#19-retrieval-philosophy)
20. [No Local Knowledge Database for the POC](#20-no-local-knowledge-database-for-the-poc)
21. [Desktop / BYOK Consideration](#21-desktop--byok-consideration)
22. [Development Phases](#22-development-phases)
23. [First POC — Test Flows](#23-first-poc--test-flows)
24. [Minimal POC Development Order](#24-minimal-poc-development-order)
25. [POC Project Philosophy](#25-poc-project-philosophy)
26. [Future Extensions](#26-future-extensions)
27. [Visual Design Direction](#27-visual-design-direction)
28. [Brand & Positioning](#28-brand--positioning)
29. [Core Product Principles](#29-core-product-principles)
30. [Final POC Architecture](#30-final-poc-architecture)

---

## 1. Product Identity

**Name:** بيان — Bayan

The name is intentionally broad. It is not limited to concepts such as "Hadith", "Quran", or "Sanad", because Bayan may eventually cover many areas of Islamic knowledge.

### What Bayan Is

Bayan is an AI-powered interface for accessing Islamic knowledge through **trusted external sources**.

### What Bayan Is Not

- Not an "AI Sheikh".
- Not an AI that presents itself as the religious authority.
- Not a general-purpose Islamic chatbot answering from pretrained knowledge.
- Not a generic web search engine.

### The Foundational Idea

> **The AI is not the source of truth. The sources are.**

The Agent is an **orchestrator** between the user and trusted knowledge sources.

The responsibility boundaries are important:

- The Agent understands the user's natural-language request.
- The Agent determines which authorized capability or tool is needed.
- MCP/tools retrieve information from trusted external sources.
- The backend validates whether sufficient evidence exists.
- The Agent may explain the retrieved evidence.
- The frontend presents Agent explanation and structured source evidence distinctly.

The Agent itself is never the authoritative Islamic knowledge source.

---

## 2. The Core Idea

Bayan is an Islamic AI application where the LLM/Agent is **heavily constrained regarding Islamic factual knowledge**.

The Agent must **NOT** answer Islamic factual, Quranic, Hadith, Tafsir, Fiqh, Fatwa, or scholarly questions from its pretrained/internal knowledge.

Instead, Islamic factual answers must flow through a retrieval-and-validation pipeline:

```text
User
  ↓
Agent / LLM
  ↓
Tool Calling
  ↓
MCP
  ↓
Trusted Source
  ↓
Structured Evidence
  ↓
Validation
  ↓
Supported → Agent explanation based on evidence
Insufficient → "لا أعلم"
```

### Responsibility Separation

| Responsibility | Belongs To |
|---|---|
| Understanding the user's request | LLM / Agent |
| Selecting an authorized tool | LLM / Agent |
| Retrieving source data | MCP / Tools |
| Providing source evidence | Trusted Sources through Tools |
| Authoritative Islamic knowledge | Trusted Sources |
| Validating evidence sufficiency | Backend |
| Explaining supported evidence | LLM / Agent |
| Rendering structured evidence | Frontend |

The LLM is therefore an **understanding, orchestration, reasoning, and explanation layer**, not the authoritative knowledge database.

This restriction applies specifically to Islamic factual knowledge.

Normal application-level or conversational information that does not claim Islamic factual authority does not need to pretend that it came from an external Islamic knowledge source.

---

## 3. Natural Language First

The system must **NOT** be designed around hardcoded question patterns.

Do not implement logic like:

```text
if question contains "آية" → Quran route
if question contains "حديث" → Hadith route
if question contains "حكم" → Fatwa route
```

Do not create fixed question templates.

The entire point of using an Agent + MCP is that the Agent can understand a natural-language request and determine which authorized capability or tool is appropriate.

### Examples of Natural User Requests

| User says | Agent determines |
|---|---|
| "ما معنى آية الكرسي؟" | Quran / Tafsir capability |
| "هل الحديث ده صحيح؟" | Hadith capability and available source evidence |
| "ما حكم كذا؟" | Fatwa capability |
| "شغل أول 3 آيات من سورة البقرة بصوت مشاري العفاسي." | Quran audio capability |
| "اذكرلي حديث عن الصبر." | Hadith capability |
| "ما تفسير الآية الأخيرة من سورة الكهف؟" | Quran / Tafsir capability |

These examples illustrate **natural-language understanding**.

They are not routing rules.

For example, the request:

> "هل الحديث ده صحيح؟"

does not mean the initial POC must contain a separate `hadith_verify` tool.

The initial Hadith capability may use `hadith_search` and whatever grading or relevant evidence the authorized source actually provides.

A dedicated `hadith_verify` tool may be considered later if real usage demonstrates the need.

The user should not need to know which database, API, website, or tool contains the answer.

The Agent handles tool selection.

---

## 4. POC Scope

The initial POC intentionally uses **a small number of trusted knowledge sources and a small capability set**.

Do not expand the POC into a giant Islamic knowledge ecosystem before the core architecture is proven.

### Initial Knowledge Domains and Sources

| Domain | Primary Source |
|---|---|
| Quran + Tafsir | Quran Foundation / Quran.com APIs |
| Hadith | Dorar.net |
| Fiqh / Fatwa | Official Ibn Baz website |

These are the initial trusted **knowledge sources** selected for the POC.

The project should not start by integrating dozens of websites.

### Separate POC Capability: Quran Audio

The initial POC also includes:

```text
quran_audio
```

Quran Audio is part of the POC, but it should be treated separately from textual Islamic knowledge retrieval.

It is a media capability that responds to natural-language playback requests and returns structured audio information for the frontend.

Therefore, the initial POC consists conceptually of:

1. Quran + Tafsir
2. Hadith
3. Fiqh / Fatwa
4. Quran Audio

The first three are Islamic knowledge retrieval domains.

Audio is a separate application capability.

---

## 5. No Internet Search in the POC

The initial POC should intentionally **NOT** include generic Internet Search.

Do not add Internet Search to the initial architecture.

### Reasons for Exclusion

- SEO spam
- Unreliable pages
- Source ranking problems
- Malicious pages
- Prompt injection from retrieved web content
- Scraping complexity
- Conflicting sources
- Search-provider dependencies
- Citation handling
- Content quality differences
- Source trust evaluation
- Additional security complexity

Internet Search may be considered **later** as a controlled fallback or additional capability.

It is explicitly outside the initial POC.

> The initial POC should prove the trusted-source architecture first.

---

## 6. Why the Limited POC Is Okay

The POC does **not** need to cover all Islamic knowledge.

There are many domains that may eventually be needed, such as:

- Seerah
- Islamic history
- Scholar biographies
- Rijal / narrator biographies
- Aqeedah
- Usul al-Fiqh
- Islamic books
- Hajj and Umrah
- Adhkar and Dua
- Quranic Arabic
- Gharib al-Quran
- Hadith sciences
- Mustalah al-Hadith
- Madhhab-specific Fiqh
- Other carefully selected Islamic knowledge domains

The POC does not need any of these.

### Example: Unsupported Domain

**User:**

> "احكيلي بالتفصيل عن غزوة بدر من كتب السيرة."

If the currently authorized POC sources do not provide sufficient evidence for the request, the correct result is:

> **"لا أعلم."**

or an equivalent statement explaining that sufficient evidence is not available through the currently authorized sources.

The reason is **insufficient authorized evidence**, not merely the name of the topic itself.

The Agent must not use pretrained knowledge to fill the gap.

This is correct behavior.

> `"لا أعلم"` when sufficient authorized evidence is unavailable is a successful guardrail outcome, not a failure.

The POC is testing whether the architecture can support:

- trustworthy retrieval
- evidence-grounded answering
- controlled refusal to guess

It is not testing whether Bayan can answer every Islamic question.

---

## 7. Extensibility

Although the POC is intentionally small, the architecture should be **conceptually extensible**.

### Example: Adding Seerah Later

Adding Seerah later could conceptually look like:

```text
Seerah Source
     ↓
Seerah MCP
     ↓
Seerah Tools
     ↓
Agent
     ↓
Frontend representation as appropriate
```

If a dedicated `SeerahCard` becomes useful, it may be introduced.

The important principle is not that every domain must always receive a unique card type.

The important principle is that adding another trusted knowledge domain should **not require rebuilding the entire Agent architecture**.

### The Extension Principle

> Add a trusted source, capability, or tool — not a giant new routing system.

A future domain may require:

- an authorized trusted source
- one or more semantic tools
- tool availability for the Agent
- an appropriate frontend representation if needed

The exact representation depends on the domain.

Do not turn this into a large adapter framework or rigid domain-registration architecture.

Keep the project lightweight.

---

## 8. MCP Philosophy

MCP is a core part of the architecture.

The Agent should interact with **semantic tools** rather than being tightly coupled to external URLs or API endpoints.

### Agent Thinks in Capabilities and Tools

For example:

```text
quran_search
quran_get_ayah
quran_get_tafsir
hadith_search
fatwa_search
quran_audio
```

rather than reasoning directly in terms of URLs such as:

```text
Quran API endpoint
Dorar URL
Ibn Baz URL
```

The MCP/backend tool layer knows how to communicate with the actual external service.

The Agent does not need to reason about the underlying external API structure.

### Simplicity Over Abstraction

- Keep the tool layer **small and practical**.
- Do not create an enormous abstraction framework with dozens of adapters.
- External API changes are acceptable.
- A change to an upstream source can be handled with a focused hotfix to the relevant tool/MCP integration.
- Do not over-engineer for hypothetical API changes.

---

## 9. Initial Tool Set

The first POC starts with a minimal tool set.

### Quran

| Tool | Purpose |
|---|---|
| `quran_search` | Search Quran content through the authorized Quran source |
| `quran_get_ayah` | Retrieve a specific ayah |
| `quran_get_tafsir` | Retrieve tafsir for an ayah |

### Hadith

| Tool | Purpose |
|---|---|
| `hadith_search` | Search Hadith information through the authorized Hadith source |

### Fatwa

| Tool | Purpose |
|---|---|
| `fatwa_search` | Search Fatwa / scholar material through the authorized Fatwa source |

### Audio

| Tool | Purpose |
|---|---|
| `quran_audio` | Retrieve structured Quran audio information for playback |

### Possible Future Tool Additions

Additional tools such as:

```text
hadith_get
hadith_verify
fatwa_get
```

may be added when real usage demonstrates the need.

They are not required for the initial POC.

Do not build every conceivable tool before testing the core flow.

---

## 10. Quran Audio

Audio is an important POC capability but should be treated **separately from knowledge retrieval**.

### Example User Request

> "شغل أول 3 آيات من سورة البقرة بصوت مشاري العفاسي."

The Agent should understand the requested operation and relevant parameters:

```text
task = audio
surah = 2
ayah_start = 1
ayah_end = 3
reciter = Mishary Alafasy
```

The Agent may then call something conceptually equivalent to:

```json
{
  "tool": "quran_audio",
  "surah": 2,
  "ayah_start": 1,
  "ayah_end": 3,
  "reciter": "mishary_alafasy"
}
```

The tool can return structured information such as:

```json
{
  "type": "audio",
  "surah": "البقرة",
  "from": 1,
  "to": 3,
  "reciter": "مشاري العفاسي",
  "audioUrl": "..."
}
```

The frontend then maps the tool result to an audio interface:

```text
audio → AudioPlayer
```

### Key Principle

The LLM does not generate the Audio Player or its HTML.

The tool returns structured audio information.

The frontend owns playback presentation.

---

## 11. Evidence-First Architecture

One of the most important product principles is:

> **The application must visually distinguish Agent-generated explanation from trusted evidence returned by tools.**

### Evidence Pipeline

```text
User
 ↓
Agent
 ↓
MCP Tool
 ↓
Trusted Source
 ↓
Structured Evidence
 ↓
Validation
 ↓
Supported / Insufficient
```

If sufficient evidence exists:

```text
Structured Evidence
      +
Agent Explanation
      ↓
Frontend
```

If sufficient evidence does not exist:

```text
Insufficient Evidence
        ↓
     "لا أعلم"
```

### The Trust Boundary

The Agent may produce natural-language explanation based on retrieved evidence.

The actual Quran, Hadith, Tafsir, Fatwa, source metadata, grading, references, and similar source-backed information should remain represented as **structured evidence returned through authorized tools**.

This creates a visual and architectural trust boundary:

```text
Agent explanation
→ model-generated conversational content

Evidence cards
→ structured source evidence returned through application tools
```

The distinction must not be blurred.

---

## 12. Cards

Different knowledge types may have different card designs while sharing the same Bayan design language.

The cards represent **structured evidence returned by tools**.

They are not free-form content invented by the Agent.

### Quran Card

Possible fields include:

- Surah name
- Ayah number
- Arabic verse text
- Tafsir when available
- Tafsir source
- Audio button
- Source/reference button
- Original source link

Concept:

```text
┌─────────────────────────┐
│ 📖 القرآن               │
│                         │
│ البقرة — 255            │
│                         │
│ اللَّهُ لَا إِلَٰهَ      │
│ إِلَّا هُوَ...          │
│                         │
│ ─────────────────────   │
│ التفسير                 │
│ تفسير ابن كثير          │
│ ...                     │
│                         │
│ ▶ استماع                │
│ 🔗 المصادر              │
└─────────────────────────┘
```

### Hadith Card

Possible fields include:

- Hadith text
- Narrator
- Book/source
- Hadith reference
- Grading when supported by the authorized source
- Isnād information when available
- Button to expand/show the chain when available
- Source links
- Original source

Concept:

```text
┌─────────────────────────┐
│ 🕌 حديث                 │
│                         │
│ "..."                   │
│                         │
│ الراوي: أبو هريرة       │
│ المصدر: صحيح البخاري    │
│ الحكم: صحيح             │
│                         │
│ الإسناد                 │
│ └─ فلان                 │
│    └─ فلان              │
│       └─ فلان           │
│                         │
│ [عرض الإسناد]           │
│ [المصادر والمراجع]      │
└─────────────────────────┘
```

> **Important:** Do not invent grading or isnād information.

Only display these fields when the authorized tool/source actually provides them.

### Fiqh / Fatwa Card

Possible fields include:

- Question
- Answer
- Scholar
- Source
- Reference
- Original source link
- Additional source references when applicable

Concept:

```text
┌─────────────────────────┐
│ ⚖️ فتوى                 │
│                         │
│ السؤال                  │
│ هل يجوز ...؟            │
│                         │
│ الإجابة                 │
│ ...                     │
│                         │
│ 👤 الشيخ: ابن باز       │
│ 📚 المصدر: موقع ابن باز │
│                         │
│ [المصدر الأصلي ↗]       │
│ [عرض التفاصيل]          │
└─────────────────────────┘
```

### Absolute Evidence Rule

Evidence cards must display only information returned through authorized tools/sources.

The Agent must not fabricate card evidence.

The frontend renders the structured tool result.

---

## 13. Sources & References UI

Every evidence card should provide a clear way to inspect its source.

### "المصادر والمراجع"

A reusable:

**المصادر والمراجع**

component/button may open a drawer, modal, panel, or another suitable frontend view showing the sources associated with the evidence.

Concept:

```text
┌─────────────────────────┐
│ 🔗 المصادر والمراجع     │
│                         │
│ • Quran Foundation      │
│   الآية 2:255           │
│                         │
│ • Tafsir Ibn Kathir     │
│   تفسير الآية           │
│                         │
│ • المصدر الأصلي ↗       │
└─────────────────────────┘
```

### Purpose

**Transparency**

Users can distinguish sourced evidence from Agent explanation.

**Traceability**

Users can move from a piece of evidence to its original reference/source when the authorized source provides that link or reference.

The evidence/source relationship should not be hidden.

---

## 14. Evidence View — "Why This Answer?"

A useful **future / POC UX concept** is an Evidence or "Why this answer?" view.

It is not required to prove the smallest possible core pipeline.

It may be introduced when implementing or refining evidence transparency.

Concept:

```text
Evidence

1. القرآن
   البقرة 255
   [فتح المصدر]

2. التفسير
   تفسير ابن كثير
   [فتح المصدر]

3. الحديث
   ...
   [فتح المصدر]

4. الفتوى
   ...
   [فتح المصدر]
```

The purpose is to reinforce that the Agent is not presenting itself as the original authority.

The answer is supported by evidence that the user can inspect.

---

## 15. Agent vs. Evidence — The Most Important Visual Distinction

The UI must make it obvious that:

### Agent Message

The conversational explanation is generated by the Agent.

### Evidence Card

The structured evidence is information returned through the application's authorized tools from trusted sources.

Concept:

```text
┌─────────────────────────────────────┐
│ 🤖 Agent Response                   │
│                                     │
│ "بحسب الأدلة المتاحة..."           │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 📖 Quran Card                       │
│                                     │
│ Quran evidence returned by tool     │
│                                     │
│ Source                              │
│ Original reference                 │
└─────────────────────────────────────┘
```

The user should visually understand:

```text
Conversational text
→ Agent explanation

Structured evidence card
→ Tool/source evidence
```

This distinction is also useful for technically knowledgeable users who understand MCP.

The UI communicates that the evidence came through application tools rather than being invented by the model.

---

## 16. The Agent Must Not Generate UI

The LLM should not generate HTML or decide the exact visual structure of evidence cards.

The responsibility flow is:

```text
Trusted Source
      ↓
MCP / Tool
      ↓
Structured Tool Result
      ↓
Frontend Component
```

Examples:

```text
type = quran
→ QuranCard

type = hadith
→ HadithCard

type = fatwa
→ FatwaCard

type = audio
→ AudioPlayer
```

The Agent may use retrieved evidence when producing its explanation.

However:

> **The Agent does not become the provenance of structured evidence.**

The structured evidence originates from the authorized tool/source pipeline.

The frontend owns its presentation.

This separation must be preserved.

---

## 17. Guardrails

The system must use multiple layers of protection.

The System Prompt is **not** the final security or quality boundary.

### Layer 1: Agent Instructions

The Agent should be instructed:

- Never answer Islamic factual/legal/Quran/Hadith/Tafsir/scholarly questions from pretrained knowledge.
- Use authorized tools for those questions.
- Never invent Quran verses.
- Never invent Hadith.
- Never invent Hadith grading.
- Never invent Tafsir.
- Never invent Fatwas.
- Never invent scholar opinions.
- Never invent citations.
- Never invent URLs.
- Never fabricate sources.
- If authorized evidence is insufficient, say `"لا أعلم."`
- If authorized sources disagree, report the disagreement and attribute the positions.
- Do not resolve source disagreements using model memory.

### Layer 2: Backend Evidence Enforcement

Do not rely on the System Prompt alone.

The backend should enforce the evidence requirement.

Conceptually:

```text
Agent
 ↓
Tool
 ↓
Trusted Source
 ↓
Structured Evidence
 ↓
Evidence Sufficient?
 ├── YES → supported answer allowed
 └── NO  → "لا أعلم"
```

If the tool/source pipeline does not provide sufficient evidence and the Agent attempts to answer the Islamic factual question from memory, the backend should block that behavior.

### Minimal Evidence Statuses

The POC can remain simple:

```text
supported
insufficient_evidence
```

A future version may add:

```text
conflicting_sources
```

if real usage demonstrates the need.

The POC does not require a complex evidence-state system.

---

## 18. "لا أعلم" Is a Success State

If the authorized sources do not provide sufficient evidence for an Islamic factual request, the correct result is not a guessed answer.

It is:

> **"لا أعلم."**

or an equivalent statement explaining that sufficient evidence is unavailable through the currently authorized sources.

This is a **successful guardrail outcome**.

### Example

**User:**

> "ما تفاصيل غزوة بدر من كتب السيرة؟"

If the POC currently has no sufficient authorized evidence for the request:

> **"لا أعلم."**

The Agent must not use pretrained knowledge to fill the gap.

The determining condition is:

```text
Sufficient authorized evidence?
```

not merely:

```text
Does the question contain a known or unknown topic label?
```

This keeps the architecture evidence-driven rather than topic-hardcoded.

---

## 19. Retrieval Philosophy

The project does not need a huge local vector database for the initial POC.

### Initial Retrieval Model

```text
LLM
+
Tool Calling
+
MCP
+
Trusted External Retrieval
+
Evidence Validation
```

The initial POC does not require:

```text
Huge Local DB
+
Embeddings
+
Vector DB
+
Complex Ingestion Pipeline
```

Direct retrieval from trusted external APIs/tools can serve the retrieval-grounded architecture.

The project can conceptually be described as **retrieval-grounded generation**.

Do not assume that retrieval-grounded generation requires embeddings or a vector database.

---

## 20. No Local Knowledge Database for the POC

The initial project should remain lightweight.

Do not create:

- a giant local canonical Islamic database
- a large ingestion pipeline
- a vector database solely for the POC
- a giant source synchronization architecture

The initial POC should rely on external trusted sources through the MCP/tool layer.

If an upstream API changes, a focused fix to the relevant tool/MCP integration is acceptable.

Do not build a massive abstraction architecture solely to protect against hypothetical upstream API changes.

This is especially relevant because a future Desktop application may be downloadable and may support BYOK.

The initial architecture should not assume that every user must download a huge Islamic knowledge database.

---

## 21. Desktop / BYOK Consideration

The eventual product may have a Desktop version.

The Desktop product should remain lightweight.

A possible future model is **BYOK — Bring Your Own Key**, where users provide their own model/API key.

This is a future consideration, not an initial POC requirement.

### Long-Term Concept

```text
                 Bayan Core
                     │
              ┌──────┴──────┐
              ↓             ↓
             Web         Desktop
```

Conceptually, both clients can use the same core ideas:

- Agent
- MCP/tools
- trusted sources
- guardrails
- evidence validation

Desktop-specific implementation topics such as:

- packaging
- credential storage
- updater systems
- desktop distribution

are outside the initial POC.

---

## 22. Development Phases

The recommended development order is:

```text
Phase 0
Core POC
Agent + MCP + Sources + Guardrails

        ↓

Phase 1
Minimal Web UI

        ↓

Phase 2
Evidence Cards + Sources + Audio + UX Polish

        ↓

Phase 3
Desktop
```

Do not start by building a complete Desktop application.

The first thing to prove is the core pipeline:

```text
Natural-language request
        ↓
Agent tool selection
        ↓
Trusted external retrieval
        ↓
Structured evidence
        ↓
Validation
        ↓
Supported explanation
or
"لا أعلم"
```

---

## 23. First POC — Test Flows

The first POC should be very small.

It should prove these flows reliably.

### Test 1 — Quran

```text
Question
↓
Quran tool
↓
Quran evidence
↓
Validation
↓
Agent explanation
```

### Test 2 — Tafsir

```text
Question
↓
Tafsir tool
↓
Tafsir evidence
↓
Validation
↓
Agent explanation
```

### Test 3 — Hadith

```text
Question
↓
Hadith tool
↓
Hadith evidence
↓
Validation
↓
Agent explanation
```

Any grading or similar information shown must come from the authorized source evidence.

A separate `hadith_verify` tool is not required for this initial test.

### Test 4 — Fiqh / Fatwa

```text
Question
↓
Fatwa tool
↓
Fatwa evidence
↓
Validation
↓
Agent explanation
```

### Test 5 — Insufficient Authorized Evidence

```text
Question
↓
No sufficient authorized evidence
↓
"لا أعلم."
```

This test can include requests from domains that the POC does not currently support, such as detailed Seerah questions.

### Test 6 — Audio

```text
Natural-language audio request
↓
quran_audio
↓
Structured audio result
↓
AudioPlayer
```

The POC is successful if these six core flows work reliably.

---

## 24. Minimal POC Development Order

Suggested practical order:

| Step | Task |
|---|---|
| 1 | Make Groq/LLM tool calling work |
| 2 | Connect the Quran MCP/tool |
| 3 | Implement the evidence validator |
| 4 | Add Hadith |
| 5 | Add Fatwa |
| 6 | Add Quran Audio |
| 7 | Create a very minimal Web UI |
| 8 | Implement evidence Cards |
| 9 | Implement Sources/References UI |

Do not add large amounts of functionality before these steps work.

The order exists to prove the core concept incrementally.

It is not a requirement to build future production infrastructure.

---

## 25. POC Project Philosophy

### Avoid Overengineering

The project intentionally does **not** need:

- Giant database architecture
- Large ingestion pipelines
- Huge source abstraction layers
- Dozens of MCP servers
- Generic Internet Search
- Complex RAG infrastructure
- Vector database
- Hardcoded question routers
- Huge frontend architecture
- Desktop packaging
- Enterprise-scale infrastructure

The initial objective is not to build the final platform.

The initial objective is to prove:

> **Natural-language Agent + MCP + trusted sources + structured evidence + evidence validation + strict "لا أعلم" behavior.**

Evidence cards and transparent source presentation then make that architecture understandable to users.

Everything else is secondary until this works.

---

## 26. Future Extensions

The following are **future possibilities, not current POC requirements**.

### Potential Future Knowledge Domains

- Seerah
- Islamic history
- Aqeedah
- Scholar biographies
- Narrator biographies / Rijal
- Islamic books
- Hajj and Umrah
- Adhkar and Dua
- Quranic Arabic
- Gharib al-Quran
- Hadith sciences
- Mustalah al-Hadith
- Usul al-Fiqh
- Madhhab-specific Fiqh
- Other carefully selected trusted Islamic sources/domains

### Potential Future Capabilities

- Internet Search as a controlled fallback
- More sophisticated source comparison
- Conflicting-source UI
- Better citation/source exploration
- More audio capabilities
- Book/document retrieval
- More detailed isnād exploration
- Scholar/source profiles
- Additional evidence presentation types

These items are documented only to preserve future direction.

They must not silently become dependencies of the initial POC.

If a future domain is not connected and the currently authorized sources cannot provide sufficient evidence, the Agent must not fall back to pretrained Islamic knowledge.

The correct result remains:

> **"لا أعلم."**

---

## 27. Visual Design Direction

The product name is:

**بيان — Bayan**

The primary brand direction is **green**.

However, the interface should **not** look like a generic "green Islamic website."

### Desired Direction

> **Modern scholarly product with Islamic visual identity.**

Useful mental references include a combination of:

- modern AI/chat interfaces
- clean research/reference products
- digital Quran applications
- scholarly reading interfaces

without excessive traditional ornamentation.

Do not make every surface green.

### Light Mode — Starting Direction

```text
Background       #F8FAF8
Surface          #FFFFFF
Text             #17201A
Secondary Text   #66736A

Primary Green    #167A4A
Light Green      #E8F5EE
Border           #DCE7E0
```

These values are **starting design tokens**, not immutable technical requirements.

Green should primarily support:

- brand identity
- active states
- buttons
- links
- focus states
- trusted/evidence-related accents

### Dark Mode — Starting Direction

```text
Background       #0D1210
Surface          #151C18
Elevated         #1B241F
Text             #F1F5F2
Secondary Text   #9AA89F

Primary Green    #45B879
Light Green      #183B29
Border           #29362F
```

The Dark Mode should feel calm and scholarly.

Avoid neon green or gaming-style aesthetics.

### Card Color System

All evidence cards should share a common Bayan design language.

Possible subtle accents:

```text
Quran    → Green
Hadith   → Teal-ish green
Fiqh     → Olive-ish green
Seerah   → Green/Gold later
Audio    → Green
```

These distinctions should remain subtle.

The cards should still clearly belong to the same product.

### Agent vs. Evidence Colors

```text
Agent messages
→ mostly neutral conversational UI

Evidence cards
→ structured UI with trusted green accents
```

The visual system should reinforce:

> The Agent explains.

> The tools provide the evidence.

---

## 28. Brand & Positioning

### Product Name

**بيان — Bayan**

The name is intentionally broader than Quran, Hadith, or Sanad because the product may eventually support more areas of Islamic knowledge.

### Possible Tagline Directions

> المعرفة الإسلامية، بمصادرها.

or:

> اسأل. افهم. وتحقق.

or similar concise language.

### Positioning

Bayan should be positioned as:

> **A trustworthy interface for accessing sourced Islamic knowledge.**

It should not be branded as an AI religious authority.

The Agent is the interface and orchestration layer.

The trusted sources remain the evidence layer.

---

## 29. Core Product Principles

These principles must remain intact regardless of implementation phase.

### Principle 1 — The LLM Is Not the Islamic Knowledge Source

```text
LLM / Agent
=
Understanding
+
Orchestration
+
Explanation


MCP / Tools
=
Retrieval


Trusted Sources
=
Authority / Evidence


Backend
=
Evidence Enforcement


Frontend
=
Transparent Presentation
```

### Principle 2 — Evidence Has Tool/Source Provenance

Structured evidence originates from:

```text
Trusted Source
↓
Tool / MCP
↓
Structured Evidence
```

The Agent may explain that evidence.

The Agent does not become the source or provenance of the evidence.

### Principle 3 — Evidence Must Be Structurally Distinct from Agent Explanation

The source/tool result should remain structurally distinct from Agent-generated conversational content.

The frontend must preserve that distinction.

Users should be able to understand which content is:

```text
Agent explanation
```

and which content is:

```text
Tool/source evidence
```

### Principle 4 — "لا أعلم" Over Guessing

If authorized sources do not provide sufficient evidence for an Islamic factual request:

> **"لا أعلم."**

The Agent must not guess or fill the gap from pretrained Islamic knowledge.

This is a successful guardrail state.

### Principle 5 — Natural Language, Not Hardcoded Routes

The Agent determines the required authorized capability from natural language.

Do not implement:

- fixed question templates
- keyword routing
- hardcoded `"if X then tool Y"` logic

The examples in this document illustrate behavior.

They are not routing rules.

### Principle 6 — Transparency and Traceability

Structured Islamic evidence should preserve enough source/reference information for users to inspect its origin when available from the authorized source.

Evidence should not be presented as if it originated from the Agent.

This traceability requirement applies to **source-backed evidence**, not to unrelated application messages or the `"لا أعلم"` guardrail result.

### Principle 7 — Backend Enforcement

The System Prompt alone is not sufficient.

The backend must enforce the evidence requirement for Islamic factual answers.

### Principle 8 — Simplicity Over Enterprise Scale

Keep the project lightweight.

Prove the product concept first.

Do not add large infrastructure because it may theoretically be useful later.

---

## 30. Final POC Architecture

### Core Knowledge Flow

```text
                         User
                           │
                           ↓
                     Agent / LLM
                        (Groq)
                           │
                           ↓
                     Tool Calling
                           │
           ┌───────────────┼───────────────┐
           ↓               ↓               ↓
       Quran MCP       Hadith MCP       Fatwa MCP
           │               │               │
           ↓               ↓               ↓
      Quran.com /       Dorar.net        Ibn Baz
      Quran Foundation
           │               │               │
           └───────────────┼───────────────┘
                           ↓
                    Structured Evidence
                           ↓
                       Validation
                      /          \
                     /            \
            sufficient          insufficient
                 │                   │
                 ↓                   ↓
       Agent explanation         "لا أعلم"
                 │
                 ↓
              Frontend
                 │
        ┌────────┼─────────┐
        ↓        ↓         ↓
    QuranCard HadithCard FatwaCard
        │        │         │
        └────────┼─────────┘
                 ↓
          Sources / References
```

The important provenance rule is:

```text
Trusted Source
→ Tool / MCP
→ Structured Evidence
```

not:

```text
Agent
→ Invented Structured Evidence
```

The Agent consumes or reasons over retrieved evidence in order to produce a supported explanation.

The evidence itself remains structurally tied to the tool/source result.

### Audio — Separate Flow

```text
User
 ↓
Agent
 ↓
quran_audio
 ↓
Structured Audio Result
 ↓
AudioPlayer
```

Audio is part of the POC but remains separate from textual knowledge retrieval.

---

## Appendix: What This Document Preserves

A developer or AI reading this document should understand:

| # | Topic |
|---|---|
| 1 | What Bayan is |
| 2 | What Bayan is not |
| 3 | Why the LLM is not the Islamic source of truth |
| 4 | Why trusted external sources provide the evidence |
| 5 | Why MCP/tools are used |
| 6 | Which trusted knowledge sources are included in the POC |
| 7 | Why Quran Audio is a separate POC capability |
| 8 | Why generic Internet Search is excluded |
| 9 | Why a local canonical DB/vector DB is not required |
| 10 | How natural-language Agent-driven tool selection works |
| 11 | Why hardcoded keyword routing is rejected |
| 12 | How structured evidence flows from sources/tools |
| 13 | How backend evidence validation works |
| 14 | Why `"لا أعلم"` is a successful state |
| 15 | How Quran/Hadith/Fatwa evidence cards work |
| 16 | How Quran Audio works |
| 17 | Why Agent messages and evidence cards are distinct |
| 18 | How source/reference transparency works |
| 19 | How future domains can be added without rebuilding the system |
| 20 | Why future domains are not current POC requirements |
| 21 | Why the POC should remain small |
| 22 | Why Web comes before Desktop |
| 23 | How BYOK/Desktop remain future considerations |
| 24 | The intended visual and brand direction |
| 25 | The core principles that must not be violated |

---

## Final Product Principle

The most important principle to preserve is:

> **Bayan does not want the LLM to be the Islamic knowledge source.**

Instead:

```text
LLM / Agent
=
Understanding + Orchestration + Explanation

MCP / Tools
=
Retrieval

Trusted Sources
=
Authority / Evidence

Backend
=
Validation + Enforcement

Frontend
=
Transparent Presentation
```

The initial POC exists to prove that this separation works reliably.

Bayan should succeed not because the model can answer everything, but because it can:

```text
understand naturally
→ use the right authorized capability
→ retrieve trusted evidence
→ preserve evidence provenance
→ validate sufficiency
→ explain only what is supported
→ say "لا أعلم" when it is not
```

That separation is the foundation of Bayan.

---

*This document is the canonical reference for the Bayan product idea, philosophy, POC boundaries, architectural direction, and UX principles. It is not an implementation specification, and future possibilities documented here must not be treated as current POC requirements.*
