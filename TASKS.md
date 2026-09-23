# Bayan Task Roadmap

This file turns the product and stack decisions in `IDEA-FLOW.md` and `STACK.md` into implementation-sized work.

It is a roadmap and planning index, not the live status tracker.

Once a task is created as a GitHub Issue, GitHub becomes the source of truth for its status, discussion, assignment, and implementation.

## Task Conventions

Roadmap IDs use this format:

```text
P0-01
P0-02
P1-01
...
```

These IDs are not GitHub Issue numbers.

When a planned task becomes a GitHub Issue, the Issue may be referenced next to the roadmap task.

Issue titles follow the same Conventional style used for commits and Pull Requests:

```text
chore:
feat:
fix:
test:
ci:
docs:
refactor:
```

Each task contains:

- **Goal**
- **Scope**
- **Done when**
- **Depends on** only when a real dependency exists

One task should normally map to one focused Pull Request.

Tasks in the same phase may run in parallel when their dependencies allow it.

---

# Phase 0 — Project Foundation

Establish the repository, development environment, quality tooling, CI, and observability required for later work.

## P0-01 — chore: bootstrap backend

**Goal**

Create the initial FastAPI backend using the agreed Python stack and repository layout.

**Scope**

- Initialize the backend with `uv`
- Add FastAPI
- Add Pydantic and `pydantic-settings`
- Add `httpx`
- Create the agreed `backend/app/` structure:
  - `api/`
  - `agent/`
  - `providers/`
  - `mcp/`
  - `tools/`
  - `schemas/`
  - `services/`
  - `core/`
- Add application settings loading
- Add a minimal health endpoint
- Add initial pytest / pytest-asyncio configuration
- Add Ruff and Pyright configuration

**Done when**

- The backend installs through `uv`
- FastAPI starts locally
- The health endpoint responds successfully
- Ruff, Pyright, and pytest can run locally

---

## P0-02 — chore: bootstrap frontend

**Goal**

Create the initial Next.js frontend using the exact agreed bootstrap configuration.

**Scope**

Bootstrap with:

```powershell
pnpm create next-app frontend --typescript --eslint --tailwind --app --src-dir --turbopack --import-alias "@/*" --use-pnpm --yes
```

Also ensure:

- TypeScript strict mode is enabled
- The App Router is used
- `src/` is used
- Tailwind CSS is available
- ESLint runs successfully
- The `@/*` alias works

**Done when**

- The frontend installs through pnpm
- Next.js starts locally
- TypeScript checks pass
- ESLint passes

---

## P0-03 — chore: add local infrastructure

**Goal**

Provide the local PostgreSQL and Redis services required by Bayan.

**Scope**

- Add Docker Compose
- Add PostgreSQL
- Add Redis
- Add development connection settings
- Add `.env.example` without secrets
- Keep FastAPI and Next.js outside Docker for normal local development

**Done when**

- PostgreSQL and Redis start through Docker Compose
- The backend can connect to both services
- A new contributor can see all required local environment variables in `.env.example`

**Depends on**

- P0-01

---

## P0-04 — ci: add initial GitHub Actions checks

**Goal**

Create the initial CI quality gate for pushes and Pull Requests.

**Scope**

Backend checks:

- Ruff
- Pyright
- pytest

Frontend checks:

- ESLint
- TypeScript

Do not add frontend tests until a frontend test framework is intentionally selected.

**Done when**

- GitHub Actions runs on pushes and Pull Requests
- Backend and frontend checks execute successfully
- CI failures are visible on Pull Requests

**Depends on**

- P0-01
- P0-02

---

## P0-05 — chore: add observability foundation

**Goal**

Add the initial error tracking and application logging foundation.

**Scope**

- Add Sentry to FastAPI
- Add Sentry to Next.js
- Add normal backend application logging
- Prevent known sensitive values from being intentionally logged
- Keep Sentry separate from normal logs

**Done when**

- Backend and frontend can report test errors to Sentry when configured
- The application still runs when Sentry is not configured locally
- Plaintext passwords, BYOK keys, session secrets, and verification codes are not intentionally logged

**Depends on**

- P0-01
- P0-02

### Phase 0 Exit Criteria

Phase 0 is complete when:

- Backend and frontend run locally
- PostgreSQL and Redis are available locally
- Core quality checks run locally and in GitHub Actions
- Basic logging and Sentry integration exist

---

