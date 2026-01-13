from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bcrypt import checkpw
from datetime import datetime
from pathlib import Path
import uuid
from bson import ObjectId
from bson.errors import InvalidId
import os

from db.db import ec_col, voters_col
from app.users.services import register_ec, create_election, add_candidate

# ---------------- FastAPI app ----------------
app = FastAPI(title="E-Voting 2.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Ensure upload folder exists
Path("static/uploads").mkdir(parents=True, exist_ok=True)

# ================= DASHBOARD =================
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("Dashboard.html", {"request": request})

# ================= EC SIGNUP =================
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
    if password != confirm_password:
        return templates.TemplateResponse(
            "EC-signup.html",
            {"request": request, "error": "Passwords do not match", "name": name, "email": email}
        )

    success, election_id = register_ec(name, email, password)
    if not success:
        return templates.TemplateResponse(
            "EC-signup.html",
            {"request": request, "error": election_id, "name": name, "email": email}
        )

    return templates.TemplateResponse(
        "EC-login.html",
        {"request": request, "message": f"Signup successful! Your Election ID: {election_id}"}
    )

# ================= EC LOGIN =================
@app.get("/ec/login", response_class=HTMLResponse)
def ec_login_get(request: Request):
    return templates.TemplateResponse("EC-login.html", {"request": request})

@app.post("/ec/login", response_class=HTMLResponse)
def ec_login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    ec = ec_col.find_one({"email": email})
    if not ec or not checkpw(password.encode("utf-8"), ec["password_hash"].encode("utf-8")):
        return templates.TemplateResponse(
            "EC-login.html",
            {"request": request, "error": "Invalid email or password", "email": email}
        )

    return RedirectResponse(f"/ec/dashboard?election_id={ec['election_id']}", status_code=303)

# ================= EC DASHBOARD =================
@app.get("/ec/dashboard", response_class=HTMLResponse)
def ec_dashboard(request: Request, election_id: str):
    ec = ec_col.find_one({"election_id": election_id})
    if not ec:
        return HTMLResponse("EC not found", status_code=404)

    election = ec.get("election", {})
    voters = list(voters_col.find({"election_id": ec["election_id"]}))
    candidates = election.get("candidates", [])

    total_voters = len(voters)
    votes_cast = sum(1 for v in voters if v.get("has_voted"))

    return templates.TemplateResponse(
        "EC-dashboard.html",
        {
            "request": request,
            "ec": ec,
            "election": election,
            "voters": voters,
            "candidates": candidates,
            "total_voters": total_voters,
            "votes_cast": votes_cast
        }
    )

# ================= CREATE ELECTION =================
@app.post("/create-election", response_class=HTMLResponse)
def create_election_post(
    request: Request,
    election_id: str = Form(...),
    name: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...)
):
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    create_election(election_id, name, start_dt, end_dt)

    return RedirectResponse(f"/ec/dashboard?election_id={election_id}", status_code=303)

# ================= ADD VOTER =================
@app.post("/add-voter", response_class=HTMLResponse)
def add_voter_post(
    request: Request,
    election_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...)
):
    voter_data = {
        "name": name,
        "email": email,
        "election_id": election_id,
        "has_voted": False
    }
    voters_col.insert_one(voter_data)
    return RedirectResponse(f"/ec/dashboard?election_id={election_id}", status_code=303)

# ================= REMOVE VOTER =================
@app.post("/remove-voter/{voter_id}", response_class=HTMLResponse)
def remove_voter(voter_id: str, election_id: str = Form(...)):
    try:
        voters_col.delete_one({"_id": ObjectId(voter_id)})
    except Exception:
        return HTMLResponse("Invalid voter ID", status_code=400)
    return RedirectResponse(f"/ec/dashboard?election_id={election_id}", status_code=303)

