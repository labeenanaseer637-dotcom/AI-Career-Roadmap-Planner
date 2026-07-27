from flask import Flask, render_template, request, session,url_for, redirect
from progress import ProgressTracker
from user import User
from data_manager import DataManager
from career_path import CareerPath
from analytics import Analytics
from visualization import Visualization
import random
from flask_mail import Mail, Message
from werkzeug.security import (check_password_hash,generate_password_hash)
from recommendation import RecommendationEngine
from advisor import CareerAdvisor
from datetime import datetime
import os 
app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "career_planner_secret_key")
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "aicareerplanner@gmail.com"
app.config["MAIL_PASSWORD"] = os.environ.get(
    "MAIL_PASSWORD"
)
mail = Mail(app)
@app.context_processor
def inject_year():

    return {
        "current_year": datetime.now().year
    }
data_manager = DataManager("data/users.csv")
career_manager = CareerPath("data/careers.csv")
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/create-profile", methods=["GET", "POST"])
def create_profile():
    careers = career_manager.get_careers()
    if request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])
        education = request.form["education"]
        study_hours = float(request.form["study_hours"])
        career_goal = request.form["career_goal"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
         return render_template("create_profile.html",
        careers=careers,error="Passwords do not match.")  
        password = generate_password_hash(password)
        email = request.form["email"]
        existing = data_manager.load_user_by_email(email)
        if existing:
            return render_template(
        "create_profile.html",
        careers=careers,
        error="Email already exists.")
        verification_code = random.randint(100000,999999)
        verified = False
        current_level = request.form["current_level"]
        programming_experience = request.form["programming_experience"]
        interests = request.form["interests"]
        learning_style = request.form["learning_style"]
        user_id = data_manager.get_next_id()
        user = User(
            user_id,
            name,
            age,
            education,
            career_goal,
            study_hours,
            password,
            current_level,
            programming_experience,
            interests,
            learning_style, email,
            verified,
            verification_code )
        msg = Message(  subject="AI Career Planner Verification",sender=app.config["MAIL_USERNAME"], recipients=[email])
        msg.body = f"""
         Hello {name},
         Welcome to AI Career Planner!
         Your verification code is:
              {verification_code}
              Enter this code to verify your account.
               If you did not create this account, you can safely ignore this email.
               Thank you!
              Regards,
              AI Career Planner Team"""
        try:
          mail.send(msg)
        except Exception as e:
          return f"Email could not be sent: {e}"
        data_manager.save_user(user)
        return redirect(
            url_for("verify", user_id=user.user_id))
    return render_template(
        "create_profile.html",
        careers=careers
    )
@app.route("/verify/<user_id>", methods=["GET","POST"])
def verify(user_id):
    user = data_manager.load_user_by_id(user_id)
    if not user:
        return "User not found"
    if request.method == "POST":
        try:
          code = int(request.form["code"])
        except ValueError:
         return render_template(
          "verify.html",
          user=user,
          error="Enter numbers only." )
        if int(code) == user.verification_code:
            user.verified = True
            user.verification_code = None
            data_manager.update_user(user)
            return redirect(url_for("login"))
        else:
            return render_template("verify.html",
            user=user,
            error="Invalid verification code.")
    return render_template(
        "verify.html",
        user=user
    )
# LOGIN ROUTE SHOULD BE HERE 👇
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        user = data_manager.load_user_by_name(name)
        if user and check_password_hash(user.password,password):
             if not user.verified:
               return "Please verify your email first."
             session["user_id"] = user.user_id 
             return redirect(url_for("dashboard"))
        else:

            return render_template(
                "login.html",
                error="Invalid name or password!"
            )

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))
    user = data_manager.load_user_by_id(session["user_id"])
    roadmap = career_manager.generate_roadmap(user.career_goal)
    progress = ProgressTracker(roadmap)
    progress.load_progress(user.user_id)
    percentage = progress.progress_percentage()
    completed = progress.completed_skills()
    total = len(roadmap)
    remaining = total - completed
    badges = []
    if completed >= 1:
     badges.append(("🥉", "First Skill Completed"))
    if percentage >= 25:
      badges.append(("🥈", "25% Complete"))
    if percentage >= 50:
      badges.append(("🥇", "50% Complete"))
    if percentage >= 75:
      badges.append(("💎", "75% Complete"))
    if percentage == 100:
      badges.append(("👑", "AI Roadmap Master"))
    advisor = CareerAdvisor()
    advice = advisor.generate_advice(user,
    progress)
    current_hour = datetime.now().hour

    if current_hour < 12:
       greeting = "☀️ Good Morning"
    elif current_hour < 17:
      greeting = "🌤️ Good Afternoon"
    else:
       greeting = "🌙 Good Evening"
    current_date = datetime.now().strftime("%A, %d %B %Y")
    return render_template(
        "dashboard.html",
        user=user,
        percentage=percentage,
        completed=completed,
        total=total,advice=advice,greeting=greeting,
        current_date=current_date,remaining=remaining,badges=badges,)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = data_manager.load_user_by_id(session["user_id"])
    return render_template(
        "profile.html",
        user=user
    )
