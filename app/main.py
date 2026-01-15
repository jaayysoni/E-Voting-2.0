from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bcrypt import checkpw
from bcrypt import hashpw, gensalt
from datetime import datetime
from pathlib import Path
import uuid


from bson import ObjectId
from bson.errors import InvalidId

from db.db import ec_col, voters_col
from app.users.services import register_ec, add_candidate  # removed create_election import

# ---------------- FastAPI app ----------------
app = FastAPI(title="E-Voting 2.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

Path("static/uploads").mkdir(parents=True, exist_ok=True)

# ---------------- Jinja2 filter for formatting dates ----------------
def datetimeformat(value, format="%d/%m/%Y %H:%M"):
    if not value:
        return "Not set"
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    return value.strftime(format)

templates.env.filters['datetimeformat'] = datetimeformat

# ================= UNIVERSAL DASHBOARD =================
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    ecs = list(ec_col.find({}))
    elections = []
    now = datetime.now()

    for ec in ecs:
        election = ec.get("election")
        # Skip incomplete elections
        if not election or not election.get("name") or not election.get("start_date") or not election.get("end_date"):
            continue

        start_time = election.get("start_date")
        end_time = election.get("end_date")

        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time)

        # Determine status
        if start_time <= now <= end_time:
            status = "Active"
        elif now < start_time:
            status = "Upcoming"
        else:
            status = "Completed"

        elections.append({
            "ec_name": ec.get("name", "Unknown EC"),
            "election_id": election.get("election_id", "N/A"),
            "name": election.get("name", "Unnamed Election"),
            "start_date": start_time,
            "end_date": end_time,
            "status": status
        })
    # Sort elections by status: Active first, Upcoming next, Completed last
    status_order = {"Active": 0, "Upcoming": 1, "Completed": 2}
    elections.sort(key=lambda x: status_order.get(x["status"], 3))

    return templates.TemplateResponse(
        "Dashboard.html",
        {
            "request": request,
            "elections": elections,
            "total_elections": len(elections),
            "active_count": sum(1 for e in elections if e["status"] == "Active"),
            "upcoming_count": sum(1 for e in elections if e["status"] == "Upcoming")
        }
    )

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
            {"request": request, "error": "Passwords do not match"}
        )

    success, result = register_ec(name, email, password)

    if not success:
        return templates.TemplateResponse(
            "EC-signup.html",
            {"request": request, "error": result}
        )

    return templates.TemplateResponse(
        "EC-login.html",
        {"request": request, "message": f"Signup successful! Election ID: {result}"}
    )

# ================= EC LOGIN =================
@app.get("/ec/login", response_class=HTMLResponse)
def ec_login_get(request: Request):
    return templates.TemplateResponse("EC-login.html", {"request": request})

@app.post("/ec/login")
def ec_login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    ec = ec_col.find_one({"email": email})

    if not ec or not checkpw(password.encode(), ec["password_hash"].encode()):
        return templates.TemplateResponse(
            "EC-login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    return RedirectResponse(
        f"/ec/dashboard?election_id={ec['election_id']}",
        status_code=303
    )

# ================= EC DASHBOARD =================
@app.get("/ec/dashboard", response_class=HTMLResponse)
def ec_dashboard(request: Request, election_id: str):
    ec = ec_col.find_one({"election_id": election_id})
    if not ec:
        return HTMLResponse("EC not found", status_code=404)

    election = ec.get("election")
    # Only treat election as existing if it has name, start and end date
    if not election or not election.get("name") or not election.get("start_date") or not election.get("end_date"):
        election = None

    voters = list(voters_col.find({"election_id": election_id}))
    candidates = election.get("candidates", []) if election else []

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
@app.post("/create-election")
def create_election_post(
    election_id: str = Form(...),
    name: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...)
):
    """Create election and save it to EC document"""
    election_data = {
        "election_id": election_id,
        "name": name,
        "start_date": datetime.fromisoformat(start_date).isoformat(),
        "end_date": datetime.fromisoformat(end_date).isoformat(),
        "status": "Upcoming",
        "candidates": []
    }

    ec_col.update_one(
        {"election_id": election_id},
        {"$set": {"election": election_data}}
    )

    return RedirectResponse(
        f"/ec/dashboard?election_id={election_id}",
        status_code=303
    )

