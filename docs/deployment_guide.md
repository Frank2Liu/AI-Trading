# Deployment Guide for AI Market Investor Stock Analysis Platform

## 1. Overview

This deployment guide explains how to deploy the AI Market Investor platform for stock analysis, market intelligence, trading strategies, order handling, and customer notifications.

The deployment targets a production-style environment with:
- FastAPI backend
- React frontend
- PostgreSQL or SQLite database
- Redis cache/queue
- Background workers for monitoring and alerts
- Optional reverse proxy and SSL termination

---

## 2. Recommended Deployment Architecture

```text
Internet / Users
    |
    v
Nginx / Reverse Proxy
    |
    +--> Frontend (React/Vite static build)
    |
    +--> Backend API (FastAPI)
    |
    +--> Background Workers

Backend services connect to:
- PostgreSQL Database
- Redis Cache
- Market Data APIs
- Broker / Paper Trading API
- Notification Providers (Email/SMS/Webhook)
```

---

## 3. Deployment Components

### 3.1 Frontend
The React frontend should be built into static assets and served by Nginx or another web server.

Typical flow:
1. Install frontend dependencies
2. Build production bundle
3. Deploy static files to web server
4. Configure API base URL

### 3.2 Backend
The FastAPI backend serves:
- market intelligence APIs
- order management APIs
- watchlist and signal endpoints
- notification endpoints

It should be run with a process manager such as:
- systemd
- Docker Compose
- Kubernetes (for larger scale)

### 3.3 Workers
Background workers handle:
- periodic price updates
- market news processing
- signal generation
- portfolio monitoring
- alert delivery

---

## 4. Environment Requirements

### Minimum server requirements
- CPU: 2+ vCPUs
- Memory: 4 GB RAM
- Storage: 50 GB SSD
- OS: Ubuntu 22.04 LTS or similar

### Software requirements
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Nginx
- Git

---

## 5. Installation Steps

### 5.1 Clone repository

```bash
git clone <your-repo-url>
cd AI Market Investor
```

### 5.2 Backend setup

```bash
cd service/server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5.3 Frontend setup

```bash
cd ../frontend
npm install
npm run build
```

### 5.4 Database setup

Create a PostgreSQL database and user:

```sql
CREATE DATABASE ai_trader;
CREATE USER ai_trader_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE ai_trader TO ai_trader_user;
```

Set environment variables:

```bash
export DATABASE_URL="postgresql://ai_trader_user:strong_password@localhost:5432/ai_trader"
export REDIS_URL="redis://localhost:6379/0"
export SECRET_KEY="change-this-secret"
```

---

## 6. Running the Services

### 6.1 Start backend

```bash
cd service/server
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 6.2 Start background workers

```bash
python worker.py
```

### 6.3 Serve frontend

Deploy the built files under the frontend build output to Nginx or another web server.

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/AI Market Investor/frontend;
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 7. Docker Deployment Option

### 7.1 Docker Compose example

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ai_trader
      POSTGRES_USER: ai_trader_user
      POSTGRES_PASSWORD: strong_password
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  backend:
    build: ./service/server
    environment:
      DATABASE_URL: postgresql://ai_trader_user:strong_password@db:5432/ai_trader
      REDIS_URL: redis://redis:6379/0
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  frontend:
    build: ./service/frontend
    ports:
      - "3000:3000"
```

---

## 8. Security Checklist

Before production deployment, ensure:
- Strong passwords are used
- HTTPS is enabled with TLS certificate
- API keys are stored in environment variables or a secret manager
- CORS is restricted to trusted domains
- Authentication and authorization are enabled
- Logs and metrics are collected

---

## 9. Monitoring and Operations

### Recommended monitoring
- Uptime monitoring for API and frontend
- Database health checks
- Redis connectivity checks
- Background worker health
- Market data ingestion failure alerts

### Useful tools
- Prometheus + Grafana
- Sentry for error tracking
- ELK / OpenSearch for logs
- Uptime Kuma for service monitors

---

## 10. Recommended Production Rollout Plan

### Phase 1: staging deployment
- Deploy backend and frontend to a staging server
- Validate authentication, watchlist, and market data ingestion
- Test order simulation and notifications

### Phase 2: production deployment
- Deploy with reverse proxy and SSL
- Enable background workers
- Configure monitoring and alerting

### Phase 3: hardening
- Add failover and backup strategy
- Introduce rate limiting and cache tuning
- Improve observability and incident runbooks

---

## 11. Final Recommendation

For a robust trading platform, the best deployment pattern is:
- Reverse proxy for the UI and API
- Separate backend service and background workers
- PostgreSQL + Redis as the core data layer
- Monitoring and alerting configured from day one

This design gives you a scalable foundation for market monitoring, signal generation, order management, and customer notifications.
