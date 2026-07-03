# Pipeline position

`mine-toread` is the **MINE team fork** of
[`fabiogiglietto/toread`](https://github.com/fabiogiglietto/toread) and the
root of the team chain:

```
mine-toread -> mine-zettelkasten     (repository_dispatch: pipeline-finalize)
```

There is no podcast or website leg — the dispatch goes straight to the team
vault, with `continue-on-error: true` (mine-zettelkasten's daily cron
self-heals a dropped event).

The canonical pipeline documentation — both chains, the DAG, event types, and
the fork policy — lives upstream:
**[toread/PIPELINE.md](https://github.com/fabiogiglietto/toread/blob/main/PIPELINE.md)**.

## Fork policy

This is a **config-diff fork**: feature code lands in upstream `toread`
(behind config flags) and arrives here via `git merge upstream/main`. The
repos should only permanently differ in:

- `config.yml` values and repo Actions variables/secrets
- generated content and state (`data/`, `output/`, `cache/`)
- these doc stubs

Do not land feature code directly in this repo.

> **Status:** unification with upstream is in progress; until it completes,
> some `src/` files still diverge from `toread`.
