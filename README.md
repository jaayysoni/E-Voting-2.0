# E-Voting 2.0
**Production-grade online voting platform** built with **FastAPI & MongoDB Atlas**

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.1-green)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen)](https://www.mongodb.com/cloud/atlas)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black)](https://github.com/features/actions)

---

## Overview

**E-Voting 2.0** is a **secure, scalable, cloud-deployed online voting system** designed to simulate **real-world election workflows** for Election Commissions (ECs).

The platform supports **multiple concurrent elections**, ensures **100% vote integrity**, and delivers **real-time result computation**, making it a strong demonstration of **backend engineering, system design, and security practices**.

> This project was built with a **backend-first mindset**, focusing on data integrity, role-based access, and production-ready architecture.

---

## Key Results & Impact

-  Supports **multiple simultaneous elections** with fully isolated voter pools  
-  Guarantees **100% duplicate vote prevention** using UUID-based vote tokens  
-  Delivers **real-time vote tracking and instant result computation**  
-  Designed to safely handle concurrent voting requests using async FastAPI  
-  Implements **secure authentication** with bcrypt and role-based access  
-  Handles **15+ edge cases** including duplicate votes, invalid IDs, and missing data  
-  Cloud-ready backend with **automated CI/CD pipeline**

---

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


## Solution

**E-Voting 2.0** addresses these challenges by:

- Enabling **secure online elections** with strong vote integrity  
- Allowing ECs to **create elections, manage voters and candidates**  
- Providing voters with a **simple, fast, and secure voting experience**  
- Ensuring **accurate, real-time result computation**  
- Maintaining **auditability** through vote tokens and logs  

---

## Engineering Approach

The system follows **industry-standard backend engineering principles**:

1. **Backend-First Architecture**  
   - FastAPI with async request handling  
   - Low-latency APIs and clean route separation  

2. **Database Modeling (MongoDB Atlas)**  
   - ECs, elections, voters, candidates, and votes  
   - Proper isolation per election  

3. **Security & Authentication**  
   - bcrypt password hashing  
   - Role-based access (EC vs Voter)  
   - UUID-based vote integrity  

4. **Data Validation & Integrity**  
   - ObjectId validation  
   - UUID validation  
   - Duplicate vote prevention  

5. **Real-Time Simulation**  
   - Immediate vote count updates  
   - On-demand result computation  

6. **Deployment & CI/CD**  
   - Cloud deployment on Render  
   - Automated builds and deployments via GitHub Actions  

---

## Features

### Election Commission (EC)

- Register & login securely  
- Create elections with timelines  
- Add / remove candidates  
- Upload candidate profile images  
- Add / remove voters  
- Track total voters and votes cast  

### Voter Portal

- Secure login with validation  
- View candidates with party & images  
- Vote using **unique vote token**  
- Duplicate voting fully prevented  

### Results Module

- Real-time vote counting  
- Percentage-based results  
- Draw & winner handling  
- Clean, interactive result UI  

---

## Security & Compliance

-  Passwords hashed using **bcrypt**  
-  Unique vote tokens ensure **vote integrity**  
-  Duplicate voting prevention  
-  Input validation for UUIDs & ObjectIds  
-  Safe fallback handling for missing images  
-  Environment-based secrets for deployment  

---

## Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | Python 3.13, FastAPI |
| Database | MongoDB Atlas |
| Frontend | Jinja2, Tailwind CSS, HTML, JavaScript |
| Auth | bcrypt |
| CI/CD | GitHub Actions |
| Testing | pytest |

---

## 📁 Project Structure

```
E-voting2.0/
│
├── app/                        # Main backend application
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── users/                  # EC (Election Commission) related modules
│   │   ├── __init__.py
│   │   ├── models.py           # User/EC data models
│   │   ├── schemas.py          # Pydantic schemas for validation
│   │   └── services.py         # Business logic (register EC, add candidate)
│   └── voters/                 # Voter-related modules
│       ├── __init__.py
│       ├── models.py           # Voter data models
│       └── schemas.py          # Voter Pydantic schemas
│
├── db/                         # Database connection and setup
│   ├── db.py                   # MongoDB connection, collections
│
├── static/                      # Static assets
│   └── uploads/
│       └── candidates/          # Candidate profile images
│
├── templates/                   # Jinja2 HTML templates
│   ├── Dashboard.html
│   ├── EC-dashboard.html
│   ├── EC-login.html
│   ├── EC-signup.html
│   ├── instruction.html
│   ├── Login.html
│   ├── Result.html
│   ├── thankyou.html
│   └── vote.html
│
├── tests/                       # Automated tests
│   └── test_dummy.py
│
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation

```

## Installation & Running Instructions

Follow these steps to set up and run E-Voting 2.0 locally or on your cloud environment:

1. Clone the Repository
```
git clone https://github.com/jaayysoni/E-voting2.0.git
cd E-voting2.0
```
2. Create a Python Virtual Environment
```
python -m venv venv
```
3. Activate the Virtual Environment
	•	Mac/Linux
```
source venv/bin/activate
```
•	Windows (Command Prompt)
```
venv\Scripts\activate
```
•	Windows (PowerShell)
```
.\venv\Scripts\Activate.ps1
```
4. Install Dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```
5. Start the FastAPI Server
```
uvicorn app.main:app --reload
```
6. Access the Application
```
http://localhost:8000
```

## License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this project for learning or development purposes.

See the [LICENSE](LICENSE) file for details.



