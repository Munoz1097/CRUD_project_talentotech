from app import db
from app.models.completed_date_model import CompletedDate

class CompletedDateService:

    @staticmethod
    def create_completed_date(fk_assignment_id):
        
        new_completed_date = CompletedDate(fk_assignment_id)

        db.session.add(new_completed_date)
        db.session.commit()

        return new_completed_date