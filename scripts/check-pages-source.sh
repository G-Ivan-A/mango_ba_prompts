#!/usr/bin/env bash
set -euo pipefail

if ! matches=$(gh api "repos/${GITHUB_REPOSITORY:?}/pages" \
    --jq '[.build_type, .source.branch, .source.path] == ["legacy", "gh-pages", "/"]'); then
    echo '::error::Cannot read the Pages site. A repository admin must check the plan and Settings > Pages, then enable Deploy from a branch (gh-pages, /) if approved. See docs/site-access.md.'
    exit 1
fi

if [[ "$matches" != "true" ]]; then
    echo '::error::Unexpected Pages source. A repository admin must verify Settings > Pages uses Deploy from a branch (gh-pages, /). See docs/site-access.md.'
    exit 1
fi

echo 'Pages source is configured as gh-pages (/).'
