from app import db
from app.models.assignment_model import Assignment
from app.utils.validations import Validations

class AssignmentService:
    @staticmethod
    def create_assignment(fk_user_id, fk_habit_id):
        
        new_assignment = Assignment(fk_user_id, fk_habit_id)
        Validations.check_data_pair_existence(Assignment.fk_user_id, fk_user_id, Assignment.fk_habit_id, fk_habit_id, 'assignment')

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
        assignments = Assignment.query.filter_by(fk_user_id = fk_user_id).all()
        assignments_validated = Validations.check_if_exists(assignments, 'Assignment')
        return assignments_validated
    
    @staticmethod
    def delete_assignment(assignment_id):
        """
        Eliminar un usuario existente.

        Args:
            user_id (int): ID del usuario a eliminar.

        Returns:
            None
        """
        # Buscar al usuario por su ID
        assignment = AssignmentService.get_assignment_by_assignment_id(assignment_id)
        # Eliminar el usuario de la base de datos
        db.session.delete(assignment)
        db.session.commit()

    @staticmethod
    def get_assignment_by_assignment_id(assignment_id):
        """
        Obtener Assignments de la base de datos por el id de la asignación.

        Returns:
            
        """
        assignment = Assignment.query.filter_by(assignment_id = assignment_id).first()
        assignment_validated = Validations.check_if_exists(assignment, 'Assignment')
        return assignment_validated