# Phase 1 — Accounts, Auth & Persistence

Build the application foundation required for real users, BYOK credentials, and persistent conversations.

## P1-01 — feat: add async database foundation

**Goal**

Add PostgreSQL persistence using the agreed asynchronous database stack.

**Scope**

- Add SQLAlchemy Async
- Add psycopg v3 async
- Add Alembic
- Add async session management
- Add a minimal migration workflow

**Done when**

- The backend can open async PostgreSQL sessions
- Alembic can create and apply migrations
- Database configuration comes from application settings

**Depends on**

- P0-01
- P0-03

---

## P1-02 — feat: add user authentication model

**Goal**

Create the database model and constraints required by the Bayan Auth Contract.

**Scope**

Represent the agreed user identity fields, including:

- user ID
- normalized unique email
- auth method
- provider user ID when applicable
- password hash when applicable
- email verification state
- name
- optional avatar
- timestamps

Enforce the initial one-account / one-auth-method contract.

**Done when**

- The user model is represented in PostgreSQL
- Email uniqueness is enforced
- Password and OAuth identity constraints match `STACK.md`
- A migration creates the required schema

**Depends on**

- P1-01

---

## P1-03 — feat: add server-side sessions

**Goal**

Implement revocable server-side authentication sessions backed by Redis.

**Scope**

- Generate opaque session identifiers
- Store session state in Redis
- Send session IDs through cookies
- Use HttpOnly cookies
- Use Secure cookies in production
- Configure SameSite appropriately
- Implement session invalidation on logout
- Avoid long-lived secrets inside session state

**Done when**

- A server session can be created, resolved, and revoked
- Logout invalidates the Redis session
- Protected backend routes can resolve the authenticated user from the session

**Depends on**

- P0-03
- P1-02

---

## P1-04 — feat: implement password authentication

**Goal**

Implement email/password signup and login without weakening the Auth Contract.

**Scope**

- Password signup
- Password login
- Argon2 hashing through `pwdlib`
- Generic login failures where appropriate
- Prevent duplicate accounts across conflicting auth methods
- Integrate successful login with server-side sessions

**Done when**

- Passwords are never stored plaintext
- Valid password users can sign in
- Invalid credentials fail safely
- Conflicting auth-method cases are rejected according to `STACK.md`

**Depends on**

- P1-02
- P1-03

---

## P1-05 — feat: add email verification

**Goal**

Require verified email for password accounts before chat access.

**Scope**

- Integrate Resend for verification email delivery
- Generate 6-digit verification codes
- Store verification state in Redis
- Make codes short-lived and one-time use
- Limit attempts
- Add resend cooldown behavior
- Mark the user verified only after successful verification

**Done when**

- A password signup can receive a verification code
- A valid code verifies the account once
- Expired or reused codes fail
- Unverified password users cannot proceed to normal chat access

**Depends on**

- P1-04
- P0-03

---

## P1-06 — feat: implement password reset

**Goal**

Provide password reset for password accounts without converting OAuth accounts.

**Scope**

- Request reset
- Deliver reset communication through Resend
- Validate reset authorization
- Set a new Argon2 password
- Use generic public responses to reduce account enumeration
- Do not create passwords for OAuth-only accounts
- Invalidate relevant security/session state after reset

**Done when**

- Password accounts can securely reset their password
- OAuth-only accounts are not converted to password accounts
- Public responses do not unnecessarily reveal account existence or auth method

**Depends on**

- P1-04
- P1-05

---

## P1-07 — feat: add Google OAuth

**Goal**

Add Google authentication while preserving Bayan's single-auth-method account model.

**Scope**

- Use Authlib
- Implement OAuth/OIDC state handling
- Require verified email
- Store stable provider user ID
- Reject cross-method account conflicts
- Handle provider email changes according to `STACK.md`
- Create a server-side Bayan session after successful authentication

**Done when**

- A new user can create a Bayan account through Google
- Returning Google users are identified by stable provider identity
- Missing verified email blocks account creation
- Conflicting existing accounts are not silently linked

**Depends on**

- P1-02
- P1-03

---

## P1-08 — feat: add GitHub OAuth

**Goal**

Add GitHub authentication under the same Auth Contract as Google.

**Scope**

- Use Authlib
- Handle OAuth state
- Retrieve a verified email
- Store stable GitHub provider user ID
- Reject cross-method conflicts
- Do not create an account if GitHub cannot provide a verified email
- Create a server-side Bayan session after successful authentication

