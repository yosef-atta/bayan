# Contributing to Bayan

Thanks for your interest in contributing to Bayan.

Keep contributions focused, discuss significant changes before implementation, and follow the repository workflow below.

## 1. Before You Start

Read these files before making product, architecture, or dependency decisions:

1. `IDEA-FLOW.md`
2. `STACK.md`
3. `TASKS.md` when available
4. Implementation

If a lower-level implementation conflicts with a higher-level document, the higher-level document wins.

Major product, architecture, authentication, stack, dependency, or infrastructure changes must be discussed before implementation.

## 2. Communication

Use GitHub as the canonical place for project collaboration.

### Issues

Use Issues for concrete, actionable work:

- confirmed bugs
- reproducible problems
- approved features or improvements
- specific implementation tasks

For an existing actionable Issue, leave a comment before starting work.

Small bugs or small fixes may be submitted directly as a Pull Request.

### Discussions

Use Discussions for:

- ideas
- questions
- proposals
- architecture or product discussion
- contribution questions

New features and significant architecture or product changes should follow:

```text
Discussion
-> Approved Issue
-> Implementation
-> Pull Request
```

### Pull Requests

Use Pull Requests for actual implementation or documentation changes.

## 3. Git Flow

Bayan follows the original Git Flow model.

### `main`

Stable production branch.

Official releases are merged here.

### `develop`

Integration and staging branch.

Completed features are merged here before release preparation.

### `feature/*`

- Create from `develop`
- Merge back into `develop`
- Contributors and maintainers may work on feature branches

Example:

```text
feature/quran-search
```

### `release/*`

- Create from `develop`
- Used for final release preparation and testing
- Merge into both `main` and `develop`
- Maintainers only

Example:

```text
release/1.0.0
```

### `hotfix/*`

- Create from `main`
- Used for urgent production fixes
- Merge into both `main` and `develop`
- Contributors and maintainers may work on hotfix branches

Example:

```text
hotfix/session-expiry
```

Contributors with repository write access may create branches in the Bayan repository.

External contributors without write access should fork the repository, create their branch in the fork, and open a Pull Request.

## 4. Repository Rulesets & Merge Policy

The protected branches are:

- `main`
- `develop`

The repository ruleset is:

```text
Protect main and develop
```

It enforces:

- branch deletion protection
- force-push protection
- Pull Requests before merging
- required approvals: 0 initially
- conversation resolution before merging
- Merge commits as the only allowed merge method

### Merge Policy

Bayan uses **normal Merge commits only**.

- Merge: allowed
- Squash merge: not allowed
- Rebase merge: not allowed

This is intentional and preserves Git Flow branch history.

Required CI status checks will be enforced through the same ruleset when the workflows are available.

Only maintainers merge Pull Requests.

## 5. Pull Requests

Keep each Pull Request focused on one change.

When applicable:

- reference the related Issue
- use `Closes #<issue-number>` when the PR should close it
- ensure all applicable CI checks pass
- resolve review conversations before merge

Contributors should not merge their own Pull Requests.

## 6. Security & Project Boundaries

Never commit:

- `.env`
- API keys
- OAuth secrets
- database credentials
- Fernet master keys
- real user secrets or credentials

Never log plaintext BYOK credentials.

Do not change core product principles, `STACK.md` decisions, the authentication contract, or introduce major dependencies or infrastructure without prior discussion and approval.

Security reporting and vulnerability-handling policy will be documented separately in `SECURITY.md`.
