# Pollen API Integration

Get real-time pollen forecasts for Denmark directly in Home Assistant.

## What You Get

Automatically creates sensors for 8 pollen types:
- Grass (Græs)
- Birch (Birk)
- Alder (El)
- Hazel (Hassel)
- Elm (Elm)
- Mugwort (Bynke)
- Alternaria
- Cladosporium

Each sensor provides:
- Current pollen level (0-5 scale)
- Today's date
- Future forecast data in attributes

## Requirements

You need the Pollen API service running:

**Docker (Recommended):**
```bash
docker run -d -p 3060:3060 --name pollen-api saturate/pollen-api:latest
```

Or see the [full documentation](https://github.com/Saturate/pollen) for other deployment options.

## Configuration

After installation:

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Pollen"
4. Enter your API URL (e.g., `http://localhost:3060`)
5. Select region: Copenhagen or Viborg
6. Choose language: English or Danish

## Data Source

Pollen data from [Astma-Allergi Danmark](https://www.astma-allergi.dk) - updated every 2 hours.