**Done when**

- New and returning GitHub users can authenticate when a verified email is available
- Missing verified email prevents account creation
- Existing conflicting accounts are not auto-linked

**Depends on**

- P1-02
- P1-03

---

## P1-09 — feat: add encrypted BYOK credential storage

**Goal**

Store the user's Groq API key server-side without storing or returning plaintext credentials.

**Scope**

- Add `cryptography`
- Encrypt provider credentials with Fernet
- Keep the Fernet master key outside PostgreSQL
- Store only ciphertext in PostgreSQL
- Decrypt only inside the backend when a provider request requires it
- Return only non-secret or masked credential state to the frontend
- Never return the stored plaintext key after saving

**Done when**

- A user can save and replace a Groq API key
- PostgreSQL contains only encrypted credential data
- The API cannot retrieve the original stored plaintext key
- Provider code can obtain the decrypted key only at request time

**Depends on**

- P1-01
- P1-02

---

## P1-10 — feat: add conversation persistence

**Goal**

Create the persistent conversation model required by Bayan chat history.

**Scope**

Persist:

- conversations
- user ownership
- messages
- message role/content
- timestamps
- structured evidence snapshots for relevant assistant turns
- source/reference metadata needed to restore previous evidence

Do not treat stored conversations as training data.

**Done when**

- Conversations belong to authenticated users
- Messages survive refresh, logout, and later login
- The schema can store evidence snapshots without re-querying upstream sources later

**Depends on**

- P1-01
- P1-02

### Phase 1 Exit Criteria

Phase 1 is complete when:

- Users can authenticate through the supported methods
- Password accounts can verify and reset credentials
- Sessions are stored server-side in Redis
- BYOK credentials are encrypted in PostgreSQL
- Conversations and evidence-capable messages can be persisted

---

# Phase 2 — Trusted Source Layer

Build Bayan's authorized source integrations and semantic tool layer without using the LLM as an Islamic knowledge source.

## P2-01 — feat: define structured evidence schemas

**Goal**

Create typed schemas for tool outputs and evidence before building source integrations.

**Scope**

Define the minimal structured contracts needed for:

- Quran evidence
- Tafsir evidence
- Hadith evidence
- Fatwa evidence
- Quran audio results
- source/reference metadata
- tool errors / unavailable source conditions

Keep source-backed evidence structurally distinct from future Agent explanation.

**Done when**

- Tool outputs can be validated through Pydantic
- Evidence types carry the metadata required by the frontend and persistence layer
- Optional source fields are not fabricated when unavailable

**Depends on**

- P0-01

---

## P2-02 — feat: add MCP and semantic tool foundation

**Goal**

Create the lightweight backend tool/MCP layer through which the Agent will access authorized capabilities.

**Scope**

- Keep MCP inside the backend
- Add a small semantic tool registry/interface
- Expose tools by capability rather than external URL
- Avoid hardcoded question routing
- Avoid a large generic adapter framework

**Done when**

- Backend code can register and invoke semantic tools consistently
- Tools can return typed structured results
- No routing logic depends on fixed Arabic/English keywords in user prompts

**Depends on**

- P2-01

---

## P2-03 — feat: add Quran and Tafsir tools

**Goal**

Integrate Quran Foundation / Quran.com for the initial Quran and Tafsir capabilities.

**Scope**

Implement:

- `quran_search`
- `quran_get_ayah`
- `quran_get_tafsir`

Use async HTTP through `httpx`.

Normalize upstream responses into Bayan evidence schemas.

**Done when**

- Quran search returns structured source-backed results
- A specific ayah can be retrieved
- Tafsir can be retrieved when supported by the source
- Source/reference metadata is preserved
- Upstream data is not rewritten into invented evidence fields

**Depends on**

- P2-01
- P2-02

---

## P2-04 — feat: add Hadith search tool

**Goal**

Integrate Dorar.net as the initial Hadith source.

**Scope**

- Implement `hadith_search`
- Retrieve available Hadith information
- Preserve grading only when the authorized source provides it
- Preserve narrator/reference metadata when available
- Do not invent isnad or grading details

**Done when**

- Hadith searches return structured evidence
- Returned grading/reference information can be traced to the source
- Missing optional fields remain missing rather than synthesized

**Depends on**

- P2-01
- P2-02

---

## P2-05 — feat: add Fatwa search tool

