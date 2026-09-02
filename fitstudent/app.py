"""
app.py – FitStudent AI Flask application entry point.
Contains all route definitions and application factory.
"""
import json
import os
from datetime import date

from flask import (Flask, render_template, request, redirect,
                   url_for, flash, session)

from config import DevelopmentConfig, ProductionConfig
from extensions import db

# ----------------------------------------------------------------
# Application factory
# ----------------------------------------------------------------

def create_app():
    app = Flask(__name__)
    # Use ProductionConfig on hosted environments (no FLASK_DEBUG set)
    cfg = DevelopmentConfig if os.environ.get("FLASK_DEBUG") else ProductionConfig
    app.config.from_object(cfg)

    db.init_app(app)

    # Import models so SQLAlchemy registers them before create_all
    from models import (User, DietPreference, WorkoutPreference,
                        WorkoutPlan, MealPlan, Progress)

    with app.app_context():
        db.create_all()

    # ----------------------------------------------------------------
    # Register routes
    # ----------------------------------------------------------------

    # ---- HOME PAGE -------------------------------------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    # ---- PROFILE ---------------------------------------------------
    @app.route("/profile", methods=["GET", "POST"])
    def profile():
        if request.method == "POST":
            errors = _validate_profile(request.form)
            if errors:
                for e in errors:
                    flash(e, "danger")
                return render_template("profile.html", form=request.form)

            user_id = session.get("user_id")

            if user_id:
                user = db.session.get(User, user_id)
            else:
                user = None

            if user:
                # Update existing profile
                _apply_profile_form(user, request.form)
                db.session.commit()
                flash("Profile updated successfully!", "success")
            else:
                # Create new user
                user = User(
                    name          = request.form["name"].strip(),
                    age           = int(request.form["age"]),
                    gender        = request.form["gender"],
                    height        = float(request.form["height"]),
                    weight        = float(request.form["weight"]),
                    activity_level= request.form["activity_level"],
                    fitness_goal  = request.form["fitness_goal"],
                    fitness_level = request.form["fitness_level"],
                )
                db.session.add(user)
                db.session.commit()
                flash("Profile created! Now set your preferences.", "success")

            session["user_id"] = user.id
            return redirect(url_for("preferences"))

        # GET – pre-fill if user exists
        user_id = session.get("user_id")
        user    = db.session.get(User, user_id) if user_id else None
        return render_template("profile.html", user=user)

    # ---- PREFERENCES -----------------------------------------------
    @app.route("/preferences", methods=["GET", "POST"])
    def preferences():
        user_id = session.get("user_id")
        if not user_id:
            flash("Please create your profile first.", "warning")
            return redirect(url_for("profile"))

        user = db.session.get(User, user_id)
        if not user:
            flash("User not found. Please create your profile.", "warning")
            return redirect(url_for("profile"))

        if request.method == "POST":
            errors = _validate_preferences(request.form)
            if errors:
                for e in errors:
                    flash(e, "danger")
                return render_template("preferences.html",
                                       diet_pref=user.diet_pref,
                                       workout_pref=user.workout_pref,
                                       form=request.form)

            # Diet preferences
            if user.diet_pref:
                dp = user.diet_pref
            else:
                dp = DietPreference(user_id=user.id)
                db.session.add(dp)

            dp.diet_type           = request.form["diet_type"]
            dp.budget              = request.form["budget"]
            dp.preferred_foods     = request.form.get("preferred_foods", "")
            dp.disliked_foods      = request.form.get("disliked_foods", "")
            dp.cultural_preference = request.form.get("cultural_preference", "general")

            # Workout preferences
            if user.workout_pref:
                wp = user.workout_pref
            else:
                wp = WorkoutPreference(user_id=user.id)
                db.session.add(wp)

            wp.daily_workout_time  = int(request.form["daily_workout_time"])
            wp.available_equipment = request.form["available_equipment"]

            db.session.commit()

            # Generate recommendations and store in DB
            _generate_and_save_plans(user)

            flash("Preferences saved! Your personalised plan is ready.", "success")
            return redirect(url_for("dashboard"))

        return render_template("preferences.html",
                               diet_pref=user.diet_pref,
                               workout_pref=user.workout_pref)

    # ---- DASHBOARD -------------------------------------------------
    @app.route("/dashboard")
    def dashboard():
        user_id = session.get("user_id")
        if not user_id:
            flash("Please create your profile first.", "warning")
            return redirect(url_for("profile"))

        user = db.session.get(User, user_id)
        if not user:
            flash("User not found.", "warning")
            return redirect(url_for("profile"))

        if not user.diet_pref or not user.workout_pref:
            flash("Please complete your preferences first.", "info")
            return redirect(url_for("preferences"))

        metrics = _get_metrics(user)

        latest_workout = (WorkoutPlan.query.filter_by(user_id=user.id)
                          .order_by(WorkoutPlan.created_at.desc()).first())
        latest_meal    = (MealPlan.query.filter_by(user_id=user.id)
                          .order_by(MealPlan.created_at.desc()).first())

        workout_summary = _workout_summary(latest_workout)
        meal_summary    = _meal_summary(latest_meal)

        return render_template(
            "dashboard.html",
            user           = user,
            metrics        = metrics,
            workout_summary= workout_summary,
            meal_summary   = meal_summary,
        )

    # ---- WORKOUT PLAN ----------------------------------------------
    @app.route("/workout-plan")
    def workout_plan():
        user_id = session.get("user_id")
        if not user_id:
            flash("Please create your profile first.", "warning")
            return redirect(url_for("profile"))

        user = db.session.get(User, user_id)
        if not user:
            return redirect(url_for("profile"))

        latest = (WorkoutPlan.query.filter_by(user_id=user.id)
                  .order_by(WorkoutPlan.created_at.desc()).first())

        plan = json.loads(latest.plan_data) if latest else []

        return render_template("workout.html", user=user, plan=plan)

    # ---- MEAL PLAN -------------------------------------------------
    @app.route("/meal-plan")
    def meal_plan():
        user_id = session.get("user_id")
        if not user_id:
            flash("Please create your profile first.", "warning")
            return redirect(url_for("profile"))

        user = db.session.get(User, user_id)
        if not user:
            return redirect(url_for("profile"))

        latest = (MealPlan.query.filter_by(user_id=user.id)
                  .order_by(MealPlan.created_at.desc()).first())

        plan    = json.loads(latest.plan_data) if latest else {}
        metrics = _get_metrics(user)

        return render_template("meal_plan.html", user=user, plan=plan, metrics=metrics)

    # ---- PROGRESS --------------------------------------------------
    @app.route("/progress")
    def progress():
        user_id = session.get("user_id")
        if not user_id:
            flash("Please create your profile first.", "warning")
            return redirect(url_for("profile"))

        user = db.session.get(User, user_id)
        if not user:
            return redirect(url_for("profile"))

        records = (Progress.query.filter_by(user_id=user.id)
                   .order_by(Progress.record_date.desc()).all())

        return render_template("progress.html", user=user, records=records,
                               today=date.today().isoformat())

    @app.route("/progress/add", methods=["GET", "POST"])
    def progress_add():
        user_id = session.get("user_id")
        if not user_id:
            flash("Please create your profile first.", "warning")
            return redirect(url_for("profile"))

        user = db.session.get(User, user_id)
        if not user:
            return redirect(url_for("profile"))

        if request.method == "POST":
            errors = _validate_progress(request.form)
            if errors:
                for e in errors:
                    flash(e, "danger")
                return render_template("progress.html",
                                       user=user,
                                       records=user.progress_records,
                                       show_form=True,
                                       form=request.form)

            record = Progress(
                user_id           = user.id,
                weight            = float(request.form["weight"]),
                workout_completed = bool(request.form.get("workout_completed")),
                notes             = request.form.get("notes", "").strip(),
                record_date       = date.fromisoformat(request.form["record_date"]),
            )
            db.session.add(record)
            db.session.commit()
            flash("Progress record added!", "success")
            return redirect(url_for("progress"))

        return render_template("progress.html",
                               user=user,
                               records=user.progress_records,
                               show_form=True,
                               today=date.today().isoformat())

    # ---- REGENERATE PLAN (convenience) ----------------------------
    @app.route("/regenerate")
    def regenerate():
        user_id = session.get("user_id")
        if user_id:
            user = db.session.get(User, user_id)
            if user and user.diet_pref and user.workout_pref:
                _generate_and_save_plans(user)
                flash("Your plan has been regenerated.", "success")
        return redirect(url_for("dashboard"))

    # ---- CLEAR SESSION (start fresh) ------------------------------
    @app.route("/reset")
    def reset():
        session.clear()
        flash("Session cleared. You can start fresh.", "info")
        return redirect(url_for("index"))

    # ---- ERROR HANDLERS -------------------------------------------
    @app.errorhandler(404)
    def not_found(e):
        return render_template("base.html",
                               error_message="Page not found (404)."), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("base.html",
                               error_message="Server error (500). Please try again."), 500

    return app


