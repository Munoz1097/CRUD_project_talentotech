from app import db
from datetime import datetime

class Assignment(db.Model):

    __tablename__ = 'assignments'

    assignment_id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    assignment_status = db.Column(db.Boolean, default=True, nullable=False)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    fk_habit_id = db.Column(db.Integer, db.ForeignKey('habits.habit_id'), nullable=False)
    completed_dates = db.relationship('CompletedDate', backref='assignment', lazy=True)  # Relación con la tabla 'assignments'


    def __init__(self, fk_user_id, fk_habit_id):

        self.fk_user_id = fk_user_id
        self.fk_habit_id = fk_habit_id