**Goal**

Integrate the official Ibn Baz website as the initial Fiqh/Fatwa source.

**Scope**

- Implement `fatwa_search`
- Retrieve relevant source material
- Normalize question/answer/scholar/reference metadata when available
- Preserve the original source reference

**Done when**

- Fatwa searches return structured evidence
- Results identify the authorized source
- The tool does not silently use generic web search

**Depends on**

- P2-01
- P2-02

---

## P2-06 — feat: add Quran audio tool

**Goal**

Implement the separate Quran audio capability.

**Scope**

- Implement `quran_audio`
- Support structured surah / ayah range / reciter parameters
- Return structured playback information
- Keep audio results separate from textual evidence authority

**Done when**

- A valid audio request can return a structured audio result
- The result contains enough metadata for a frontend AudioPlayer
- The tool does not generate frontend HTML

**Depends on**

- P2-01
- P2-02

---

## P2-07 — test: cover trusted source tools

**Goal**

Verify source integrations and normalization behavior independently of the Agent.

**Scope**

Test:

- expected tool outputs
- missing optional source fields
- upstream failures
- malformed upstream responses
- timeouts
- evidence schema validation
- source provenance preservation

**Done when**

- Each initial tool has backend test coverage for success and meaningful failure paths
- Tests prove that source data is not silently fabricated

**Depends on**

- P2-03
- P2-04
- P2-05
- P2-06

### Phase 2 Exit Criteria

Phase 2 is complete when:

- Every initial POC capability can be invoked without the Agent
- Tool outputs are structured and source-backed
- Tool failures are represented safely
- No generic internet search or local Islamic knowledge database exists

---

# Phase 3 — Agent & Evidence Core

Add Groq and build the constrained orchestration layer that selects tools, validates evidence, and refuses unsupported Islamic factual answers.

## P3-01 — feat: add Groq provider

**Goal**

Integrate Groq as Bayan's initial LLM provider without building a large provider abstraction framework.

**Scope**

- Use the official Groq Python SDK
- Create a focused provider module
- Load the user's decrypted BYOK credential at request time
- Keep provider-specific logic isolated enough for future provider modules
- Do not create a generic multi-provider framework now

**Done when**

- The backend can make an authenticated Groq request using a user's stored BYOK credential
- Plaintext provider keys are not persisted or logged
- Provider failures are surfaced safely

**Depends on**

- P1-09

---

## P3-02 — feat: implement natural-language tool orchestration

**Goal**

Allow the Agent to select authorized tools from natural-language requests.

**Scope**

- Expose the approved semantic tool set to the Agent
- Support tool calls through the Groq interaction flow
- Let the model choose capabilities based on the user request
- Do not implement keyword routing such as `if question contains ...`
- Do not allow generic internet search

**Done when**

- Natural-language requests can trigger the appropriate available tools
- Tool selection is not implemented through fixed prompt keywords
- The Agent cannot call capabilities outside the approved POC tool set

**Depends on**

- P2-02
- P2-03
- P2-04
- P2-05
- P2-06
- P3-01

---

## P3-03 — feat: implement evidence validation

**Goal**

Create the backend enforcement layer that determines whether retrieved evidence is sufficient for an Islamic factual answer.

**Scope**

Implement the initial evidence states:

- `supported`
- `insufficient_evidence`

Keep conflicting-source handling for future scope unless required by actual POC behavior.

**Done when**

- Tool output is evaluated before an Islamic factual answer is accepted
- Supported and insufficient states are represented explicitly
- Validation logic is backend-controlled rather than only prompt-controlled

**Depends on**

- P2-01
- P3-02

---

## P3-04 — feat: enforce evidence-only Islamic answers

**Goal**

Prevent the Agent from filling Islamic factual gaps from pretrained/internal knowledge.

**Scope**

- Apply Agent instructions for Bayan's trust model
- Enforce the rule in backend answer handling
- Allow explanation only from validated retrieved evidence
- Return `لا أعلم.` or the approved equivalent when authorized evidence is insufficient
- Do not treat unsupported-domain refusal as an application failure

**Done when**

- Islamic factual answers require validated evidence
- Insufficient authorized evidence results in the defined refusal state
- The Agent cannot silently answer unsupported Islamic factual questions from internal knowledge

**Depends on**

- P3-03

---

## P3-05 — feat: define chat answer response contract

**Goal**

Create the backend response shape that keeps model explanation separate from source/tool evidence.

