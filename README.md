# Pollen API Relay

Clean REST API for Nordic pollen data (Denmark, Sweden). Transforms complex upstream APIs into a simple, standardized format for home automation and dashboards.

## Components

- **[API Service](./api)** - Rust-based relay service (Docker)
- **[Home Assistant Integration](./homeassistant)** - HACS integration

## Usage

```bash
docker compose up -d
```

API runs on `http://localhost:3060`

## License

MIT
