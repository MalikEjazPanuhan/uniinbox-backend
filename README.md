---
title: UniInbox AI
emoji: 📧
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# UniInbox AI - Personal AI Communication Agent

Multi-persona AI communication platform for professionals.

## Features

- 🤖 AI-powered reply suggestions
- 👤 Multi-persona support (Doctor, Realtor, Developer, etc.)
- 📧 Unified inbox for multiple channels
- 🔐 Secure authentication with JWT
- 🗄️ PostgreSQL database

## API Documentation

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- Health Check: `/health`

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django-style secret key |
| `ENCRYPTION_KEY` | For encryption |
| `JWT_SECRET_KEY` | JWT signing key |
| `OPENAI_API_KEY` | OpenAI API key |
| `DATABASE_URL` | PostgreSQL connection string |

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- OpenAI API
- JWT Authentication
---