**Scope**

Represent:

- Agent explanation
- evidence validation status
- structured evidence
- tool/source provenance
- references
- audio result when applicable
- application-level error state when applicable

**Done when**

- The frontend can render explanation and evidence separately without parsing free-form model output
- Persistence can store the response evidence snapshot
- Audio remains a structured capability rather than model-generated UI

**Depends on**

- P3-03
- P3-04

---

## P3-06 — test: protect the core trust model

**Goal**

Add tests for the behaviors that make Bayan evidence-first.

**Scope**

Cover:

- supported evidence path
- insufficient evidence path
- unsupported Islamic factual request
- tool-selection flow
- refusal to invent missing evidence fields
- separation of explanation and evidence
- absence of hardcoded keyword routing

**Done when**

- Regression tests fail if an unsupported Islamic factual answer bypasses evidence validation
- The `لا أعلم` path is tested as a successful guardrail state

**Depends on**

- P3-02
- P3-03
- P3-04
- P3-05

### Phase 3 Exit Criteria

Phase 3 is complete when:

- Groq can orchestrate the approved tools
- Evidence sufficiency is enforced by the backend
- Islamic factual answers cannot bypass the evidence pipeline
- Unsupported requests safely produce the insufficient-evidence response

---

# Phase 4 — Core POC

Prove the complete Bayan architecture end to end before investing heavily in UI polish.

## P4-01 — feat: add chat execution API

**Goal**

Expose the complete question-to-answer pipeline through a backend chat API.

**Scope**

Connect:

```text
Authenticated User
-> Conversation
-> Agent
-> Tool Calls
-> Trusted Sources
-> Structured Evidence
-> Validation
-> Agent Explanation or Insufficient Evidence
-> Response
```

**Done when**

- An authenticated user can submit a message to a conversation
- The backend runs the complete orchestration pipeline
- The API returns the structured response contract

**Depends on**

- P1-03
- P1-10
- P3-05

---

## P4-02 — feat: persist answer evidence snapshots

**Goal**

Persist the exact evidence and references associated with assistant turns.

**Scope**

Store with relevant assistant messages:

- answer/explanation
- tool calls or diagnostic execution metadata needed by the application
- validation status
- structured evidence snapshot
- source/reference metadata

Reopening a conversation should not require re-querying upstream sources merely to reconstruct the original evidence UI.

**Done when**

- A completed assistant turn is persisted with its evidence snapshot
- Reloading the conversation restores the saved answer and evidence
- Historical evidence is not silently replaced by newly fetched upstream data

**Depends on**

- P1-10
- P4-01

---

## P4-03 — test: verify Quran and Tafsir POC flows

**Goal**

Prove the first two required POC flows end to end.

**Scope**

Verify:

1. Quran request
2. Tafsir request

Include tool selection, retrieval, validation, response, and persistence.

**Done when**

- Both flows complete end to end with source-backed evidence
- Reloading the conversation restores the saved evidence

**Depends on**

- P4-02

---

## P4-04 — test: verify Hadith and Fatwa POC flows

**Goal**

Prove the Hadith and Fatwa POC flows end to end.

**Scope**

Verify:

3. Hadith request
4. Fatwa request

Include source metadata and optional fields only when supplied by the source.

**Done when**

- Both flows complete end to end
- Source-backed grading/reference fields are preserved correctly
- No missing source information is fabricated

**Depends on**

- P4-02

---

## P4-05 — test: verify insufficient evidence and audio POC flows

**Goal**

Prove the final two required POC flows.

**Scope**

Verify:

5. Unsupported / insufficient evidence request -> `لا أعلم.`
6. Quran audio request -> structured audio result

**Done when**

- Unsupported Islamic factual requests do not receive pretrained factual answers
- Audio requests return structured playback data
- Both flows can be persisted and restored appropriately

**Depends on**

- P4-02

### Phase 4 Exit Criteria

Phase 4 is complete when all six canonical POC flows work end to end:

1. Quran
2. Tafsir
3. Hadith
4. Fatwa
5. Insufficient evidence -> `لا أعلم.`
6. Quran audio

---

# Phase 5 — Minimal Web App

Build the smallest usable web product around the proven backend POC.

## P5-01 — feat: add frontend API and server-state foundation

**Goal**

Create the frontend data-access foundation.

**Scope**

