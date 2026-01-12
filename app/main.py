from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from passlib.context import CryptContext
import random
import string

# ---------------- FastAPI app ----------------
app = FastAPI(title="E-Voting 2.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------- MongoDB ----------------
client = MongoClient("mongodb://localhost:27017")
db = client["evoting_db"]
ec_collection = db["ecs"]

# ---------------- Password hashing (Argon2) ----------------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using Argon2"""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(password, hashed)

def generate_election_id(length=8) -> str:
    """Generate a random election ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# ---------------- Routes ----------------

# ---------------- Dashboard ----------------
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("Dashboard.html", {"request": request})

# ---------------- EC Signup ----------------
@app.get("/ec/signup", response_class=HTMLResponse)
def ec_signup_get(request: Request):
    return templates.TemplateResponse("EC-signup.html", {"request": request})

@app.post("/ec/signup", response_class=HTMLResponse)
def ec_signup_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    # Validate password match
    if password != confirm_password:
        return templates.TemplateResponse(
            "EC-signup.html",
            {"request": request, "error": "Passwords do not match", "name": name, "email": email}
        )

    # Check if email already exists
    if ec_collection.find_one({"email": email}):
        return templates.TemplateResponse(
            "EC-signup.html",
            {"request": request, "error": "Email already registered", "name": name, "email": email}
        )

    # Hash password and save EC
    hashed_password = hash_password(password)
    election_id = generate_election_id()
    ec_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password,
        "election_id": election_id
    })

    return templates.TemplateResponse(
        "EC-login.html",
        {"request": request, "message": f"Signup successful! Your election ID: {election_id}"}
    )

# ---------------- EC Login ----------------
@app.get("/ec/login", response_class=HTMLResponse)
def ec_login_get(request: Request):
    return templates.TemplateResponse("EC-login.html", {"request": request})

@app.post("/ec/login", response_class=HTMLResponse)
def ec_login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    ec = ec_collection.find_one({"email": email})
    if not ec or not verify_password(password, ec["password"]):
        return templates.TemplateResponse(
            "EC-login.html",
            {"request": request, "error": "Invalid email or password", "email": email}
        )

    return templates.TemplateResponse(
        "EC-dashboard.html",
        {"request": request, "ec": ec}
    )

# ---------------- Vote page placeholder ----------------
@app.get("/vote", response_class=HTMLResponse)
def vote(request: Request):
    return templates.TemplateResponse("vote.html", {"request": request})


@app.get("/auth/google", name="google_oauth_login")
def google_oauth_login():
    return "Google OAuth not implemented yet"