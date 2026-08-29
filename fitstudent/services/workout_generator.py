"""
services/workout_generator.py
-----------------------------------------------------------------------
Generates a personalised 7-day workout plan based on:
  - fitness_goal    : weight_loss | weight_gain | muscle_building |
                      general_fitness | improve_stamina
  - fitness_level   : beginner | intermediate | advanced
  - equipment       : no_equipment | dumbbells | resistance_bands |
                      basic_home_equipment | full_gym_access
  - daily_minutes   : int  (available workout time per day)

Returns a list of 7 day-dicts, each with:
  {
    "day"      : "Monday",
    "focus"    : "Full Body / Cardio / ...",
    "type"     : "workout" | "rest" | "active_recovery",
    "exercises": [ { name, sets, reps, duration, rest, instructions }, ... ]
  }
-----------------------------------------------------------------------
"""

import copy

# ------------------------------------------------------------------
# Exercise Library
# ------------------------------------------------------------------

EXERCISE_LIBRARY = {
    # ---- Bodyweight -----------------------------------------------
    "bodyweight_squat": {
        "name": "Bodyweight Squat",
        "sets": 3, "reps": "15", "duration": "—",
        "rest": "45 sec",
        "instructions": (
            "Stand with feet shoulder-width apart. Lower your hips until thighs are "
            "parallel to the floor, keeping knees over toes. Drive through heels to stand."
        ),
    },
    "pushup": {
        "name": "Push-Up",
        "sets": 3, "reps": "10-15", "duration": "—",
        "rest": "45 sec",
        "instructions": (
            "Hands slightly wider than shoulders. Lower chest to the floor keeping "
            "body in a straight line. Push back up explosively."
        ),
    },
    "lunge": {
        "name": "Forward Lunge",
        "sets": 3, "reps": "12 each leg", "duration": "—",
        "rest": "45 sec",
        "instructions": (
            "Step forward with one foot, lower back knee toward the floor, "
            "then push back to starting position. Alternate legs."
        ),
    },
    "plank": {
        "name": "Plank",
        "sets": 3, "reps": "—", "duration": "30 sec",
        "rest": "30 sec",
        "instructions": (
            "Forearms on the floor, body in a straight line from head to heels. "
            "Engage core and hold. Do not let hips sag."
        ),
    },
    "jumping_jacks": {
        "name": "Jumping Jacks",
        "sets": 3, "reps": "30", "duration": "—",
        "rest": "30 sec",
        "instructions": (
            "Start with feet together, arms at sides. Jump feet out while raising arms "
            "overhead, then return to start."
        ),
    },
    "high_knees": {
        "name": "High Knees",
        "sets": 3, "reps": "—", "duration": "40 sec",
        "rest": "30 sec",
        "instructions": (
            "Run in place driving knees up to hip height alternately. "
            "Pump arms to increase intensity."
        ),
    },
    "mountain_climber": {
        "name": "Mountain Climbers",
        "sets": 3, "reps": "—", "duration": "40 sec",
        "rest": "30 sec",
        "instructions": (
            "Start in a high plank. Drive knees alternately toward chest rapidly "
            "keeping hips level."
        ),
    },
    "glute_bridge": {
        "name": "Glute Bridge",
        "sets": 3, "reps": "15", "duration": "—",
        "rest": "30 sec",
        "instructions": (
            "Lie on your back, knees bent. Drive hips up by squeezing glutes, "
            "hold 1 second at top, lower slowly."
        ),
    },
    "burpee": {
        "name": "Burpee",
        "sets": 3, "reps": "10", "duration": "—",
        "rest": "60 sec",
        "instructions": (
            "From standing, drop hands to floor, kick feet back to plank, "
            "do a push-up, jump feet to hands, then jump up with arms overhead."
        ),
    },
    "tricep_dip_chair": {
        "name": "Chair Tricep Dip",
        "sets": 3, "reps": "12", "duration": "—",
        "rest": "45 sec",
        "instructions": (
            "Place hands on a sturdy chair edge, legs extended. Lower by bending elbows "
            "to 90°, then push back up."
        ),
    },
    "superman": {
        "name": "Superman Hold",
        "sets": 3, "reps": "12", "duration": "—",
        "rest": "30 sec",
        "instructions": (
            "Lie face down, arms extended. Simultaneously lift arms, chest, and legs "
            "off floor. Hold 2 seconds at top."
        ),
    },
    "side_plank": {
        "name": "Side Plank",
        "sets": 2, "reps": "—", "duration": "25 sec each side",
        "rest": "30 sec",
        "instructions": (
            "Lie on one side, elbow under shoulder. Raise hips to form a straight line. "
            "Hold. Repeat other side."
        ),
    },
    "light_jog": {
        "name": "Light Jog / Brisk Walk",
        "sets": 1, "reps": "—", "duration": "20-30 min",
        "rest": "—",
        "instructions": (
            "Jog at a comfortable pace where you can hold a conversation. "
            "If outdoors is unavailable, march vigorously in place."
        ),
    },
    "walking": {
        "name": "Brisk Walking",
        "sets": 1, "reps": "—", "duration": "30 min",
        "rest": "—",
        "instructions": (
            "Walk at a brisk pace (~5-6 km/h). Maintain upright posture and engage core."
        ),
    },
    "stretching_routine": {
        "name": "Full-Body Stretching",
        "sets": 1, "reps": "—", "duration": "15-20 min",
        "rest": "—",
        "instructions": (
            "Hold each major muscle-group stretch for 20-30 seconds. "
            "Focus on quads, hamstrings, chest, shoulders, and back."
        ),
    },
    # ---- Dumbbell -------------------------------------------------
    "db_bicep_curl": {
        "name": "Dumbbell Bicep Curl",
        "sets": 3, "reps": "12", "duration": "—",
        "rest": "60 sec",
        "instructions": (
            "Stand with a dumbbell in each hand, palms forward. Curl weights to shoulders "
            "squeezing biceps, lower slowly."
        ),
    },
    "db_shoulder_press": {
        "name": "Dumbbell Shoulder Press",
        "sets": 3, "reps": "10-12", "duration": "—",
        "rest": "60 sec",
        "instructions": (
            "Hold dumbbells at shoulder height, palms facing forward. Press overhead "
            "until arms are nearly straight, lower slowly."
        ),
    },
    "db_goblet_squat": {
        "name": "Dumbbell Goblet Squat",
        "sets": 3, "reps": "12", "duration": "—",
        "rest": "60 sec",
        "instructions": (
            "Hold one dumbbell vertically at chest height. Squat down until thighs are "
            "parallel to floor, keeping back straight."
        ),
    },
    "db_bent_over_row": {
        "name": "Dumbbell Bent-Over Row",
        "sets": 3, "reps": "10-12 each arm", "duration": "—",
        "rest": "60 sec",
        "instructions": (
            "Hinge at hips with slight knee bend. Pull dumbbell to hip, "
            "squeezing back at top. Lower with control."
        ),
    },
    "db_deadlift": {
        "name": "Dumbbell Romanian Deadlift",
        "sets": 3, "reps": "12", "duration": "—",
        "rest": "60 sec",
        "instructions": (
            "Hold dumbbells in front of thighs. Hinge at hips lowering weights "
            "down shins, feeling hamstring stretch, then drive hips forward to stand."
        ),
    },
    "db_chest_press": {
        "name": "Dumbbell Chest Press (Floor)",
        "sets": 3, "reps": "10-12", "duration": "—",
        "rest": "60 sec",
        "instructions": (
            "Lie on floor holding dumbbells at chest. Press directly up until arms "
            "extend, lower slowly under control."
        ),
    },
    "db_lateral_raise": {
        "name": "Dumbbell Lateral Raise",
        "sets": 3, "reps": "12-15", "duration": "—",
        "rest": "45 sec",
        "instructions": (
            "Hold dumbbells at sides. Raise arms to shoulder height keeping slight bend "
            "in elbows. Lower slowly."
        ),
    },
    # ---- Gym / Barbell -------------------------------------------
    "barbell_squat": {
        "name": "Barbell Back Squat",
        "sets": 4, "reps": "8-10", "duration": "—",
        "rest": "90 sec",
        "instructions": (
            "Bar resting on traps. Squat down keeping chest tall, knees tracking "
            "over toes. Drive through heels to stand."
        ),
    },
    "bench_press": {
        "name": "Barbell Bench Press",
        "sets": 4, "reps": "8-10", "duration": "—",
        "rest": "90 sec",
        "instructions": (
            "Lie on bench, grip slightly wider than shoulders. Lower bar to chest "
            "under control, press back up powerfully."
        ),
    },
    "deadlift": {
        "name": "Conventional Deadlift",
        "sets": 4, "reps": "6-8", "duration": "—",
        "rest": "2 min",
        "instructions": (
            "Bar over mid-foot. Hip-hinge and grab bar, maintain neutral spine. "
            "Drive through floor keeping bar close to body to lockout."
        ),
    },
    "lat_pulldown": {
        "name": "Lat Pulldown",
        "sets": 3, "reps": "10-12", "duration": "—",
        "rest": "75 sec",
        "instructions": (
            "Sit at cable machine. Pull bar to upper chest squeezing lats, "
            "return slowly until arms are fully extended."
        ),
    },
    "seated_cable_row": {
        "name": "Seated Cable Row",
        "sets": 3, "reps": "10-12", "duration": "—",
        "rest": "75 sec",
        "instructions": (
            "Sit upright at cable machine, pull handle to abdomen squeezing shoulder "
            "blades together, return slowly."
        ),
    },
    "overhead_press": {
        "name": "Barbell Overhead Press",
        "sets": 3, "reps": "8-10", "duration": "—",
        "rest": "90 sec",
        "instructions": (
            "Bar at shoulder height in front. Press overhead, locking out arms at top. "
            "Lower with control."
        ),
    },
    "leg_press": {
        "name": "Leg Press",
        "sets": 3, "reps": "12-15", "duration": "—",
        "rest": "75 sec",
        "instructions": (
            "Place feet shoulder-width on platform. Lower until knees reach 90°, "
            "press through heels to extend."
        ),
    },
    "cable_tricep_pushdown": {
        "name": "Cable Tricep Pushdown",
        "sets": 3, "reps": "12-15", "duration": "—",
        "rest": "45 sec",
        "instructions": (
            "Stand at cable stack with rope/bar at head height. Extend elbows pressing "
            "down, keeping upper arms stationary."
        ),
    },
    "treadmill_run": {
        "name": "Treadmill Run",
        "sets": 1, "reps": "—", "duration": "25-30 min",
        "rest": "—",
        "instructions": (
            "Warm up at 5 km/h for 5 min, then run at 8-10 km/h for 20-25 min, "
            "cool down at 5 km/h for 5 min."
        ),
    },
    # ---- Resistance Bands ----------------------------------------
    "band_squat": {
        "name": "Resistance Band Squat",
        "sets": 3, "reps": "15", "duration": "—",
        "rest": "45 sec",
        "instructions": (
            "Step on band, hold handles at shoulders. Perform a squat, feeling "
            "extra resistance as you stand."
        ),
    },
    "band_row": {
        "name": "Resistance Band Row",
        "sets": 3, "reps": "12", "duration": "—",
        "rest": "45 sec",
        "instructions": (
            "Anchor band at waist height. Pull handles to sides of torso squeezing "
            "shoulder blades. Return slowly."
        ),
    },
    "band_chest_press": {
        "name": "Resistance Band Chest Press",
        "sets": 3, "reps": "12", "duration": "—",
        "rest": "45 sec",
        "instructions": (
            "Anchor band behind you at chest height. Press handles forward until arms "
            "extend, return slowly."
        ),
    },
    "band_bicep_curl": {
        "name": "Resistance Band Bicep Curl",
        "sets": 3, "reps": "12-15", "duration": "—",
        "rest": "45 sec",
        "instructions": (
            "Stand on band, curl handles to shoulders. Lower slowly. "
            "Keep elbows pinned at sides."
        ),
    },
}