- Add TanStack Query
- Add the minimal API client layer
- Configure authenticated requests
- Use TanStack Query only for server state
- Keep purely local UI state in normal React/local state

**Done when**

- Frontend code can query and mutate backend data through a consistent boundary
- Authentication cookies work with backend requests
- Local UI state is not unnecessarily moved into TanStack Query

**Depends on**

- P0-02
- P4-01

---

## P5-02 — feat: build minimal landing page

**Goal**

Provide the initial public entry point for Bayan.

**Scope**

- Minimal Bayan positioning
- Clear start/sign-in action
- Responsive layout
- Follow the visual direction in `IDEA-FLOW.md` without heavy polish yet

**Done when**

- Logged-out users can understand what Bayan is and enter the authentication flow
- The page is usable on desktop and mobile

**Depends on**

- P0-02

---

## P5-03 — feat: build authentication UI

**Goal**

Expose the supported authentication flows in the web app.

**Scope**

- Email/password signup and login
- 6-digit verification flow
- Password reset
- Google OAuth entry
- GitHub OAuth entry
- Logout
- Route behavior:
  - logged-out `/chat` -> `/auth`
  - authenticated `/` -> `/chat`
  - authenticated `/auth` -> `/chat`
  - authenticated `/chat` remains chat

Do not add account linking or an in-app account switcher.

**Done when**

- Each supported backend auth flow is usable from the web app
- Route behavior matches the Auth Contract
- Verification is required where applicable

**Depends on**

- P1-04
- P1-05
- P1-06
- P1-07
- P1-08
- P5-01

---

## P5-04 — feat: build BYOK settings UI

**Goal**

Allow authenticated users to configure the Groq credential needed to use Bayan.

**Scope**

- Save/replace Groq API key
- Display only non-secret or masked saved-state information
- Never retrieve the stored plaintext key
- Provide clear success/error states

**Done when**

- A user can configure a Groq credential from the web app
- The browser never receives the stored plaintext credential after saving

**Depends on**

- P1-09
- P5-01
- P5-03

---

## P5-05 — feat: build minimal chat interface

**Goal**

Create the basic usable Bayan conversation experience.

**Scope**

- `/chat` layout
- Message composer
- User and assistant message rendering
- Submit messages
- Loading state
- Basic failure state
- Keep evidence rendering minimal until Phase 6

**Done when**

- An authenticated user with a configured BYOK key can send a question and receive a Bayan response
- The interface handles normal loading and failure states

**Depends on**

- P4-01
- P5-01
- P5-03
- P5-04

---

## P5-06 — feat: add conversation history UI

**Goal**

Expose persistent conversations in the web app.

**Scope**

- Conversation list
- Open an existing conversation
- Restore saved messages
- Restore saved evidence payloads for later Phase 6 rendering
- Create a new conversation

**Done when**

- A user can leave and later reopen a conversation
- Historical messages load from PostgreSQL-backed APIs
- Evidence snapshots remain attached to their original assistant messages

**Depends on**

- P1-10
- P4-02
- P5-05

---

## P5-07 — feat: complete minimal responsive app states

**Goal**

Make the minimal web experience coherent before evidence-specific UI work.

**Scope**

- Empty chat state
- Loading states
- API error states
- Missing BYOK state
- Authentication-expired state
- Basic responsive behavior
- Basic keyboard/accessibility behavior

**Done when**

- Core flows remain understandable when data is empty, loading, expired, or failed
- Main app screens are usable across common desktop and mobile sizes

**Depends on**

- P5-03
- P5-04
- P5-05
- P5-06

### Phase 5 Exit Criteria

Phase 5 is complete when a real user can:

- create/sign in to an account
- configure BYOK
- start a conversation
- ask Bayan a question
- close the app
- return later and reopen the saved conversation

---

# Phase 6 — Evidence UX

Make Bayan's trust model visible to the user through structured evidence components and source transparency.

## P6-01 — feat: add structured evidence renderer

**Goal**

Create the frontend boundary that maps backend evidence types to application components.

**Scope**

Map structured payloads conceptually as:

```text
Quran evidence -> QuranCard
Hadith evidence -> HadithCard
Fatwa evidence -> FatwaCard
Audio result -> AudioPlayer
```

The Agent must never generate component HTML.

**Done when**

- Frontend rendering is selected from typed evidence data
- Free-form model text cannot impersonate an evidence component

**Depends on**

- P3-05
- P5-05

---

