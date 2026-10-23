# EZ-Office architecture and deployment

For the current per-module scorecard, test evidence and upcoming work, see **[Buildout Audit — Pass 01](BUILDOUT_AUDIT.md)**.

## Runtime

EZ-Office is an HTML/CSS/JavaScript application with no framework or Node/Electron runtime. Open `index.html` as a local file or publish it under a static web host. The shell lazily loads each tool on first use; only one tool's UI and document state are mounted at a time. Disposers clean event handlers, media buffers and object URLs when possible. Leaving a document with unsaved changes triggers a browser confirmation, but **there is no autosave or in-place overwrite**.

Source modules:

- `shell.js` — lifecycle, lazy loading, file pickers, downloads, unsaved-edit guard.
- `apps/writer.js` — formatted contenteditable document, find/replace, sanitized HTML import, DOCX/HTML/TXT export and browser print.
- `apps/sheets.js` — bounded CSV/workbook model, formulas, clipboard paste, cell navigation and independently positioned scrolling coordinate gutters. A native mobile scrollport, not sticky table cells, keeps the row and column labels aligned.
- `apps/slides.js` — multimedia slide decks, themes, presenter notes, slide navigation and outline export.
- `apps/media.js` — browser media playback, speed/loop, metadata and local export.
- `apps/mail.js` — local plain-text EML editing plus delegated Gmail and Microsoft Graph OAuth adapters (the latter **not tested with live accounts**).
- `lib/office-export.js` — dependency-free basic OOXML ZIP export for DOCX, XLSX and PPTX. **No native OOXML import**.
- `styles.css` — responsive shell, document, slide and media layout.

No user file is sent to a server for document workflows. Mail intentionally accesses provider APIs **only after** an explicit OAuth connection. Never embed OAuth client secrets in this static application.

## Output and interoperability

DOCX, XLSX and PPTX output consists of actual ZIP/OOXML entries, which automated tests validate structurally. It does not promise pixel-identical formatting or all Office functions. PPTX has limited native audio/video interoperability; `.ezslides` is the higher-fidelity multimedia round-trip. EML import supports basic plain-text messages; unsupported MIME structures are rejected. PDFs are made using the browser's native **Print → Save as PDF**, not a PDF serializer.

## Deployment

1. GitHub Actions `.github/workflows/ci.yml` runs syntax checks and browser interactions, including WebKit tests of the mobile sheet.
2. `.github/workflows/pages.yml` packages the actual app as static assets, checks syntax and attempts a GitHub Pages deployment from `main`.
3. The standalone Pages URL (`/EZ-Office/`) requires GitHub Pages to be enabled and **GitHub Actions** selected as source. The repo owner may need to perform this one-time setting before deployment can succeed.
4. The BEAN Workshop (`/BEAN/portfolio/ez-office/`) holds a separately vendored copy. When releasing, synchronize files and pass the BEAN Workshop browser and Pages deployment gates; merging EZ-Office alone does not update BEAN.
5. Test on actual iPhone Safari and venvWin WebKitGTK hardware before calling either runtime supported or optimized.

## Memory and packaging

The office scripts and HTML are small and only one tool DOM is mounted. This does **not** remove browser engine RAM, and JavaScript GC may not immediately return memory to the OS. The spreadsheet renders one 35-row page of inputs and keeps the workbook data in memory, while media uses browser-native object URLs. Measure RSS/PSS, cold boot and memory after tool switching on the intended Linux target instead of equating file size with peak RAM.

## Maintenance expectations

Every buildout pass should include: (1) a specific user-visible improvement; (2) an actual browser interaction/format round-trip test; (3) a clear supported-versus-untested claim; (4) a clean deployment to the Workshop and source; (5) updates to the [audit](BUILDOUT_AUDIT.md). Native Office import, cross-app sharing, and provider credentials should not appear as finished features until their tests exist.
