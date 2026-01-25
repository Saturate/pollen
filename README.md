# Pollen

Home Assistant integration for Nordic pollen data. Get real-time pollen forecasts directly in your smart home.

**API Service:** [Saturate/pollen-api](https://github.com/Saturate/pollen-api)

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

- **API URL**: Uses public API by default (`https://pollen.akj.io`), or enter your own if self-hosting
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

- **State**: Numeric pollen level (0-5 scale)
- **Attributes**:
  - `level_text`: Translated text label (None/Very Low/Low/Moderate/High/Very High)
  - `date`, `pollen_type`, `pollen_name`: Current data details
  - `forecast`: Array of upcoming forecast days

## Dashboard Examples

See the [examples/](examples/) folder for ready-to-use dashboard card configurations:
- **Glance Card** - Compact view with automatic color coding
- **Gauge Cards** - Visual representation with severity colors
- **Grid Layout** - Responsive multi-sensor display
- **Alert Card** - Conditional warnings for high levels
- **Entities Card** - Simple list view

## API Service

The integration uses the Pollen API relay service:

- **Public API**: `https://pollen.akj.io` (used by default)
- **Self-hosting**: See [Saturate/pollen-api](https://github.com/Saturate/pollen-api) for deployment instructions

## License

MIT
