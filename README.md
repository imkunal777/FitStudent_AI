# FitStudent AI – Personalized Fitness and Nutrition Companion

A medium-sized AI-powered web application that generates **personalised workout plans** and **daily meal plans** for students, based on their unique body metrics, fitness goals, dietary preferences, budget, cultural food habits, and available equipment.

> ⚠️ **Disclaimer:** All fitness and nutrition recommendations provided by this application are general estimates for educational/informational purposes only. They are **not medical or professional dietary advice**. Consult a qualified healthcare provider or certified nutritionist before starting any new fitness or diet programme.

---

## Features

| Feature | Description |
|---|---|
| **Profile Creation** | Collect name, age, gender, height, weight, activity level, fitness goal, and fitness level |
| **Fitness Analysis** | Calculate BMI, BMI category, BMR, daily calorie target, protein range, water intake |
| **Workout Plan** | Personalised 7-day plan based on goal, fitness level, and available equipment |
| **Meal Plan** | Daily meals (breakfast/lunch/snack/dinner) based on diet type, budget, and culture |
| **Cultural Food Preferences** | Supports Bengali, North Indian, South Indian, and General Indian food styles |
| **Equipment-Based Workouts** | Adapts plans for No Equipment, Dumbbells, Resistance Bands, Basic Home, Full Gym |
| **Budget-Aware Meals** | Low / Medium / Flexible budget settings affect food recommendations |
| **Progress Tracking** | Log daily weight and workout completion; view weight chart and history |
| **Preference Management** | Update dietary and workout preferences at any time |
| **Plan Regeneration** | Regenerate plans instantly from the dashboard |

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3, minimal JavaScript |
| **Backend** | Python 3.10+, Flask 3.x |
| **Database** | MySQL (via Flask-SQLAlchemy + PyMySQL) |
| **Configuration** | python-dotenv (.env file) |
| **Calculations** | Pure Python (no external API) |

---

## Project Structure

```
fitstudent_ai/
│
├── app.py                  # Flask application, all routes
├── config.py               # Configuration classes
├── extensions.py           # Shared Flask extensions (db)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── README.md               # This file
│
├── models/
│   ├── __init__.py
│   ├── user.py             # User profile
│   ├── diet_preference.py  # Dietary preferences
│   ├── workout_preference.py
│   ├── workout_plan.py     # Generated plan (JSON)
│   ├── meal_plan.py        # Generated meal plan (JSON)
│   └── progress.py         # Daily progress records
│
├── services/
│   ├── fitness_calculator.py    # BMI, BMR, calories, protein, water
│   ├── recommendation_engine.py # Orchestrates all generators
│   ├── workout_generator.py     # 7-day workout plan logic
│   └── meal_generator.py        # Daily meal plan logic
│
├── data/
│   └── food_data.py        # Structured food dataset (40+ foods)
│
├── templates/
│   ├── base.html           # Master layout
│   ├── index.html          # Home / landing page
│   ├── profile.html        # Profile form
│   ├── preferences.html    # Workout + diet + budget preferences
│   ├── dashboard.html      # Personalised dashboard
│   ├── workout.html        # Full 7-day workout plan
│   ├── meal_plan.html      # Daily meal plan
│   └── progress.html       # Progress tracker
│
├── static/
│   ├── css/style.css       # All styles
│   └── js/script.js        # Form validation + UI interactions
│
└── database/
    └── mysql_setup.sql     # Database and table creation script
```

---

## Installation Instructions

### Prerequisites

- Python 3.10 or newer
- MySQL 8.x (or MariaDB 10.x)
- `pip`

---

### Step 1 – Download the project

```bash
# If using git:
git clone <repository-url>
cd fitstudent_ai

# Or simply extract the downloaded ZIP into a folder.
```

---

### Step 2 – Create a Python virtual environment

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

---

### Step 3 – Install dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4 – Create the MySQL database

Open your MySQL client (MySQL Workbench, DBeaver, or command line) and run:

```bash
mysql -u root -p < database/mysql_setup.sql
```

Or paste the contents of `database/mysql_setup.sql` directly into MySQL Workbench and execute.

---

### Step 5 – Configure environment variables

```bash
# Copy the example file
cp .env.example .env
```

Open `.env` and fill in your actual MySQL credentials:

```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_actual_password
MYSQL_DB=fitstudent_ai
MYSQL_PORT=3306
SECRET_KEY=some-long-random-string
```

---

### Step 6 – Run the Flask application

```bash
python app.py
```

The application will start at: **http://127.0.0.1:5000**

---

## Application Workflow

```
Home Page (/)
    ↓
Create Profile (/profile)      ← Enter body metrics and fitness goal
    ↓
Set Preferences (/preferences) ← Diet, budget, equipment, culture
    ↓
Plan Generation                ← Recommendation engine runs
    ↓
Dashboard (/dashboard)         ← View fitness analysis + plan summary
    ↓
Workout Plan (/workout-plan)   ← Full 7-day plan with exercises
    ↓
Meal Plan (/meal-plan)         ← Daily breakfast/lunch/snack/dinner
    ↓
Progress Tracker (/progress)   ← Log weight and workout completion
```

---

## Recommendation System

The recommendation engine (`services/recommendation_engine.py`) works as follows:

1. **Fitness Metrics**: Calculates BMI, BMR, TDEE (adjusted for activity + goal), protein range, and water intake using the Mifflin-St Jeor formula.

2. **Workout Plan Selection**: The workout generator (`services/workout_generator.py`) selects a plan template from a library of pre-built 7-day templates based on:
   - Fitness goal (weight loss / muscle building / stamina etc.)
   - Fitness level (beginner / intermediate / advanced)
   - Available equipment

3. **Meal Plan Generation**: The meal generator (`services/meal_generator.py`) scores foods from the food dataset (`data/food_data.py`) using:
   - Diet type compatibility (vegetarian / non-vegetarian / vegan / eggetarian)
   - Budget level (low / medium / flexible)
   - Cultural preference (Bengali / North Indian / South Indian)
   - User's preferred and disliked foods
   - Calorie distribution across meals (25% breakfast / 35% lunch / 10% snack / 30% dinner)
   - High-protein prioritisation for muscle building / weight gain goals

4. **Personalisation**: No two users with meaningfully different profiles receive the same plan. Equipment, budget, cultural preference, diet type, and goal all change the output.

The engine is architected so a real ML model or external AI API can be plugged in later by replacing or extending `_score_user()` in `recommendation_engine.py`.

---

## Database Tables

| Table | Description |
|---|---|
| `users` | Core profile data |
| `diet_preferences` | Diet type, budget, preferred/disliked foods, culture |
| `workout_preferences` | Daily time, equipment |
| `workout_plans` | JSON-encoded 7-day plan |
| `meal_plans` | JSON-encoded daily meal plan |
| `progress` | Daily weight + workout completion records |

---

## Disclaimer

FitStudent AI is a college project built for educational purposes.

All fitness metrics (BMI, BMR, calorie estimates, protein targets) are general reference values based on widely-used fitness formulas. They **do not constitute professional medical, dietary, or clinical advice**.

Individuals with medical conditions, eating disorders, or special health considerations should consult a qualified healthcare professional before using any fitness or nutrition guidance.
