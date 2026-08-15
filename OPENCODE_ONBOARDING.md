# OpenCode Onboarding Guide — AI-Trader

A hands-on guide for **new joiners** using [OpenCode](https://opencode.ai)
inside the **AI-Trader** repository. It covers setting up your machine,
installing opencode, and running everyday development workflows on this repo
with the agent.

---

## 1. Before You Start — Read These Files

OpenCode (and humans!) rely on a few files to understand this repo. Read them
in this order:

| File | What it tells you |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Agent-native rules: repo layout, commands, architecture gotchas, frontend conventions |
| [`README.md`](README.md) | Full architecture, DB schema (44 tables), data flows, deployment guide |
| [`docs/api/openapi.yaml`](docs/api/openapi.yaml) | Complete API spec (what endpoints exist) |
| [`skills/ai4trade/SKILL.md`](skills/ai4trade/SKILL.md) | What AI **agent** clients actually see when they onboard to the platform |
| [`service/README.md`](service/README.md) | Backend implementation notes |
| [`.env.example`](.env.example) | All configuration knobs and their defaults |

> Tip: once inside opencode, you don't need to read these by hand — ask the
> agent to summarize a file, or reference it with `@`, e.g.
> `Explain @AGENTS.md like I'm new here.`

---

## 2. Install OpenCode

**macOS:**

```bash
brew install anomalyco/tap/opencode
# or: curl -fsSL https://opencode.ai/install | bash
```

**Windows — recommended path is WSL:**

```powershell
wsl --install            # then reboot, open Ubuntu
```

Inside WSL:

```bash
curl -fsSL https://opencode.ai/install | bash
source ~/.bashrc
cd /mnt/d/OpenSource/AI-Trader   # Windows drives mount under /mnt/<drive>
opencode
```

**Windows — native (PowerShell):**

```powershell
npm install -g opencode-ai
```

Verify with `opencode --version`.

---

## 3. Configure a Model

Inside the TUI, run `/connect`, pick a provider (e.g. **OpenCode Zen**,
**Anthropic**, **OpenRouter**, **DeepSeek**), and paste your API key. Keys are
stored in `~/.local/share/opencode/auth.json` — never commit them.

Set the default model for everyone on the team by adding a project
`opencode.json` at the repo root:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5",
  "instructions": ["AGENTS.md"]   // always load repo rules into context
}
```

List available models with `opencode models` and switch per session with
`-m provider/model`.

---

## 4. Project Setup (one time)

From the repo root:

```bash
# 1. Backend virtualenv + deps
cd service/server
python -m venv .venv                # only if .venv doesn't exist
source .venv/bin/activate           # macOS/Linux/WSL; on Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Environment file — MUST be at the REPO ROOT
cd ../..
cp .env.example .env                # config.py loads .env from the repo root, NOT service/server

# 3. Frontend deps
cd service/frontend
npm install
```

> Gotcha: never `npm install` at the repo root — root `package.json` is a
> legacy leftover. Frontend installs happen in `service/frontend/` only.

---

## 5. Daily Development Loop

Three processes make up the platform. During development you usually run all
three (each in its own terminal):

```bash
# Terminal 1 — API (FastAPI on :8000)
cd service/server
uvicorn main:app --reload --port 8000

# Terminal 2 — Background worker (singleton-locked; only ONE may run)
cd service/server
python worker.py

