markdown
# UniInbox AI Backend

A Personal AI Communication Agent - Multi-persona AI-powered email assistant with Gmail integration, AI draft generation, and intelligent communication management.

---

## 🚀 **Live API**
- **Swagger UI:** https://malik-2025-uniinbox-ai.hf.space/docs
- **ReDoc:** https://malik-2025-uniinbox-ai.hf.space/redoc
- **Health Check:** https://malik-2025-uniinbox-ai.hf.space/health

---

## 📋 **Table of Contents**
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Schema](#database-schema)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ **Features**

### 🤖 **AI-Powered Communication**
- **AI Draft Generation**: Generate professional email drafts using GitHub Models (free tier)
- **Persona-Based Responses**: Each user can create multiple AI personas (Doctor, Realtor, Developer, etc.)
- **Man-in-the-Loop Review**: AI suggests → User reviews → Approve/Edit/Reject before sending
- **Context-Aware Suggestions**: AI replies based on conversation history

### 📧 **Multi-Channel Support**
- **Gmail Integration**: Connect Gmail accounts (OAuth 2.0)
- **Unified Inbox**: View messages from all channels in one place
- **Channel Management**: Connect, disconnect, and sync channels
- **Mock Channel Support**: Test without real credentials

### 👤 **Persona Management**
- **Create Personas**: AI-generated personas based on user profile
- **Industry-Specific**: Healthcare, Real Estate, Banking, Software Development, etc.
- **Customizable**: Edit persona context, tone, and signature
- **Default Persona**: Set a default persona for quick access

### 🔐 **Authentication & Security**
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: SHA256 encryption for passwords
- **Role-Based Access**: Protected routes and endpoints
- **Session Management**: Token refresh and expiration

### 📊 **Message Management**
- **Unified Inbox**: View all messages across channels
- **Read/Unread Tracking**: Mark messages as read or unread
- **Flagging**: Flag important messages
- **Reply System**: Reply to messages with AI assistance
- **Thread View**: View full conversation threads

---

## 🛠️ **Tech Stack**

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.104.1 | Web framework |
| **Python** | 3.11+ | Programming language |
| **SQLAlchemy** | 2.0.23 | ORM for database |
| **PostgreSQL** | 15+ | Database (Supabase) |
| **Alembic** | 1.12.1 | Database migrations |
| **Pydantic** | 2.5.0 | Data validation |
| **JWT** | 2.8.0 | Authentication |
| **OpenAI** | 1.3.0 | AI integration (GitHub Models) |
| **Celery** | 5.3.4 | Background tasks |
| **Redis** | 5.0.1 | Caching and queues |
| **Google API** | 2.108.0 | Gmail integration |
| **Uvicorn** | 0.24.0 | ASGI server |
| **Docker** | - | Containerization |

### AI Models
| Provider | Model | Purpose |
|----------|-------|---------|
| **GitHub Models** | `gpt-4o-mini` | AI draft generation |
| **GitHub Models** | `gpt-4o` | High-quality drafts |
| **GitHub Models** | `DeepSeek-R1` | Reasoning tasks |

---

## 🏗️ **Architecture**
┌─────────────────────────────────────────────────────────────┐
│ Frontend (React) │
│ http://localhost:5173 │
└─────────────────────────┬───────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ FastAPI │
│ (Hugging Face Spaces) │
│ https://malik-2025-uniinbox-ai.hf.space │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ API │ │ Auth │ │ AI │ │ Gmail │ │
│ │ Routes │ │ JWT │ │Service │ │ OAuth │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────┘ │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Persona │ │ Message │ │ Channel │ │
│ │ Service │ │ Service │ │ Service │ │
│ └─────────┘ └─────────┘ └─────────┘ │
└─────────────────────────┬───────────────────────────────────┘
│
┌───────────┴───────────┐
▼ ▼
┌─────────────────────────┐ ┌─────────────────────────┐
│ PostgreSQL (Supabase) │ │ GitHub Models (AI) │
│ Database │ │ Free Tier Models │
└─────────────────────────┘ └─────────────────────────┘

text

---

## 📚 **API Endpoints**

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Register new user |
| `POST` | `/api/v1/auth/login` | Login and get JWT token |
| `POST` | `/api/v1/auth/refresh` | Refresh access token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/users/me` | Get current user profile |
| `PUT` | `/api/v1/users/me/update` | Update user profile |
| `GET` | `/api/v1/users/preferences` | Get user preferences |
| `PUT` | `/api/v1/users/preferences` | Update preferences |

### Personas
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/personas/` | Create persona |
| `GET` | `/api/v1/personas/` | List all personas |
| `GET` | `/api/v1/personas/{id}` | Get persona by ID |
| `PUT` | `/api/v1/personas/{id}` | Update persona |
| `DELETE` | `/api/v1/personas/{id}` | Delete persona |
| `POST` | `/api/v1/personas/{id}/set-default` | Set as default persona |

### Onboarding (AI Persona Generation)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/onboarding/generate-persona` | Generate AI persona |
| `POST` | `/api/v1/onboarding/save-persona` | Save generated persona |
| `GET` | `/api/v1/onboarding/industries` | Get supported industries |
| `GET` | `/api/v1/onboarding/industry-questions/{industry}` | Get industry questions |

### Messages
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/messages/` | List messages |
| `POST` | `/api/v1/messages/` | Create message |
| `GET` | `/api/v1/messages/{id}` | Get message |
| `PUT` | `/api/v1/messages/{id}/read` | Mark as read |
| `PUT` | `/api/v1/messages/{id}/unread` | Mark as unread |
| `PUT` | `/api/v1/messages/{id}/flag` | Toggle flag |
| `POST` | `/api/v1/messages/{id}/reply` | Reply to message |
| `GET` | `/api/v1/messages/thread/{thread_id}` | Get thread |

### Channels
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/channels/` | Connect channel |
| `GET` | `/api/v1/channels/` | List channels |
| `GET` | `/api/v1/channels/{id}` | Get channel |
| `PUT` | `/api/v1/channels/{id}` | Update channel |
| `DELETE` | `/api/v1/channels/{id}` | Disconnect channel |
| `POST` | `/api/v1/channels/{id}/sync` | Sync channel |
| `POST` | `/api/v1/channels/{id}/send-email` | Send email via Gmail |

### AI Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/ai/suggestions` | Get AI reply suggestions |
| `POST` | `/api/v1/ai/draft` | Generate AI draft |
| `POST` | `/api/v1/ai/summarize` | Summarize thread |

---

## 📦 **Installation**

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Git

### Clone the Repository
```bash
git clone https://github.com/MalikEjazPanuhan/uniinbox-backend.git
cd uniinbox-backend
Create Virtual Environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Install Dependencies
bash
pip install -r requirements.txt
Environment Variables
bash
# Copy example env file
cp .env.example .env

# Edit .env with your values
nano .env
Database Setup
bash
# Run migrations
alembic upgrade head

# Seed default data (optional)
python scripts/seed_personas.py
Run Development Server
bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
Access API Documentation
Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

🔑 Environment Variables
Variable	Description	Required
SECRET_KEY	Django-style secret key	✅ Yes
ENCRYPTION_KEY	For encryption	✅ Yes
JWT_SECRET_KEY	JWT signing key	✅ Yes
DATABASE_URL	PostgreSQL connection string	✅ Yes
REDIS_URL	Redis connection URL	✅ Yes
CELERY_BROKER_URL	Celery broker URL	✅ Yes
CELERY_RESULT_BACKEND	Celery result backend	✅ Yes
GITHUB_TOKEN	GitHub token for AI Models	✅ Yes
HF_TOKEN	Hugging Face token	✅ Yes
GMAIL_CLIENT_ID	Google OAuth client ID	❌ No
GMAIL_CLIENT_SECRET	Google OAuth client secret	❌ No
GMAIL_REDIRECT_URI	Gmail OAuth callback URL	❌ No
ALLOWED_ORIGINS	CORS allowed origins	✅ Yes
LLM_MODEL	AI model to use	✅ Yes
ACCESS_TOKEN_EXPIRE_MINUTES	JWT access token expiry	✅ Yes
REFRESH_TOKEN_EXPIRE_DAYS	JWT refresh token expiry	✅ Yes
PYTHON_VERSION	Python version	✅ Yes
🗄️ Database Schema
Users Table
sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    job_title VARCHAR(255),
    default_persona_id UUID,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
Personas Table
sql
CREATE TABLE personas (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    persona_type VARCHAR(50) NOT NULL,
    context JSONB NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
Messages Table
sql
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    channel_id UUID REFERENCES channels(id),
    persona_id UUID REFERENCES personas(id),
    subject VARCHAR(500),
    body TEXT,
    sender JSONB NOT NULL,
    recipients JSONB NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
Channels Table
sql
CREATE TABLE channels (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    channel_type VARCHAR(50) NOT NULL,
    channel_name VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
🚀 Deployment
Hugging Face Spaces
Create a Space:

Go to https://huggingface.co/new-space

Select Docker as SDK

Choose Free CPU hardware

Push Code:

bash
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/uniinbox-ai
git push hf main
Add Secrets:

Go to Space Settings → Variables and secrets

Add all environment variables

Deploy:

The Space will automatically rebuild on push

Wait for the build to complete

Docker Deployment
bash
# Build the image
docker build -t uniinbox-backend .

# Run the container
docker run -p 8000:8000 --env-file .env uniinbox-backend
Docker Compose
bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# Stop all services
docker-compose -f docker/docker-compose.yml down
🧪 Testing
bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api/test_auth.py
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
Proprietary - All rights reserved. This project is for portfolio demonstration purposes only.

📞 Contact
Author: Malik Ejaz

Email: malikejaz6858@gmail.com

GitHub: https://github.com/MalikEjazPanuhan

Live API: https://malik-2025-uniinbox-ai.hf.space

🙏 Acknowledgments
FastAPI - Modern web framework

Hugging Face - Free hosting with Docker support

Supabase - PostgreSQL database hosting

GitHub Models - Free AI model access

OpenAI - AI capabilities

Google - Gmail API integration

📊 API Statistics
Endpoint Group	Count
Authentication	3
Users	4
Personas	6
Onboarding	4
Messages	8
Channels	7
AI Features	3
Total	35
🎯 Roadmap
User Authentication

Persona Management

AI Draft Generation

Message Management

Channel Integration

Gmail OAuth

Real-time Notifications

WebSocket Support

Mobile App

Analytics Dashboard

Built with ❤️ by Malik Ejaz

text

---

## ✅ **Save and Commit**

```powershell
cd F:\uniinbox\backend
git add README.md
git commit -m "Add comprehensive README.md for backend"
git push origin main
