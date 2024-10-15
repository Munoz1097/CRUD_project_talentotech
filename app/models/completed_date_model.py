from app import db
from datetime import datetime

class CompletedDate(db.Model):

    __tablename__ = 'completed_dates'
    
    completed_date_id = db.Column(db.Integer, primary_key=True)
    completed_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    fk_assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.assignment_id'), nullable=False)
    
    def __init__(self, fk_assignment_id):
        
        self.fk_assignment_id = fk_assignment_id