# ------------------------------------------------------------------
# Day names
# ------------------------------------------------------------------
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ------------------------------------------------------------------
# Workout Templates
# Each template is a list of 7 day-specs (one per day).
# A day-spec: { focus, type, exercise_keys }
# ------------------------------------------------------------------

def _e(key):
    """Return a deep copy of an exercise dict by key."""
    return copy.deepcopy(EXERCISE_LIBRARY[key])


def _build_plan(day_specs: list) -> list:
    """Convert a list of day-specs into the full output format."""
    plan = []
    for i, spec in enumerate(day_specs):
        day_dict = {
            "day": DAYS[i],
            "focus": spec["focus"],
            "type": spec["type"],
            "exercises": [_e(k) for k in spec.get("exercise_keys", [])],
        }
        plan.append(day_dict)
    return plan


# ------------------------------------------------------------------
# Template: Beginner · No Equipment
# ------------------------------------------------------------------
BEGINNER_NO_EQUIPMENT = [
    {"focus": "Full Body Intro",       "type": "workout",         "exercise_keys": ["bodyweight_squat", "pushup", "plank", "jumping_jacks", "glute_bridge"]},
    {"focus": "Active Recovery / Walk","type": "active_recovery", "exercise_keys": ["walking", "stretching_routine"]},
    {"focus": "Lower Body",            "type": "workout",         "exercise_keys": ["bodyweight_squat", "lunge", "glute_bridge", "side_plank"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
    {"focus": "Upper Body + Core",     "type": "workout",         "exercise_keys": ["pushup", "tricep_dip_chair", "plank", "superman"]},
    {"focus": "Cardio Circuit",        "type": "workout",         "exercise_keys": ["jumping_jacks", "high_knees", "mountain_climber", "burpee"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
]

# ------------------------------------------------------------------
# Template: Beginner · Weight Loss · No Equipment
# ------------------------------------------------------------------
BEGINNER_WEIGHT_LOSS_NO_EQ = [
    {"focus": "Cardio + Core",         "type": "workout",         "exercise_keys": ["jumping_jacks", "high_knees", "plank", "mountain_climber"]},
    {"focus": "Brisk Walk",            "type": "active_recovery", "exercise_keys": ["walking"]},
    {"focus": "Full Body Circuit",     "type": "workout",         "exercise_keys": ["bodyweight_squat", "pushup", "lunge", "burpee", "glute_bridge"]},
    {"focus": "Active Recovery",       "type": "active_recovery", "exercise_keys": ["light_jog", "stretching_routine"]},
    {"focus": "Cardio Blast",          "type": "workout",         "exercise_keys": ["jumping_jacks", "burpee", "high_knees", "mountain_climber"]},
    {"focus": "Lower Body + Cardio",   "type": "workout",         "exercise_keys": ["bodyweight_squat", "lunge", "glute_bridge", "light_jog"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
]

# ------------------------------------------------------------------
# Template: Intermediate · Weight Loss · No Equipment
# ------------------------------------------------------------------
INTERMEDIATE_WEIGHT_LOSS_NO_EQ = [
    {"focus": "HIIT Circuit",          "type": "workout",         "exercise_keys": ["burpee", "mountain_climber", "high_knees", "jumping_jacks", "plank"]},
    {"focus": "Strength + Cardio",     "type": "workout",         "exercise_keys": ["bodyweight_squat", "pushup", "lunge", "tricep_dip_chair", "light_jog"]},
    {"focus": "Active Recovery",       "type": "active_recovery", "exercise_keys": ["walking", "stretching_routine"]},
    {"focus": "Full Body Strength",    "type": "workout",         "exercise_keys": ["bodyweight_squat", "pushup", "glute_bridge", "superman", "side_plank"]},
    {"focus": "Cardio Run",            "type": "workout",         "exercise_keys": ["light_jog"]},
    {"focus": "Upper Body + Core",     "type": "workout",         "exercise_keys": ["pushup", "plank", "mountain_climber", "side_plank"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
]

# ------------------------------------------------------------------
# Template: Beginner · Dumbbells
# ------------------------------------------------------------------
BEGINNER_DUMBBELLS = [
    {"focus": "Upper Body",            "type": "workout",         "exercise_keys": ["db_chest_press", "db_bent_over_row", "db_bicep_curl", "db_lateral_raise"]},
    {"focus": "Active Recovery",       "type": "active_recovery", "exercise_keys": ["walking", "stretching_routine"]},
    {"focus": "Lower Body",            "type": "workout",         "exercise_keys": ["db_goblet_squat", "db_deadlift", "lunge", "glute_bridge"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
    {"focus": "Shoulders + Arms",      "type": "workout",         "exercise_keys": ["db_shoulder_press", "db_bicep_curl", "db_lateral_raise", "tricep_dip_chair"]},
    {"focus": "Full Body Circuit",     "type": "workout",         "exercise_keys": ["db_goblet_squat", "db_chest_press", "db_bent_over_row", "plank"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
]

# ------------------------------------------------------------------
# Template: Intermediate · Muscle Building · Dumbbells
# ------------------------------------------------------------------
INTERMEDIATE_MUSCLE_DUMBBELLS = [
    {"focus": "Chest + Triceps",       "type": "workout",         "exercise_keys": ["db_chest_press", "pushup", "tricep_dip_chair", "db_lateral_raise"]},
    {"focus": "Back + Biceps",         "type": "workout",         "exercise_keys": ["db_bent_over_row", "db_bicep_curl", "superman"]},
    {"focus": "Active Recovery",       "type": "active_recovery", "exercise_keys": ["walking", "stretching_routine"]},
    {"focus": "Legs + Glutes",         "type": "workout",         "exercise_keys": ["db_goblet_squat", "db_deadlift", "lunge", "glute_bridge"]},
    {"focus": "Shoulders + Core",      "type": "workout",         "exercise_keys": ["db_shoulder_press", "db_lateral_raise", "plank", "side_plank"]},
    {"focus": "Full Body Compound",    "type": "workout",         "exercise_keys": ["db_goblet_squat", "db_chest_press", "db_bent_over_row", "db_shoulder_press"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
]

# ------------------------------------------------------------------
# Template: Resistance Bands
# ------------------------------------------------------------------
BEGINNER_BANDS = [
    {"focus": "Upper Body",            "type": "workout",         "exercise_keys": ["band_chest_press", "band_row", "band_bicep_curl", "db_lateral_raise"]},
    {"focus": "Active Recovery",       "type": "active_recovery", "exercise_keys": ["walking", "stretching_routine"]},
    {"focus": "Lower Body",            "type": "workout",         "exercise_keys": ["band_squat", "lunge", "glute_bridge", "side_plank"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
    {"focus": "Full Body",             "type": "workout",         "exercise_keys": ["band_squat", "band_chest_press", "band_row", "plank"]},
    {"focus": "Cardio + Core",         "type": "workout",         "exercise_keys": ["jumping_jacks", "high_knees", "mountain_climber", "plank"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
]

# ------------------------------------------------------------------
# Template: Full Gym Access · Muscle Building
# ------------------------------------------------------------------
GYM_MUSCLE_INTERMEDIATE = [
    {"focus": "Chest + Triceps",       "type": "workout",         "exercise_keys": ["bench_press", "db_chest_press", "pushup", "cable_tricep_pushdown"]},
    {"focus": "Back + Biceps",         "type": "workout",         "exercise_keys": ["deadlift", "lat_pulldown", "seated_cable_row", "db_bicep_curl"]},
    {"focus": "Active Recovery / Cardio","type":"active_recovery","exercise_keys": ["treadmill_run", "stretching_routine"]},
    {"focus": "Legs",                  "type": "workout",         "exercise_keys": ["barbell_squat", "leg_press", "db_deadlift", "glute_bridge"]},
    {"focus": "Shoulders + Arms",      "type": "workout",         "exercise_keys": ["overhead_press", "db_lateral_raise", "db_bicep_curl", "cable_tricep_pushdown"]},
    {"focus": "Full Body + Core",      "type": "workout",         "exercise_keys": ["bench_press", "lat_pulldown", "barbell_squat", "plank", "side_plank"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
]

GYM_MUSCLE_ADVANCED = [
    {"focus": "Heavy Chest",           "type": "workout",         "exercise_keys": ["bench_press", "db_chest_press", "cable_tricep_pushdown", "pushup"]},
    {"focus": "Heavy Back",            "type": "workout",         "exercise_keys": ["deadlift", "lat_pulldown", "seated_cable_row", "db_bent_over_row"]},
    {"focus": "Active Recovery",       "type": "active_recovery", "exercise_keys": ["treadmill_run", "stretching_routine"]},
    {"focus": "Heavy Legs",            "type": "workout",         "exercise_keys": ["barbell_squat", "leg_press", "deadlift", "glute_bridge"]},
    {"focus": "Shoulders + Arms",      "type": "workout",         "exercise_keys": ["overhead_press", "db_lateral_raise", "db_bicep_curl", "cable_tricep_pushdown"]},
    {"focus": "Power Full Body",       "type": "workout",         "exercise_keys": ["deadlift", "bench_press", "barbell_squat", "overhead_press"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
]

# ------------------------------------------------------------------
# Template: Stamina / Cardio Focus
# ------------------------------------------------------------------
STAMINA_INTERMEDIATE = [
    {"focus": "Cardio + Core",         "type": "workout",         "exercise_keys": ["light_jog", "plank", "mountain_climber"]},
    {"focus": "Interval Training",     "type": "workout",         "exercise_keys": ["high_knees", "jumping_jacks", "burpee", "mountain_climber"]},
    {"focus": "Active Recovery",       "type": "active_recovery", "exercise_keys": ["walking", "stretching_routine"]},
    {"focus": "Endurance Run",         "type": "workout",         "exercise_keys": ["light_jog"]},
    {"focus": "Bodyweight Strength",   "type": "workout",         "exercise_keys": ["bodyweight_squat", "pushup", "lunge", "glute_bridge"]},
    {"focus": "Long Steady Cardio",    "type": "workout",         "exercise_keys": ["light_jog"]},
    {"focus": "Rest",                  "type": "rest",            "exercise_keys": []},
]

# ------------------------------------------------------------------
# Main selector function
# ------------------------------------------------------------------

def _normalise(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def generate_workout_plan(fitness_goal: str, fitness_level: str,
                          equipment: str, daily_minutes: int) -> list:
    """
    Entry point: select and return the most appropriate 7-day workout plan.

    Args:
        fitness_goal   : user's fitness goal (display string)
        fitness_level  : beginner | intermediate | advanced
        equipment      : available equipment (display string)
        daily_minutes  : minutes available per day

    Returns:
        list of 7 day-dicts (see module docstring for schema)
    """
    goal   = _normalise(fitness_goal)
    level  = _normalise(fitness_level)
    equip  = _normalise(equipment)

    # ---- Stamina goal → stamina template regardless of equipment ----
    if goal == "improve_stamina":
        return _build_plan(STAMINA_INTERMEDIATE)

    # ---- Muscle building -------------------------------------------
    if goal == "muscle_building":
        if equip == "full_gym_access":
            if level == "advanced":
                return _build_plan(GYM_MUSCLE_ADVANCED)
            return _build_plan(GYM_MUSCLE_INTERMEDIATE)
        if equip in ("dumbbells", "basic_home_equipment"):
            return _build_plan(INTERMEDIATE_MUSCLE_DUMBBELLS)
        if equip == "resistance_bands":
            return _build_plan(BEGINNER_BANDS)
        # No equipment – bodyweight strength focus
        return _build_plan(INTERMEDIATE_WEIGHT_LOSS_NO_EQ)

    # ---- Weight loss -----------------------------------------------
    if goal == "weight_loss":
        if equip == "full_gym_access":
            # Gym cardio + compound lifts
            return _build_plan(GYM_MUSCLE_INTERMEDIATE)
        if equip in ("dumbbells", "basic_home_equipment"):
            return _build_plan(BEGINNER_DUMBBELLS)
        if level == "beginner":
            return _build_plan(BEGINNER_WEIGHT_LOSS_NO_EQ)
        return _build_plan(INTERMEDIATE_WEIGHT_LOSS_NO_EQ)

    # ---- Weight gain -----------------------------------------------
    if goal == "weight_gain":
        if equip == "full_gym_access":
            return _build_plan(GYM_MUSCLE_INTERMEDIATE)
        if equip in ("dumbbells", "basic_home_equipment"):
            return _build_plan(BEGINNER_DUMBBELLS)
        if equip == "resistance_bands":
            return _build_plan(BEGINNER_BANDS)
        return _build_plan(BEGINNER_NO_EQUIPMENT)

    # ---- General fitness (default) ---------------------------------
    if equip == "full_gym_access":
        return _build_plan(GYM_MUSCLE_INTERMEDIATE)
    if equip in ("dumbbells", "basic_home_equipment"):
        return _build_plan(BEGINNER_DUMBBELLS)
    if equip == "resistance_bands":
        return _build_plan(BEGINNER_BANDS)
    if level == "beginner":
        return _build_plan(BEGINNER_NO_EQUIPMENT)
    return _build_plan(INTERMEDIATE_WEIGHT_LOSS_NO_EQ)
