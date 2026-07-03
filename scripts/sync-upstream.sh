#!/usr/bin/env bash
# Sync this fork with upstream toread — the ONLY supported way to bring in
# code changes (see CLAUDE.md fork policy). Behavior differences are driven
# by repo Actions variables (PIPELINE_DISPATCH_*, SLACK_REQUIRE_HASHTAG,
# SLACK_ATTRIBUTE_SUGGESTERS) and secrets (GOOGLE_OAUTH_*), not code.
#
# One-time local setup:
#   git remote add upstream https://github.com/fabiogiglietto/toread.git
#   git config merge.ours.driver true
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

if ! git remote get-url upstream >/dev/null 2>&1; then
  echo "Adding upstream remote..."
  git remote add upstream https://github.com/fabiogiglietto/toread.git
fi
git config merge.ours.driver true

if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree not clean — commit or stash first." >&2
  exit 1
fi

git fetch upstream
tag="pre-sync-$(date -u +%Y%m%dT%H%M%SZ)"
git tag "$tag"
echo "Rollback point: git reset --hard $tag"

# NOTE: the FIRST sync ever needs --allow-unrelated-histories (copy-paste
# fork). The script adds it automatically when no merge base exists.
extra=""
git merge-base HEAD upstream/main >/dev/null 2>&1 || extra="--allow-unrelated-histories"

git merge $extra upstream/main --no-edit || {
  echo "Merge stopped with conflicts. Resolve rule of thumb:"
  echo "  take upstream: src/ tests/ schema/ .github/ requirements* SCHEMA.md"
  echo "  keep ours:     config.yml data/ output/ cache/ README.md CLAUDE.md PIPELINE.md .gitattributes scripts/"
  echo "Then: git checkout HEAD -- data output cache && git commit"
  exit 1
}

# Belt and braces: generated data/state must never move on a sync.
git checkout HEAD -- data output cache 2>/dev/null || true
if ! git diff --quiet HEAD -- data output cache; then
  git commit -am "Restore data/output/cache after upstream sync"
fi

echo "Synced. Review 'git log --oneline -5', run pytest, then push."
