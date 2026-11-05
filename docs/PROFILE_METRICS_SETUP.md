# Profile analytics

The README displays one coordinated telemetry panel in two sizes:
- `assets/metrics/github.svg` — 960px desktop.
- `assets/metrics/github-mobile.svg` — 480px phone fallback.

Each contains the same three Lowlighter Metrics modules: a full-year isometric contribution calendar, repository language usage, and recent coding patterns. These are activity measurements, not skill ratings. Until a successful refresh, a small, explicit “awaiting first sync” state is shown. No sample statistics are committed.

## Enable the first refresh

1. Create a **classic personal access token with no scopes** and an expiration date. The selected public-data plugins support a scopeless token. Do not grant private repository access for this profile.
2. In **Senyobrahhh/Senyobrahhh → Settings → Secrets and variables → Actions**, save it as **METRICS_TOKEN**. Keep the value out of commits, issues and chat.
3. Open **Actions → Refresh profile dashboard metrics → Run workflow** and select the branch to update.
4. Verify that both generation steps succeed. A green run with a “Metrics skipped” notice means the token is still missing; it is not evidence that data was generated.

The workflow runs daily at 03:26 UTC once it is on the default branch, and on changes to its own workflow file on `main`. Each size writes to the branch that triggered the workflow. The separate built-in `GITHUB_TOKEN` publishes the images with repository `contents: write` permission; the Metrics token only reads public data. A plugin error fails the generation step rather than replacing a panel with an error chart. Missing credentials leave existing files untouched.

The token may reveal aggregate private contribution counts already enabled on your public GitHub profile, but is not granted access to private source code. Repository language statistics may include languages other than SQL, C# and Python; they describe repository contents, not a claim of proficiency.

## Contribution animation

The existing snake workflow and the original light/dark output files are retained. Two additional files, `github-snake-orbital.svg` and `github-snake-orbital-static.svg`, provide the dashboard palette and a static fallback. `scripts/prepare_snake.py` changes only colors and adds reduced-motion CSS (or disables animation in the static variant); it preserves every contribution cell and animation path. The README keeps the animation inside an expandable section so it remains available without competing with the portfolio.

## Maintenance

- `python3 scripts/build_assets.py` rebuilds the designed SVG panels using the Python standard library. It never overwrites generated metrics.
- `python3 scripts/validate_profile.py` checks SVG XML, README image references and motion safeguards.
- Update the pinned Metrics action deliberately and recheck the custom styles. Its action reference is pinned to the inspected stable v3.34 source; its default runtime uses the upstream v3.34 prebuilt container.
- Revoke or rotate the Metrics token when it expires. Previously generated images remain visible if a later run fails.
- The generated panel includes its update timestamp. Statistics are not promised to be live to the second.

## References

- [Lowlighter Metrics](https://github.com/lowlighter/metrics)
- [GitHub Action setup and token requirements](https://github.com/lowlighter/metrics/blob/latest/.github/readme/partials/documentation/setup/action.md)
- [Isometric calendar](https://github.com/lowlighter/metrics/blob/latest/source/plugins/isocalendar/README.md)
- [Language statistics](https://github.com/lowlighter/metrics/blob/latest/source/plugins/languages/README.md)
- [Coding habits](https://github.com/lowlighter/metrics/blob/latest/source/plugins/habits/README.md)
- [Custom CSS and output options](https://github.com/lowlighter/metrics/blob/latest/source/plugins/core/README.md)
- [Contribution snake](https://github.com/Platane/snk)

