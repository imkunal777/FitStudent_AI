"""
models/progress.py – User's progress records (weight, workout completion).
"""
from datetime import datetime, date
from extensions import db


class Progress(db.Model):
    __tablename__ = "progress"

    id                = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    user_id           = db.Column(db.Integer,  db.ForeignKey("users.id", ondelete="CASCADE"),
                                  nullable=False)
    weight            = db.Column(db.Float,    nullable=False)
    workout_completed = db.Column(db.Boolean,  nullable=False, default=False)
    notes             = db.Column(db.Text,     nullable=True)
    record_date       = db.Column(db.Date,     nullable=False, default=date.today)
    created_at        = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("User", back_populates="progress_records")

    def __repr__(self):
        return f"<Progress user_id={self.user_id} date={self.record_date} weight={self.weight}>"
