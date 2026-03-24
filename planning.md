# Token Manager - Implementation Plan

## Architecture Overview (DRY/KISS)

```
tokenmanager/
├── backend/              # FastAPI + Python
│   ├── api/             # REST endpoints
│   ├── services/        # API clients (ElevenLabs, Brave, OpenClaw)
│   └── models/          # Data schemas
├── frontend/            # React + Vite UI
├── docker/
│   ├── Dockerfile       # Backend container
│   ├── Dockerfile.frontend  # Frontend container
│   └── docker-compose.yml   # Multi-container setup
├── scripts/
│   ├── build.sh         # Build all containers
│   └── deploy.sh        # Deploy to production
└── data/                # Token usage history (optional persistence)
```

## Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Backend | Python FastAPI | Lightweight, async support, good for API integrations |
| Frontend | React + Vite | Already in Juan's preferred stack |
| Container | Docker + Compose | Easy deployment and port mapping |

---

## Phases

### Phase 1: Project Setup ✅ (NOW)

**Goal**: Initialize backend and frontend scaffolding with Docker configuration

**Deliverables**:
- [ ] FastAPI backend with basic structure
- [ ] React + Vite frontend with routing
- [ ] Dockerfile for backend (port 7776)
- [ ] Dockerfile for frontend (port 7777)
- [ ] docker-compose.yml for multi-container setup

**Estimate**: 30 minutes

---

### Phase 2: API Client Integration

**Goal**: Create clients for ElevenLabs, Brave, and OpenClaw models

**Deliverables**:
- [ ] `services/elevenlabs_client.py` - Get token usage
- [ ] `services/brave_client.py` - API consumption stats
- [ ] `services/openclaw_client.py` - Model usage tracking (primary + vision)
- [ ] Configuration loading from `~/.openclaw/openclaw.json`
- [ ] Test each client independently

**API Endpoints Needed**:
- ElevenLabs: `/v1/usage/character-tokens` (if available) or `/v1/voice-library`
- Brave: Use configured API key from openclaw.json
- OpenClaw: Parse usage logs from QMD or session memory

**Estimate**: 45 minutes

---

### Phase 3: Backend API Endpoints

**Goal**: Create REST endpoints for token data

**Deliverables**:
- [ ] `GET /api/usage/tokens` - Total tokens used
- [ ] `GET /api/usage/by-provider` - Breakdown by ElevenLabs, Brave, Model
- [ ] `GET /api/models/primary` - Primary model usage stats
- [ ] `GET /api/models/vision` - Vision model usage stats
- [ ] `GET /api/api-consumption` - API call counts
- [ ] Error handling for missing credentials

**Estimate**: 1 hour

---

### Phase 4: Data Persistence

**Goal**: Store token history and provide filtering

**Deliverables**:
- [ ] SQLite/JSON storage for usage history
- [ ] `POST /api/history` - Log new usage entry
- [ ] `GET /api/history?start=2026-03-01&end=2026-03-31` - Filter by date range
- [ ] Daily/weekly/monthly aggregation endpoints

**Estimate**: 45 minutes

---

### Phase 5: Frontend UI

**Goal**: Complete user-facing dashboard

**Deliverables**:
- [ ] Summary cards (total tokens, API calls, cost estimate)
- [ ] Provider breakdown chart (pie/bar chart)
- [ ] Model usage comparison (primary vs vision)
- [ ] Daily/weekly/monthly usage timeline
- [ ] Settings panel for refresh intervals

**Estimate**: 2 hours

---

### Phase 6: Docker Deployment Scripts

**Goal**: Build and deploy scripts

**Deliverables**:
- [ ] `scripts/build.sh` - Build all containers
- [ ] `scripts/deploy.sh` - Deploy to server
- [ ] Environment variable documentation
- [ ] Health check endpoints in Docker

**Estimate**: 1 hour

---

### Phase 7: Polish & Documentation

**Goal**: Production-ready app

**Deliverables**:
- [ ] Input validation + error messages
- [ ] Loading states for API calls
- [ ] README.md with setup instructions
- [ ] Docker Compose documentation
- [ ] Example usage scenarios

**Estimate**: 1 hour

---

## Total Estimated Time: ~6 hours

## Next Step

Start with **Phase 1: Project Setup** by spawning an Opencode session.
