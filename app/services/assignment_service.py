from app import db
from app.models.assignment_model import Assignment

class AssignmentService:

    @staticmethod
    def create_assignment(fk_user_id, fk_habit_id):
        
        new_assignment = Assignment(fk_user_id, fk_habit_id)

        db.session.add(new_assignment)
        db.session.commit()

        return new_assignment