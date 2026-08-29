"""
services/fitness_calculator.py
-----------------------------------------------------------------------
Pure-function fitness calculation service.
No Flask or database imports – only standard Python maths.
All results are general fitness estimates and NOT medical advice.
-----------------------------------------------------------------------
"""


# -----------------------------------------------------------------------
# Activity-level multipliers (Harris-Benedict / Mifflin-St Jeor convention)
# -----------------------------------------------------------------------
ACTIVITY_MULTIPLIERS = {
    "sedentary":          1.2,
    "lightly_active":     1.375,
    "moderately_active":  1.55,
    "very_active":        1.725,
}

# -----------------------------------------------------------------------
# Goal-based calorie adjustments
# -----------------------------------------------------------------------
GOAL_CALORIE_ADJUSTMENTS = {
    "weight_loss":       -400,
    "weight_gain":       +400,
    "muscle_building":   +250,
    "general_fitness":     0,
    "improve_stamina":   -100,
}

# -----------------------------------------------------------------------
# Protein multipliers (g per kg of body weight)
# -----------------------------------------------------------------------
PROTEIN_MULTIPLIERS = {
    "weight_loss":       (1.6, 2.0),
    "weight_gain":       (1.6, 2.2),
    "muscle_building":   (1.8, 2.5),
    "general_fitness":   (1.2, 1.8),
    "improve_stamina":   (1.4, 1.8),
}


def _normalise_key(value: str) -> str:
    """Convert a display string such as 'Lightly Active' to 'lightly_active'."""
    return value.strip().lower().replace(" ", "_")


# -----------------------------------------------------------------------
# BMI
# -----------------------------------------------------------------------

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """
    Return BMI rounded to one decimal place.

    BMI = weight (kg) / height (m) ^ 2
    """
    height_m = height_cm / 100.0
    if height_m <= 0:
        return 0.0
    return round(weight_kg / (height_m ** 2), 1)


def get_bmi_category(bmi: float) -> str:
    """Return a human-readable BMI category string."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Healthy Range"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obesity"


# -----------------------------------------------------------------------
# BMR  –  Mifflin-St Jeor equation
# -----------------------------------------------------------------------

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Basal Metabolic Rate (kcal/day) using the Mifflin-St Jeor equation.

    Male  : 10 × weight + 6.25 × height − 5 × age + 5
    Female: 10 × weight + 6.25 × height − 5 × age − 161
    """
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age
    if gender.lower() in ("male", "m"):
        bmr += 5
    else:
        bmr -= 161
    return round(bmr, 1)


# -----------------------------------------------------------------------
# Daily calorie requirement
# -----------------------------------------------------------------------

def calculate_daily_calories(bmr: float, activity_level: str, fitness_goal: str) -> int:
    """
    Estimate total daily energy expenditure (TDEE) adjusted for fitness goal.

    Returns an integer calorie value.
    """
    act_key  = _normalise_key(activity_level)
    goal_key = _normalise_key(fitness_goal)

    multiplier = ACTIVITY_MULTIPLIERS.get(act_key, 1.2)
    adjustment = GOAL_CALORIE_ADJUSTMENTS.get(goal_key, 0)

    tdee = bmr * multiplier + adjustment
    return max(1200, int(round(tdee)))   # Floor at 1 200 kcal for safety


# -----------------------------------------------------------------------
# Protein requirement
# -----------------------------------------------------------------------

def calculate_protein_requirement(weight_kg: float, fitness_goal: str) -> dict:
    """
    Return a dict with 'min_g' and 'max_g' daily protein targets.

    Multipliers are in grams per kilogram of body weight.
    """
    goal_key = _normalise_key(fitness_goal)
    low, high = PROTEIN_MULTIPLIERS.get(goal_key, (1.2, 1.8))
    return {
        "min_g": round(weight_kg * low,  1),
        "max_g": round(weight_kg * high, 1),
    }


# -----------------------------------------------------------------------
# Water intake recommendation
# -----------------------------------------------------------------------

def calculate_water_intake(weight_kg: float) -> float:
    """
    Approximate daily water requirement in litres.

    General guideline: 35 ml per kg of body weight.
    """
    litres = (weight_kg * 35) / 1000
    return round(litres, 1)


# -----------------------------------------------------------------------
# Convenience – all metrics in one call
# -----------------------------------------------------------------------

def get_all_metrics(weight_kg: float, height_cm: float, age: int,
                    gender: str, activity_level: str, fitness_goal: str) -> dict:
    """
    Return a single dictionary containing every calculated fitness metric.
    This is what Flask routes will typically call.
    """
    bmi      = calculate_bmi(weight_kg, height_cm)
    category = get_bmi_category(bmi)
    bmr      = calculate_bmr(weight_kg, height_cm, age, gender)
    calories = calculate_daily_calories(bmr, activity_level, fitness_goal)
    protein  = calculate_protein_requirement(weight_kg, fitness_goal)
    water    = calculate_water_intake(weight_kg)

    return {
        "bmi":            bmi,
        "bmi_category":   category,
        "bmr":            bmr,
        "daily_calories": calories,
        "protein_min_g":  protein["min_g"],
        "protein_max_g":  protein["max_g"],
        "water_litres":   water,
    }
