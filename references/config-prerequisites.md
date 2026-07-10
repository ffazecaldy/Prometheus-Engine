# Config Prerequisites for Agentic Prometheus Engine

The prometheus-engine skill assumes up to 100 parallel subagents. The Hermes default config caps this at **3**, which silently breaks the entire system. These settings must be in `config.yaml` before activating the loop.

## Required Settings

### 1. `delegation.max_concurrent_children` → 100 (default: 3)

**What it does:** Maximum number of subagents that can run in parallel in a single `delegate_task` batch call.

**Why 100:** The prometheus-engine decomposes Tier 3-4 goals into 50-100 atomic tasks, each dispatched as a parallel subagent. With the default of 3, only 3 tasks run at a time — the entire "massive parallel" design is defeated. The skill's Tier system, decomposition patterns, and streaming quality gate all assume high parallelism.

**Set it:**
```bash
hermes config set delegation.max_concurrent_children 100
```

**Verify:**
```bash
grep max_concurrent_children ~/.hermes/config.yaml
# Expected: max_concurrent_children: 100
```

### 2. `delegation.max_spawn_depth` → 2 (default: 1)

**What it does:** How many levels deep subagents can spawn their own subagents. Depth 1 = leaf only (no re-delegation). Depth 2 = orchestrator subagents can spawn leaf workers.

**Why 2:** The prometheus-engine uses orchestrator-role subagents for complex tasks (e.g., an orchestrator manages 5 leaf workers building different parts of a module). Without depth 2, orchestrators are blocked from delegating, forcing all work into a single flat batch.

**Set it:**
```bash
hermes config set delegation.max_spawn_depth 2
```

### 3. `agent.max_turns` → 120 (default: 60)

**What it does:** Maximum conversation turns (LLM calls + tool calls) per session before the agent loop stops.

**Why 120:** Autonomous loops on Tier 3-4 goals require many turns: decomposition + dispatch + streaming gather + retries + self-learning + final report. 60 turns can cut off mid-loop on complex goals. 120 gives enough headroom for Tier 4 full-stack systems with 50+ tasks, retries, self-learning, and deploy.

**Set it:**
```bash
hermes config set agent.max_turns 120
```

### 4. `delegation.max_iterations` → 100 (default: 50)

**What it does:** Maximum iterations (LLM calls + tool calls) per subagent.

**Why 100:** A subagent implementing a complex module (model + routes + tests) may need 50+ iterations just for the happy path. With 50, it can run out mid-task. 100 gives enough room for implement + test + fix cycles.

**Set it:**
```bash
hermes config set delegation.max_iterations 100
```

### 5. `delegation.child_timeout_seconds` → 600 (default: 0)

**What it does:** Wall-clock timeout per subagent. 0 = no timeout.

**Why 600 (10 min):** A subagent building a complex module with tests can take 3-5 minutes. With 300s (5 min), it might get killed mid-fix. 600s gives enough margin for Tier 4 tasks without letting zombie agents run forever.

**Set it:**
```bash
hermes config set delegation.child_timeout_seconds 600
```

### 6. `delegation.subagent_auto_approve` → true (default: false)

**What it does:** Controls whether subagents auto-approve or auto-deny dangerous commands.

**Why true:** Without this, subagents that need to run `git push`, `npm install`, or `pip install` get silently blocked (auto-deny). This breaks the autonomous loop. With `true`, subagents can execute these commands with an audit log line.

**Set it:**
```bash
hermes config set delegation.subagent_auto_approve true
```

### 7. `approvals.mode` → smart (default: manual)

**What it does:** Controls whether Hermes prompts the user before running shell commands flagged as potentially destructive.
- `manual` — always prompt (default)
- `smart` — use an auxiliary LLM to auto-approve low-risk commands, prompt only on high-risk
- `off` — skip all approval prompts

**Why smart:** The prometheus-engine runs many `git commit`, `git push`, `pytest`, `curl` commands automatically. With `manual` mode, every git push triggers an approval prompt, breaking the autonomous loop. `smart` auto-approves low-risk commands (git add, git commit, pytest, curl) while still prompting for genuinely dangerous ones (rm -rf, git reset --hard).

**Set it:**
```bash
hermes config set approvals.mode smart
```

## Required Toolsets

The prometheus-engine needs these toolsets enabled. Check with `hermes tools list`:

| Toolset | Required for | Status if missing |
|---------|-------------|-------------------|
| `terminal` | Shell commands, git, builds, tests | Loop cannot execute anything |
| `file` | Read/write/patch files | Cannot create or modify code |
| `delegation` | Spawn subagents | **100 subagents impossible** |
| `memory` | Self-learning persistence | Pattern capture broken |
| `skills` | Load complementary skills (plan, TDD, etc.) | Ecosystem integration broken |
| `session_search` | Recall past patterns | Token-efficient recall broken |
| `web` | Research phase (some decomposition patterns) | Reduced research capability |
| `browser` | Navigate sites if task involves web | Browser tasks fail |
| `code_execution` | Python sandbox for data processing | Limited processing |
| `clarify` | Ask user when genuinely ambiguous | Falls back to guessing |
| `todo` | Track multi-step task progress | Progress tracking broken |
| `cronjob` | Scheduled/autonomous tasks | Cannot schedule |

**Enable a toolset:**
```bash
hermes tools enable delegation
hermes tools enable memory
# etc.
```

**Note:** Tool changes take effect on `/reset` (new session), not mid-conversation.

## Session Restart Requirement

**All config changes require a new session to take effect.** The config is read once at startup and snapshotted.

- In the desktop app: start a new session (`/reset` or `/new`)
- In the CLI: exit and relaunch `hermes`
- In gateway: `/restart`

If you set `max_concurrent_children: 100` but don't restart, the running session still uses the old value (3). Always verify after restart:

```bash
hermes config | grep -A2 "delegation"
```

## Quick Verification Script

Run this after making changes + restarting to confirm everything is active:

```bash
echo "=== Delegation ===" && grep -E "max_concurrent_children|max_spawn_depth" ~/.hermes/config.yaml && echo "=== Agent ===" && grep max_turns ~/.hermes/config.yaml && echo "=== Approvals ===" && grep -A2 "approvals:" ~/.hermes/config.yaml && echo "=== Toolsets ===" && hermes tools list 2>/dev/null | grep -E "delegation|memory|skills|session_search"
```
