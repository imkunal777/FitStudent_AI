"""
data/food_data.py
-----------------------------------------------------------------------
Structured food dataset used by the meal generator.
Each entry is a dict with the following keys:

    name            str   – display name
    diet            list  – compatible diet types
                            ("vegetarian", "non_vegetarian", "eggetarian", "vegan")
    calories        int   – approximate kcal per standard serving
    protein_g       float – approximate protein in grams per serving
    serving_size    str   – human-readable serving description
    budget          list  – compatible budget levels: "low", "medium", "flexible"
    meal_type       list  – suitable meals: "breakfast", "lunch", "snack", "dinner"
    culture         list  – compatible cultural preferences
                            ("general", "north_indian", "south_indian", "bengali")
    food_group      str   – "grain", "protein", "dairy", "vegetable",
                            "fruit", "fat", "beverage"
-----------------------------------------------------------------------
"""

FOODS = [
    # ----------------------------------------------------------------
    # GRAINS / STAPLES
    # ----------------------------------------------------------------
    {
        "name": "Cooked Rice (1 cup)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 200,
        "protein_g": 4.0,
        "serving_size": "1 cup (150 g cooked)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "grain",
    },
    {
        "name": "Whole Wheat Roti (2 rotis)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 180,
        "protein_g": 5.0,
        "serving_size": "2 medium rotis (60 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian"],
        "food_group": "grain",
    },
    {
        "name": "Oats (cooked, 1 bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 150,
        "protein_g": 6.0,
        "serving_size": "1 bowl (80 g dry)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "grain",
    },
    {
        "name": "Brown Rice (1 cup cooked)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 215,
        "protein_g": 5.0,
        "serving_size": "1 cup (150 g cooked)",
        "budget": ["medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "grain",
    },
    {
        "name": "Idli (2 pieces)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 120,
        "protein_g": 4.0,
        "serving_size": "2 medium idlis",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast"],
        "culture": ["south_indian", "general"],
        "food_group": "grain",
    },
    {
        "name": "Poha (1 bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 160,
        "protein_g": 3.5,
        "serving_size": "1 bowl (100 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast"],
        "culture": ["north_indian", "general"],
        "food_group": "grain",
    },
    {
        "name": "Bread (2 slices, whole wheat)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 140,
        "protein_g": 6.0,
        "serving_size": "2 slices (60 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast", "snack"],
        "culture": ["general", "north_indian", "bengali"],
        "food_group": "grain",
    },

    # ----------------------------------------------------------------
    # PROTEIN SOURCES – PLANT
    # ----------------------------------------------------------------
    {
        "name": "Dal (cooked, 1 bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 150,
        "protein_g": 9.0,
        "serving_size": "1 bowl (200 ml)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "protein",
    },
    {
        "name": "Chana (boiled, 1 cup)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 210,
        "protein_g": 11.0,
        "serving_size": "1 cup (160 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "snack", "dinner"],
        "culture": ["general", "north_indian", "bengali"],
        "food_group": "protein",
    },
    {
        "name": "Rajma (kidney beans, cooked)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 220,
        "protein_g": 13.0,
        "serving_size": "1 cup (170 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian"],
        "food_group": "protein",
    },
    {
        "name": "Soybean / Soy Chunks (cooked, 1 cup)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 180,
        "protein_g": 22.0,
        "serving_size": "1 cup (100 g cooked)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian", "bengali"],
        "food_group": "protein",
    },
    {
        "name": "Paneer (100 g)",
        "diet": ["vegetarian", "eggetarian"],
        "calories": 265,
        "protein_g": 18.0,
        "serving_size": "100 g",
        "budget": ["medium", "flexible"],
        "meal_type": ["lunch", "dinner", "snack"],
        "culture": ["general", "north_indian"],
        "food_group": "protein",
    },
    {
        "name": "Tofu (100 g)",
        "diet": ["vegetarian", "vegan", "eggetarian"],
        "calories": 120,
        "protein_g": 13.0,
        "serving_size": "100 g",
        "budget": ["medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general"],
        "food_group": "protein",
    },
    {
        "name": "Peanuts (1 handful, ~30 g)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 175,
        "protein_g": 7.0,
        "serving_size": "30 g",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["snack"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "protein",
    },
    {
        "name": "Mixed Lentil Soup (1 bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 130,
        "protein_g": 8.0,
        "serving_size": "1 bowl (250 ml)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "protein",
    },

    # ----------------------------------------------------------------
    # PROTEIN SOURCES – EGGS
    # ----------------------------------------------------------------
    {
        "name": "Boiled Eggs (2 eggs)",
        "diet": ["non_vegetarian", "eggetarian"],
        "calories": 155,
        "protein_g": 12.5,
        "serving_size": "2 large eggs",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast", "snack"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "protein",
    },
    {
        "name": "Egg Omelette (2 eggs)",
        "diet": ["non_vegetarian", "eggetarian"],
        "calories": 185,
        "protein_g": 14.0,
        "serving_size": "2-egg omelette",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast"],
        "culture": ["general", "north_indian", "bengali"],
        "food_group": "protein",
    },

    # ----------------------------------------------------------------
    # PROTEIN SOURCES – NON-VEGETARIAN
    # ----------------------------------------------------------------
    {
        "name": "Chicken Breast (grilled, 100 g)",
        "diet": ["non_vegetarian"],
        "calories": 165,
        "protein_g": 31.0,
        "serving_size": "100 g",
        "budget": ["medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian", "bengali"],
        "food_group": "protein",
    },
    {
        "name": "Rohu / Catla Fish (cooked, 100 g)",
        "diet": ["non_vegetarian"],
        "calories": 130,
        "protein_g": 20.0,
        "serving_size": "100 g",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["bengali", "general"],
        "food_group": "protein",
    },
    {
        "name": "Chicken Curry (1 serving)",
        "diet": ["non_vegetarian"],
        "calories": 280,
        "protein_g": 26.0,
        "serving_size": "1 serving (~150 g)",
        "budget": ["medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["north_indian", "general", "bengali"],
        "food_group": "protein",
    },
    {
        "name": "Egg Curry (2 eggs)",
        "diet": ["non_vegetarian", "eggetarian"],
        "calories": 220,
        "protein_g": 14.0,
        "serving_size": "2 eggs in curry",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian", "bengali"],
        "food_group": "protein",
    },

    # ----------------------------------------------------------------
    # DAIRY
    # ----------------------------------------------------------------
    {
        "name": "Milk (1 glass, 250 ml)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian"],
        "calories": 120,
        "protein_g": 8.0,
        "serving_size": "250 ml",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast", "snack"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "dairy",
    },
    {
        "name": "Curd / Yogurt (1 bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian"],
        "calories": 100,
        "protein_g": 6.0,
        "serving_size": "1 bowl (150 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "snack"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "dairy",
    },
    {
        "name": "Whey Protein Shake (1 scoop)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian"],
        "calories": 120,
        "protein_g": 24.0,
        "serving_size": "30 g scoop in water",
        "budget": ["flexible"],
        "meal_type": ["breakfast", "snack"],
        "culture": ["general"],
        "food_group": "dairy",
    },

    # ----------------------------------------------------------------
    # VEGETABLES
    # ----------------------------------------------------------------
    {
        "name": "Mixed Sabzi / Stir-fried Vegetables",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 80,
        "protein_g": 2.5,
        "serving_size": "1 serving (100 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "vegetable",
    },
    {
        "name": "Spinach Sabzi",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 70,
        "protein_g": 3.0,
        "serving_size": "1 katori (100 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["lunch", "dinner"],
        "culture": ["general", "north_indian", "bengali"],
        "food_group": "vegetable",
    },
    {
        "name": "Sambar (1 bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 100,
        "protein_g": 4.5,
        "serving_size": "1 bowl (200 ml)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast", "lunch", "dinner"],
        "culture": ["south_indian", "general"],
        "food_group": "vegetable",
    },

    # ----------------------------------------------------------------
    # FRUITS
    # ----------------------------------------------------------------
    {
        "name": "Banana (1 medium)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 90,
        "protein_g": 1.1,
        "serving_size": "1 medium banana (~120 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast", "snack"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "fruit",
    },
    {
        "name": "Apple (1 medium)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 80,
        "protein_g": 0.4,
        "serving_size": "1 medium apple (~150 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["snack"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "fruit",
    },
    {
        "name": "Papaya (1 bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 60,
        "protein_g": 0.5,
        "serving_size": "1 cup cubed (~150 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast", "snack"],
        "culture": ["general", "south_indian", "bengali"],
        "food_group": "fruit",
    },
    {
        "name": "Mixed Seasonal Fruit Bowl",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 100,
        "protein_g": 1.0,
        "serving_size": "1 bowl (~150 g)",
        "budget": ["medium", "flexible"],
        "meal_type": ["breakfast", "snack"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "fruit",
    },

    # ----------------------------------------------------------------
    # SNACKS / LIGHT
    # ----------------------------------------------------------------
    {
        "name": "Chana Chaat (1 small bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 180,
        "protein_g": 8.0,
        "serving_size": "1 small bowl (100 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["snack"],
        "culture": ["general", "north_indian", "bengali"],
        "food_group": "protein",
    },
    {
        "name": "Sprouts Salad (1 bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 110,
        "protein_g": 8.0,
        "serving_size": "1 bowl (100 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["snack", "breakfast"],
        "culture": ["general", "north_indian", "bengali"],
        "food_group": "protein",
    },
    {
        "name": "Peanut Butter Toast (1 slice)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian"],
        "calories": 200,
        "protein_g": 8.0,
        "serving_size": "1 slice bread + 1 tbsp peanut butter",
        "budget": ["medium", "flexible"],
        "meal_type": ["breakfast", "snack"],
        "culture": ["general"],
        "food_group": "protein",
    },
    {
        "name": "Roasted Makhana (1 bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 90,
        "protein_g": 3.5,
        "serving_size": "1 bowl (30 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["snack"],
        "culture": ["general", "north_indian", "bengali"],
        "food_group": "grain",
    },
    {
        "name": "Vegetable Upma (1 bowl)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 190,
        "protein_g": 5.0,
        "serving_size": "1 bowl (150 g)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast"],
        "culture": ["south_indian", "general"],
        "food_group": "grain",
    },
    {
        "name": "Green Tea (1 cup)",
        "diet": ["vegetarian", "non_vegetarian", "eggetarian", "vegan"],
        "calories": 5,
        "protein_g": 0.0,
        "serving_size": "1 cup (200 ml)",
        "budget": ["low", "medium", "flexible"],
        "meal_type": ["breakfast", "snack"],
        "culture": ["general", "north_indian", "south_indian", "bengali"],
        "food_group": "beverage",
    },
]


def get_foods_for(diet_type: str, budget: str, cultural_preference: str,
                  meal_type: str = None) -> list:
    """
    Filter the food list for a given diet, budget, culture, and optional meal type.

    Args:
        diet_type           : e.g. "vegetarian", "non_vegetarian"
        budget              : e.g. "low", "medium", "flexible"
        cultural_preference : e.g. "bengali", "north_indian"
        meal_type           : "breakfast" | "lunch" | "snack" | "dinner" | None

    Returns a list of matching food dicts.
    """
    diet_key    = diet_type.strip().lower().replace(" ", "_")
    budget_key  = budget.strip().lower().replace(" ", "_").replace(" budget", "")
    culture_key = cultural_preference.strip().lower().replace(" ", "_")

    results = []
    for food in FOODS:
        if diet_key not in food["diet"]:
            continue
        if budget_key not in food["budget"]:
            continue
        culture_match = (
            culture_key in food["culture"]
            or "general" in food["culture"]
        )
        if not culture_match:
            continue
        if meal_type and meal_type not in food["meal_type"]:
            continue
        results.append(food)
    return results
