# EZ-Office • functionality and deployability audit

**Pass 01 — October 22, 2026**

## How to interpret status

- **Implemented:** UI and application logic are present in the repository.
- **Automated coverage:** Tested through the real local-file browser application, not a fake data model.
- **Deployable:** Static files can be published to an existing GitHub Pages host; production access requires a successful host deployment.
- **Not verified:** Integration tests requiring customer accounts, external providers, desktop Linux hardware, or full Office applications have not been performed.

## Module scorecard

| Area | Pre-pass limitations | Pass 01 improvement | Verification and important remaining gaps |
| --- | --- | --- | --- |
| Shared shell | Could lose edits by accidentally closing/reloading browser | Native unsaved-edit warning for reload/tab close; existing switch confirmation and explicit teardown preserved | Browser dialog behavior depends on browser; no autosave or persistent open-file handles |
| Writer | Rich formatting and DOCX export but no document search | Find next and replace all, preserving formatting in other text nodes | Real browser edits/HTML sanitization/DOCX ZIP and XML tested; matches spanning several formatted text nodes are not supported; no DOCX import |
| Sheets | Formula evaluation, CSV/XLSX export, native workbook and stable mobile grid but awkward data entry | Paste Excel/Sheets tab-separated rectangular ranges; jump directly to A1-style cell references | Real browser tests exercise dependencies, export, clipboard paste and jump; import of XLSX, charts, drag fill, filters, and formula-reference rewriting after sorts remain unavailable |
| Slides | Rich multimedia decks without an overview or useful notes export | Clickable slide navigator and export of text outline plus presenter notes | Real browser tests exercise navigator, `.ezslides` media round-trip and PPTX ZIP/XML; full native PPTX audio/video playback and animations not guaranteed |
| Media | Browser media player, original download, PNG frame capture without transport preferences | Real audio/video speed, loop, and dimensions/duration indicators | Browser file playback and speed/loop controls tested with generated WAV; codec coverage, transcoding and non-image printing not implemented |
| Mail | EML draft export and delegated Gmail/Outlook OAuth code, no EML reopening | Load local plain-text `.eml` drafts for editing and reexport | Plain-text EML round-trip tested. Multipart attachments/HTML/quoted-printable/base64 import rejected honestly. No live account authorization validated; provider OAuth needs owner-created public client registration/approval |
| Deployment | EZ-Office Pages site may 404 until repository owner enables it; Workshop manually vendored | Retain lightweight static artifact, add this release audit and browser verification across Chromium + WebKit for mobile grid | Workshop is the functional demo host; standalone Pages still requires owner action. Production publish receipt is separate from an application test |

## Current release gates

1. JavaScript syntax: `node --check shell.js lib/*.js apps/*.js`.
2. Actual browser workflows: `python tests/browser_smoke.py` after installing Playwright 1.55.0 Chromium + WebKit.
3. Office outputs: ZIP integrity and required OOXML parts validated with Python `zipfile` and XML parser.
4. Mobile: 360px and 390px viewport overflow tests plus independent row/column axis geometry at 390px in Chromium and WebKit.
5. Network boundary: offline test requires no HTTP requests for ordinary document operations. External API traffic is only expected after explicit mail authorization.
6. Workshop publication: BEAN deploy workflow must be green, and the vendored copies of the application assets must match tested EZ-Office source.

## Release architecture and memory

One browser engine and one active app DOM; scripts load lazily. Media object URLs are revoked when leaving Media. The 35-row paged spreadsheet avoids rendering thousands of inputs. None of this proves lower RSS/PSS than native programs: run actual host measurements on target venvWin hardware before replacing desktop office applications.

## Next passes, based on measured gaps

**Pass 02 (interoperability):** native DOCX and XLSX import, tabular cell formatting and data filters, robust DOCX/PPTX compatibility fixtures, proper print ranges and PDF layout, image accessibility.

**Pass 03 (connected workflows):** provider-approved OAuth app registration and end-to-end Gmail/Outlook read/send tests with test accounts, richer MIME/attachments, credential lifecycle, saved file permissions, accessibility keyboard audit.

**Pass 04 (deployment/performance):** venvWin App launcher, real iPhone Safari acceptance test, WebKitGTK cold/warm RSS/PSS benchmarking, browser launch behavior, offline packaged-release smoke.

Neither the next passes nor any hardware/account verification is claimed as complete in this pass.
