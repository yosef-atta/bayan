# Bayan Stack

## Purpose

This file defines the agreed technology stack and technical boundaries for the Bayan POC and its first web implementation.

The project documentation has the following authority order:

1. IDEA-FLOW.md — defines what Bayan is, why it exists, its product principles, trust model, and POC boundaries.
2. STACK.md — defines the technologies and technical conventions used to implement that product direction.
3. TASKS.md — will define implementation order and completion criteria.
4. Code — implements the decisions above.

If STACK.md conflicts with IDEA-FLOW.md, IDEA-FLOW.md wins.

This document is a technology contract, not a full architecture specification. It should not be expanded with infrastructure, abstractions, or services merely because they may become useful someday.

---

## 1. Stack at a Glance

### Backend

- Python
- FastAPI
- uv
- Pydantic
- pydantic-settings
- httpx with async usage

### Agent / LLM

- Groq for the initial implementation
- Official Groq Python SDK
- Tool calling through the Agent
- No generic multi-provider framework in the POC

### MCP

- Python
- MCP belongs to the backend
- No top-level mcp/ application or repository
- backend/app/mcp/ may be used when MCP-specific organization is needed

### Database

- PostgreSQL
- SQLAlchemy Async
- psycopg v3 async driver
- Alembic migrations

### Ephemeral State

- Redis
- Official redis Python package with asyncio support

### Authentication

- Self-hosted in FastAPI
- Email + Password
- Google OAuth/OIDC
- GitHub OAuth
- Authlib
- pwdlib
- Argon2 password hashing
- Server-side sessions
- HttpOnly + Secure + SameSite cookies
- Resend for transactional email
- 6-digit email verification codes

### BYOK Credential Security

- Server-side storage only
- PostgreSQL for persistent encrypted credentials
- cryptography
- Fernet symmetric encryption
- Master encryption key stored outside PostgreSQL

### Frontend

