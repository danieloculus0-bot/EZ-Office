# EZ-Office

Lightweight, offline-first desktop productivity tools written in plain HTML, CSS, and JavaScript. Intended for local use and eventual integration with **venvWin Portable**, not Axiom.

## Direction
- **One window, one shared web engine.** Open one tool at a time; unload document state, DOM, and object URLs when switching.
- **No Electron, React, npm runtime, external fonts, accounts, analytics, or always-on application server.**
- **Files belong to the user.** Open local documents and export local files; do not transmit their contents to a service.
- **Keep native Linux fallbacks until real document-compatibility, performance, and RAM benchmarks justify replacing them.**
- **Never claim DOCX, XLSX, PPTX, IMAP, SMTP, or full office compatibility without implementing and testing it.**

The first version will contain real, intentionally limited tools: text editor, CSV spreadsheet, plain-text slide presenter, local media viewer, and email draft composer. Email delivery and inbox sync need a backend and are not part of the offline MVP.

See `docs/architecture.md` after bootstrap for memory design and verified functionality.