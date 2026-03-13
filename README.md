# Autonomous B2B Sales Agent

![React](https://img.shields.io/badge/React-18-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.111-blue) ![LangGraph](https://img.shields.io/badge/LangGraph-Production-orange)

A modular, production-oriented multi-tenant SaaS for driving autonomous B2B cold outreach leveraging LLMs and Agentic Workflows.

## Overview
This platform allows users to instruct an AI autonomous agent with target ICPs and messaging. The agent scales out using LangGraph to discover leads, enrich context, score them, and natively draft hyper-personalized copy for outbound outreach.

## Getting Started Locally

### Prerequisites
- Docker & Docker Compose
- Node.js 20 & Python 3.12 (if running natively)

### Using Docker Compose (Recommended)
You can bring up the entire stack using Docker.

1. Create environment configs:
```bash
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env
```
2. Start the magic:
```bash
make start
# OR simply run
docker-compose up --build
```
3. App will be live at `http://localhost:5173/` and backend at `http://localhost:8000/`.

## Architecture Details
Please view the detailed architectural specifications within the `/docs` folder:
- [System Architecture](./docs/SYSTEM_ARCHITECTURE.md)
- [Agent Workflow](./docs/AGENT_WORKFLOW.md)
- [Deployment Guide](./docs/DEPLOYMENT_GUIDE.md)

## Launching to Production
Follow the **[Production Launch Checklist](./docs/PRODUCTION_LAUNCH_CHECKLIST.md)** exactly before distributing to customers to ensure secure CORS configuration, proper environment proxies, and applied DB migrations.
