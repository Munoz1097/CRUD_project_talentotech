from app import db
from app.models.assignment_model import Assignment

class AssignmentService:

    @staticmethod
    def create_assignment(fk_user_id, fk_habit_id):
        
        new_assignment = Assignment(fk_user_id, fk_habit_id)

        db.session.add(new_assignment)
        db.session.commit()

        return new_assignment
    @staticmethod
    def get_all_assignments():
        """
        Obtener todos los Assignments de la base de datos.

        Returns:
            List[Assignments]: Lista de todos los Assignments en la base de datos.
        """
        # Recuperar todos los registros de la tabla Assignments
        return Assignment.query.all()
    @staticmethod
    def get_assignments_by_user_id(fk_user_id):
        """
        Obtener Assignments de la base de datos por el id del usuario.

        Returns:
            
        """
        return Assignment.query.filter_by(fk_user_id = fk_user_id).all()
        