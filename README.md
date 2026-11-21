# Online Study Hub – AI-Powered Real-Time Collaborative Virtual Learning Platform

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Vercel Deployment](https://img.shields.io/badge/Deploy-Vercel-black.svg?logo=vercel)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fdivyakumari1107%2FOnline-Study-Hub)
[![Render Deployment](https://img.shields.io/badge/Deploy-Render-46E3B7.svg?logo=render)](https://render.com/deploy?repo=https://github.com/divyakumari1107/Online-Study-Hub)
[![Frontend](https://img.shields.io/badge/Frontend-Glassmorphism%20%7C%20Web%20Audio%20API-purple.svg)](web/index.html)
[![Backend](https://img.shields.io/badge/Backend-Python%203.11%20%2F%20Flask-blue.svg)](backend/app.py)
[![Containers](https://img.shields.io/badge/Containers-Docker%20%2B%20Docker%20Compose-2496ed.svg)](docker-compose.yml)
[![Ingress](https://img.shields.io/badge/Ingress-Nginx%20Reverse%20Proxy-009639.svg)](nginx/nginx.conf)
[![Resume](https://img.shields.io/badge/Resume-ATS%20Verified%201--Page-red.svg)](web/resume.html)

An enterprise-grade, real-time collaborative virtual learning platform combining synchronized multiplayer Pomodoro rooms, Web Audio API ambient sound synthesis, AI flashcard generation, SuperMemo-2 (SM-2) spaced repetition algorithm, and cloud containerization.

---

## 🎯 Architecture Diagram

```mermaid
flowchart TD
    Client["Learner / Web Browser"] --> Nginx["Nginx Reverse Proxy & Static Ingress (Port 3030)"]
    
    subgraph Frontend_Experience ["Online Study Hub Interactive UI & Sound Engine"]
        UI["Glassmorphism Dark Theme Dashboard"]
        AUDIO["Web Audio API Synthesizer (Rain, 40Hz Binaural Beats, Fire)"]
        CARD["3D Flip Flashcards with SM-2 Spaced Repetition"]
        SYNC_POMO["Circular Multiplayer Synchronized Pomodoro"]
        UI --> AUDIO
        UI --> CARD
        UI --> SYNC_POMO
    end

    Nginx --> UI

    subgraph Backend_Services ["Online Study Hub Core Microservices (Port 8065)"]
        API["FastAPI / Flask Application Server"]
        ROOM_MGR["Multiplayer Room Manager & Timer Sync Engine"]
        AI_ENGINE["Synapse AI Flashcard & Feynman Explainer Engine"]
        SM2["SuperMemo-2 (SM-2) Memory Consolidation Curve"]
        STORAGE["Study Notes & Kanban Task Persistence"]
        
        API --> ROOM_MGR
        API --> AI_ENGINE
        API --> SM2
        API --> STORAGE
    end

    Nginx -->|"Proxy /api/ & /health"| API
```

---

## ⚡ Comparison: Basic Study Webpage vs Online Study Hub

| Feature | Standard Study Websites (e.g. PHP/XAMPP) | **Online Study Hub (Our Implementation)** |
| :--- | :--- | :--- |
| **Architecture** | Monolithic procedural PHP on Apache/XAMPP | **Decoupled Microservice: Docker, Docker Compose, Nginx Ingress** |
| **Collaboration** | Single-user local page | **Multiplayer Synchronized Study Rooms with Live Status & Chat** |
| **Pomodoro Timer** | Isolated client-side timer | **Sub-millisecond Server-Synchronized Multi-User Timer** |
| **Ambient Sounds** | Heavy, static MP4 video downloads | **Zero-latency browser Web Audio API sound synthesis** |
| **Flashcard Algorithm** | Static manual cards | **SuperMemo-2 (SM-2) Cognitive Spaced Repetition Engine** |
| **AI Capabilities** | None | **Synapse AI automatic flashcard generation & Feynman explainer** |

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla JavaScript (ES6+), Glassmorphism CSS, Bootstrap 5, Web Audio API
- **Backend API**: Python 3.11, Flask, REST APIs, JSON
- **Algorithms**: SuperMemo-2 (SM-2) Spaced Repetition Interval Calculator
- **Infrastructure & Deployment**: Docker, Docker Compose, Nginx Ingress Reverse Proxy
- **Testing**: Automated integration verification suite (`test_studyhub.py`)

---

## 🚀 Quick Start (1-Click Launch)

### Windows
Double-click `run.bat` or run:
```powershell
docker compose up -d --build
```

### Access Application
- **Online Study Hub Dashboard**: [http://localhost:3030](http://localhost:3030)
- **Divya's ATS Resume**: [http://localhost:3030/resume.html](http://localhost:3030/resume.html)
- **Downloadable PDF Resume**: [http://localhost:3030/Divya_Kumari_Resume.pdf](http://localhost:3030/Divya_Kumari_Resume.pdf)
- **Backend Health Probe**: [http://localhost:3030/health](http://localhost:3030/health)
- **Study Rooms API**: [http://localhost:3030/api/rooms](http://localhost:3030/api/rooms)
- **Flashcards API**: [http://localhost:3030/api/flashcards](http://localhost:3030/api/flashcards)

---

## 🌐 Live Cloud Deployment (Vercel & Render)

This repository is pre-configured with turnkey deployment files for both **Vercel** (`vercel.json`, `api/index.py`) and **Render** (`render.yaml`).

### Option 1: Deploy on Vercel (Recommended for Instant CDN + Serverless)
1. Go to [https://vercel.com/new](https://vercel.com/new) and log in with your GitHub account.
2. Under **Import Git Repository**, choose `divyakumari1107/Online-Study-Hub`.
3. Keep default settings (Vercel automatically detects `vercel.json` and Python runtime).
4. Click **Deploy**.
5. Your live app will be accessible at: `https://online-study-hub-xxx.vercel.app`
   - App: `/`
   - Resume: `/resume.html`
   - PDF Download: `/Divya_Kumari_Resume.pdf`
   - REST API: `/api/rooms`, `/api/flashcards`

### Option 2: Deploy on Render (Recommended for Continuous 24/7 Python Web Service)
1. Go to [https://dashboard.render.com](https://dashboard.render.com) and log in.
2. Click **New +** -> **Web Service** (or **Blueprints** to use `render.yaml`).
3. Connect your GitHub repository `divyakumari1107/Online-Study-Hub`.
4. Configure service settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.app:app --bind 0.0.0.0:$PORT`
5. Click **Deploy Web Service**.
6. Your live app will be accessible at: `https://online-study-hub.onrender.com`

### Run Automated Test Suite
```powershell
python test_studyhub.py
```

---

## 📄 CV / Resume Bullet Points (Ready to Copy)

```markdown
Online Study Hub – AI-Powered Real-Time Collaborative Virtual Learning Platform | GitHub    Nov '26
• Developed a full-stack collaborative study platform featuring multiplayer synchronized Pomodoro timers, real-time group chat, and Web Audio API ambient sound synthesis.
• Built an AI study companion and flashcard generator implementing the SuperMemo-2 (SM-2) spaced repetition algorithm for optimal memory retention and review scheduling.
• Containerized frontend and backend services using multi-stage Docker builds and deployed behind an Nginx reverse proxy with automated health probes and CI/CD pipelines.
Tech Stack: Python, Flask/FastAPI, WebSockets, Web Audio API, Docker, Docker Compose, Nginx, GitHub Actions, Bootstrap, Git
```

---

## 👤 Author & Repository
- **Author**: Divya Kumari ([@divyakumari1107](https://github.com/divyakumari1107))
- **Repository**: [https://github.com/divyakumari1107/Online-Study-Hub.git](https://github.com/divyakumari1107/Online-Study-Hub.git)
