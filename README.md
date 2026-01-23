# Pollen

Clean REST API for Nordic pollen data with Home Assistant integration. Transforms Denmark's complex Firestore pollen API into simple, usable endpoints with multi-language support.

## Home Assistant Component

### Via HACS (Recommended)

1. Open HACS → Integrations
2. Click ⋮ (menu) → Custom repositories
3. Add repository: `https://github.com/Saturate/pollen`
4. Category: Integration
5. Search for "Pollen" and install
6. Restart Home Assistant
7. Add integration: Settings → Devices & Services → Add Integration → Pollen

### Configuration

During setup, configure:

- **API URL**: Where your API is running (default: `http://localhost:3060`)
- **Country**: `dk` (Denmark)
- **Region**: `copenhagen` or `viborg` (or aliases `east`/`west`)
- **Language**: `da` (Danish) or `en` (English)

### Sensors Created

The integration automatically creates sensors for each pollen type:

- `sensor.pollen_grass` (Græs)
- `sensor.pollen_birch` (Birk)
- `sensor.pollen_alder` (El)
- ect..

Each sensor includes:

- **State**: Current pollen level (0-5)
- **Attributes**: Date, pollen type, forecast data

## API

### Docker Hub (Easiest)

```bash
docker run -d -p 3060:3060 --name pollen-api saturate/pollen-api:latest
```

Or with docker-compose:

```yaml
services:
  pollen-api:
    image: saturate/pollen-api:latest
    container_name: pollen-api
    ports:
      - "3060:3060"
    restart: unless-stopped
```

### Docker Compose (Build from Source)

```bash
docker compose up -d
```

API available at `http://localhost:3060`

### Building from Source

```bash
cd api
cargo build --release
./target/release/pollen-api
```

## API Endpoints

```
GET /                                      # API info
GET /v1/dk                                # Denmark info
GET /v1/dk/regions                        # List regions
GET /v1/dk/pollen-types                   # List pollen types
GET /v1/dk/copenhagen/forecast            # Copenhagen forecast (alias: /east)
GET /v1/dk/viborg/forecast                # Viborg forecast (alias: /west)
```

### Query Parameters

- `?lang=da` - Danish translations (default: `en`)
- `?types=grass,birch` - Filter specific pollen types

### Examples

**All pollen types (English):**

```bash
curl http://localhost:3060/v1/dk/copenhagen/forecast
```

**Filtered types (Danish):**

```bash
curl 'http://localhost:3060/v1/dk/copenhagen/forecast?lang=da&types=grass,birch'
```

## License

MIT
