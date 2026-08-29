# models/__init__.py
# Imports all models so they are registered with SQLAlchemy metadata.

from .user import User
from .diet_preference import DietPreference
from .workout_preference import WorkoutPreference
from .workout_plan import WorkoutPlan
from .meal_plan import MealPlan
from .progress import Progress

__all__ = [
    "User",
    "DietPreference",
    "WorkoutPreference",
    "WorkoutPlan",
    "MealPlan",
    "Progress",
]
