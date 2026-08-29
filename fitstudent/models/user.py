"""
models/user.py – SQLAlchemy model for the 'users' table.
"""
from datetime import datetime
from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id             = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    name           = db.Column(db.String(120),  nullable=False)
    age            = db.Column(db.Integer,      nullable=False)
    gender         = db.Column(db.String(20),   nullable=False)
    height         = db.Column(db.Float,        nullable=False, comment="Height in cm")
    weight         = db.Column(db.Float,        nullable=False, comment="Weight in kg")
    activity_level = db.Column(db.String(40),   nullable=False)
    fitness_goal   = db.Column(db.String(60),   nullable=False)
    fitness_level  = db.Column(db.String(30),   nullable=False)
    created_at     = db.Column(db.DateTime,     nullable=False, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime,     nullable=False, default=datetime.utcnow,
                               onupdate=datetime.utcnow)

    # Relationships – cascade deletes so removing a user removes all related data
    diet_pref       = db.relationship("DietPreference",   back_populates="user",
                                      uselist=False, cascade="all, delete-orphan")
    workout_pref    = db.relationship("WorkoutPreference", back_populates="user",
                                      uselist=False, cascade="all, delete-orphan")
    workout_plans   = db.relationship("WorkoutPlan",  back_populates="user",
                                      cascade="all, delete-orphan")
    meal_plans      = db.relationship("MealPlan",     back_populates="user",
                                      cascade="all, delete-orphan")
    progress_records = db.relationship("Progress",   back_populates="user",
                                       order_by="Progress.record_date",
                                       cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} name={self.name!r}>"
