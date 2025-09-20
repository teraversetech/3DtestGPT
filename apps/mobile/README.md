# Fashion3D Mobile (Expo)

Expo/React Native client that handles capture, chunked upload, timeline browsing, and notifications.

## Development

```bash
pnpm install
pnpm --filter mobile start
```

Scan the QR code with Expo Go or run `pnpm --filter mobile android` / `ios`.

## Screens

- `Auth` – email/password login with consent copy.
- `Capture` – guided orbit UI (ring overlay, TODO: motion heuristics) using `expo-camera` with chunked uploads + resumable indicator.
- `UploadProgress` – polls `/jobs/{id}` every 8 seconds until complete.
- `Feed` – timeline list with CTA to capture.
- `PostDetail` – preview image, TODO: interactive viewer via `expo-three`.
- `Profile` – plan info, logout, TODO: billing upgrades via Stripe SDK.

## Testing

```bash
pnpm --filter mobile test
```

## Notes

- Buffer polyfill is initialised in `_layout.tsx` to support chunk assembly.
- Face blurring, EXIF scrubbing, and push notifications are marked with `TODO:` for production hardening.
