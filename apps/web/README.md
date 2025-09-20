# Fashion3D Web

Next.js 15 + React 19 front-end with Three.js viewer for Fashion3D timelines and post detail pages.

## Development

```bash
pnpm install
pnpm --filter web dev
```

Environment variables: `.env.example` (`NEXT_PUBLIC_API_BASE`).

## Available pages

- `/login` – email/password auth using the FastAPI backend.
- `/feed` – realtime-ish feed (`SWR` refreshes every 10 seconds). 3D viewer spins glTF assets on hover using Three.js.
- `/post/[id]` – individual artifact view with SEO ready metadata.
- `/u/[username]` – profile feed.

## Testing

```bash
pnpm --filter web test
```

Vitest + React Testing Library snapshot coverage lives under `apps/web/tests`.

## Styling

Tailwind CSS + shadcn-inspired primitives shared from `@fashion3d/ui`. Three.js scenes use soft lighting + auto-fit bounding box.
