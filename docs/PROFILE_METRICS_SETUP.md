# GitHub profile dashboard — one-time live metrics setup

The profile README already contains three branded placeholders for Lowlighter Metrics:

- `assets/metrics/calendar.svg` — isometric contribution calendar.
- `assets/metrics/languages.svg` — repository language breakdown.
- `assets/metrics/activity.svg` — coding-activity charts.

The workflow is `.github/workflows/profile-metrics.yml`. The placeholders are deliberately not real statistics until the generator runs.

## Enable live cards

1. On GitHub, open **Settings → Developer settings → Personal access tokens** and create a token for Lowlighter Metrics. The project's documentation specifies a **personal access token**, because the built-in repository-scoped `GITHUB_TOKEN` cannot access all user-related metrics. Start with a classic token with **no scopes** for public metrics; only add permissions if a plugin explicitly requires them. Set an expiration date.
2. Open your profile repository's **Settings → Secrets and variables → Actions → New repository secret**.
3. Set **Name** to `METRICS_TOKEN` and paste the token as its **Value**. **Never add the value to README.md, a commit, an issue, or a chat message.**
4. Open **Actions → Refresh profile dashboard metrics → Run workflow**. Alternatively, the workflow runs on its daily schedule.
5. Open that workflow run and inspect the logs. On success, Lowlighter replaces the placeholder SVGs with real generated data. The README already references the correct file paths.
6. If GitHub reports a write-permission error, check **Settings → Actions → General → Workflow permissions**. The workflow requests `contents: write`, but repository or organization settings may restrict the token.

## Notes

- The metrics are a measure of **public GitHub activity**, not a comprehensive proof of skill or every hour of work.
- Private repositories may require more permissions; do not give your token broad access merely to populate a public profile.
- The language graph may contain languages outside your declared current SQL/C#/Python toolkit; GitHub code statistics and a self-described professional stack are different things.
- The workflow uses `lowlighter/metrics@latest` and will use the current stable Metrics release. Review third-party action permissions periodically.
- You can turn it off by removing the `METRICS_TOKEN` secret; the last committed images remain visible until you replace them.

Sources:
- https://github.com/lowlighter/metrics
- https://github.com/lowlighter/metrics/blob/master/.github/readme/partials/documentation/setup/action.md
