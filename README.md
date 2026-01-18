# E-Voting 2.0

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.1-green)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen)](https://www.mongodb.com/cloud/atlas)

---

## **Project Overview**

E-Voting 2.0 is a **secure, scalable, cloud-deployed online voting platform** built with **Python, FastAPI, and MongoDB Atlas**, designed to modernize election management for Election Commissions (ECs) while providing voters a seamless, risk-free voting experience.  

This project demonstrates **advanced backend engineering skills**, including **asynchronous request handling, secure authentication, database modeling, and real-time data processing**, making it a perfect showcase for production-grade system design.

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

### **Key Highlights**

- Multi-election support with isolated voter and candidate pools
- Secure authentication with bcrypt, session management, and role-based access (EC vs Voter)
- Real-time vote tracking and accurate result computation
- Fully deployable cloud architecture with CI/CD automation
- Interactive dashboards for ECs and voters
- Handles **edge cases and security constraints**, like duplicate votes, invalid IDs, and default candidate images

---

## **Problem Statement**

Traditional elections are often:

- Manual and error-prone
- Difficult to scale
- Vulnerable to tampering and delays

**E-Voting 2.0 solves these problems** by:

- Enabling **secure online voting** with data integrity
- Allowing ECs to **create elections, add candidates, and track results**
- Providing voters a **fast, interactive voting experience**
- Maintaining **auditability** with vote tokens and accurate logs

---

## **Objective**

The primary objective is to design and implement a **real-world, backend-focused voting system** that demonstrates:

- Scalable system design for multiple elections and users
- Secure user authentication and role management
- Efficient data storage, validation, and retrieval in MongoDB
- Real-time updates and frontend-backend synchronization
- Production-ready deployment using cloud platforms and CI/CD pipelines

---

## **Engineering Approach**

E-Voting 2.0 follows **industry-standard backend engineering principles**:

1. **Backend-first architecture:** Built with FastAPI for asynchronous, low-latency APIs.
2. **Database Modeling:** MongoDB Atlas collections for ECs, voters, elections, and candidates.
3. **Secure Authentication:** bcrypt password hashing, session handling, and voter role checks.
4. **Data Validation:** UUIDs for voters, ObjectId checks, and vote integrity verification.
5. **Real-Time System Simulation:** Immediate vote updates and result calculations.
6. **Error Handling & Edge Cases:** Duplicate votes, invalid IDs, empty candidate fields, and default images.
7. **Deployment & CI/CD:** Cloud deployment on Render with GitHub Actions for automated builds, testing, and releases.

---

## **Features**

### **EC Dashboard**

- Create elections with start and end dates
- Add or remove candidates (with optional images)
- Add or remove voters
- Track total voters and votes cast in real time

### **Voter Portal**

- Secure login and role validation
- Display candidate profiles with images and party information
- Vote submission with **unique vote tokens**
- Prevent duplicate voting

### **Results Module**

- Real-time computation of votes per candidate
- Percentage calculation for transparency
- Handles **draw scenarios** and winner determination
- Displays results in an interactive, user-friendly format

### **Technical Features**

- Built with **Python 3.13 and FastAPI**
- MongoDB Atlas for scalable, secure data storage
- Password hashing with **bcrypt** for security
- Jinja2 templates + Tailwind CSS for responsive dashboards
- File upload handling for candidate profile images
- Comprehensive validation (UUIDs, ObjectId, duplicate votes)
- Cloud-ready deployment with environment variables
- Automated CI/CD pipeline with GitHub Actions

### **Security & Compliance**

This project implements several security best practices to ensure data integrity and safe operation:

- **Passwords are hashed with bcrypt** for secure storage  
- **Vote integrity** ensured with unique vote tokens  
- **Prevents duplicate voting** by tracking voter status  
- **Input validation** for UUIDs and ObjectIds to prevent invalid data  
- **Default handling** for missing candidate images to avoid broken UI  
- **Cloud-ready**: uses HTTPS and environment-based secrets for deployment

---

## **Tech Stack**

| Layer / Purpose      | Technology / Tool |
|---------------------|-----------------|
| Backend             | Python 3.13, FastAPI |
| Database            | MongoDB Atlas |
| Frontend            | Jinja2, Tailwind CSS, HTML5, CSS3, JavaScript |
| Authentication      | bcrypt, secure password hashing |
| CI/CD               | GitHub Actions |
| Testing             | pytest |

---

## **Project Structure**

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
└── venv/                        # Python virtual environment

```
---

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