# ----------------------------------------------------------------
# Helper: validation
# ----------------------------------------------------------------

def _validate_profile(form) -> list:
    errors = []
    name = form.get("name", "").strip()
    if not name:
        errors.append("Name is required.")

    try:
        age = int(form.get("age", 0))
        if age < 10 or age > 100:
            errors.append("Age must be between 10 and 100.")
    except ValueError:
        errors.append("Age must be a valid number.")

    try:
        height = float(form.get("height", 0))
        if height < 50 or height > 300:
            errors.append("Height must be between 50 and 300 cm.")
    except ValueError:
        errors.append("Height must be a valid number.")

    try:
        weight = float(form.get("weight", 0))
        if weight < 20 or weight > 500:
            errors.append("Weight must be between 20 and 500 kg.")
    except ValueError:
        errors.append("Weight must be a valid number.")

    if not form.get("gender"):
        errors.append("Gender is required.")
    if not form.get("activity_level"):
        errors.append("Activity level is required.")
    if not form.get("fitness_goal"):
        errors.append("Fitness goal is required.")
    if not form.get("fitness_level"):
        errors.append("Fitness level is required.")

    return errors


def _validate_preferences(form) -> list:
    errors = []
    if not form.get("diet_type"):
        errors.append("Diet type is required.")
    if not form.get("budget"):
        errors.append("Budget is required.")
    try:
        mins = int(form.get("daily_workout_time", 0))
        if mins < 10 or mins > 240:
            errors.append("Daily workout time must be between 10 and 240 minutes.")
    except ValueError:
        errors.append("Daily workout time must be a number.")
    if not form.get("available_equipment"):
        errors.append("Available equipment is required.")
    return errors


