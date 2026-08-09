import re
import os
import random
import requests

from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    session,
    url_for,
    redirect
)

from dotenv import load_dotenv

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from progress import ProgressTracker
from user import User
from data_manager import DataManager
from career_path import CareerPath
from analytics import Analytics
from visualization import Visualization
from recommendation import RecommendationEngine
from advisor import CareerAdvisor


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

os.makedirs(DATA_DIR, exist_ok=True)


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


app.secret_key = os.environ.get(
    "SECRET_KEY",
    "career_planner_secret_key"
)


# =========================================================
# MAIL CONFIGURATION (Brevo HTTPS API)
# =========================================================
# NOTE: Render's free tier blocks outbound SMTP ports
# (25, 465, 587), which is why Flask-Mail/SMTP hung and
# crashed the worker. Brevo's API sends over HTTPS (port
# 443), which is never blocked.

BREVO_API_KEY = os.environ.get(
    "BREVO_API_KEY"
)

# This must be a sender you've verified in Brevo
# (Settings -> Senders, Domains, IPs -> Senders).
BREVO_FROM_ADDRESS = os.environ.get(
    "BREVO_FROM_ADDRESS",
    "aicareerplanner@gmail.com"
)

BREVO_FROM_NAME = os.environ.get(
    "BREVO_FROM_NAME",
    "TechPath AI"
)


def send_email(to_email, subject, html):
    """
    Sends an email via the Brevo HTTPS API.
    Raises an exception on failure so callers can decide
    how to handle it (same contract as the old mail.send()).
    """

    if not BREVO_API_KEY:
        raise RuntimeError(
            "BREVO_API_KEY is not set in the environment."
        )

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={
            "sender": {
                "name": BREVO_FROM_NAME,
                "email": BREVO_FROM_ADDRESS,
            },
            "to": [
                {"email": to_email}
            ],
            "subject": subject,
            "htmlContent": html,
        },
        timeout=10,
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"Brevo API error {response.status_code}: "
            f"{response.text}"
        )

    return response.json()


# =========================================================
# DATA MANAGERS
# =========================================================

database_file = os.path.join(
    DATA_DIR,
    "techpath.db"
)
print("🔥 DATABASE PATH:", database_file)
careers_file = os.path.join(
    DATA_DIR,
    "careers.csv"
)
print("🔥 CAREERS FILE PATH:", careers_file)

data_manager = DataManager(
    database_file
)
print("🔥 USERS IN DATABASE:", [
    {
        "id": u.user_id,
        "email": u.email,
        "verified": u.verified
    }
    for u in data_manager.load_users()
])

career_manager = CareerPath(
    careers_file
)


# =========================================================
# PASSWORD VALIDATION
# =========================================================

def is_strong_password(password):

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(
        r"[!@#$%^&*(),.?\":{}|<>]",
        password
    ):
        return False

    return True


# =========================================================
# CONTEXT PROCESSOR
# =========================================================

@app.context_processor
def inject_year():

    return {
        "current_year": datetime.now().year
    }


# =========================================================
# CURRENT USER
# =========================================================

def get_current_user():

    if "user_id" not in session:
        return None

    return data_manager.load_user_by_id(
        session["user_id"]
    )


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# CREATE PROFILE
# =========================================================

