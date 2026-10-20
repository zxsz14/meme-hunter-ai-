# Meme Hunter AI 2.0

A mobile-first static Solana token discovery dashboard with two modes: Early (0–30 minutes) and Momentum (1–24 hours). Python fetches DEX Screener public endpoints and writes `data.json`. GitHub Actions schedules updates (best effort, may be delayed).

## Upgrade existing GitHub Pages repo

Upload `index.html`, `update_data.py`, and `data.json` to the repository root, replacing old versions. Upload `.github/workflows/refresh.yml` only if the existing workflow differs; it is already compatible with `python update_data.py`. Commit changes. Under Actions > Refresh Solana data > Run workflow, run it and check the logs. After Pages redeploys, refresh the site. If workflow pushes are blocked, in Settings > Actions > General enable workflow read/write permissions.

## Limits

No credentials or paid APIs required. DEX Screener discovery endpoints return a limited selection of recently profiled/boosted tokens, **not** a comprehensive feed of all new pools. The scanner does not verify smart-contract security, LP locks, mint/freeze authorities or holder concentration. Risk warnings are simple heuristics. No guaranteed returns. GitHub Pages sites are public, not private/authenticated. GitHub Actions cron runs are not real-time and can be delayed.
