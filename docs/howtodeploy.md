# 🚀 Project Deployment Guide

This guide describes two deployment strategies:

* ⚡ **Hackathon Deployment** – Optimized for rapid local development and demonstrations.
* ☁️ **Production Deployment** – Designed for long-term scalability, reliability, and maintainability.

---

# ⚡ Hackathon Deployment (Quick Local Setup)

During a hackathon, rapid setup is essential. Follow these steps to launch the application locally in just a few minutes.

## 1. Clone the Repository

Open a terminal and clone the project.

```bash
git clone https://github.com/TienNhat5103/X_project.git
cd X_project
```

---

## 2. Start the Backend

Open a new terminal window (**Terminal 1**) and execute:

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

python main.py
```

---

## 3. Start the Frontend

Open another terminal (**Terminal 2**) and run:

```bash
cd frontend

streamlit run app.py
```

---

## 4. Access the Application

Once both services are running, open your browser and navigate to:

> **Local URL:**
> http://localhost:8501

---

# ☁️ Production Deployment (Long-Term Architecture)

While the hackathon version prioritizes development speed, a production deployment requires improved reliability, scalability, and security.

Instead of manually running multiple scripts, the application should be deployed using containers and cloud infrastructure.

---

# 🧱 Phase 1: Containerization (Docker)

Package each component into its own Docker container to ensure a consistent execution environment across different platforms.

### Project Structure

```
backend/
├── Dockerfile

frontend/
├── Dockerfile

docker-compose.yml
```

### Components

* **backend/Dockerfile**

  * Packages the FastAPI backend service.

* **frontend/Dockerfile**

  * Packages the Streamlit frontend application.

* **docker-compose.yml**

  * Orchestrates all services.
  * Starts the complete application with a single command:

```bash
docker-compose up --build
```

---

# ☁️ Phase 2: Cloud Deployment

Replace local execution with cloud-hosted services for public accessibility.

## Recommended Architecture

| Component       | Recommended Services                       |
| --------------- | ------------------------------------------ |
| **Frontend**    | Streamlit Community Cloud, Render, AWS ECS |
| **Backend API** | Render, Railway, AWS EC2, AWS ECS          |
| **Database**    | Supabase (PostgreSQL), MongoDB Atlas       |

### Architecture Overview

```
Users
   │
   ▼
Frontend (Streamlit)
   │
   ▼
Backend API (FastAPI)
   │
   ▼
Cloud Database
(PostgreSQL / MongoDB)
```

---

# 🛠️ Phase 3: Production Best Practices

For a reliable production environment, implement the following best practices.

## 🔐 Environment Variables

Avoid hardcoding:

* API keys
* Database credentials
* Secret tokens

Instead, store sensitive configuration in a `.env` file and configure them through your cloud provider.

Example:

```env
DATABASE_URL=...
SUPABASE_URL=...
SUPABASE_KEY=...
SECRET_KEY=...
```

---

## ⚙️ Production ASGI Server

Running

```bash
python main.py
```

is suitable for development but not for production.

Instead, use a production-grade ASGI server such as **Uvicorn** or **Gunicorn**.

Example:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🔄 CI/CD Pipeline

Automate testing and deployment using **GitHub Actions**.

A typical workflow includes:

1. Push code to the `main` branch.
2. Execute automated tests.
3. Build Docker images.
4. Deploy to the cloud automatically.

This eliminates manual deployment and ensures every release is validated before going live.

---

# 📌 Recommended Production Stack

| Layer            | Technology                 |
| ---------------- | -------------------------- |
| Frontend         | Streamlit                  |
| Backend          | FastAPI                    |
| Containerization | Docker & Docker Compose    |
| Database         | Supabase (PostgreSQL)      |
| Deployment       | Render / Railway / AWS ECS |
| CI/CD            | GitHub Actions             |
| ASGI Server      | Uvicorn                    |

---
