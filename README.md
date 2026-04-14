# E-Voting 2.0

**Production-grade secure online voting platform** built with FastAPI & MongoDB Atlas

[![Live on AWS EC2](https://img.shields.io/badge/Live%20on-AWS%20EC2-ff9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://evoting.jaayysoni.com)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.1-green)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen)](https://www.mongodb.com/cloud/atlas)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Live Demo:** [https://evoting.jaayysoni.com](https://evoting.jaayysoni.com)

## **Screenshots**

| Dashboard | EC Signup |
|-----------|-----------|
| <img src="https://github.com/user-attachments/assets/77946883-d032-4e3f-a870-aaf0f5a515e9" alt="Dashboard" width="500"/> | <img src="https://github.com/user-attachments/assets/fa5bb9f2-27a1-4595-b095-34ae9f2388a7" alt="EC Signup" width="500"/> |

| EC Login | EC Dashboard 1 |
|----------|----------------|
| <img src="https://github.com/user-attachments/assets/2a9f9431-c7ff-4b0b-a13e-920bc54ab7ea" alt="EC Login" width="500"/> | <img src="https://github.com/user-attachments/assets/cac460b2-9aa8-4c68-b7ab-da1279c07e68" alt="EC Dashboard 1" width="500"/> |

| EC Dashboard 2 | Voter Login |
|----------------|------------|
| <img src="https://github.com/user-attachments/assets/8057ab0e-71d0-43ce-acb7-b33a9d65cecb" alt="EC Dashboard 2" width="500"/> | <img src="https://github.com/user-attachments/assets/27efb621-7cf6-4ede-8d3f-5656e4543dbc" alt="Voter Login" width="500"/> |

| Voting Page | Result Page |
|-------------|------------|
| <img src="https://github.com/user-attachments/assets/2d4b9c80-4f94-456a-8f59-8ec8e3002597" alt="Voting Page" width="500"/> | <img src="https://github.com/user-attachments/assets/05e39779-63a8-4d4c-bca7-8972e0f89bf2" alt="Result Page" width="500"/> |

| Thank You Page |
|----------------|
| <img width="1465" height="834" alt="Screenshot 2026-01-18 at 15 47 59" src="https://github.com/user-attachments/assets/81cd1dde-d9f4-4860-8bf7-ba023d7c5c7b" />| |

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Security Design](#security-design)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Screenshots](#screenshots)
- [License](#license)

---

## Overview

E-Voting 2.0 is a secure, scalable, cloud-deployed online voting system designed to simulate real-world election workflows for Election Commissions (ECs). The platform supports multiple concurrent elections, guarantees 100% vote integrity through UUID-based vote tokens, and delivers real-time result computation.

> Built with a **backend-first mindset** — focused on data integrity, role-based access control, and production-ready architecture.

### What problems does it solve?

Traditional voting systems struggle with duplicate vote prevention, real-time result aggregation, and secure multi-role access. E-Voting 2.0 addresses all three with a clean, API-driven architecture that separates EC and voter concerns while maintaining a single source of truth in MongoDB.

---

## Key Features

### For Election Commissions
- Secure registration and login
- Create elections with configurable start/end timelines
- Add and remove candidates with profile images
- Add and remove registered voters
- Real-time dashboard showing total voters and votes cast

### For Voters
- Secure login with bcrypt-hashed credentials
- View candidates with party information and profile images
- Cast vote using a unique UUID-based vote token
- Full duplicate vote prevention — once voted, login is blocked

### Results Module
- Real-time vote counting and percentage computation
- Automatic winner detection with draw handling
- Clean result UI accessible via election ID

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, FastAPI |
| Database | MongoDB Atlas |
| Frontend | Jinja2, Tailwind CSS, HTML, JavaScript |
| Authentication | bcrypt password hashing |
| File Storage | Local static file serving via FastAPI |
| CI/CD | GitHub Actions |
| Deployment | AWS EC2 |
| Testing | pytest |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Client                           │
│              (Browser — Jinja2 Templates)               │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP Requests
┌───────────────────────▼─────────────────────────────────┐
│                   FastAPI Application                   │
│                                                         │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐  │
│   │  EC Routes  │   │Voter Routes │   │Result Routes│  │
│   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘  │
│          │                 │                  │         │
│   ┌──────▼─────────────────▼──────────────────▼──────┐  │
│   │              Business Logic / Services           │  │
│   │   register_ec | add_candidate | vote validation  │  │
│   └──────────────────────┬───────────────────────────┘  │
└──────────────────────────┼──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│                    MongoDB Atlas                        │
│                                                         │
│   ┌──────────────┐        ┌────────────────────────┐   │
│   │  ec_col      │        │      voters_col        │   │
│   │  - EC info   │        │  - voter credentials   │   │
│   │  - election  │        │  - has_voted flag      │   │
│   │  - candidates│        │  - vote_token (UUID)   │   │
│   └──────────────┘        └────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Data Flow — Voting

```
Voter Login → Credential Check → Duplicate Vote Check
     → Render Ballot → Submit Vote → Generate UUID Token
     → Update voter (has_voted=True, vote_token) → Thank You Page
```

---

## Project Structure

```
E-voting2.0/
│
├── app/                        # Main backend application
│   ├── main.py                 # FastAPI entry point, all route definitions
│   ├── users/
│   │   ├── models.py           # EC data models
│   │   ├── schemas.py          # Pydantic schemas for request validation
│   │   └── services.py         # Business logic — register EC, add candidate
│   └── voters/
│       ├── models.py           # Voter data models
│       └── schemas.py          # Voter Pydantic schemas
│
├── db/
│   └── db.py                   # MongoDB connection, collection references
│
├── static/
│   └── uploads/
│       └── candidates/         # Uploaded candidate profile images
│
├── templates/                  # Jinja2 HTML templates
│   ├── Dashboard.html          # Universal election dashboard
│   ├── EC-dashboard.html       # EC management panel
│   ├── EC-login.html
│   ├── EC-signup.html
│   ├── Login.html              # Voter login
│   ├── vote.html               # Ballot page
│   ├── Result.html             # Election results
│   ├── thankyou.html           # Post-vote confirmation
│   └── instruction.html
│
├── tests/
│   └── test_dummy.py           # pytest test suite
│
├── requirements.txt
└── README.md
```

---

## API Reference

### EC Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Universal dashboard — all elections with status |
| GET | `/ec/signup` | EC registration page |
| POST | `/ec/signup` | Register new Election Commission |
| GET | `/ec/login` | EC login page |
| POST | `/ec/login` | Authenticate EC, redirect to dashboard |
| GET | `/ec/dashboard?election_id=` | EC management dashboard |
| POST | `/create-election` | Create election with timeline |
| POST | `/add-candidate` | Add candidate with optional profile image |
| POST | `/remove-candidate/{candidate_id}` | Remove candidate from election |
| POST | `/add-voter` | Register voter to election |
| POST | `/remove-voter/{voter_id}` | Remove voter from election |

### Voter Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/voter/login` | Voter login page |
| POST | `/voter/login` | Authenticate voter, render ballot |
| POST | `/vote` | Submit vote, generate UUID token |

### Result Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/result?election_id=` | View real-time election results |
| GET | `/instructions?election_id=` | Voting instructions page |

---

## Security Design

### Authentication
- EC and voter passwords are hashed using **bcrypt** with auto-generated salts
- Passwords are never stored or compared in plaintext
- Role separation — EC routes and voter routes are fully independent

### Vote Integrity
- Each voter receives a unique **UUID vote token** on successful vote submission
- The `has_voted` flag is set atomically on vote submission
- Duplicate vote attempts are blocked at login — already-voted users cannot access the ballot
- Candidate IDs and voter IDs are validated using ObjectId regex and UUID checks before any DB operation

### Input Validation
- All form inputs go through Pydantic schema validation
- ObjectId values validated with `^[0-9a-fA-F]{24}$` regex before DB queries
- File uploads restricted to `.jpg`, `.jpeg`, `.png`, `.gif` extensions
- Environment-based secrets — no credentials hardcoded

### Edge Cases Handled
- Duplicate voter email prevention
- Invalid or missing candidate/voter IDs
- Elections with zero votes (safe division handling in result computation)
- Draw detection when multiple candidates have equal top votes
- Missing profile images fall back to default image gracefully

---

## Getting Started

### Prerequisites

- Python 3.13+
- MongoDB Atlas account (or local MongoDB)
- Git

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/jaayysoni/E-voting2.0.git
cd E-voting2.0
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

**3. Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the root directory:
```env
MONGO_URI=your_mongodb_atlas_connection_string
DB_NAME=evoting
```

**5. Start the development server**
```bash
uvicorn app.main:app --reload
```

**6. Open in browser**
```
http://localhost:8000
```

---

## Running Tests

```bash
pytest tests/
```

---

## CI/CD Pipeline

The project uses **GitHub Actions** for automated deployment.

```
Push to main branch
       │
       ▼
GitHub Actions triggered
       │
       ▼
Install dependencies & run tests
       │
       ▼
SSH into AWS EC2 instance
       │
       ▼
Pull latest code & restart server
```

The workflow file is located at `.github/workflows/deploy.yml`.

---

## Screenshots

| Dashboard | EC Signup |
|-----------|-----------|
| ![Dashboard](https://github.com/user-attachments/assets/77946883-d032-4e3f-a870-aaf0f5a515e9) | ![EC Signup](https://github.com/user-attachments/assets/fa5bb9f2-27a1-4595-b095-34ae9f2388a7) |

| EC Login | EC Dashboard |
|----------|--------------|
| ![EC Login](https://github.com/user-attachments/assets/2a9f9431-c7ff-4b0b-a13e-920bc54ab7ea) | ![EC Dashboard](https://github.com/user-attachments/assets/cac460b2-9aa8-4c68-b7ab-da1279c07e68) |

| Voting Page | Result Page |
|-------------|-------------|
| ![Voting Page](https://github.com/user-attachments/assets/2d4b9c80-4f94-456a-8f59-8ec8e3002597) | ![Result Page](https://github.com/user-attachments/assets/05e39779-63a8-4d4c-bca7-8972e0f89bf2) |

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Licensed under the **MIT License** — free to use, modify, and distribute for learning or development purposes. See the [LICENSE](LICENSE) file for details.

---

> Built by [Jay Soni](https://sde-jaysoni-portfolio.vercel.app) · [GitHub](https://github.com/jaayysoni) · [LinkedIn](https://www.linkedin.com/in/jaayysoni)



