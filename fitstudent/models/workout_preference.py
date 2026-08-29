"""
models/workout_preference.py – Workout preferences for a user.
"""
from datetime import datetime
from extensions import db


class WorkoutPreference(db.Model):
    __tablename__ = "workout_preferences"

    id                 = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    user_id            = db.Column(db.Integer,  db.ForeignKey("users.id", ondelete="CASCADE"),
                                   nullable=False)
    daily_workout_time = db.Column(db.Integer,  nullable=False, comment="Minutes per day")
    available_equipment = db.Column(db.String(60), nullable=False)
    created_at         = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at         = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                                   onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="workout_pref")

    def __repr__(self):
        return f"<WorkoutPreference user_id={self.user_id} equipment={self.available_equipment!r}>"
