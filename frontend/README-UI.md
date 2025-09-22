# Frontend UI Architecture Guide

This document explains the current UI structure, layout, and styling so we can quickly reason about changes (e.g., sponsors, sticky headers, spacing) without guesswork.

## Top-level layout

- File: `src/App.jsx`
- Pattern: 3‑column CSS Grid
  - Grid template: `[left rail] [center content] [right rail]`
  - Example (current): `gridTemplateColumns: '400px 1fr 320px'`
  - Gap between columns: `16px`
  - Page background: `#BE6428` (orange), applied on the grid wrapper
  - Horizontal page padding: `padding: '0 32px'`

## Columns

- Left rail (`<aside>`)
  - Position: `position: sticky; top: <offset>` so it follows scroll and pins under the main title area
  - Vertical alignment: `alignSelf: 'start'`
  - Background: `#BE6428` to match page
  - Inner padding: e.g., `padding: '12px 48px'` to pull content off the outer edge
  - Content centering: `display: 'flex'; justifyContent: 'center'`
  - Typical content: sponsor `<a><img/></a>` with explicit width (e.g., `360px`) to control scale independent of rail width

- Center content (`<main>`) – contains the app’s primary component `MaterialTrends`
  - Optional: constrained max width (e.g., `maxWidth: '1100px'`) to keep the table readable

- Right rail (`<aside>`)
  - Same behaviors as left rail; currently empty by design

### Why centering can look off in a rail

- The rail itself can be wide (e.g., `400px`), but the image can be limited (e.g., `300–360px`).
- Edge distance is defined by two things:
  1) The grid wrapper padding (e.g., `32px`) and
  2) The rail’s inner padding (e.g., `48px`).
- The image is centered inside the rail by flexbox; increasing inner padding increases the visible margin to the screen edge.

## Primary content: `MaterialTrends.jsx`

- File: `src/components/MaterialTrends.jsx`
- Responsibilities:
  - Fetch latest 36 observations per series from Firestore (`materialTrends`)
  - Compute/format latest date display (“Latest BLS Month: …”)
  - Render data as grouped tables by category

### Header & month label
- Main page title: large `<h1>` at the top (clinical typography)
- Latest month text: inline CSS font-size (`1.5rem`) and centered

### Sticky headers (categories + table header row)
- Category header bars (blue) are implemented as `position: sticky; top: 0; zIndex: 50` inside the scrolling page so each section label pins to the viewport top while its body scrolls beneath.
- Table header row (Material / MoM / YoY / Trend) cells are also sticky with a top offset (e.g., `top: 44`) so they stick directly under the category bar when the user scrolls.
- Important: We removed container `overflow: auto` wrappers that break sticky behavior relative to the viewport.

### Table contents
- 4 columns: Material | Month over Month | Year over Year | 36‑Month Trend (sparkline)
- Value coloring: red for negative, green for positive
- Sparkline: simple inline SVG in `Sparkline` helper

## GPT Chat widget

- File: `src/components/GPTChatAssistant.jsx`
- Behavior: floating FAB button (“Ask the AI”) launches an overlay panel
- Position: fixed; independent of scroll and grid layout
- Backend base URL: renders prod (`whatsitcost.onrender.com`) unless `localhost`

## Styling approach

- We migrated away from Tailwind in this component and now use explicit inline CSS for predictability.
- Key colors
  - Page background: `#BE6428`
  - Category header (blue): `#4DAAf8` (bars), `#3886C8` (table header cells)
  - Text/body shades: slate/gray scales used in inline styles

## Sponsor integration

- Asset placement
  - Put images under `public/sponsors/` (e.g., `public/sponsors/Studio 1049.png`)
  - Refer via absolute path from root: `/sponsors/Studio%201049.png` (URL-encode spaces)
- Link wrapping
  - Wrap with `<a href="https://example.com" target="_blank" rel="noopener noreferrer">`
- Sizing and alignment
  - Control size via explicit `width` on `<img>` (e.g., `360px`)
  - Center within rail using `display: 'flex'; justifyContent: 'center'`
  - Adjust page/rail padding to increase left/right breathing room relative to the viewport edge
- Vertical alignment
  - To align the ad’s top exactly with the table ("Econ Indicators" bar), we dynamically measure the grid’s top and use it as the sticky offset:
    1) Add an id to the container where the grid starts:
       - In `MaterialTrends.jsx`: `<div id="gridStart" ...>` (the white table wrapper)
    2) In `App.jsx`, compute a spacer with `getBoundingClientRect().top` and use it as the sticky `top` for the left/right rails:
       - State: `const [railSpacer, setRailSpacer] = useState(0);`
       - Effect:
         - Query: `const el = document.getElementById('gridStart');`
         - Measure: `const top = el.getBoundingClientRect().top;`
         - Update: `setRailSpacer(Math.max(0, Math.round(top)));`
         - Recompute on load, resize, and scroll (use `requestAnimationFrame` for smoothness)
       - Apply to rails: `style={{ position: 'sticky', top: \`${railSpacer}px\` }}`
    3) Notes:
       - This keeps the ad top locked to the grid’s top regardless of title/month height or viewport changes.
       - If you need a small nudge, add an offset: `top: \`${railSpacer + 12}px\``.

## Responsiveness

- Current grid widths are fixed pixel rails with a flexible center.
- For small screens, consider:
  - Hiding rails (`display: none`) or stacking them below the table
  - Reducing rail widths and image sizes

## Common tweaks and where to change them

- Change rail widths: `src/App.jsx` → `gridTemplateColumns`
- Increase distance from the page edge: grid wrapper `padding` and rail `padding`
- Make sponsor bigger/smaller: `<img style={{ width: '<px>' }}>`
- Align sponsor vertically: rail `top` sticky offset
- Constrain center content width: `<main style={{ maxWidth: '<px>' }}>`
- Category header stickiness: `MaterialTrends.jsx` category header style (sticky, top, zIndex)
- Table header stickiness: `MaterialTrends.jsx` `<th>` style (sticky top offset)

## Dev & Deploy

- Dev: `npm run dev` (Vite at `http://localhost:5173/`)
- Build: `npm run build` (outputs to `frontend/dist`)
- Deploy (Firebase Hosting): run `npx firebase deploy --only hosting --project what-s-it-cost`

---
This guide should make sponsor placement, spacing, and sticky behavior predictable. If something feels off, first check rail width, rail padding, image width, and sticky top offset.
