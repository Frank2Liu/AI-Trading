# OpenCode Setup Guide for New Users

A beginner-friendly guide to installing **OpenCode** (the open-source AI coding
agent) on **Windows** and **macOS**, using its CLI, and building a daily
routine with it — including a full worked example. **You can run it entirely
for free** — no credit card required (see [section 5](#5-use-opencode-for-free--no-charges)).

Official docs: <https://opencode.ai/docs>

---

## 1. What is OpenCode?

OpenCode is an open-source AI coding agent that runs in your terminal. You
describe what you want in plain English, and it reads your code, plans, writes
or edits files, runs commands, and reports back. It works in the terminal as an
interactive TUI, or non-interactively as a one-shot CLI command.

---

## 2. Prerequisites

Before installing, make sure you have:

- A **modern terminal** (macOS users: the built-in Terminal or iTerm2 works;
  Windows users: Windows Terminal or Git Bash).
- **Git** installed (`git --version` to check).
- An **No credit card needed**: many
  providers have permanent free tiers (Google Gemini, Groq, Cerebras, Mistral,
  NVIDIA), and you can also run models locally with free API key applying with below approach. See
  [section 5](#5-use-opencode-for-free--no-charges) for the free options, then
  you'll add the key to OpenCode in step 4.
- (Optional) **Node.js 18+** — only needed for the npm install method.
  Check with `node --version`.

---

## 3. Install OpenCode

### macOS

**Option A — Homebrew (recommended):**

```bash
brew install anomalyco/tap/opencode
```

> Tip: the official `brew install opencode` formula also exists but is updated
> less frequently. Prefer the `anomalyco/tap` version.

**Option B — Install script:**

```bash
curl -fsSL https://opencode.ai/install | bash
```

**Option C — npm:**

```bash
npm install -g opencode-ai
```

### Windows

#### Recommended: install inside WSL (Windows Subsystem for Linux)

This gives full compatibility and the best experience.

```powershell
wsl --install        # installs Ubuntu; reboot when prompted
```

Then open the Ubuntu terminal and run:

```bash
curl -fsSL https://opencode.ai/install | bash
source ~/.bashrc
opencode --version   # verify
```

Your Windows files live under `/mnt/c/` and `/mnt/d/`, so a repo at
`D:\myproject` is `/mnt/d/myproject` inside WSL:

```bash
cd /mnt/d/myproject
opencode
```

#### Windows — native (no WSL)

Any one of these works:

```powershell
# Chocolatey
choco install opencode

# Scoop
scoop install opencode

# npm
npm install -g opencode-ai
```

> Note: native Windows works fine for most tasks. A few advanced features
> (shell commands, LSP) behave best under WSL.

### Verify the install

```bash
opencode --version
```

You should see a version number like `v0.1.xx`.

> Problem? Check the official troubleshooting docs:
> <https://opencode.ai/docs/troubleshooting/>

---

## 4. First-Time Setup: Connect a Model

OpenCode needs an LLM to answer you. Run this once:

```bash
opencode auth login
```

You'll be prompted to pick a provider and paste your API key. Your keys are
stored locally in `~/.local/share/opencode/auth.json` — **never commit or share
this file**.

Alternative: inside the interactive interface, run the `/connect` command and
follow the prompts.

> 💡 **Want to pay $0?** When the provider picker appears, choose a free one:
> **Google Gemini**, **Groq**, **Cerebras**, **Mistral**, **NVIDIA**, or
> **OpenRouter** (its `:free` models). All work inside OpenCode exactly like a
> paid provider. Full details in the next section.

Useful related commands:

```bash
opencode auth list        # which providers are configured
opencode models           # list all available models (provider/model format)
opencode models --refresh # refresh the cached model list after a new model ships
```

---

## 5. Use OpenCode for Free — No Charges

You don't need a card or a paid subscription to use OpenCode daily. Pick **one**
of the options below. The two easiest are **Google Gemini** (best model quality
at $0) and **Groq** (fastest). All of them plug into OpenCode the same way:
get a free API key, `/connect`, and start coding.

> **A note on signup:** every hosted provider below requires a free account
> and a working email — **check the inbox of whatever email you register with
> (Hotmail works fine) and click the verification link** before you try to log
> in or generate a key. Most providers also show a CAPTCHA on first signup;
> no provider below needs a phone number or credit card for its free tier.

### Option A — Google Gemini (best free model quality)

Sign up at **<https://aistudio.google.com>** → **Get API key** (free, no credit
card). It gives you generous daily free usage of Gemini Flash models.

**Step by step:**

1. Go to <https://aistudio.google.com> and click **Sign in** with your Google
   account (or create one with any email address, e.g. a Hotmail address).
2. If Google asks, verify the email — check your inbox for the confirmation
   link **before** proceeding. New accounts may also hit a phone-verification /
   CAPTCHA prompt; complete those and you're in.
3. Accept the terms, then click **Get API key** (top-left) → **Create API key**
   → select your project → **copy** the key.
4. Open OpenCode and connect:

```bash
# in the TUI
/connect          # select "Google" (Gemini) and paste the key
/models           # pick a Gemini Flash model, e.g. gemini-2.5-flash
```

> No Google account yet? You can sign up with **any** email, including Hotmail:
> the API key is free and no credit card is required.

### Option B — Groq (fastest free inference)

Sign up at **<https://console.groq.com>** → **API Keys** → **Create API Key**
(free, no credit card). Runs Llama and other open models extremely fast.

**Step by step:**

1. Go to <https://console.groq.com> → **Sign Up** (or **Sign in** with Google /
   GitHub).
2. Groq emails a **verification link** — open it in your inbox before logging
   in. No phone number is required for the free tier.
3. Once logged in, click **API Keys** (left sidebar) → **Create API Key** →
   name it (e.g. `opencode`) → **copy** the key.
4. Connect in OpenCode:

```bash
/connect          # select "Groq" and paste the key
/models           # pick e.g. llama-3.3-70b-versatile
```

### Option C — Cerebras (very fast, open models)

**Step by step:**

1. Go to **<https://inference.cerebras.ai>** → **Sign Up** with your email
   (works with Hotmail too).
2. Check your inbox for the **confirmation email** and click the verify link.
3. In the dashboard, click **API Key** → **Generate** → **copy** the key.
4. Connect in OpenCode:

```bash
/connect          # select "Cerebras" and paste the key
/models           # pick e.g. gpt-oss-120b
```

### Option D — Mistral (free developer tier)

Its free developer tier includes code-focused models like **Codestral**
(256K context).

**Step by step:**

1. Go to **<https://mistral.ai>** → **Sign up** with your email.
2. Open the **verification email** from Mistral and confirm your address
   (this also unlocks the "Experiment" free tier).
3. In the console go to **API Keys** → **Create new key** → name it → **copy**.
4. Connect in OpenCode:

```bash
/connect          # select "Mistral" and paste the key
/models           # pick codestral or devstral
```

### Option E — OpenRouter (one key, many free models)

Many models have a free variant (they end in `:free`).

**Step by step:**

1. Go to **<https://openrouter.ai>** → **Sign up** (email, Google, or GitHub).
2. Confirm your email via the link OpenRouter sends you.
3. Go to **Keys** → **Create API Key** → name it → **copy** the key (no card
   needed for the free tier).
4. Connect in OpenCode:

```bash
/connect          # select "OpenRouter" and paste the key
/models           # look for models marked free, e.g. deepseek/deepseek-r1:free
```

### Option F — OpenCode Zen (official, has free models)

**Step by step:**

1. Run `/connect`, select **OpenCode Zen** — it opens <https://opencode.ai/auth>
   in your browser.
2. Sign in / create an account (email signup is supported; verify via the email
   they send). You do **not** need billing details for the free models.
3. Click **Create API Key**, then paste it into the `/connect` prompt.
4. Run `/models` and pick a model whose price shows `$0` / "free", e.g.
   `opencode/big-pickle` or `opencode/deepseek-v4-flash-free`. Paid Zen models
   are optional.

### Option G — NVIDIA (free key)

**Step by step:**

1. Go to **<https://build.nvidia.com>** → **Sign up** with your email.
2. Verify your address via the email NVIDIA sends.
3. Under a model page (e.g. *Nemotron-3*), click **Get API Key** →
   **Generate Key** → **copy** the key.
4. Connect in OpenCode:

```bash
/connect          # select "NVIDIA" and paste the key
/models           # pick e.g. nemotron-3-super
```

### Option H — Run locally with Ollama (truly free, private, offline)

Download **Ollama** (<https://ollama.com>), pull a model, and point OpenCode at
it. No API key, no rate limits, no data leaving your machine — but you need
enough RAM/GPU for a decent model.

```bash
# install Ollama, then pull a coding model
ollama pull qwen3-coder
```

Add this to your project's `opencode.json`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": {
        "qwen3-coder": { "name": "Qwen3 Coder (local)" }
      }
    }
  }
}
```

Then start with `opencode -m ollama/qwen3-coder`.

### Quick comparison

| Option | Cost | No card? | Best for | Model examples |
|---|---|---|---|---|
| Google Gemini | Free tier | ✅ | Model quality, long context | gemini-2.5-flash |
| Groq | Free tier | ✅ | Speed | llama-3.3-70b, qwen3-32b |
| Cerebras | Free tier | ✅ | Speed | gpt-oss-120b |
| Mistral | Free dev tier | ✅ | Code generation | codestral |
| OpenRouter | Free models | ✅ | Variety, one key | many `:free` models |
| OpenCode Zen | Has free models | ✅ | Official, tested | opencode/big-pickle |
| NVIDIA NIM | Free key | ✅ | Open models | nemotron-3-super |
| Ollama (local) | Free | — | Privacy, offline, unlimited | qwen3-coder, deepseek |

### Reading the fine print (free tier gotchas)

- **Free ≠ unlimited.** Every hosted tier caps you at so many requests per
  minute and per day (e.g. Gemini ~15 RPM / 500–1500 requests per day). For
  normal daily coding this is usually plenty; you'll hit it only on heavy
  refactors.
- **Privacy trade-off.** Free tiers are often funded by your prompts (Google
  may use free-tier data to improve its models unless you're in the EU/UK/EEA;
  Mistral's free tier opts into training). Keep proprietary code off free tiers
  — use the paid tier or local Ollama for sensitive work.
- **Models come and go.** Providers occasionally drop or rename free models. If
  you get a model-not-found error, run `/models` and pick the current name.
- **You can stack.** Add several free keys; if one rate-limits you, switch with
  `-m provider/model` instead of waiting.

---

## 6. Your First Session

Go to a project you want to work on and start the interactive interface:

```bash
cd path/to/your/project
opencode
```

The first time, run `/init`. OpenCode analyzes the project and creates an
`AGENTS.md` file (repo rules that help the agent help you). Commit that file to
git.

---

## 7. The Daily Routine — Common Everyday Jobs

Here are the everyday jobs you'll do over and over, and how to do them.

### 7.1 Ask questions about the codebase

```bash
opencode
```

Then type, referencing files with `@`:

```
How is authentication handled in @src/api/index.ts?
```

Or non-interactively:

```bash
opencode run "Explain what src/tasks.py does"
```

### 7.2 Fix a bug (plan first, then build)

```
./tests fail: `npm test` errors on the login test.
Read the failure, find the root cause, propose a plan.
```

Press `Tab` to enter **Plan mode** (OpenCode only suggests a plan, makes no
changes), review the plan, press `Tab` again to switch back to **Build mode**,
then:

```
Sounds good. Implement the fix.
```

Verify yourself with `npm test` — or ask the agent to run it.

### 7.3 Add a feature

```
Add a "dark mode" toggle to the settings page. Follow the existing pattern in
@src/pages/Settings.tsx and add a test under src/__tests__.
```

Give context, examples, and constraints — talk to it like a junior teammate.

### 7.4 Refactor

```
Rename the function getTotal to calculateBalance everywhere it's used.
```

### 7.5 Write or update tests

```
Add unit tests for src/utils/format.ts covering empty input, negative values,
and edge cases like 0.
```

### 7.6 Code review / summarize a pull request

```bash
opencode run "Summarize the changes in this branch and flag any risks"
```

### 7.7 Check your usage/cost

```bash
opencode stats              # token usage and cost
opencode stats --days 7     # last 7 days
```

---

## 8. Daily-Routine Walkthrough (Complete Example)

Imagine you're starting the day on a small Node.js project and you see this
email: *"The checkout page crashes when a user adds an empty cart to the order."*

**Step 1 — open the project:**

```bash
cd ~/myproject
opencode
```

**Step 2 — ask the agent to investigate (Plan mode):**

Press `Tab` to enter Plan mode, then type:

```
A user crashes the checkout page when they add an empty cart.
Find the code that handles checkout (@src/checkout.ts) and figure out why an
empty cart crashes it. Propose a fix.
```

The agent reads the code and proposes, for example: "`totalPrice` is computed
from an empty array, so `cart.reduce(...)` returns `undefined`, and
`totalPrice.toFixed(2)` throws `TypeError`. Add an early return for empty
carts."

**Step 3 — iterate:**

```
Good, but also show a friendly "Your cart is empty" message instead of a bare error.
```

**Step 4 — build it:**

Press `Tab` to return to Build mode, then:

```
Implement the fix now.
```

**Step 5 — verify:**

```
Run the test suite and report pass/fail counts.
```

**Step 6 — course-correct if needed:**

If the result isn't what you wanted:

```
/undo
```

...refine your prompt, and let it try again.

**Step 7 — review the diff and commit yourself:**

```bash
git diff        # inspect what changed
git add -A && git commit -m "fix: guard checkout against empty cart"
```

---

## 9. Handy CLI Reference

```bash
opencode                              # interactive TUI
opencode run "prompt"                 # one-shot task, prints the answer
opencode run -c "prompt"              # continue the last session
opencode run -m anthropic/claude-sonnet-4-5 "prompt"   # pick a specific model
opencode run -m gemini/gemini-2.5-flash "prompt"       # e.g. a free Gemini model
opencode run --file src/main.py "review this file"     # attach a file
opencode -m provider/model            # pick model in the TUI
opencode auth login                   # add an API key
opencode models                       # list available models
opencode session list                 # see past sessions
opencode session delete <id>          # delete a session
opencode stats                        # token usage / cost
opencode upgrade                      # self-update to latest
opencode uninstall                    # remove everything
```

Inside the TUI:

| Key / Command | What it does |
|---|---|
| `Tab` | Toggle **Plan mode** (suggest only) ↔ **Build mode** (make changes) |
| `@` | Fuzzy-search and reference a file |
| `/init` | Generate an `AGENTS.md` for the project |
| `/undo` | Revert the last agent change |
| `/redo` | Re-apply an undone change |
| `/share` | Create a shareable link to the current conversation |
| Drag & drop | Attach an image into your prompt |

---

## 10. Pro Tips for Good Results

1. **Give context.** Reference files with `@` and mention the relevant code,
   tests, or error messages.
2. **Use Plan mode for anything non-trivial.** Review the plan before letting
   it edit files.
3. **Ask it to verify.** "Run the tests" — let the agent prove the fix works.
4. **Use `/undo` freely.** It's a safety net; if a change is wrong, undo and
   rephrase.
5. **Commit `AGENTS.md`** once `/init` creates it — the agent (and your
   teammates) use it to understand the repo.
6. **Keep prompts specific.** "Fix the login bug" is worse than "The login
   test fails with `Unexpected token` at src/auth.ts:42 when the email is
   empty".
7. **Mind the free-tier limits.** Big refactors on a free key can hit
   per-minute caps. Break large jobs into smaller prompts, or add a second free
   key (e.g. Groq for speed + Gemini for quality) and switch with `-m`.

---

## 11. Resources

- Official docs: <https://opencode.ai/docs/>
- Providers (free & paid): <https://opencode.ai/docs/providers/>
- Windows/WSL notes: <https://opencode.ai/docs/windows-wsl/>
- CLI reference: <https://opencode.ai/docs/cli/>
- Troubleshooting: <https://opencode.ai/docs/troubleshooting/>
- Free LLM API keys: Google AI Studio <https://aistudio.google.com>,
  Groq <https://console.groq.com>, Cerebras <https://inference.cerebras.ai>,
  Mistral <https://mistral.ai>, OpenRouter <https://openrouter.ai>,
  NVIDIA <https://build.nvidia.com>, Ollama <https://ollama.com>
- GitHub: <https://github.com/anomalyco/opencode>
