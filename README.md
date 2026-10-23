# EZ-Office

**An offline, lightweight HTML productivity suite** for local files. Designed to eventually run inside [venvWin Portable](https://github.com/danieloculus0-bot/venvWin) using a shared browser engine. No Electron, React, accounts, telemetry or network service required.

## Standalone GitHub Pages

**Public URL:** https://danieloculus0-bot.github.io/EZ-Office/

The repository includes `.github/workflows/pages.yml`, which assembles only the actual HTML, CSS, JavaScript and SVG app assets and publishes them automatically whenever those files change on `main`. It uses the official GitHub Pages artifact and deploy actions; it does not depend on Jekyll, a Node application build or a paid hosting service.

**One-time repository setting (required if that URL returns 404):** Open [EZ-Office Settings → Pages](https://github.com/danieloculus0-bot/EZ-Office/settings/pages), select **GitHub Actions** under **Build and deployment → Source**, then use the **Publish EZ-Office to GitHub Pages** workflow in the [Actions tab](https://github.com/danieloculus0-bot/EZ-Office/actions/workflows/pages.yml) to run it if it has not deployed automatically. The standard repository `GITHUB_TOKEN` cannot reliably enable Pages for the first time by itself; this repository setting may require the owner. Verify the action shows a successful deployment before treating the public URL as live.

## Try the live Workshop demo

**[Launch EZ-Office in BEAN Workshop](https://danieloculus0-bot.github.io/BEAN/portfolio/ez-office/)** · [Workshop project directory](https://danieloculus0-bot.github.io/BEAN/portfolio/)

The Workshop hosts a **version-pinned copy of the actual application**, not a mockup. Verify its release version before assuming newer features from this repository have been mirrored there. Writer, CSV Sheets, Slides, Media, and Mail drafts run locally in your browser. OAuth login is optional for mail; opening ordinary document files never uploads them to a server. Save a copy before switching tools or leaving the page. Avoid confidential files on shared devices.

The Workshop copy is currently published from a known version of EZ-Office. Source updates to this repository are **not automatically synchronized** to the Workshop; version upgrades require copying and testing the changed assets in BEAN.

## Start
Open `index.html` in a modern browser. All tool scripts, styles and icons ship locally. The workspace uses one window and loads tools only when selected, with no installation step or dependency download.

## Engineering buildout — pass 01

**[Read the functionality/deployability audit](docs/BUILDOUT_AUDIT.md)** for current evidence, supported file formats, deployment gates, known limitations and the next prioritized iterations.

This pass strengthens every app without increasing the runtime framework footprint: Writer can find and replace content while preserving existing text formatting, Sheets can paste ranges and jump to cells, Slides has a clickable navigator and notes/outline export, Media adds playback speed/loop and metadata, Mail can reopen plain-text EML drafts, and the shell warns before leaving with unsaved changes.

Actual tests run in Chromium, plus WebKit tests covering the mobile spreadsheet header alignment. The Gmail/Outlook connectors still require separately registered OAuth public clients and live external-account verification; native DOCX/XLSX/PPTX **import** has not been implemented. **Do not infer account readiness, file-format fidelity, or low RAM from a passing frontend test.**

## Real office tools and output formats

EZ-Office is no longer just a text box. It is a **working small office suite**, built with plain JavaScript and no Electron/React/runtime frameworks.

| Tool | Functional editing | Viable outputs |
| --- | --- | --- |
| **EZ Writer** | Rich formatting, find/replace, headings, colors, alignment, lists, undo/redo, sanitized HTML import and plain-text paste | **DOCX**, HTML, TXT, **Print / Save as PDF** |
| **EZ Sheets** | Recalculating formulas and ranges, SUM/AVERAGE/MIN/MAX/COUNT/IF, circular error reporting, tabular clipboard paste, cell navigation and CSV import | **XLSX** with formulas, CSV, editable `.ezsheet` file, **Print / Save as PDF** |
| **EZ Slides** | Slide navigator, titles, speaker notes, themes, reordering, duplication, fullscreen presentations and **embedded images, audio and video** | **PPTX** (limited), native `.ezslides` retaining multimedia, **text outline/notes**, **Print / Save as PDF** |
| **EZ Media** | Browser-supported image/audio/video, playback speed, loop, and dimensions/duration display | **Save original**, export current image/video frame to PNG, **Print / Save as PDF** |
| **EZ Mail** | Offline EML import/edit/export; Gmail preview/send OAuth and Outlook OAuth PKCE adapters (client registration required) | **EML**, system mail handler, authorized Gmail/Outlook send, **Print / Save as PDF** |

**Interoperability boundaries:** DOCX/XLSX/PPTX exports are actual zipped Office Open XML packages, not files renamed to those extensions. The test suite inspects their ZIP members and XML. These are basic document outputs, not full Office replacements: complex Word layout, native DOCX/XLSX/PPTX *import*, charts, advanced formatting, PowerPoint animations and seamless audio/video playback in every presentation viewer are not promised. Use `.ezslides` to preserve the richest in-browser presentation media and editing capabilities.

**Email setup:** The Gmail and Outlook integrations make real delegated provider API requests, but require you to register an OAuth public client in Google Cloud / Microsoft Entra, configure the specific hosted HTTPS origin/redirect, and consent to the requested mail scopes. No built-in app credentials or passwords are supplied. Tokens are held in session memory, and an OAuth provider may require admin approval. **The standalone file:// mode cannot connect to providers**; it still supports offline EML drafts. Do not enter secrets into the client-ID fields.

Print / PDF uses the operating system browser printing dialog; choose **Save as PDF** where available. There is no fake proprietary PDF encoder.


## Design
- One HTML shell, one active app at a time; lazy scripts and explicit cleanup of active document state
- Local file picker and downloads, no document uploads and no always-on background polling
- CSV grid renders a maximum of 35 rows at once and caps file/table sizes
- Local media uses blob URLs revoked at closure to avoid retaining full video data in JS
- Browser engine RAM remains significant and must be measured on actual venvWin hardware; tiny KB source size alone does not prove low RAM
- **Native venvWin office apps stay in place** until compatibility and memory benchmarks justify replacement

[Engineering design, RAM considerations, and verification](docs/architecture.md)

## Validation
GitHub Actions executes JavaScript syntax checks and a **real offline browser smoke test** covering every tool, file round-trips, and local URL disposal. Locally, use:

```sh
for file in shell.js lib/*.js apps/*.js; do node --check "$file"; done
python -m pip install playwright
python -m playwright install chromium webkit
python tests/browser_smoke.py
```

The Playwright dependency is for development tests only, **not** required to use EZ-Office. The CI checks include WebKit spreadsheet scrolling; they do not prove an actual iPhone Safari session, production OAuth approval, venvWin memory, or hardware boot.

## Project scope
EZ-Office is a standalone lightweight productivity experiment, **not an Axiom ERP module**. See source files for the working implementations, and retain independent native applications as fallback.
