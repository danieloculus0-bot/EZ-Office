# EZ-Office engineering boundaries

## October 22 feature expansion: viable output per application

This suite now includes an **actual Office Open XML exporter** in `lib/office-export.js`, implemented with a small dependency-free ZIP writer (CRC32, central directory, UTF-8 path entries) and minimal DOCX, XLSX and PPTX package builders. Each is a genuine XML-based Office archive; complex fidelity is limited. The export test downloads files through Chromium, checks ZIP integrity and parses their XML entries. The PDF route uses native print / Save as PDF, not an invented binary serializer.

- **Writer:** contenteditable formatted text, toolbar, restricted HTML import, DOCX, HTML and TXT save; print/PDF. Future work: DOCX import, tables, page styles and robust accessibility.
- **Sheets:** bounded recursive-descent formula evaluation with dependency tracking, circular reference errors, standard arithmetic and SUM/AVERAGE/MIN/MAX/COUNT/IF; XLSX, CSV and native JSON workbook export; print/PDF. Formula cells are exported with actual SpreadsheetML formula nodes, not just rendered values. Future work: XLSX import, formatting, sorting/filtering and charts.
- **Slides:** title, body, notes, themes, ordering, fullscreen, bounded embedded image/audio/video asset persistence. PPTX export contains basic presentation XML and embedded asset entries. Image media has slide relationships; audio/video entries are retained for interoperability experiments, but their native PowerPoint playback is not verified. The `.ezslides` native format is the faithful multimedia round-trip. Entire deck prints as multiple pages.
- **Media:** save unmodified originals, export still PNG frames, print images; browser codec support determines playable formats. No transcoding.
- **Mail:** `.eml`, print/PDF and system mail handoff work offline; optional real Google Gmail and Microsoft Graph delegated OAuth/PKCE adapters can fetch message previews and send drafts only after user-approved authorization and registration of OAuth public client IDs. No token persistence, passwords, secret keys or silent sending. The static site does not provide a pre-registered provider application.

Security and compatibility boundaries: never parse untrusted formulas with `eval`; HTML import strips scripts, event handlers and active/remote content; embedded slide media and table dimensions are capped. Cross-application editing should maintain local data boundaries and explicit download/save semantics. The mail OAuth scopes must be approved under Google/Microsoft policies. The DOCX/PPTX/XLSX implementations are an initial interoperable subset, not Microsoft Office feature parity.

## What exists in this iteration
- **EZ Writer:** edits real plain-text and Markdown files, has word/character count, local download copy, keyboard shortcut.
- **EZ Sheets:** parses and exports CSV with quoted commas, escaped quotes and multiline cells; bounded to 5,000 rows and 40 columns, renders at most 45 rows per page. No formula evaluation or XLSX.
- **EZ Slides:** edits text decks using a line containing `---` between slides, local save, next/previous and fullscreen presentation. No PPTX.
- **EZ Media:** opens local images, audio, and video with browser-supported codecs, pauses and revokes object URLs on closure. No transcoding.
- **EZ Mail:** constructs real `.eml` drafts and can hand off to a configured desktop mail client through `mailto:`. No IMAP, SMTP, inbox, account tokens, sending or synchronization.

Every tool is actual working file/UI code, not a demo placeholder for a promised backend. No user file is uploaded. Browser file-picker and download APIs require user interaction and cannot overwrite originals silently.

## RAM design
1. The browser/GTK WebKit engine is **shared by the whole EZ-Office window**. An installed browser can still use substantial memory independently of the tiny HTML files.
2. The shell loads the code for a tool via a classic local `script` element **on first activation**. This works when opening `file://.../index.html`, unlike several browser-restricted ES module import patterns.
3. Only one tool's DOM and working data live at a time. On switching, its disposal hook removes event listeners, clears document arrays and releases object URLs. JavaScript garbage collection is owned by the browser, not the app; closed resources become collectible but immediate OS RAM release is not guaranteed.
4. No React, Electron, npm runtime, per-tool browser processes, telemetry, service workers, auto-sync or background timers. The only timer is a short-lived downloaded-blob cleanup.
5. The data budget is intentionally constrained. Spreadsheets use a **paged DOM**; media uses a blob URL instead of `file.arrayBuffer()` of the entire movie.

## Integration with venvWin
venvWin's current core image already includes Epiphany/WebKit for the FUN games; Firefox ESR is used in the larger profiles. A separate desktop launcher can open EZ-Office's local index file in the existing engine. **Do not remove AbiWord, Gnumeric, mousepad, or other native fallbacks yet:** the EZ-Office MVP does not offer comparable document compatibility or measured peak RAM.

A future common app-host may embed a persistent, single WebKit view and switch local routes, but first measure whether the chosen WebKit browser reuses one renderer or creates extra processes/tabs. “Shared engine” does **not** inherently mean shared memory pages or a single process. Browser cache, GPU, font and codec memory must be accounted for.

## Test and measurement
- `python tests/browser_smoke.py` opens the exact local `file://` URL in headless Chromium, edits and round-trips a text file/CSV, presents slides, tests media URL revocation, exports a mail draft and checks no HTTP(S) requests occur. Development-only dependency: `pip install playwright && python -m playwright install chromium`.
- `node --check shell.js` and `node --check apps/*.js` (per file) verify JavaScript syntax.
- Real RAM numbers require measuring RSS/PSS with `/usr/bin/time -v`, `smem`, or `/proc/<pid>/smaps_rollup` on the **target machine**, comparing native app cold boot, shared engine idle, each tool loaded and after closing. Do not infer OS RAM from source-file KB, a JS heap statistic, or a successful smoke test.
- Chromium is a development test browser; Epiphany/WebKit on actual venvWin hardware requires separate validation.

## Next work
Actual DOCX/XLSX/PPTX interoperability, rich-text layout and printing fidelity, data formulas, secure document conversion, PDF annotation, OS file associations, and email transport would require dedicated engines/backend work. Track separately and prove each feature with real file fixtures.
