# Token Manager

Monitor token usage across all services: ElevenLabs, Brave API, and OpenClaw models.

## Features

- **ElevenLabs tracking** - Character usage for text-to-speech
- **Brave API tracking** - Search query consumption
- **OpenClaw model tracking** - Primary (Qwen3) and Vision (VL) model tokens

## Tech Stack

- **Backend**: Python FastAPI (port 7776)
- **Frontend**: React + Vite (port 7777)
- **Container**: Docker + Compose

## Setup

### Local Development

```bash
# Backend
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

### Docker Deployment

```bash
# Build containers
./scripts/build.sh

# Deploy
./scripts/deploy.sh

# Access
# Frontend: http://localhost:7777
# Backend API: http://localhost:7776
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/usage/tokens` | GET | Total tokens across all services |
| `/api/usage/by-provider` | GET | Breakdown by ElevenLabs, Brave |
| `/api/models/primary` | GET | Primary model usage stats |
| `/api/models/vision` | GET | Vision model usage stats |
| `/api/api-consumption` | GET | API call counts and status |
| `/api/history` | GET | Get usage history with date filtering |
| `/api/history` | POST | Log new usage entry |
| `/api/history/aggregate` | GET | Aggregated usage statistics |

### Input Validation

All POST endpoints validate input:
- Required fields must be present
- Numeric values are validated
- Dates must be in ISO format (YYYY-MM-DD)
- Invalid requests return 422 status with error details

### Query Parameters

- `start` - Start date filter (ISO format)
- `end` - End date filter (ISO format)
- `provider` - Filter by provider name
- `limit` - Max records (default 100, max 1000)

## Configuration

API keys are loaded from:
- `~/.openclaw/openclaw.json` (preferred)
- `~/.openclaw/workspace/.credentials/elevenlabs.json`

### Data Persistence

Usage history is stored in SQLite at:
- `backend/data/usage_history.db`

The database is auto-created on first run and includes:
- Timestamped usage records
- Provider and metric type tracking
- Indexed queries for performance

## License

MIT