@app.route(
    "/create-profile",
    methods=["GET", "POST"]
)
def create_profile():

    careers = career_manager.get_careers()

    if request.method == "POST":

        try:

            # -------------------------------------------------
            # GET FORM DATA
            # -------------------------------------------------

            name = request.form.get(
                "name"
            )

            age = int(
                request.form.get("age")
            )

            education = request.form.get(
                "education"
            )

            study_hours = float(
                request.form.get("study_hours")
            )

            career_goal = request.form.get(
                "career_goal"
            )

            email = request.form.get(
                "email"
            ).strip().lower()

            password = request.form.get(
                "password"
            )

            confirm_password = request.form.get(
                "confirm_password"
            )

            current_level = request.form.get(
                "current_level"
            )

            programming_experience = request.form.get(
                "programming_experience"
            )

            interests = request.form.get(
                "interests"
            )

            learning_style = request.form.get(
                "learning_style"
            )


            # -------------------------------------------------
            # PASSWORD MATCH
            # -------------------------------------------------

            if password != confirm_password:

                return render_template(
                    "create_profile.html",
                    careers=careers,
                    error="Passwords do not match."
                )


            # -------------------------------------------------
            # STRONG PASSWORD
            # -------------------------------------------------

            if not is_strong_password(password):

                return render_template(
                    "create_profile.html",
                    careers=careers,
                    error=(
                        "Password must contain at least "
                        "8 characters, uppercase, lowercase, "
                        "number and special character."
                    )
                )


            # -------------------------------------------------
            # CHECK EXISTING EMAIL
            # -------------------------------------------------

            existing_user = (
                data_manager.load_user_by_email(
                    email
                )
            )
            print("📧 EMAIL BEING CHECKED:", repr(email))
            print("👤 EXISTING USER:", existing_user)

            if existing_user:

                return render_template(
                    "create_profile.html",
                    careers=careers,
                    error="Email already exists."
                )


            # -------------------------------------------------
            # GENERATE USER ID
            # -------------------------------------------------

            user_id = data_manager.get_next_id()


            # -------------------------------------------------
            # VERIFICATION CODE
            # -------------------------------------------------

            verification_code = random.randint(
                100000,
                999999
            )


            # -------------------------------------------------
            # HASH PASSWORD
            # -------------------------------------------------

            hashed_password = generate_password_hash(
                password
            )


            # -------------------------------------------------
            # CREATE USER
            # -------------------------------------------------

            user = User(
                user_id,
                name,
                age,
                education,
                career_goal,
                study_hours,
                hashed_password,
                current_level,
                programming_experience,
                interests,
                learning_style,
                email,
                False,
                verification_code
            )


            # -------------------------------------------------
            # SAVE USER
            # -------------------------------------------------

            data_manager.save_user(
                user
            )


            # -------------------------------------------------
            # VERIFICATION EMAIL
            # -------------------------------------------------

            verification_html = render_template(
                "emails/verification_email.html",
                name=name,
                code=verification_code,
                year=datetime.now().year
            )


            try:

                send_email(
                    to_email=email,
                    subject="TechPath AI - Email Verification",
                    html=verification_html
                )

            except Exception as e:

                # Remove user if email sending fails
                data_manager.delete_user(
                    user_id
                )

                return (
                    f"Email could not be sent: {e}"
                )


            # -------------------------------------------------
            # REDIRECT TO VERIFICATION
            # -------------------------------------------------

            return redirect(
                url_for(
                    "verify",
                    user_id=user.user_id
                )
            )


        except Exception as e:

            print(
                "🔥 CREATE PROFILE ERROR:",
                repr(e)
            )

            return render_template(
                "create_profile.html",
                careers=careers,
                error=f"Something went wrong: {e}"
            )


    return render_template(
        "create_profile.html",
        careers=careers
    )


# =========================================================
# VERIFY EMAIL
# =========================================================