# ================= ADD CANDIDATE =================
@app.post("/add-candidate", response_class=HTMLResponse)
def add_candidate_post(
    request: Request,
    election_id: str = Form(...),
    name: str = Form(...),
    party: str = Form(...),
    moto: str = Form(None),
    profile_pic: UploadFile | None = File(None)
):
    file_path = None

    if profile_pic and profile_pic.filename:
        upload_dir = Path("static/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        ext = Path(profile_pic.filename).suffix
        unique_filename = f"{uuid.uuid4()}{ext}"
        full_path = upload_dir / unique_filename
        with open(full_path, "wb") as f:
            f.write(profile_pic.file.read())
        file_path = f"uploads/{unique_filename}"

    add_candidate(election_id, name, party, moto, file_path)
    return RedirectResponse(f"/ec/dashboard?election_id={election_id}", status_code=303)

# ================= REMOVE CANDIDATE =================
@app.post("/remove-candidate/{candidate_id}", response_class=HTMLResponse)
def remove_candidate(candidate_id: str, election_id: str = Form(...)):
    try:
        ec = ec_col.find_one({"election_id": election_id})
        if not ec or "election" not in ec:
            return HTMLResponse("Election not found", status_code=404)

        ec["election"]["candidates"] = [
            c for c in ec["election"].get("candidates", [])
            if str(c["_id"]) != candidate_id
        ]
        ec_col.update_one({"election_id": election_id}, {"$set": {"election": ec["election"]}})
    except Exception:
        return HTMLResponse("Invalid candidate ID", status_code=400)

    return RedirectResponse(f"/ec/dashboard?election_id={election_id}", status_code=303)

# ================= VOTER LOGIN =================
@app.get("/voter/login", response_class=HTMLResponse)
def voter_login_get(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})

@app.post("/voter/login", response_class=HTMLResponse)
def voter_login_post(request: Request, email: str = Form(...)):
    voter = voters_col.find_one({"email": email})
    if not voter:
        return templates.TemplateResponse(
            "Login.html",
            {"request": request, "error": "Voter not found", "email": email}
        )

    ec = ec_col.find_one({"election_id": voter["election_id"]})
    election = ec.get("election", {})
    candidates = election.get("candidates", [])

    return templates.TemplateResponse(
        "vote.html",
        {"request": request, "voter": voter, "election": election, "candidates": candidates}
    )

# ================= VOTE =================
@app.post("/vote", response_class=HTMLResponse)
def submit_vote(request: Request, voter_id: str = Form(...), candidate_id: str = Form(...)):
    try:
        voter = voters_col.find_one({"_id": ObjectId(voter_id)})
    except Exception:
        return HTMLResponse("Invalid voter ID", status_code=400)

    if not voter:
        return HTMLResponse("Voter not found", status_code=404)
    if voter.get("has_voted"):
        return HTMLResponse("Voter has already voted", status_code=400)

    voters_col.update_one(
        {"_id": ObjectId(voter_id)},
        {"$set": {"has_voted": True, "voted_for": candidate_id}}
    )

    ec = ec_col.find_one({"election_id": voter["election_id"]})
    election = ec.get("election", {})

    return templates.TemplateResponse(
        "thankyou.html",
        {
            "request": request,
            "voter": voter,
            "election": election,
            "vote_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

# ================= RESULT =================
@app.get("/result", response_class=HTMLResponse)
def result_page(request: Request, election_id: str):
    ec = ec_col.find_one({"election_id": election_id})
    if not ec:
        return HTMLResponse("Election not found", status_code=404)

    election = ec.get("election", {})
    candidates = election.get("candidates", [])
    voters = list(voters_col.find({"election_id": election_id}))

    total_votes = sum(1 for v in voters if v.get("has_voted"))

    for candidate in candidates:
        candidate_votes = sum(1 for v in voters if v.get("voted_for") == str(candidate["_id"]))
        candidate["votes"] = candidate_votes
        candidate["percentage"] = round((candidate_votes / total_votes * 100) if total_votes else 0, 1)

    candidates.sort(key=lambda c: c["votes"], reverse=True)

    return templates.TemplateResponse(
        "Result.html",
        {"request": request, "election": election, "candidates": candidates, "total_votes": total_votes}
    )

# ================= OAUTH PLACEHOLDER =================
@app.get("/auth/google")
def google_oauth_login():
    return {"message": "Google OAuth not implemented yet"}