# ================= ADD VOTER =================
@app.post("/add-voter")
def add_voter_post(
    election_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    password_hash = hashpw(password.encode(), gensalt()).decode()

    voters_col.insert_one({
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "election_id": election_id,
        "has_voted": False
    })

    return RedirectResponse(
        f"/ec/dashboard?election_id={election_id}",
        status_code=303
    )

# ================= REMOVE VOTER =================
@app.post("/remove-voter/{voter_id}")
def remove_voter(
    voter_id: str,
    election_id: str = Form(...)
):
    try:
        voters_col.delete_one({"_id": ObjectId(voter_id)})
    except InvalidId:
        return HTMLResponse("Invalid voter ID", status_code=400)

    return RedirectResponse(
        f"/ec/dashboard?election_id={election_id}",
        status_code=303
    )

# ================= ADD CANDIDATE =================
@app.post("/add-candidate")
def add_candidate_post(
    election_id: str = Form(...),
    name: str = Form(...),
    party: str = Form(...),
    moto: str = Form(None),
    profile_pic: UploadFile | None = File(None)
):
    image_path = None

    if profile_pic and profile_pic.filename:
        ext = Path(profile_pic.filename).suffix
        filename = f"{uuid.uuid4()}{ext}"
        full_path = Path("static/uploads") / filename

        with open(full_path, "wb") as f:
            f.write(profile_pic.file.read())

        image_path = f"uploads/{filename}"

    add_candidate(election_id, name, party, moto, image_path)

    return RedirectResponse(
        f"/ec/dashboard?election_id={election_id}",
        status_code=303
    )

# ================= REMOVE CANDIDATE =================
@app.post("/remove-candidate/{candidate_id}")
def remove_candidate(
    candidate_id: str,
    election_id: str = Form(...)
):
    ec = ec_col.find_one({"election_id": election_id})
    if not ec or "election" not in ec:
        return HTMLResponse("Election not found", status_code=404)

    ec["election"]["candidates"] = [
        c for c in ec["election"]["candidates"]
        if str(c["_id"]) != candidate_id
    ]

    ec_col.update_one(
        {"election_id": election_id},
        {"$set": {"election": ec["election"]}}
    )

    return RedirectResponse(
        f"/ec/dashboard?election_id={election_id}",
        status_code=303
    )

# ================= VOTER LOGIN =================
@app.get("/voter/login", response_class=HTMLResponse)
def voter_login_get(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})

@app.post("/voter/login", response_class=HTMLResponse)
def voter_login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    voter = voters_col.find_one({"email": email})

    if not voter:
        return templates.TemplateResponse(
            "Login.html",
            {"request": request, "error": "Voter not found"}
        )

    # Verify password
    if not checkpw(password.encode(), voter["password_hash"].encode()):
        return templates.TemplateResponse(
            "Login.html",
            {"request": request, "error": "Incorrect password"}
        )

    ec = ec_col.find_one({"election_id": voter["election_id"]})
    election = ec.get("election", {})

    return templates.TemplateResponse(
        "vote.html",
        {
            "request": request,
            "voter": voter,
            "election": election,
            "candidates": election.get("candidates", [])
        }
    )

# ================= VOTE =================
@app.post("/vote", response_class=HTMLResponse)
def submit_vote(
    request: Request,
    voter_id: str = Form(...),
    candidate_id: str = Form(...)
):
    voter = voters_col.find_one({"_id": ObjectId(voter_id)})

    if not voter or voter.get("has_voted"):
        return HTMLResponse("Invalid vote", status_code=400)

    voters_col.update_one(
        {"_id": ObjectId(voter_id)},
        {"$set": {"has_voted": True, "voted_for": candidate_id}}
    )

    ec = ec_col.find_one({"election_id": voter["election_id"]})

    return templates.TemplateResponse(
        "thankyou.html",
        {
            "request": request,
            "election": ec.get("election", {}),
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
    voters = list(voters_col.find({"election_id": election_id}))
    candidates = election.get("candidates", [])

    total_votes = sum(1 for v in voters if v.get("has_voted"))

    for c in candidates:
        votes = sum(1 for v in voters if v.get("voted_for") == str(c["_id"]))
        c["votes"] = votes
        c["percentage"] = round((votes / total_votes * 100) if total_votes else 0, 1)

    candidates.sort(key=lambda x: x["votes"], reverse=True)

    return templates.TemplateResponse(
        "Result.html",
        {
            "request": request,
            "election": election,
            "candidates": candidates,
            "total_votes": total_votes
        }
    )

# ================= dummy oauth =================
@app.get("/auth/google", name="google_oauth_login")
def google_oauth_login():
    return HTMLResponse("Google login coming soon!")