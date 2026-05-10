# Agents manifest for this repository

Purpose
-------
This file documents the assistant/agent roles and how to use them for tasks in this repository. It is intended to be a lightweight agents manifest for maintainers and automation.

Relationship with `copilot-instructions.md`
-------------------------------------------
`copilot-instructions.md` contains the operational guidance for Copilot when editing the codebase. `AGENTS.md` is a focused manifest describing available agent responsibilities, invocation examples, and when to call each agent. Keep both files in sync when updating agent behavior or responsibilities.

Available agents / roles
------------------------
- **Copilot assistant**: primary coding assistant used for implementing features, tests, and migrations. Follows guidance in `copilot-instructions.md`.
- **modernize-java**: specialized agent (if used) for upgrading Java projects — not typically used in this repository but included for completeness.
- **Explore**: read-only exploration agent for fast codebase scans and Q&A.

When to use which agent
-----------------------
- Use the **Copilot assistant** for most development tasks: adding endpoints, models, migrations, tests, and frontend type updates.
- Use **Explore** when you need a quick codebase analysis or to gather references before implementing a feature.
- Use **modernize-java** only for Java-specific upgrade tasks; not applicable to the Python/Angular stack here unless a Java component is added.

Invocation and examples
-----------------------
- Request the Copilot assistant to implement a UC by referencing the UC file path (for example, `docs/UC004.md`) and specifying end-to-end vs backend-only.
- Ask the Explore agent: "Explore the codepaths supporting UC001 and list missing endpoints".

Agent responsibilities and constraints
------------------------------------
- Agents must not make assumptions that contradict `docs/` without raising a TODO or creating an issue.
- Database schema changes require an Alembic migration and tests demonstrating the change.
- Frontend API contract changes must be coordinated: update frontend types and add a short migration/compatibility note in PRs.

Keeping agents in sync
----------------------
- Update `copilot-instructions.md` when agents' behavior or repository conventions change.
- Use this manifest to record new agents or to retire ones no longer relevant.

Next steps (suggested)
----------------------
- If you want this manifest expanded into a GitHub Actions workflow or to register agents with tooling, tell me which agent(s) to wire and I will create the necessary files.