- Next.js
- TypeScript
- pnpm
- App Router
- src/ directory
- Turbopack
- Tailwind CSS
- ESLint
- @/* import alias
- TanStack Query for server state

### Testing / Quality

Backend:

- pytest
- pytest-asyncio
- Ruff
- Pyright

Frontend:

- ESLint
- TypeScript strict mode
- Frontend tests when a testing framework is introduced

### Observability

- Sentry for backend and frontend error tracking
- Normal application logging in addition to Sentry

### CI

- GitHub Actions
- Run checks on pushes and pull requests

### Local Development

Docker Compose runs:

- PostgreSQL
- Redis

Run directly on the development machine:

- FastAPI via uv
- Next.js via pnpm

### Initial Production Direction

- VPS
- Single-server deployment direction
- Keep infrastructure simple and cost-conscious

---

## 2. Repository Layout

Bayan uses two top-level application directories:

~~~text
bayan/
├── backend/
├── frontend/
├── IDEA-FLOW.md
├── STACK.md
└── ...
~~~

MCP is considered part of the backend.

Do not create a top-level mcp/ application.

The backend starts with the following organizational direction:

~~~text
backend/
└── app/
    ├── api/
    ├── agent/
    ├── providers/
    ├── mcp/
    ├── tools/
    ├── schemas/
    ├── services/
    └── core/
~~~

These directories exist to make a public repository understandable to contributors.

They must not become an excuse to introduce unnecessary architectural layers. Add internal modules only when they have a real responsibility.

---

## 3. Backend

### Language

Python is the backend language.

### Framework

FastAPI is the backend web framework.

### Package Management

Use uv for:

- dependency management
- virtual environment workflow
- running backend commands
- dependency locking

Do not introduce a second Python package manager without a concrete need.

### Data Validation

Use Pydantic for:

- API request and response validation
- structured tool results
- evidence models
- audio result models
- validation states
- other typed application boundaries

FastAPI and Pydantic should remain the primary API/schema boundary.

### Configuration

Use pydantic-settings for backend configuration.

Local development uses:

~~~text
.env
.env.example
~~~

.env must not be committed.

.env.example should document required variable names without containing secrets.

---

## 4. Async-First Backend I/O

The backend is async-first for I/O-bound operations.

This includes:

- PostgreSQL access
- Redis operations
- HTTP calls to trusted external sources
- OAuth network operations
- Groq/provider calls
- MCP/tool integrations when the underlying operation is asynchronous

Use httpx for async HTTP requests.

Do not use synchronous HTTP clients inside async request paths without a specific reason.

---

## 5. Agent and LLM Provider

### Initial Provider

The initial LLM provider is Groq.

Use the official Groq Python SDK directly.

The POC does not need a large provider abstraction framework.

A simple provider organization is acceptable:

~~~text
backend/app/providers/
└── groq.py
~~~

If Bayan later supports another provider, it can receive its own focused integration module, for example:

~~~text
providers/
├── groq.py
├── openai.py
└── ...
~~~

This future possibility does not justify building factories, adapter hierarchies, provider registries, or a generic multi-provider platform during the POC.

### Agent Boundary

The Agent is responsible for:

- understanding natural-language requests
- selecting authorized tools
- orchestrating tool use
- explaining supported evidence

The Agent is not the source of Islamic evidence.

The provenance rules defined in IDEA-FLOW.md remain mandatory.

---

## 6. MCP and Tools

MCP is implemented in Python and belongs inside the backend.

Possible organization:

~~~text
backend/app/
├── mcp/
└── tools/
~~~

The exact internal split should follow actual implementation needs.

The POC should keep the tool layer small and semantic.

Initial capability direction remains aligned with IDEA-FLOW.md:

~~~text
quran_search
quran_get_ayah
quran_get_tafsir
hadith_search
fatwa_search
quran_audio
~~~

Do not add a generic routing system, giant adapter framework, or dozens of MCP servers.

Do not hardcode natural-language routing with keyword checks.

---

## 7. PostgreSQL

PostgreSQL is the persistent application database from the beginning.

It is used for durable Bayan application data such as:

- users
- authentication identity metadata
- encrypted BYOK credentials
- conversations
- messages
- structured evidence snapshots
- persistent account data
- future persistent settings or subscription data when those features exist

### Important Knowledge Boundary

PostgreSQL is not a canonical Islamic knowledge database.

Do not ingest the Quran, Hadith corpus, Fatwa corpus, or other large Islamic knowledge collections into PostgreSQL as a replacement for Bayan's trusted external-source architecture.

Islamic knowledge retrieval remains source/tool based as defined by IDEA-FLOW.md.

---

## 8. SQLAlchemy and Database Access

Use:

- SQLAlchemy
- AsyncSession
- psycopg v3 async mode

Database access should be asynchronous.

Do not maintain parallel sync and async database layers unless a concrete implementation need appears.

---

## 9. Database Migrations

Use Alembic for PostgreSQL schema migrations.

All schema changes must be represented by migrations rather than undocumented manual database changes.

This is particularly important because Bayan is a public repository and contributors must be able to reproduce the application schema.

---

## 10. Redis

Redis is included from day one for short-lived, ephemeral application state.

Use the official redis Python package with asyncio support.

Initial Redis responsibilities include:

- server-side sessions
- email verification codes
- OAuth state/nonces
- rate limiting
- other short-lived state when genuinely needed

Redis must not become:

- the canonical user database
- the BYOK credential store
- the conversation history database
- an Islamic knowledge database

Persistent application state belongs in PostgreSQL.

Ephemeral state belongs in Redis where appropriate.

---

## 11. Authentication Model

Authentication is self-hosted in the FastAPI backend.

Supported authentication methods:

1. Email + Password
2. Google
3. GitHub

Use Authlib for Google and GitHub OAuth/OIDC flows.

Do not manually reimplement OAuth protocol plumbing with raw HTTP requests unless a provider limitation requires it.

Bayan owns its users and sessions. Google and GitHub authenticate external identity; they do not become Bayan's session system.

---

## 12. Auth Contract

The initial authentication model intentionally avoids account-linking complexity.

### Core Rules

#### Rule 1 — One normalized verified email equals one Bayan account

A verified email must map to at most one Bayan account.

The application must normalize email input consistently before uniqueness checks.

Do not allow casing or surrounding whitespace to create duplicate accounts.

#### Rule 2 — One Bayan account has one authentication method initially

An account is initially one of:

~~~text
password
google
github
~~~

A Bayan account does not simultaneously use multiple auth methods in the initial product.

#### Rule 3 — OAuth identity uses the provider's stable user identifier

For OAuth accounts, identity must preserve:

- provider
- stable provider user ID
- verified email

Do not identify returning OAuth users solely by matching an email string on every login.

#### Rule 4 — No account linking initially

Do not implement:

- automatic Google ↔ GitHub linking
- automatic OAuth ↔ Password linking
- manual connected-account management
- adding a second auth method to an existing account

Account linking may become a future feature only if real product need justifies the additional security and UX complexity.

#### Rule 5 — No account switcher initially

Bayan does not keep multiple active identities in an in-app account selector.

To use another Bayan account:

~~~text
Logout
→ Login with the other account
~~~

---

## 13. Auth Route Behavior

### Logged-Out User

~~~text
/
→ Landing

Landing
→ Start
→ /auth

/chat
→ redirect to /auth
~~~

### Authenticated User

~~~text
/
→ redirect to /chat

/auth
→ redirect to /chat

/chat
→ Chat
~~~

The landing page is primarily for visitors.

The chat is the primary application destination for authenticated users.

---

## 14. Email + Password Authentication

### Password Storage

Use:

- pwdlib
- Argon2

Never store plaintext passwords.

### Signup

Conceptual flow:

~~~text
Email + Password Signup
→ create unverified account
→ generate 6-digit verification code
→ send code through Resend
→ user submits code
→ backend verifies code
→ mark email/account verified
→ user enters authenticated application flow
→ /chat
~~~

The exact expiry, resend cooldown, and maximum-attempt values should be defined during implementation, but they must be finite and security-conscious.

Verification codes must:

- be short-lived
- be one-time use
- have limited verification attempts
- have resend throttling

Redis is the initial storage location for short-lived verification state.

### Password Login

A correct password for a verified password account allows login.

Incorrect credentials should return a generic authentication failure rather than exposing sensitive account details.

---

## 15. Google and GitHub Authentication

Use Authlib for provider flows.

### Creating an OAuth Bayan Account

Bayan should create an OAuth-backed account only when it receives the identity information required by the Auth Contract, including a verified email.

If a provider cannot supply a verified email, do not create the Bayan account.

### Returning OAuth User

The provider's stable user ID is the primary OAuth identity binding.

The verified email remains important for Bayan account uniqueness.

### Provider Email Changes

If the same stored provider identity later returns a different verified email:

- it is still the same provider identity
- do not create a duplicate Bayan user
- do not silently overwrite an email that conflicts with another Bayan account
- a conflicting email requires explicit resolution rather than automatic merging

---

## 16. Cross-Method Auth Edge Cases

The following behavior is part of the initial Auth Contract.

### Existing Google account, then Password signup with same email

Do not:

- create another Bayan account
- add a password to the Google account
- link authentication methods automatically

Reject the signup and direct the user toward the existing sign-in method without exposing unnecessary account information.

### Existing GitHub account, then Password signup with same email

Same behavior as above.

### Existing Password account, then Google/GitHub login with same email

Do not automatically link the OAuth identity to the password account.

Do not create a duplicate account.

Reject the conflicting auth method.

### Existing Google account, then GitHub login with same verified email

Do not automatically link Google and GitHub.

Reject the conflicting auth method.

### Existing GitHub account, then Google login with same verified email

Same behavior.

### OAuth provider ID differs but email matches an existing account

Do not treat the incoming identity as the existing account solely because the email matches.

Reject the identity conflict rather than silently reassigning ownership.

### Same person uses different verified emails across providers

Bayan does not attempt to infer that two different provider identities belong to the same human.

Different verified emails may therefore result in different Bayan accounts.

---

## 17. Password Reset Contract

Password reset applies to Password accounts.

Conceptual flow:

~~~text
Forgot Password
→ request reset
→ send reset communication
→ verify reset authorization
→ choose new password
→ invalidate/reset security state as appropriate
~~~

For OAuth-only accounts:

- do not create a password through the forgot-password flow
- do not silently convert the account to Password authentication

Public reset responses should be generic enough to avoid unnecessary account enumeration.

---

## 18. Server-Side Sessions

Bayan uses server-side sessions.

The browser receives an opaque session identifier through a cookie.

Cookie requirements:

- HttpOnly
- Secure in production
- SameSite configured appropriately for the application flow

Session state is stored in Redis.

Conceptually:

~~~text
Browser
→ opaque session cookie
→ FastAPI
→ Redis session state
→ Bayan user identity
~~~

Logout invalidates the server-side session.

The application should be able to revoke sessions without waiting for a client token to expire.

Do not store BYOK keys or other long-lived secrets inside session state.

---

## 19. Transactional Email

Use Resend for transactional email.

Initial use cases:

- email verification
- password reset
- account/security email flows when required

Resend is the delivery provider.

Bayan remains responsible for generating and validating verification/reset state.

The current email verification UX uses a 6-digit code.

Do not couple authentication logic directly to Resend-specific concepts where a small email service boundary is sufficient.

---

## 20. BYOK Credential Storage

Bayan uses a BYOK model for LLM provider credentials.

Browser storage is not the canonical storage location for provider API keys.

Persist BYOK credentials server-side.

### Encryption

Use:

- cryptography
- Fernet

Flow:

~~~text
User API Key
→ FastAPI
→ encrypt with Fernet
→ store ciphertext in PostgreSQL
~~~

When required for a provider request:

~~~text
encrypted credential
→ decrypt inside backend
→ use for provider request
~~~

### Master Encryption Key

The master encryption key must:

- remain outside PostgreSQL
- be provided through secure server configuration/secrets
- never be committed to the repository

### Browser Exposure

After a credential has been saved, Bayan must not send the stored plaintext API key back to the browser.

The UI may show non-secret metadata or a masked state, but the original stored secret should not be retrievable through normal frontend APIs.

### Scope

The POC starts with Groq.

Future providers can use the same high-level secure-storage principle without requiring a generic provider framework now.

---

## 21. Chat Persistence

Chat history is persistent from day one.

Use PostgreSQL for:

- conversations
- individual messages
- ownership by authenticated user
- structured evidence snapshots associated with relevant assistant turns
- source/reference metadata required to restore the evidence shown at answer time

Chat history should survive:

- page refresh
- logout
- later login

### Evidence Snapshot Principle

Do not persist only user text and assistant text.

Bayan's product philosophy depends on structured evidence.

When an answer uses Quran/Hadith/Fatwa evidence, the stored conversation should preserve the evidence snapshot shown with that answer.

This allows reopening a historical conversation without re-querying upstream sources merely to reconstruct the original UI.

It also preserves the context needed to investigate answer-quality problems later.

### Diagnostic Value

Persisted conversation/evidence data can help identify whether an issue came from:

- tool selection
- source retrieval
- evidence returned
- evidence validation
- Agent explanation

Do not automatically treat stored user conversations as model-training data.

Any future training, analytics, retention, or privacy policy requires its own explicit product decision.

---

## 22. Frontend

Use Next.js with TypeScript.

The agreed bootstrap command is:

~~~powershell
pnpm create next-app frontend --typescript --eslint --tailwind --app --src-dir --turbopack --import-alias "@/*" --use-pnpm --yes
~~~

This establishes:

- Next.js
- TypeScript
- pnpm
- ESLint
- Tailwind CSS
- App Router
- src/ directory
- Turbopack
- @/* import alias

### TypeScript

Use TypeScript strict mode.

Do not weaken type safety globally merely to bypass implementation errors.

---

## 23. Frontend State

Use TanStack Query for server state.

Examples include:

- conversation lists
- conversation messages
- profile/account data
- provider/BYOK settings metadata
- server mutations
- refetching and cache invalidation

Use normal React/local state mechanisms for local UI state such as:

- input state
- modal state
- disclosure state
- purely local interaction state

Do not use TanStack Query as a replacement for every form of frontend state.

---

## 24. Frontend Evidence Boundary

The frontend owns presentation.

Structured evidence returned through the tool/backend pipeline maps to application components such as:

~~~text
Quran evidence
→ QuranCard

Hadith evidence
→ HadithCard

Fatwa evidence
→ FatwaCard

Audio result
→ AudioPlayer
~~~

Do not ask the LLM to generate HTML or fabricate the contents of evidence cards.

Agent explanation and source/tool evidence must remain visibly and structurally distinct as required by IDEA-FLOW.md.

---

## 25. Local Development

### Docker Compose

Docker Compose is used for local infrastructure services:

~~~text
PostgreSQL
Redis
~~~

### FastAPI

Run FastAPI locally using uv during development.

### Next.js

Run Next.js locally using pnpm during development.

### Development Principle

Do not require developers to run the frontend and backend inside Docker containers merely because PostgreSQL and Redis use Docker Compose.

This keeps local hot reload, debugging, and contributor workflows straightforward.

---

## 26. Desktop Boundary

The current Docker decision does not define the future Desktop packaging model.

A future Bayan Desktop application should be distributable as a normal desktop application and must not require end users to install Docker merely to run Bayan.

The Desktop framework has not been selected in this stack.

Desktop-specific implementation remains future scope as defined by IDEA-FLOW.md.

---

## 27. Testing

### Backend

Use:

- pytest
- pytest-asyncio

Testing should cover the behaviors that protect Bayan's core trust model, including:

- tool behavior
- evidence validation
- unsupported/insufficient-evidence behavior
- authentication contracts
- persistence boundaries
- critical API behavior

### Frontend

The exact frontend test framework is not yet selected.

Do not add one merely to make the stack look complete.

When frontend tests are introduced, GitHub Actions should run them.

---

## 28. Code Quality

### Backend

Use:

- Ruff
- Pyright

### Frontend

Use:

- ESLint
- TypeScript strict mode

The goal is a clean public repository with predictable contributor feedback, not a large collection of overlapping linting tools.

---

## 29. Observability and Logging

Use Sentry from day one for:

- FastAPI/backend error tracking
- Next.js/frontend error tracking
- production stack traces and issue visibility

Also maintain normal application logging.

Sentry does not replace logs.

Do not log:

- plaintext passwords
- plaintext BYOK API keys
- session secrets
- verification codes
- other sensitive credentials

---

## 30. CI

Use GitHub Actions.

CI runs on:

- pushes
- pull requests

### Backend CI

Run:

- Ruff
- Pyright
- pytest

### Frontend CI

Run:

- ESLint
- TypeScript checks
- frontend tests when they exist

Keep CI as a release/contribution quality gate.

Do not turn the initial workflow into a large deployment or enterprise CI platform.

---

## 31. Deployment Direction

The initial production direction is a VPS / single-server deployment.

The target is:

- simple
- understandable
- cost-conscious
- under direct project control

The production environment will need to host the web/backend stack and its required services, including:

- Next.js
- FastAPI
- PostgreSQL
- Redis

The exact production process manager/container arrangement is not fixed by this document yet.

Do not assume managed split deployment such as separate frontend, backend, database, and Redis SaaS products unless a later decision changes the deployment direction.

---

## 32. Security Boundaries

The following are non-negotiable stack-level rules:

- Passwords are hashed with Argon2 and never stored plaintext.
- BYOK API keys are encrypted before database persistence.
- The Fernet master key is stored outside the database.
- Stored plaintext BYOK keys are not returned to the frontend.
- Sessions are server-side.
- Session cookies are HttpOnly and Secure in production.
- OAuth accounts require the identity information defined by the Auth Contract.
- No automatic account linking.
- Verification codes are short-lived and one-time use.
- Sensitive values must not appear in logs or Sentry payloads.
- Islamic factual answers remain subject to the evidence rules in IDEA-FLOW.md.

---

## 33. Explicitly Not in the Initial Stack

The following are intentionally not part of the current POC stack:

- Vector database
- Embedding provider
- Large local Islamic knowledge database
- Large knowledge ingestion pipeline
- Generic Internet Search provider
- Web crawler
- Generic source-ranking engine
- Microservices architecture
- Message/event bus
- Kubernetes
- Large provider abstraction framework
- Mandatory desktop runtime/framework
- Account linking
- Multi-account switcher
- Multiple simultaneous authentication methods per account
- External KMS/Vault requirement for the initial deployment

Some of these may become useful in the future.

Future usefulness alone is not enough reason to add them now.

---

## 34. Version and Dependency Policy

Exact library/runtime versions are not permanently defined by this product document.

When the project is bootstrapped:

- use stable versions compatible with the chosen stack
- pin/lock actual project dependencies
- keep the lockfiles in the repository
- avoid unnecessary major-version churn during the POC
- document compatibility constraints when a specific version is required

Do not update major dependencies merely because a newer major version exists.

---

## 35. Stack Decision Summary

~~~text
Frontend
Next.js + TypeScript + pnpm
App Router + src/ + Turbopack
Tailwind CSS + ESLint
TanStack Query

            ↓ HTTP

Backend
Python + FastAPI + uv
Pydantic + pydantic-settings
httpx async

            ↓

Agent
Groq SDK
Natural-language tool calling

            ↓

MCP / Tools
Python
Inside backend

            ↓

Trusted External Sources
Quran / Tafsir
Hadith
Fatwa
Quran Audio


Persistent Application Data
PostgreSQL
SQLAlchemy Async
psycopg v3 async
Alembic

Ephemeral State
Redis
async redis client

Authentication
Email/Password
Google
GitHub
Authlib
pwdlib + Argon2
Server-side Redis sessions
Resend + 6-digit verification

BYOK
PostgreSQL encrypted storage
cryptography + Fernet

Observability
Sentry + application logs

Local Infrastructure
Docker Compose
PostgreSQL + Redis

CI
GitHub Actions

Initial Deployment
VPS / single-server direction
~~~

---

## 36. Final Stack Principle

The stack exists to support Bayan's product model, not to redefine it.

Every technical choice should preserve the separation established in IDEA-FLOW.md:

~~~text
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
Validation + Enforcement + Persistence

Frontend
=
Transparent Presentation
~~~

When choosing between additional complexity and the smallest implementation that correctly preserves Bayan's trust model, prefer the smaller implementation until a real requirement proves otherwise.
