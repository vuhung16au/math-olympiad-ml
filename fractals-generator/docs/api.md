# API

## `GET /api/v1/[family]/[preset]`

Returns a rendered fractal PNG for any supported family/preset.

### Path Parameters

- `family`: one of:
  - `ifs`
  - `lsystem`
  - `escape-time`
  - `newton`
  - `strange-attractor`
  - `circle-inversion`
- `preset`: preset key from `GET /api/presets`

### Query Parameters

- `width` (optional): image width in px, default `1280`
- `height` (optional): image height in px, default `720`
- `backgroundColor` (optional): default `white`; accepts `white`, `black`, hex (`#RRGGBB`)
- `mainColorScheme` (optional): default `acu`; accepts `acu`, `matrix`, `emerald`, `ink`
- family-specific parameters are also supported (examples):
  - escape-time: `etMaxIterations`, `etBailout`, `etPower`, `etJuliaRe`, `etJuliaIm`
  - ifs: `ifsIterations`, `ifsDensity`, `ifsPointSize`, `ifsColor`
  - lsystem: `lsIterations`, `lsDistance`, `lsAngle`, `lsScale`, `lsLineWidth`, `lsColor`, `lsAxiom`, `lsRules`

### Responses

- `200`: `image/png`
- `400`: invalid width/height
- `404`: unknown family or preset

### Example

```bash
curl -L "http://127.0.0.1:3000/api/v1/escape-time/multibrot?width=1280&height=720&backgroundColor=white&mainColorScheme=acu" \
  --output multibrot.png
```

## Existing API (unchanged)

### `POST /api/render`

Returns `image` as JSON RGBA array for app rendering compatibility.

## Test Suite

- Quick API test:
  - `npm run test:api:v1:quick`
- Full family sweep:
  - `npm run test:api:v1:full`

Set `FRACTALS_API_BASE` if your app is not running on `http://127.0.0.1:3000`.
