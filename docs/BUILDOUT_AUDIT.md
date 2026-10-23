# EZ-Office • buildout and deployability audit

## Pass 02 — Office interoperability and usable sheet outputs (October 22, 2026)

This release adds an **offline, bounded DOCX/XLSX reader**, sorting/filtering views and a proper sheet print layout. Office files never leave the user's browser when opened or saved.

### Module-by-module changes and evidence

| Area | Implemented this pass | Verification target and boundary |
| --- | --- | --- |
| Writer | **Open DOCX** — imports ordinary Word paragraphs, headings, basic bold/italic/underline/strikethrough; text, notes and existing edit/export tools remain | Round-trip EZ-Office DOCX after ZIP DEFLATE recompression. No images, tracked changes, tables with layout, headers/footers, charts, macros or sophisticated Word formatting |
| Sheets | **Open XLSX** — reads first worksheet, ZIP/DEFLATE, shared strings, inline strings, numeric values and basic formulas | Round-trip ZIP-compressed exported workbook plus externally shaped relationship path/shared-string fixture. No XLSX style/layout/merged cells, dates as formatted dates, charts, pivot tables or multiple editable sheet tabs |
| Sheets views | Filter text across data rows; non-destructively sort by a chosen column ascending/descending; export **visible CSV with evaluated values** | Browser verifies filtered row count, physical coordinate labels, view sort and CSV output. Source sheet order and formulas are unchanged. Ordinary Save XLSX/CSV saves the full source order; export visible CSV follows the active view |
| Sheets PDF | **Print / PDF** generates a complete table of the visible rows, values and headings, rather than only the first 35 editor rows | Print bounded to 200 data rows and 20 columns. Large data must use XLSX/CSV. PDF is the browser's native Save as PDF option |
| Mobile | Maintains tested **independent** row-number and column-letter gutters with one native touch-scrollable cell viewport | Existing Chromium/WebKit two-axis geometry tests remain a mandatory gate; view sort must not freeze any data column |
| Shared import engine | Local ZIP reader with stored/DEFLATE blocks, CRC verification, central-directory parsing, XML parsing and resource caps | 10 MB input, 16 MB max per uncompressed part, 40 MB total. Reject encrypted archives, unsupported ZIP methods, malformed XML and oversized files rather than attempting unsupported transformations |
| Slides | Keep existing media decks, PPTX output, navigator, outline/notes export, multi-slide PDF | Native PPTX import, animations, consistent embedded audio/video playback, complete PowerPoint notes/objects not yet supported |
| Media | Keep playback speed, looping, metadata and image/video PNG frame output | Media transcoding and comprehensive browser-codec compatibility remain unsupported |
| Mail | Keep offline EML draft round-trip, Gmail/Microsoft delegated OAuth adapters | Real provider approval, token/session expiry flows, attachments and external mailbox tests not yet verified |
| Deployment | Keep static Pages artifact and separately mirror tested build into BEAN Workshop | Verify source and Workshop tests, then merge, then confirm Pages deployment; standalone EZ-Office Pages still requires owner setting |

### Security and technical boundaries

- The import library uses **no online document conversion**. It reads ZIP contents locally, rejects over-budget entries and verifies checksums before parsing XML; does not invoke script contents.
- The first Excel worksheet is parsed. Formula **text** is preserved for the existing local evaluator; unsupported functions may correctly display an error rather than an invented result. Shared formulas and external workbook links are not guaranteed to be reconstructed.
- Non-destructive sort/filter avoids corrupting cell references. A sorted/filtered view is not a destructive reorder of the underlying workbook. The user can download the visible table as evaluated CSV.
- Print output is deliberately limited to manageable dimensions to prevent freezing mobile browsers on thousands of rows.
- Neither tiny JavaScript files nor browser tests constitute evidence of venvWin hardware RAM savings.

### Release gates

1. JavaScript syntax checks on all \`shell.js\`, \`apps/*.js\` and \`lib/*.js\`.
2. Actual browser tests in Chromium, plus WebKit coverage for the phone-size spreadsheet coordinate layer.
3. Import **DEFLATE-compressed Office archives**, native-export round-trips, a shared-string workbook and corrupted/over-budget file rejection.
4. The original working features (Writer formatting and DOCX export; Sheets formulas/CSV/XLSX export; Slides multimedia/PowerPoint export; Media file playback; Mail draft export) must continue passing their tests.
5. A clean BEAN Workshop copy from the validated main tree and a successful Pages deployment receipt. Do not call the standalone Pages site live unless enabled and verified.

### Next gaps (Pass 03)

More complete DOCX tables and lists, Excel cell styles/dates/merged ranges, formula-relative sorting only when its correctness can be proven, PPTX compatibility and note retention, real Gmail/Outlook provider-approved authorization with test accounts, better accessible print output and performance measurements on actual venvWin.

## Pass 01 — prior established baseline

Pass 01 added Writer find/replace, Sheets tabular clipboard paste/cell navigation and mixed text/numeric formula aggregates, Slides navigator and outline/notes output, Media playback speed/loop metadata, Mail plain-text EML import, and a shared unsaved-edit confirmation. This pass preserves those features and the independent mobile spreadsheet header architecture.