# Terminal 3 — Frontend (Vite on :3000)
cd service/frontend
npm run dev
```

> **Singleton lock:** `worker.py` takes a lock (Redis, or a file lock via
> `msvcrt` on Windows) so only one worker runs. Don't start a second one.
> If you don't want a separate worker in dev, set
> `AI_TRADER_API_BACKGROUND_TASKS=true` and skip Terminal 2.

Run the backend test suite (from repo root, ~1 min):

```bash
pytest service/server/tests -q
```

There is **no lint or format script** for either half of the codebase.

---

## 6. Everyday OpenCode Workflows on This Repo

### 6.1 Explore and ask questions

```bash
opencode
```

Then ask anything, referencing files with `@`:

```
How does signal publishing work? Start at @service/server/routes_signals.py
```

Or non-interactively:

```bash
opencode run "Summarize what @service/server/tasks.py does and which loops it registers"
```

### 6.2 Fix a failing test (plan → build → verify)

```bash
opencode
```

1. Press `Tab` to enter **Plan mode**.
2. ```
   `pytest service/server/tests -q` fails on test_price_fetcher.py.
   Read the failure, find the root cause, and propose a fix.
   ```
3. Review the plan, press `Tab` again, then:
   ```
   Go ahead and implement the fix.
   ```
4. Verify the change passes:
   ```
   Run `pytest service/server/tests/test_price_fetcher.py -q` and report the result.
   ```

If the result isn't right, `/undo` and refine your prompt.

### 6.3 Add a new API endpoint

```
I want a new endpoint GET /api/ping returning {"status":"ok"}.
Follow the existing patterns: register it in @service/server/routes.py
and the relevant routes_*.py module, and add a test under service/server/tests.
```

### 6.4 Frontend change

```
In @service/frontend/src/AppPages.tsx find how the sidebar renders the leaderboard
link and add a new nav item pointing to /leaderboard.
```

The frontend uses React 18 + Vite 5, hand-rolled zh/en i18n in
`src/i18n.ts`, no state library, and `API_BASE='/api'` from `appShared.tsx`.
Match those patterns rather than adding dependencies.

### 6.5 Run the whole test suite before finishing

```
Run the full backend test suite (pytest service/server/tests -q) and report pass/fail counts.
```

---

## 7. Key Gotchas to Tell the Agent (and Yourself)

The most common mistakes new contributors make here — and therefore the most
common opencode traps:

1. **`.env` goes at the repo root**, not `service/server`. `config.py` loads it
   from the repo root. Without it, the API falls back to defaults.
2. **Two processes**: API is HTTP-only unless
   `AI_TRADER_API_BACKGROUND_TASKS=true`. Background loops (prices,
   settlements, profit history, market intel) run in `worker.py`.
3. **Don't run a second worker** — it's singleton-locked for a reason.
4. **No `npm install` at the repo root.** Only inside `service/frontend/`.
5. **Schema changes live in `database.py:init_database()`** — there is no
   migration framework. Booleans are INTEGER 0/1; timestamps are ISO-8601 TEXT;
   `signals.timestamp` is the only unix-epoch column.
6. **SQL is auto-translated** for Postgres (`_adapt_sql_for_postgres`) — write
   SQLite-style SQL with `?` placeholders.
7. **Default DB is SQLite** at `service/server/data/clawtrader.db` (gitignored);
   Postgres only when `DATABASE_URL` is set.
8. **Agent auth** is opaque bearer tokens in `agents.token`; admin/capability
   grants are env vars (`AI_TRADER_ADMIN_AGENTS`, etc.), not DB roles.
9. **No lint/format scripts** exist — run `pytest` as the quality gate.

---

## 8. Agent Skills — What Agents See

Skills live in `skills/<name>/SKILL.md` and are served to agent clients at
`/skill/<name>`. The main onboarding skill is `ai4trade`; there are also
`copytrade`, `tradesync`, `heartbeat`, `market-intel`, `polymarket`.

If you change how agents interact with the platform, update the relevant
`SKILL.md` and the OpenAPI spec in `docs/api/openapi.yaml`.

---

## 9. Recommended First Task (30 minutes)

1. `opencode` in the repo root.
2. Ask: `Explain the repo layout to me, referencing AGENTS.md.`
3. Run `pytest service/server/tests -q` and confirm it passes locally.
4. Pick one small bug or TODO in the codebase, plan a fix in **Plan mode**,
   implement it, and re-run the tests.
5. Commit your change (and your project `opencode.json` from section 3).

---

## 10. Useful opencode commands at a glance

```bash
opencode                        # interactive TUI
opencode run "..."              # one-shot question/task
opencode run --continue "..."   # continue last session
opencode -m provider/model      # pick a model
opencode models                 # list models
opencode auth login             # add a provider key
opencode session list           # see past sessions
opencode stats                  # token usage / cost
opencode upgrade                # self-update
```

Inside the TUI: `Tab` toggles Plan/Build mode, `@` references files,
`/init` generates an `AGENTS.md`, `/undo` reverts the last agent change,
`/share` creates a shareable conversation link.

---

## Resources

- Official opencode docs: https://opencode.ai/docs
- Windows/WSL notes: https://opencode.ai/docs/windows-wsl
- This repo: `AGENTS.md`, `README.md`, `docs/api/openapi.yaml`