## P6-02 — feat: build QuranCard

**Goal**

Render Quran and Tafsir evidence clearly and accurately.

**Scope**

Support only fields supplied by structured evidence, such as:

- surah
- ayah number
- Arabic text
- tafsir when present
- tafsir source
- source/reference actions

**Done when**

- Quran evidence is visually distinct from Agent explanation
- Missing optional evidence fields are not invented or shown as factual placeholders

**Depends on**

- P6-01

---

## P6-03 — feat: build HadithCard

**Goal**

Render Hadith evidence without fabricating grading or isnad information.

**Scope**

Support available fields such as:

- Hadith text
- narrator
- source/book
- reference
- grading when provided
- isnad information when provided
- source/reference actions

**Done when**

- Hadith source evidence is clearly separated from Agent explanation
- Grading/isnad appear only when returned by the authorized source

**Depends on**

- P6-01

---

## P6-04 — feat: build FatwaCard

**Goal**

Render Fatwa / scholar evidence from the authorized source.

**Scope**

Support available fields such as:

- question
- answer
- scholar
- source
- reference
- original source link

**Done when**

- Fatwa evidence is clearly attributable to the source
- The component never presents Agent-generated text as source evidence

**Depends on**

- P6-01

---

## P6-05 — feat: build Quran AudioPlayer

**Goal**

Render structured Quran audio results as a native application playback experience.

**Scope**

- Reciter information
- Surah
- Ayah range
- Playback controls
- Loading/error states
- Use structured audio URL/data returned by the backend

**Done when**

- A `quran_audio` result can be played from the frontend
- The Agent does not generate playback markup

**Depends on**

- P6-01

---

## P6-06 — feat: add sources and references UI

**Goal**

Give users a clear way to inspect the provenance of evidence.

**Scope**

Create a reusable source/reference view that can display:

- trusted source
- citation/reference
- original source link when available
- evidence-specific metadata

The exact UI may be a drawer, modal, panel, or another simple implementation.

**Done when**

- Every evidence component can expose its available source information
- Users can distinguish source provenance from Agent explanation

**Depends on**

- P6-02
- P6-03
- P6-04

---

## P6-07 — feat: add evidence explanation view

**Goal**

Implement the optional "Why this answer?" / evidence view without blurring the trust boundary.

**Scope**

- Show which structured evidence supported the answer
- Show validation status where useful
- Preserve the distinction between Agent explanation and source evidence
- Do not generate fake reasoning traces or expose hidden model chain-of-thought

**Done when**

- Users can inspect the evidence basis for a supported answer
- The UI does not present private model reasoning as evidence

**Depends on**

- P6-01
- P6-06

### Phase 6 Exit Criteria

Phase 6 is complete when:

- Quran, Hadith, Fatwa, and Audio have structured UI
- Sources and references are inspectable
- Agent explanation and trusted evidence are visibly distinct
- Historical conversations restore the same saved evidence presentation

---

# Phase 7 — Hardening & First Web Release

Harden the proven product for an initial public web deployment.

## P7-01 — feat: add Redis rate limiting

**Goal**

Protect authentication and chat endpoints from basic abuse.

**Scope**

Use Redis-backed rate limiting for appropriate high-risk or expensive endpoints, including relevant:

- authentication attempts
- verification flows
- reset flows
- chat/provider requests

Avoid arbitrary limits that make normal usage impractical.

**Done when**

- Selected endpoints enforce server-side limits
- Rate-limit responses are predictable
- Limits can be configured without code changes

**Depends on**

- P0-03
- P5-05

---

## P7-02 — fix: harden authentication and session edge cases

**Goal**

Review the complete Auth Contract against the implemented system before deployment.

**Scope**

Verify and fix:

- cross-method conflicts
- provider identity conflicts
- provider email changes
- verified-email requirements
- session revocation
- logout
- reset behavior
- cookie production settings
- account-enumeration-sensitive responses

**Done when**

- Automated tests cover critical Auth Contract edge cases
- Known violations of the Auth Contract are resolved

**Depends on**

- P1-04
- P1-05
- P1-06
- P1-07
- P1-08
- P5-03

---

## P7-03 — fix: harden trusted source failure handling

**Goal**

Make upstream source failures safe and understandable in production.

**Scope**

Review:

- timeouts
- connection errors
- malformed responses
- unavailable upstream source
- empty results
- retry behavior where appropriate
- distinction between source failure and insufficient evidence

