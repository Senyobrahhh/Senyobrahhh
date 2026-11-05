# Orbital profile redesign

The profile uses larger type, a restrained charcoal/navy palette and a clear reading order: identity, present work, interests, planned learning, then GitHub activity. The typography and linework live inside self-contained SVGs; the README uses supported images, picture sources, links and details elements.

## What changed

- A new animated satellite banner keeps **SENYOBRAHHH** and **Software • Robotics • Space**. The orbit uses CSS animation. Explicit static image sources support reduced-motion preferences even when a browser does not forward them into SVG images.
- A local typing SVG preserves the rotating introduction and removes its external image-service dependency. Social buttons are also local SVGs.
- The profile, interests and roadmap use larger text and consistent spacing. Separate phone assets switch at a 600px viewport; they stack content instead of shrinking the desktop dashboard.
- Eight explicitly planned milestones replace the seven-stage diagram. Autonomous robotics and robotic arms now have their own stage.
- The duplicated executive summary and trajectory table are consolidated into the visual profile and an expandable text version. The full text remains available to recruiters, search and assistive technology.
- Three decorative placeholder graphs become one honest empty state until Lowlighter produces actual measurements. The same three analytics modules remain configured in the unified panel.
- The contribution snake remains in an expandable section, with a muted cyan variant and a reduced-motion rule. Original light/dark output files are retained.
- No unfinished repositories are promoted. The showcase is omitted until completed, documented projects are available.

## Rendering boundary

GitHub owns the surrounding page background, spacing and fonts. This change styles the image panels only. There is no README JavaScript, injected page CSS, external font dependency or simulated interactive UI. The supporting SVGs use vector geometry and system fonts. The text version remains useful when images are unavailable.

GitHub may cache generated images. Native GitHub Markdown spacing can vary slightly from local validation previews. Phone selection uses viewport width, not the exact README container width.

## Review and rollback

The original implementation is preserved on `main`; changes are developed on `design/orbital-profile`. Review the branch README before merging. New animated and static orbital snake assets are added to the existing `output` branch without modifying its original light/dark assets. After merging, a revert of the design commit restores the previous README and workflows.

See [PROFILE_METRICS_SETUP.md](./PROFILE_METRICS_SETUP.md) for the one-time Metrics secret setup and maintenance commands.
