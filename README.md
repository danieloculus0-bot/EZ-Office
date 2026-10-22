# EZ-Office

**An offline, lightweight HTML productivity suite** for local files. Designed to eventually run inside [venvWin Portable](https://github.com/danieloculus0-bot/venvWin) using a shared browser engine. No Electron, React, accounts, telemetry or network service required.

## Standalone GitHub Pages

**Public URL:** https://danieloculus0-bot.github.io/EZ-Office/

The repository includes `.github/workflows/pages.yml`, which assembles only the actual HTML, CSS, JavaScript and SVG app assets and publishes them automatically whenever those files change on `main`. It uses the official GitHub Pages artifact and deploy actions; it does not depend on Jekyll, a Node application build or a paid hosting service.

**One-time repository setting (required if that URL returns 404):** Open [EZ-Office Settings → Pages](https://github.com/danieloculus0-bot/EZ-Office/settings/pages), select **GitHub Actions** under **Build and deployment → Source**, then use the **Publish EZ-Office to GitHub Pages** workflow in the [Actions tab](https://github.com/danieloculus0-bot/EZ-Office/actions/workflows/pages.yml) to run it if it has not deployed automatically. The standard repository `GITHUB_TOKEN` cannot reliably enable Pages for the first time by itself; this repository setting may require the owner. Verify the action shows a successful deployment before treating the public URL as live.

## Try the live Workshop demo

**[Launch EZ-Office in BEAN Workshop](https://danieloculus0-bot.github.io/BEAN/portfolio/ez-office/)** · [Workshop project directory](https://danieloculus0-bot.github.io/BEAN/portfolio/)

The Workshop hosts the **working HTML/CSS/JavaScript suite**, not a mockup. Writer, CSV Sheets, Slides, Media, and Mail drafts run locally in your browser. No login or server-side upload is part of the app. Save a copy before switching tools or leaving the page. Avoid confidential files on shared devices.

The Workshop copy is currently published from a known version of EZ-Office. Source updates to this repository are **not automatically synchronized** to the Workshop; version upgrades require copying and testing the changed assets in BEAN.

## Start
Open `index.html` in a modern browser. All tool scripts, styles and icons ship locally. The workspace uses one window and loads tools only when selected, with no installation step or dependency download.

## Implemented tools

| Tool | Real working features | Honest boundaries |
| --- | --- | --- |
| Writer | Open and edit TXT/MD, word count, keyboard save and local file download | Plain text, not DOCX or rich text |
| Sheets | CSV import/export with proper quoted-field handling, editable cells, paged grid, add rows/columns | No XLSX or formulas |
| Slides | Edit text slides, previous/next, fullscreen, export editable deck | No PPTX |
| Media | Local video/audio playback and image display, release resources on switch | Browser-supported codecs only |
| Mail drafts | Compose to/cc/subject/body, export .eml, open system mail application | No inbox, IMAP/SMTP connection or sending |

**No fake backend:** every listed operation is implemented. Unimplemented compatibility and synchronization are explicitly excluded.

## Design
- One HTML shell, one active app at a time; lazy scripts and explicit cleanup of active document state
- Local file picker and downloads, no document uploads and no always-on background polling
- CSV grid renders a maximum of 45 rows at once and caps file/table sizes
- Local media uses blob URLs revoked at closure to avoid retaining full video data in JS
- Browser engine RAM remains significant and must be measured on actual venvWin hardware; tiny KB source size alone does not prove low RAM
- **Native venvWin office apps stay in place** until compatibility and memory benchmarks justify replacement

[Engineering design, RAM considerations, and verification](docs/architecture.md)

## Validation
GitHub Actions executes JavaScript syntax checks and a **real offline browser smoke test** covering every tool, file round-trips, and local URL disposal. Locally, use:

```sh
for file in shell.js apps/*.js; do node --check "$file"; done
python -m pip install playwright
python -m playwright install chromium
python tests/browser_smoke.py
```

The Playwright dependency is for development tests only, **not** required to use EZ-Office. This test proves Chromium behavior with a local file, not Epiphany-on-vEnvWin memory or hardware boot.

## Project scope
EZ-Office is a standalone lightweight productivity experiment, **not an Axiom ERP module**. See source files for the working implementations, and retain independent native applications as fallback.
