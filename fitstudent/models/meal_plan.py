"""
models/meal_plan.py – A generated daily meal plan stored as JSON text.
"""
from datetime import datetime
from extensions import db


class MealPlan(db.Model):
    __tablename__ = "meal_plans"

    id         = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    user_id    = db.Column(db.Integer,  db.ForeignKey("users.id", ondelete="CASCADE"),
                           nullable=False)
    plan_data  = db.Column(db.Text,     nullable=False, comment="JSON-encoded daily meal plan")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="meal_plans")

    def __repr__(self):
        return f"<MealPlan id={self.id} user_id={self.user_id}>"