@app.route(
    "/verify/<user_id>",
    methods=["GET", "POST"]
)
def verify(user_id):

    user = data_manager.load_user_by_id(
        user_id
    )

    if not user:

        return (
            f"User not found. ID received: {user_id}"
        )


    if request.method == "POST":

        try:

            code = int(
                request.form["code"]
            )

        except ValueError:

            return render_template(
                "verify.html",
                user=user,
                error="Enter numbers only."
            )


        if code == user.verification_code:

            user.verified = True
            user.verification_code = None

            data_manager.update_user(
                user
            )

            return redirect(
                url_for("login")
            )


        else:

            return render_template(
                "verify.html",
                user=user,
                error="Invalid verification code."
            )


    return render_template(
        "verify.html",
        user=user
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email"
        ).strip().lower()

        password = request.form.get(
            "password"
        )

        user = data_manager.load_user_by_email(
            email
        )


        if (
            user
            and check_password_hash(
                user.password,
                password
            )
        ):

            if not user.verified:

                return (
                    "Please verify your email first."
                )

            session["user_id"] = user.user_id

            return redirect(
                url_for("dashboard")
            )


        return render_template(
            "login.html",
            error="Invalid email or password!"
        )


    return render_template(
        "login.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user = get_current_user()


    if user is None:

        session.clear()


        return redirect(
            url_for("login")
        )


    roadmap = career_manager.generate_roadmap(
        user.career_goal,
        user
    )


    progress = ProgressTracker(
        roadmap
    )

    progress.load_progress(
        user.user_id
    )


    percentage = progress.progress_percentage()

    completed = progress.completed_skills()

    total = len(roadmap)

    remaining = total - completed


    badges = []


    if completed >= 1:

        badges.append(
            ("🥉", "First Skill Completed")
        )


    if percentage >= 25:

        badges.append(
            ("🥈", "25% Complete")
        )


    if percentage >= 50:

        badges.append(
            ("🥇", "50% Complete")
        )


    if percentage >= 75:

        badges.append(
            ("💎", "75% Complete")
        )


    if percentage == 100:

        badges.append(
            ("👑", "AI Roadmap Master")
        )


    advisor = CareerAdvisor()


    advice = advisor.generate_advice(
        user,
        progress
    )


    current_hour = datetime.now().hour


    if current_hour < 12:

        greeting = "☀️ Good Morning"

    elif current_hour < 17:

        greeting = "🌤️ Good Afternoon"

    else:

        greeting = "🌙 Good Evening"


    current_date = datetime.now().strftime(
        "%A, %d %B %Y"
    )


    return render_template(
        "dashboard.html",
        user=user,
        percentage=percentage,
        completed=completed,
        total=total,
        advice=advice,
        greeting=greeting,
        current_date=current_date,
        remaining=remaining,
        badges=badges
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user = get_current_user()


    if user is None:

        session.clear()

        return redirect(
            url_for("login")
        )


    return render_template(
        "profile.html",
        user=user
    )


# =========================================================
# CHANGE PASSWORD
# =========================================================

@app.route(
    "/change-password",
    methods=["GET", "POST"]
)
def change_password():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user = get_current_user()


    if user is None:

        session.clear()

        return redirect(
            url_for("login")
        )


    if request.method == "POST":

        current_password = request.form[
            "current_password"
        ]

        new_password = request.form[
            "new_password"
        ]

        confirm_password = request.form[
            "confirm_password"
        ]


        if not check_password_hash(
            user.password,
            current_password
        ):

            return render_template(
                "change_password.html",
                error="Current password is incorrect."
            )


        if new_password != confirm_password:

            return render_template(
                "change_password.html",
                error="New passwords do not match."
            )


        if not is_strong_password(
            new_password
        ):

            return render_template(
                "change_password.html",
                error=(
                    "Password must be at least 8 "
                    "characters long and contain an "
                    "uppercase letter, lowercase letter, "
                    "number, and special character."
                )
            )


        user.password = generate_password_hash(
            new_password
        )


        data_manager.update_user(
            user
        )


        return render_template(
            "change_password.html",
            success="Password updated successfully!"
        )


    return render_template(
        "change_password.html"
    )


# =========================================================
# DELETE ACCOUNT
# =========================================================

@app.route(
    "/delete-account",
    methods=["GET", "POST"]
)
def delete_account():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user = get_current_user()


    if user is None:

        session.clear()

        return redirect(
            url_for("login")
        )


    if request.method == "POST":

        password = request.form[
            "password"
        ]


        if not check_password_hash(
            user.password,
            password
        ):

            return render_template(
                "delete_account.html",
                error="Incorrect password."
            )


        data_manager.delete_progress(
            user.user_id
        )

        data_manager.delete_user(
            user.user_id
        )

        session.clear()


        return render_template(
            "index.html",
            success=(
                "Your account has been deleted successfully."
            )
        )


    return render_template(
        "delete_account.html"
    )


# =========================================================
# FORGOT PASSWORD
# =========================================================

@app.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form[
            "email"
        ].strip().lower()


        user = data_manager.load_user_by_email(
            email
        )


        if not user:

            return render_template(
                "forgot_password.html",
                error="No account found with this email."
            )


        reset_code = random.randint(
            100000,
            999999
        )


        user.verification_code = reset_code


        data_manager.update_user(
            user
        )


        reset_html = f"""
        <p>Hello {user.name},</p>
        <p>We received a request to reset your password.</p>
        <p>Your verification code is:</p>
        <h2>{reset_code}</h2>
        <p>If you did not request a password reset,
        you can safely ignore this email.</p>
        <p>Regards,<br>TechPath AI Team</p>
        """

        try:

            send_email(
                to_email=email,
                subject="Reset Your TechPath AI Password",
                html=reset_html
            )

        except Exception as e:

            return render_template(
                "forgot_password.html",
                error=f"Email could not be sent: {e}"
            )


        session["reset_email"] = email


        return redirect(
            url_for("reset_verify")
        )


    return render_template(
        "forgot_password.html"
    )


# =========================================================
# RESET VERIFY
# =========================================================

@app.route(
    "/reset-verify",
    methods=["GET", "POST"]
)
def reset_verify():

    if "reset_email" not in session:

        return redirect(
            url_for("forgot_password")
        )


    email = session[
        "reset_email"
    ]


    user = data_manager.load_user_by_email(
        email
    )


    if request.method == "POST":

        try:

            code = int(
                request.form["code"]
            )

        except ValueError:

            return render_template(
                "reset_verify.html",
                error="Enter numbers only."
            )


        if user and code == user.verification_code:

            session["reset_verified"] = True

            return redirect(
                url_for("reset_password")
            )


        return render_template(
            "reset_verify.html",
            error="Invalid verification code."
        )


    return render_template(
        "reset_verify.html"
    )


# =========================================================
# RESET PASSWORD
# =========================================================

@app.route(
    "/reset-password",
    methods=["GET", "POST"]
)
def reset_password():

    if "reset_verified" not in session:

        return redirect(
            url_for("forgot_password")
        )


    email = session[
        "reset_email"
    ]


    user = data_manager.load_user_by_email(
        email
    )


    if request.method == "POST":

        password = request.form[
            "password"
        ]

        confirm = request.form[
            "confirm_password"
        ]


        if password != confirm:

            return render_template(
                "reset_password.html",
                error="Passwords do not match."
            )


        if not is_strong_password(
            password
        ):

            return render_template(
                "reset_password.html",
                error=(
                    "Password must be at least 8 "
                    "characters long and contain an "
                    "uppercase letter, lowercase letter, "
                    "number, and special character."
                )
            )


        user.password = generate_password_hash(
            password
        )

        user.verification_code = None


        data_manager.update_user(
            user
        )


        session.pop(
            "reset_email",
            None
        )

        session.pop(
            "reset_verified",
            None
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "reset_password.html"
    )


# =========================================================
# EDIT PROFILE
# =========================================================

@app.route(
    "/edit-profile",
    methods=["GET", "POST"]
)
def edit_profile():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user = get_current_user()


    if user is None:

        session.clear()

        return redirect(
            url_for("login")
        )


    careers = career_manager.get_careers()


    if request.method == "POST":

        user.name = request.form[
            "name"
        ]

        user.age = int(
            request.form["age"]
        )

        user.education = request.form[
            "education"
        ]

        user.study_hours = float(
            request.form["study_hours"]
        )

        user.career_goal = request.form[
            "career_goal"
        ]


        data_manager.update_user(
            user
        )


        return redirect(
            url_for("profile")
        )


    return render_template(
        "edit_profile.html",
        user=user,
        careers=careers
    )


# =========================================================
# ROADMAP
# =========================================================

@app.route("/roadmap")
def roadmap():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user = get_current_user()


    if user is None:

        session.clear()

        return redirect(
            url_for("login")
        )


    roadmap = career_manager.generate_roadmap(
        user.career_goal,
        user
    )


    engine = RecommendationEngine()


    roadmap = engine.recommend(
        user,
        roadmap
    )


    progress = ProgressTracker(
        roadmap
    )


    progress.load_progress(
        user.user_id
    )


    search = request.args.get(
        "search",
        ""
    ).strip()


    difficulty = request.args.get(
        "difficulty",
        ""
    )


    category = request.args.get(
        "category",
        ""
    )


    filtered = roadmap


    if category:

        filtered = [
            skill
            for skill in filtered
            if skill.category == category
        ]


    if search:

        filtered = [
            skill
            for skill in filtered
            if search.lower()
            in skill.name.lower()
        ]


    if difficulty:

        filtered = [
            skill
            for skill in filtered
            if skill.difficulty == difficulty
        ]


    completed = progress.completed_skills()

    total = len(progress.roadmap)

    percentage = progress.progress_percentage()


    categories = sorted(
        list(
            set(
                skill.category
                for skill in progress.roadmap
            )
        )
    )


    return render_template(
        "roadmap.html",
        user=user,
        roadmap=filtered,
        progress=progress,
        completed=completed,
        total=total,
        percentage=percentage,
        search=search,
        difficulty=difficulty,
        category=category,
        categories=categories
    )


# =========================================================
# COMPLETE SKILL
# =========================================================

@app.route(
    "/complete/<skill_name>"
)
def complete_skill(skill_name):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user = get_current_user()


    if user is None:

        session.clear()

        return redirect(
            url_for("login")
        )


    roadmap = career_manager.generate_roadmap(
        user.career_goal,
        user
    )


    engine = RecommendationEngine()


    roadmap = engine.recommend(
        user,
        roadmap
    )


    progress = ProgressTracker(
        roadmap
    )


    progress.load_progress(
        user.user_id
    )


    progress.complete_skill(
        skill_name
    )


    progress.save_progress(
        user.user_id
    )


    return redirect(
        url_for("roadmap")
    )


# =========================================================
# ANALYTICS
# =========================================================

@app.route("/analytics")
def analytics():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user = get_current_user()


    if user is None:

        session.clear()

        return redirect(
            url_for("login")
        )


    roadmap = career_manager.generate_roadmap(
        user.career_goal,
        user
    )


    engine = RecommendationEngine()


    roadmap = engine.recommend(
        user,
        roadmap
    )


    progress = ProgressTracker(
        roadmap
    )


    progress.load_progress(
        user.user_id
    )


    analytics = Analytics(
        progress.roadmap
    )


    visual = Visualization(
        progress.roadmap
    )


    visual.progress_pie_chart()

    visual.category_bar_chart()

    visual.difficulty_chart()


    return render_template(
        "analytics.html",
        user=user,
        analytics=analytics
    )


# =========================================================
# CAREER PREVIEW
# =========================================================

@app.route(
    "/career/<career_name>"
)
def career_preview(career_name):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    user = get_current_user()


    if user is None:

        session.clear()

        return redirect(
            url_for("login")
        )


    roadmap = career_manager.generate_roadmap(
        career_name,
        user
    )


    return render_template(
        "career_preview.html",
        user=user,
        career_name=career_name,
        roadmap=roadmap
    )


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def internal_error(error):

    print(
        "🔥 INTERNAL SERVER ERROR:",
        repr(error)
    )

    return f"""
    <h1>Internal Server Error</h1>
    <pre>{error}</pre>
    """, 500


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
