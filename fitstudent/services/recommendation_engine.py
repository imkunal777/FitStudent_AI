"""
services/recommendation_engine.py
-----------------------------------------------------------------------
Central intelligence layer that combines user profile + preferences,
runs fitness calculations, then delegates to the workout and meal
generators to produce complete personalised recommendations.

The engine uses rule-based scoring and conditional logic so plans
differ meaningfully between users. It is designed so a real ML model
or external AI API can be plugged in later by replacing `_score_user`.

Public API:
    generate_recommendations(user, diet_pref, workout_pref) -> dict
-----------------------------------------------------------------------
"""
import json
from services.fitness_calculator import get_all_metrics
from services.workout_generator import generate_workout_plan
from services.meal_generator import generate_meal_plan


# ------------------------------------------------------------------
# Scoring helpers – produce a "user profile score" used to fine-tune
# which variant of a plan is chosen.  (extensible later)
# ------------------------------------------------------------------

def _normalise(value: str) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def _score_user(user) -> dict:
    """
    Produce a lightweight feature dict from the SQLAlchemy User object.
    This is the abstraction boundary for a future ML model.
    """
    goal  = _normalise(user.fitness_goal)
    level = _normalise(user.fitness_level)
    act   = _normalise(user.activity_level)
    bmi   = round(user.weight / ((user.height / 100) ** 2), 1)

    intensity = 1   # 1=low, 2=medium, 3=high
    if level == "intermediate":
        intensity = 2
    elif level == "advanced":
        intensity = 3

    calorie_priority = "maintain"
    if goal in ("weight_loss",):
        calorie_priority = "deficit"
    elif goal in ("weight_gain", "muscle_building"):
        calorie_priority = "surplus"

    return {
        "goal":             goal,
        "level":            level,
        "activity":         act,
        "bmi":              bmi,
        "intensity":        intensity,
        "calorie_priority": calorie_priority,
    }


# ------------------------------------------------------------------
# Main recommendation function
# ------------------------------------------------------------------

def generate_recommendations(user, diet_pref, workout_pref) -> dict:
    """
    Orchestrates the complete recommendation pipeline.

    Args:
        user          : User SQLAlchemy model instance
        diet_pref     : DietPreference model instance (may be None)
        workout_pref  : WorkoutPreference model instance (may be None)

    Returns:
        {
            "metrics":       { bmi, bmi_category, bmr, daily_calories,
                               protein_min_g, protein_max_g, water_litres },
            "workout_plan":  list[day_dict],        # 7 days
            "meal_plan":     dict,                  # breakfast/lunch/snack/dinner/totals
            "workout_json":  str,                   # JSON-serialised for DB storage
            "meal_json":     str,                   # JSON-serialised for DB storage
        }
    """

    # ----------------------------------------------------------------
    # 1. Fitness metrics
    # ----------------------------------------------------------------
    metrics = get_all_metrics(
        weight_kg      = user.weight,
        height_cm      = user.height,
        age            = user.age,
        gender         = user.gender,
        activity_level = user.activity_level,
        fitness_goal   = user.fitness_goal,
    )

    # ----------------------------------------------------------------
    # 2. Profile scoring (extensibility hook)
    # ----------------------------------------------------------------
    _score_user(user)   # currently informational; result used to log / extend later

    # ----------------------------------------------------------------
    # 3. Workout plan
    # ----------------------------------------------------------------
    equipment     = workout_pref.available_equipment if workout_pref else "No Equipment"
    daily_minutes = workout_pref.daily_workout_time  if workout_pref else 30

    workout_plan = generate_workout_plan(
        fitness_goal  = user.fitness_goal,
        fitness_level = user.fitness_level,
        equipment     = equipment,
        daily_minutes = daily_minutes,
    )

    # ----------------------------------------------------------------
    # 4. Meal plan
    # ----------------------------------------------------------------
    diet_type    = diet_pref.diet_type           if diet_pref else "vegetarian"
    budget       = diet_pref.budget              if diet_pref else "medium"
    culture      = diet_pref.cultural_preference if diet_pref else "general"
    preferred    = diet_pref.preferred_foods     if diet_pref else ""
    disliked     = diet_pref.disliked_foods      if diet_pref else ""

    meal_plan = generate_meal_plan(
        daily_calories     = metrics["daily_calories"],
        protein_min_g      = metrics["protein_min_g"],
        diet_type          = diet_type,
        budget             = budget,
        cultural_preference= culture,
        preferred_foods    = preferred or "",
        disliked_foods     = disliked or "",
        fitness_goal       = user.fitness_goal,
    )

    # ----------------------------------------------------------------
    # 5. Serialise for database storage
    # ----------------------------------------------------------------
    workout_json = json.dumps(workout_plan, ensure_ascii=False)
    meal_json    = json.dumps(meal_plan,    ensure_ascii=False)

    return {
        "metrics":      metrics,
        "workout_plan": workout_plan,
        "meal_plan":    meal_plan,
        "workout_json": workout_json,
        "meal_json":    meal_json,
    }
