# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## What this repo is

`mine-toread` is the **MINE team fork** of
[`fabiogiglietto/toread`](https://github.com/fabiogiglietto/toread) — the same
Paperpile/Slack → enriched JSON feed generator, re-pointed at the MINE team
Slack workspace and feeding `mine-zettelkasten` instead of the fg chain.

For architecture, development commands, testing, and conventions, read the
**upstream CLAUDE.md**:
https://github.com/fabiogiglietto/toread/blob/main/CLAUDE.md
Everything there applies here.

## What differs from upstream (deliberate)

- **Downstream target:** the workflow dispatches `pipeline-finalize` directly
  to `mine-zettelkasten` (no research-radio / website legs), with
  `continue-on-error: true`.
- **Team attribution:** the feed's `_slack_suggestion` carries
  `submitted_by` / `submitted_by_id` (see `SCHEMA.md`).
- **Drive auth:** suggestion PDFs upload with OAuth user credentials
  (`GOOGLE_OAUTH_*`) into a My-Drive inbox folder, not a service account.
  One-time token minting: `scripts/mint_oauth_token.py`.

## Fork policy — read before changing code

This is a **config-diff fork**. Feature code and bug fixes land in upstream
`toread` (behind config flags defaulting to fg behavior) and arrive here via
`git merge upstream/main`. Permanent local differences are limited to
`config.yml` values, repo Actions variables/secrets, generated content/state
(`data/`, `output/`, `cache/`), and these doc stubs. **Do not land feature
code directly in this repo** — implement upstream, flag it, then merge.

Pipeline DAG for both chains:
https://github.com/fabiogiglietto/toread/blob/main/PIPELINE.md
