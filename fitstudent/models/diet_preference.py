"""
models/diet_preference.py – Dietary preferences for a user.
"""
from datetime import datetime
from extensions import db


class DietPreference(db.Model):
    __tablename__ = "diet_preferences"

    id                  = db.Column(db.Integer,   primary_key=True, autoincrement=True)
    user_id             = db.Column(db.Integer,   db.ForeignKey("users.id", ondelete="CASCADE"),
                                    nullable=False)
    diet_type           = db.Column(db.String(40),  nullable=False)
    budget              = db.Column(db.String(30),  nullable=False)
    preferred_foods     = db.Column(db.Text,         nullable=True)
    disliked_foods      = db.Column(db.Text,         nullable=True)
    cultural_preference = db.Column(db.String(60),   nullable=True)
    created_at          = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at          = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                                    onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="diet_pref")

    def __repr__(self):
        return f"<DietPreference user_id={self.user_id} diet={self.diet_type!r}>"
