from app import db
from app.models.completed_date_model import CompletedDate
from app.models.assignment_model import Assignment
from app.utils.validations import Validations

class CompletedDateService:
    """
    Servicio para gestionar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    relacionadas con las fechas en que un usuario completó un hábito.
    """

    @staticmethod
    def create_completed_date(assignment_id, completed_date):
        """
        Crear una nueva fecha de completación para una asignación.
        ---
        Este método permite crear una nueva entrada de fecha de completación asociada a una asignación.

        Args:
            assignment_id (int): ID de la asignación a la que se le agrega la fecha de completación.
            completed_date (date): Fecha de completación del hábito.

        Returns:
            CompletedDate: La nueva fecha de completación creada.

        Raises:
            ValueError: Si la asignación no existe o si la fecha de completación ya existe.
        """
        Validations.check_fk_existence(Assignment.assignment_id, assignment_id, 'assignments')
        Validations.check_data_pair_existence(CompletedDate.fk_assignment_id, assignment_id, CompletedDate.completed_date, completed_date, 'date')
        
        new_completed_date = CompletedDate(assignment_id, completed_date)

        db.session.add(new_completed_date)
        db.session.commit()

        return new_completed_date
    
    @staticmethod
    def get_date_by_date_id(date_id):
        """
        Obtener una fecha de completación por su ID.

        Args:
            date_id (int): ID de la fecha de completación a buscar.

        Returns:
            CompletedDate: La fecha de completación encontrada.

        Raises:
            ValueError: Si la fecha de completación no existe.
        """
        date = CompletedDate.query.filter_by(completed_date_id=date_id).first()
        date_validated = Validations.check_if_exists(date, 'CompletedDate')
        return date_validated
    
    @staticmethod
    def get_all_dates_by_assignment_id(assignment_id):
        """
        Obtener todas las fechas de completación asociadas a una asignación específica.

        Args:
            assignment_id (int): ID de la asignación para la cual se buscan las fechas de completación.

        Returns:
            List[CompletedDate]: Lista de fechas de completación asociadas a la asignación.
        """
        return CompletedDate.query.filter_by(fk_assignment_id=assignment_id).all()
    
    @staticmethod
    def get_all_dates():
        """
        Obtener todas las fechas de completación en la base de datos.

        Returns:
            List[CompletedDate]: Lista de todas las fechas de completación en la base de datos.
        """
        return CompletedDate.query.all()
