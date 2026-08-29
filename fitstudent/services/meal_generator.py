"""
services/meal_generator.py
-----------------------------------------------------------------------
Generates a personalised daily meal plan (breakfast / lunch / snack /
dinner) based on:
  - daily_calories      int
  - protein_min_g       float
  - diet_type           str
  - budget              str
  - cultural_preference str
  - preferred_foods     str  (comma-separated, may be empty)
  - disliked_foods      str  (comma-separated, may be empty)
  - fitness_goal        str

Returns:
  {
    "breakfast": [ { name, calories, protein_g, serving_size, food_group } ],
    "lunch":     [ ... ],
    "snack":     [ ... ],
    "dinner":    [ ... ],
    "totals":    { calories, protein_g }
  }
-----------------------------------------------------------------------
"""
import random
from data.food_data import get_foods_for


# Approximate calorie distribution per meal
MEAL_DISTRIBUTION = {
    "breakfast": 0.25,
    "lunch":     0.35,
    "snack":     0.10,
    "dinner":    0.30,
}

# How many items to try to include per meal
MEAL_ITEM_COUNT = {
    "breakfast": 2,
    "lunch":     3,
    "snack":     1,
    "dinner":    3,
}


def _normalise(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_")


def _parse_list(text: str) -> list:
    """Turn a comma-separated preference string into a lowercase list."""
    if not text:
        return []
    return [item.strip().lower() for item in text.split(",") if item.strip()]


def _score_food(food: dict, preferred: list, disliked: list,
                cultural_key: str, target_cal: float) -> float:
    """
    Score a food item higher when it matches preferences.
    Returns a float score (higher = better).
    """
    score = 0.0

    # Cultural bonus
    if cultural_key in food["culture"]:
        score += 2.0

    # Preferred food bonus
    name_lower = food["name"].lower()
    for pref in preferred:
        if pref in name_lower:
            score += 3.0

    # Disliked food penalty
    for dis in disliked:
        if dis in name_lower:
            score -= 10.0   # effectively removes the item

    # Calorie proximity: reward foods close to the target
    cal_diff = abs(food["calories"] - target_cal)
    score += max(0.0, 5.0 - cal_diff / 50.0)

    # Protein reward (heavier for muscle/weight-gain goals handled in caller)
    score += food["protein_g"] * 0.1

    return score


def _select_items(meal_type: str, diet_key: str, budget_key: str,
                  culture_key: str, preferred: list, disliked: list,
                  target_calories: float, n: int = 2,
                  high_protein: bool = False) -> list:
    """
    Select `n` food items for a given meal slot.

    Scores all eligible foods and returns the top-n (with a small random
    perturbation so plans are not identical between close-preference users).
    """
    candidates = get_foods_for(diet_key, budget_key, culture_key, meal_type)

    if not candidates:
        # Fallback: relax culture filter
        candidates = get_foods_for(diet_key, budget_key, "general", meal_type)

    if not candidates:
        return []

    # Per-item target calorie share
    per_item_cal = target_calories / max(n, 1)

    scored = []
    for food in candidates:
        s = _score_food(food, preferred, disliked, culture_key, per_item_cal)
        if high_protein:
            s += food["protein_g"] * 0.3   # extra weight for protein foods
        # Small random jitter so repeated calls vary slightly
        s += random.uniform(-0.5, 0.5)
        scored.append((s, food))

    # Sort descending, filter out items the user dislikes (score < -5)
    scored = [(s, f) for s, f in scored if s > -5.0]
    scored.sort(key=lambda x: x[0], reverse=True)

    # Pick top-n, but avoid duplicate food groups where possible
    selected = []
    seen_groups = set()
    for _, food in scored:
        if food["food_group"] not in seen_groups or len(selected) < n:
            selected.append(food)
            seen_groups.add(food["food_group"])
        if len(selected) >= n:
            break

    return selected


def generate_meal_plan(daily_calories: int, protein_min_g: float,
                       diet_type: str, budget: str,
                       cultural_preference: str,
                       preferred_foods: str = "",
                       disliked_foods: str = "",
                       fitness_goal: str = "general_fitness") -> dict:
    """
    Entry point: build a full-day meal plan.

    Returns a dict with keys: breakfast, lunch, snack, dinner, totals.
    """
    diet_key    = _normalise(diet_type)
    budget_key  = _normalise(budget).replace("_budget", "")
    culture_key = _normalise(cultural_preference) if cultural_preference else "general"
    preferred   = _parse_list(preferred_foods)
    disliked    = _parse_list(disliked_foods)

    goal_key    = _normalise(fitness_goal)
    high_protein = goal_key in ("muscle_building", "weight_gain")

    plan    = {}
    total_cal  = 0
    total_prot = 0.0

    for meal in ("breakfast", "lunch", "snack", "dinner"):
        target_cal = daily_calories * MEAL_DISTRIBUTION[meal]
        n          = MEAL_ITEM_COUNT[meal]

        items = _select_items(
            meal_type     = meal,
            diet_key      = diet_key,
            budget_key    = budget_key,
            culture_key   = culture_key,
            preferred     = preferred,
            disliked      = disliked,
            target_calories = target_cal,
            n             = n,
            high_protein  = high_protein,
        )

        plan[meal] = items
        for item in items:
            total_cal  += item["calories"]
            total_prot += item["protein_g"]

    plan["totals"] = {
        "calories":  total_cal,
        "protein_g": round(total_prot, 1),
    }

    return plan
