# Guardian Frontend Architecture

## 1) Goal
Create a common frontend baseline with React + Vite, keep mobile-first UI defaults, and establish a clear contract with backend before GN-2.

## 2) Folder structure

```text
front/
  public/                     # static assets + PWA icons
  src/
    components/               # reusable UI blocks
    hooks/                    # stateful UI logic and side effects
    services/                 # API calls and infrastructure adapters
    styles/                   # global style layers (mobile-first)
    types/                    # shared TypeScript contracts
    App.tsx                   # application entry composition
    main.tsx                  # React bootstrap + SW registration
  docs/
    FRONTEND_ARCHITECTURE.md
```

## 3) Naming conventions
- Components: `PascalCase` (example: `BaseScreen.tsx`).
- Hooks: `useCamelCase` (example: `useAnalyze.ts`).
- Services: `kebab-or-dot` by domain (example: `analyze.service.ts`).
- Types: domain contracts grouped by feature (example: `analyze.ts`).
- CSS: component file colocated (`BaseScreen.css`) + global base in `styles/base.css`.

## 4) Data flow (frontend <-> backend)
1. UI triggers an action (component).
2. Hook manages loading/error state and calls service.
3. Service performs HTTP request to backend endpoint.
4. Typed response returns to hook.
5. Hook updates UI state and component renders result.

This keeps HTTP concerns outside components and improves testability.

## 5) API contract proposal (`POST /analyze`)

### Request
```json
{
  "text": "string",
  "language": "es"
}
```

### Response
```json
{
  "verdict": "safe",
  "score": 0.12,
  "risks": [
    { "label": "toxicity", "score": 0.1 }
  ],
  "summary": "Low risk content"
}
```

### Notes
- `verdict`: one of `safe | warning | danger`.
- `score`: normalized range `0..1`.
- `risks`: variable list by model output.
- `summary`: short explanation for the UI.

## 6) PWA baseline
- `vite-plugin-pwa` configured in `vite.config.ts`.
- Manifest metadata and icons are in `public/`.
- Service worker is registered from `main.tsx` with auto-update strategy.