@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = data_manager.load_user_by_id(session["user_id"])
    careers = career_manager.get_careers()
    if request.method == "POST":
        user.name = request.form["name"]
        user.age = int(request.form["age"])
        user.education = request.form["education"]
        user.study_hours = float(request.form["study_hours"])
        user.career_goal = request.form["career_goal"]
        user.password = generate_password_hash(request.form["password"])
        new_password = request.form["password"]
        if new_password:
           user.password = generate_password_hash(new_password)
        data_manager.update_user(user)

        return redirect(url_for("profile"))

    return render_template(
        "edit_profile.html",
        user=user,
        careers=careers
    )
@app.route("/roadmap")
def roadmap():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = data_manager.load_user_by_id(session["user_id"])

    roadmap = career_manager.generate_roadmap(
    user.career_goal)

    engine = RecommendationEngine()
    roadmap = engine.recommend(
    user,
    roadmap)

    progress = ProgressTracker(roadmap)
    progress.load_progress(user.user_id)

    # Search
    search = request.args.get("search", "").strip()

    # Difficulty Filter
    difficulty = request.args.get("difficulty", "")
    category = request.args.get("category", "")
    filtered = roadmap
    if category:
     filtered = [
        skill for skill in filtered
        if skill.category == category]

    if search:
        filtered = [
            skill for skill in filtered
            if search.lower() in skill.name.lower()
        ]

    if difficulty:
        filtered = [
            skill for skill in filtered
            if skill.difficulty == difficulty
        ]

    completed = progress.completed_skills()
    total = len(progress.roadmap)
    percentage = progress.progress_percentage()
    categories = sorted(
    list(set(skill.category for skill in progress.roadmap)))
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
@app.route("/complete/<skill_name>")
def complete_skill(skill_name):

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = data_manager.load_user_by_id(session["user_id"])

    roadmap = career_manager.generate_roadmap(
    user.career_goal)
    engine = RecommendationEngine()
    roadmap = engine.recommend(
    user,
    roadmap)
    progress = ProgressTracker(roadmap)
    progress.load_progress(user.user_id)
    progress.complete_skill(skill_name)
    progress.save_progress(user.user_id)
    return redirect(url_for("roadmap"))
@app.route("/analytics")
def analytics():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = data_manager.load_user_by_id(session["user_id"])

    roadmap = career_manager.generate_roadmap(
    user.career_goal)
    engine = RecommendationEngine()
    roadmap = engine.recommend(
    user,
    roadmap)

    progress = ProgressTracker(roadmap)

    progress.load_progress(user.user_id)

    analytics = Analytics(progress.roadmap)

    visual = Visualization(progress.roadmap)

    visual.progress_pie_chart()
    visual.category_bar_chart()
    visual.difficulty_chart()

    return render_template(
        "analytics.html",
        user=user,
        analytics=analytics
    )
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"),404
@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"),500
# THIS MUST ALWAYS BE LAST 👇

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)