def _validate_progress(form) -> list:
    errors = []
    try:
        w = float(form.get("weight", 0))
        if w < 20 or w > 500:
            errors.append("Weight must be between 20 and 500 kg.")
    except ValueError:
        errors.append("Weight must be a valid number.")
    if not form.get("record_date"):
        errors.append("Date is required.")
    return errors


# ----------------------------------------------------------------
# Helper: apply profile form data to an existing User object
# ----------------------------------------------------------------

def _apply_profile_form(user, form):
    user.name           = form["name"].strip()
    user.age            = int(form["age"])
    user.gender         = form["gender"]
    user.height         = float(form["height"])
    user.weight         = float(form["weight"])
    user.activity_level = form["activity_level"]
    user.fitness_goal   = form["fitness_goal"]
    user.fitness_level  = form["fitness_level"]


# ----------------------------------------------------------------
# Helper: generate and save plans to DB
# ----------------------------------------------------------------

def _generate_and_save_plans(user):
    from services.recommendation_engine import generate_recommendations
    from models import WorkoutPlan, MealPlan

    result = generate_recommendations(user, user.diet_pref, user.workout_pref)

    wp = WorkoutPlan(user_id=user.id, plan_data=result["workout_json"])
    mp = MealPlan(user_id=user.id,    plan_data=result["meal_json"])
    db.session.add(wp)
    db.session.add(mp)
    db.session.commit()


# ----------------------------------------------------------------
# Helper: get fitness metrics for a user
# ----------------------------------------------------------------

def _get_metrics(user) -> dict:
    from services.fitness_calculator import get_all_metrics
    return get_all_metrics(
        weight_kg      = user.weight,
        height_cm      = user.height,
        age            = user.age,
        gender         = user.gender,
        activity_level = user.activity_level,
        fitness_goal   = user.fitness_goal,
    )


# ----------------------------------------------------------------
# Summary helpers for dashboard
# ----------------------------------------------------------------

def _workout_summary(workout_plan_row) -> dict:
    if not workout_plan_row:
        return {}
    days = json.loads(workout_plan_row.plan_data)
    workout_days = [d for d in days if d["type"] == "workout"]
    rest_days    = [d for d in days if d["type"] == "rest"]
    focuses      = list(dict.fromkeys(d["focus"] for d in workout_days))
    return {
        "workout_days": len(workout_days),
        "rest_days":    len(rest_days),
        "focuses":      focuses[:4],   # show first 4 focus areas
    }


def _meal_summary(meal_plan_row) -> dict:
    if not meal_plan_row:
        return {}
    data = json.loads(meal_plan_row.plan_data)
    breakfast_names = [f["name"] for f in data.get("breakfast", [])]
    lunch_names     = [f["name"] for f in data.get("lunch",     [])]
    totals          = data.get("totals", {})
    return {
        "breakfast_names": breakfast_names,
        "lunch_names":     lunch_names,
        "total_calories":  totals.get("calories", "—"),
        "total_protein":   totals.get("protein_g", "—"),
    }


# ----------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
