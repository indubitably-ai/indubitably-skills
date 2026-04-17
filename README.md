# indubitably-skills

A small collection of reusable agent skills. Each skill is self-contained, lives in its own top-level directory, and exposes its entrypoint through a `SKILL.md` file with `name` and `description` frontmatter.

This repository is organized for progressive disclosure:

- Start with the index.
- Open the matching `SKILL.md`.
- Read `references/`, `scripts/`, or `SELF-TEST.md` only if the skill points you there.

## Start Here

If you are browsing manually, read the skill index and jump straight to the folder that matches your task.

If you are an agent, discovery should be deterministic:

1. Enumerate top-level `*/SKILL.md` files.
2. Read each file's `name` and `description` frontmatter.
3. Open the selected skill's `SKILL.md`.
4. Load only the referenced local files you actually need.

## Skill Index

The discovery cues below are intentionally literal so simple text search works well.

| Skill | Path | Use It For | Discovery Cues | Supporting Material |
|---|---|---|---|---|
| `agent-session-history` | [`agent-session-history/SKILL.md`](./agent-session-history/SKILL.md) | Mining past agent sessions for prompts, decisions, and repeated working patterns | `what did I ask`, `find that prompt`, `history`, `session archaeology` | `references/`, `scripts/`, `SELF-TEST.md` |
| `codebase-archaeologist` | [`codebase-archaeologist/SKILL.md`](./codebase-archaeologist/SKILL.md) | Systematic exploration of unfamiliar or legacy codebases | `onboarding`, `what does this do`, `legacy code`, `architecture` | `references/`, `SELF-TEST.md` |
| `command-guard` | [`command-guard/SKILL.md`](./command-guard/SKILL.md) | Handling blocked destructive commands and agent safety guardrails | `blocked command`, `git reset --hard`, `rm -rf`, `safety guardrails` | `references/`, `scripts/`, `SELF-TEST.md` |
| `de-slopify` | [`de-slopify/SKILL.md`](./de-slopify/SKILL.md) | Removing AI-sounding writing patterns from docs and public text | `README polish`, `AI slop`, `docs tone`, `public-facing text` | `references/` |
| `software-optimization` | [`software-optimization/SKILL.md`](./software-optimization/SKILL.md) | Profile-driven performance work with behavior proofs | `optimize`, `slow`, `bottleneck`, `latency`, `throughput`, `p95` | `references/` |
| `ui-polish` | [`ui-polish/SKILL.md`](./ui-polish/SKILL.md) | Iterative UI/UX refinement for already-functional interfaces | `polish UI`, `world-class`, `desktop`, `mobile`, `visual refinement` | `references/` |

## Repository Contract

The repository follows a simple layout so agents can discover skills without guessing:

- One top-level directory equals one skill.
- The skill entrypoint is always `<skill>/SKILL.md`.
- `SKILL.md` starts with YAML frontmatter containing `name` and `description`.
- Optional supporting material stays inside the same skill directory.
- Relative links inside a skill should resolve within that skill directory.

Supporting files are used consistently:

- `references/` contains deeper documentation.
- `scripts/` contains helper commands or validation tools.
- `SELF-TEST.md` describes how to validate the skill.

## Quick Discovery Commands

```bash
rg -n "^name:|^description:" */SKILL.md
rg --files
```

## Skill Notes

<details>
<summary><code>agent-session-history</code></summary>

Purpose: recover prompts, decisions, and work patterns from prior agent sessions.

Good fit:

- "What did I ask last time?"
- "Find that prompt we kept reusing."
- Session archaeology across a project workspace

What is inside:

- A workflow-first `SKILL.md`
- Search and analysis helpers under `scripts/`
- A `SELF-TEST.md` for validation

</details>

<details>
<summary><code>codebase-archaeologist</code></summary>

Purpose: build a working mental model of an unfamiliar codebase without wandering randomly.

Good fit:

- New project onboarding
- Legacy code understanding
- Architecture, data-flow, and integration mapping

What is inside:

- A documentation-first exploration workflow
- Reference material for patterns, languages, and examples
- A `SELF-TEST.md` for checking the approach

</details>

<details>
<summary><code>command-guard</code></summary>

Purpose: respond correctly when destructive commands are blocked and prefer recoverable alternatives.

Good fit:

- `git reset --hard` or `rm -rf` got blocked
- You need to explain risk clearly before a human override
- You want to configure safer command workflows

What is inside:

- A strict decision workflow for blocked commands
- Supporting references for configuration, packs, and troubleshooting
- Validation material and helper scripts

</details>

<details>
<summary><code>de-slopify</code></summary>

Purpose: manually revise documentation so it sounds natural and not machine-generated.

Good fit:

- README cleanup
- API docs polish
- Removing formulaic AI phrasing from public-facing text

What is inside:

- A direct editing workflow
- Pattern guidance in `references/`

</details>

<details>
<summary><code>software-optimization</code></summary>

Purpose: optimize software by measuring first, proving behavior stayed the same, and changing one lever at a time.

Good fit:

- Slow commands or services
- Bottleneck analysis
- Latency or throughput work that needs evidence

What is inside:

- A profile-first optimization loop
- Technique catalogs and language-specific references

</details>

<details>
<summary><code>ui-polish</code></summary>

Purpose: iteratively improve UI/UX quality once the product already works.

Good fit:

- Raising a decent interface to a more polished state
- Separate desktop and mobile refinement passes
- Multi-iteration visual and interaction cleanup

What is inside:

- A repeatable polish prompt
- Supporting prompts and checklists in `references/`

</details>

## Using These Skills

If your agent runtime supports local skills, copy or symlink the skill directories you want into its skill search path and preserve the directory structure. The internal relative paths matter because `SKILL.md` files reference local `references/`, `scripts/`, and `SELF-TEST.md` files.

## Adding New Skills

To keep this repository discoverable, new skills should follow the same pattern:

1. Create a top-level directory named after the skill.
2. Add a `SKILL.md` entrypoint with `name` and `description` frontmatter.
3. Keep deeper documentation in local `references/`.
4. Add `scripts/` and `SELF-TEST.md` when the skill needs executable helpers or validation.
