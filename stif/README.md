# stif

stif is a minimal client-side starter app — a tiny list manager built with plain ES modules and localStorage. It's designed as a starting point for experiments and small demos.

Features

- Add items by typing and pressing Enter or clicking Add.
- Toggle completion with checkboxes.
- Delete items.
- Data persisted in localStorage (key: stif.items.v1).

Getting started

You can open index.html directly in modern browsers, but some browser security settings block module loading via the file:// protocol. Recommended ways to run locally:

- Use a static server (recommended):
  - With npx: `npx http-server -c-1 . -p 8080` then open http://localhost:8080/stif/
  - Or: `npx serve stif` (requires the 'serve' package via npx)
- Or open the file directly (may work depending on browser config): `stif/index.html`

Project structure

- stif/index.html — entry point
- stif/src/app.js — app logic and UI wiring
- stif/src/store.js — simple localStorage helpers
- stif/src/styles.css — basic styles
- stif/assets — placeholder for images/assets

Known bugs / TODO

- Rapid duplicate adds can occur (no debounce / race conditions).
- No undo / edit item features.
- Accessibility needs more attention (keyboard flows and announcements).
- Consider migrating to a bundler or framework for larger apps.

Contributing

This is intentionally small. If you want to extend it:

- Add edit-in-place for items.
- Add tests and linting.
- Replace localStorage with IndexedDB or a backend API.

License

Unlicensed starter (add a LICENSE if you intend to publish).