Do not silently replace failed authorized sources with generic internet search.

**Done when**

- Upstream failures do not crash the chat pipeline
- Source failure cannot cause the model to answer from internal Islamic knowledge
- Errors are observable without leaking sensitive information

**Depends on**

- P2-07
- P4-01

---

## P7-04 — test: expand release-critical backend coverage

**Goal**

Strengthen tests around the behaviors that would be costly to break in production.

**Scope**

Prioritize:

- evidence guardrails
- authentication
- sessions
- BYOK encryption boundaries
- conversation ownership
- evidence persistence
- chat execution
- upstream failure behavior

**Done when**

- Release-critical backend behavior has meaningful regression coverage
- CI consistently runs the suite

**Depends on**

- P7-02
- P7-03

---

## P7-05 — chore: harden production observability

**Goal**

Prepare Sentry and logs for real production traffic without leaking secrets.

**Scope**

- Review sensitive-data scrubbing
- Verify no plaintext BYOK credentials reach logs/Sentry
- Verify passwords, verification codes, and session secrets are excluded
- Add useful request/error context that is safe to retain

**Done when**

- Production exceptions are observable
- Sensitive credential data is excluded from intended logging and Sentry capture

**Depends on**

- P0-05
- P1-09

---

## P7-06 — chore: prepare VPS deployment

**Goal**

Prepare the initial simple single-server deployment direction defined in `STACK.md`.

**Scope**

Prepare a production configuration for:

- Next.js
- FastAPI
- PostgreSQL
- Redis
- environment/secrets
- HTTPS/reverse proxy arrangement as required
- startup/restart behavior
- database migrations
- basic backup/restore considerations for durable PostgreSQL data

Do not introduce Kubernetes or a distributed microservice platform.

**Done when**

- Bayan can be deployed reproducibly to the chosen VPS
- Production secrets are not committed
- Database migrations can be applied safely
- The deployed app can reach PostgreSQL and Redis

**Depends on**

- P5-07
- P7-01
- P7-05

---

## P7-07 — chore: run web quality pass

**Goal**

Resolve major usability, accessibility, and performance issues before the first public web release.

**Scope**

Review:

- keyboard usability
- basic screen-reader semantics
- responsive behavior
- obvious layout failures
- major loading/performance issues
- error recovery
- evidence readability

Avoid redesigning the product solely for polish.

**Done when**

- No known blocker prevents normal use of the core web flows
- Major accessibility or responsive defects found in the pass are resolved

**Depends on**

- P6-07

---

## P7-08 — ci: enforce required status checks

**Goal**

Turn the stable GitHub Actions checks into required repository rules.

**Scope**

Update the existing `Protect main and develop` ruleset to require the stable CI checks before merge.

Keep:

- normal Merge commits only
- no Squash merge
- no Rebase merge

**Done when**

- Pull Requests into `main` and `develop` cannot merge while required checks fail
- The required checks correspond to real, stable workflows

**Depends on**

- P0-04
- P7-04

### Phase 7 Exit Criteria

Phase 7 is complete when:

- Core security and failure paths are hardened
- Release-critical CI is enforced
- Production observability is configured
- The web app can be deployed reproducibly to the initial VPS target
- No known blocker prevents the six core POC flows from being used through the web app

Only after these criteria are met should the maintainers decide whether `develop` is ready for the project's first `release/*` branch.

---

# Future — Outside the Initial Roadmap

The following remain intentionally outside the initial implementation roadmap unless a later approved Discussion and Issue changes scope:

- Desktop application
- Additional LLM providers
- Additional Islamic knowledge domains
- Seerah
- Islamic history
- Aqeedah
- Rijal / narrator biographies
- Islamic books
- Hajj and Umrah
- Adhkar and Dua
- Quranic Arabic / Gharib al-Quran
- Hadith sciences
- Usul al-Fiqh
- Madhhab-specific Fiqh
- Controlled internet search
- advanced conflicting-source handling
- account linking
- multi-account switcher
- vector database
- embeddings
- large local Islamic knowledge database
- large ingestion pipeline
- microservices
- Kubernetes

Future work must continue to preserve the core Bayan principle:

```text
LLM / Agent
= Understanding + Orchestration + Explanation

MCP / Tools
= Retrieval

Trusted Sources
= Authority / Evidence

Backend
= Validation + Enforcement + Persistence

Frontend
= Transparent Presentation
```
