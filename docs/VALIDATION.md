# Validation record

Validated locally on 5 November 2026.

- Parsed all 22 SVG assets as XML and resolved all 22 local README image references.
- Rendered the README in Chromium at 1200px, 390px and 320px viewports, with no failed images or horizontal overflow. Both expandable sections open correctly.
- Checked SVG text bounding boxes against each viewBox and corrected the mobile roadmap heading.
- Verified the orbit and typing animations advance, and that direct SVG reduced-motion settings disable animation. Added explicit static picture sources to handle browsers that do not pass motion preferences into image documents.
- Verified phone picture-source selection and desktop/phone static fallbacks.
- Parsed all three workflow files and checked every Lowlighter input against the inspected stable action definition.
- Confirmed that recolored and static snake variants preserve all contribution cells and animation paths from the existing generated snake; only style content changes.
- Checked for whitespace errors and added a read-only CI workflow to validate assets and reproduce generated design files.

## Limits

The local preview uses GitHub-like content spacing; it is not the actual GitHub renderer. GitHub owns the surrounding page layout and image caching. The SVG panels themselves are the delivered assets, not a separate website mockup.

Live Lowlighter output has not been generated in this session. It requires a valid `METRICS_TOKEN` repository secret and a successful workflow run. The committed empty state says so explicitly. The workflow configuration and supported input names were checked, but a live token-backed run is still needed to validate the generated analytics output.
