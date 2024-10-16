from app import db
from app.models.habit_model import Habit
from app.utils.validations import Validations

class HabitService:
    """
    Servicio para gestionar las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) 
    relacionadas con los hábitos en la base de datos.
    """

    @staticmethod
    def create_habit(habit_name, time_of_day):
        """
        Crear un nuevo hábito.

        Args:
            habit_name (str): El nombre del hábito.
            time_of_day (str): El momento del día en el que se realiza el hábito (puede ser "mañana", "tarde" o "noche").

        Returns:
            Habit: El objeto del hábito recién creado.
        """
        # Verificando que el nuevo habito que se va a crear no exista
        Validations.check_habit_pair_existence(Habit.habit_name, habit_name, Habit.time_of_day, time_of_day)        
        # if db.session.query(db.exists().where(db.and_(Habit.habit_name == habit_name, Habit.time_of_day == time_of_day))).scalar():
        #     raise ValueError('A habit with the same name and time of day already exists. Please choose a different habit name or time slot.')   
        # Crear un nuevo objeto Habit con sus datos
        new_habit = Habit(habit_name, time_of_day)
        # Agregar el nuevo hábito a la base de datos y confirmar la transacción
        db.session.add(new_habit)
        db.session.commit()
        # Retorna el hábito creado
        return new_habit

    @staticmethod
    def update_habit(habit_id, new_data):
        """
        Actualizar un hábito existente.

        Args:
            habit_id (int): El ID del hábito a actualizar.
            new_data (dict): Un diccionario con los nuevos datos para actualizar el hábito.

        Returns:
            Habit: El hábito actualizado.

        Raises:
            ValueError: Si el hábito no se encuentra.
        """
        # Buscar el hábito por su id
        habit = HabitService.get_habit_by_id(habit_id)
        # Validamos si existe la combinacion de nombre de habito y jornada
        Validations.check_habit_pair_existence(Habit.habit_name, new_data['habit_name'], Habit.time_of_day, new_data['time_of_day'])
        # Actualizar el nombre y la jornada del hábito
        habit.habit_name = new_data['habit_name']
        habit.time_of_day = new_data['time_of_day']
        # Guardar los cambios en la base de datos
        db.session.commit()

    @staticmethod
    def delete_habit(habit_id):
        """
        Eliminar un hábito existente.

        Args:
            habit_id (int): El ID del hábito a eliminar.

        Raises:
            ValueError: Si el hábito no se encuentra.
        """
        habit = HabitService.get_habit_by_id(habit_id)

        Validations.check_if_exists(habit, 'Habit')

        # Eliminar el hábito de la base de datos y confirmar la transacción
        db.session.delete(habit)
        db.session.commit()

    @staticmethod
    def get_all_habits():
        """
        Obtener todos los hábitos.

        Returns:
            List[Habit]: Una lista de todos los hábitos almacenados en la base de datos.
        """
        return Habit.query.all()
    
    @staticmethod
    def get_habit_by_id(habit_id):
        """
        Obtener un hábito por su id.

        Args:
            user_id (int): ID del usuario a buscar.

        Returns:
            Habit: retorna el hábito.
            ValueError: User not found, si el hábito no existe.
        """
        # Filtrar hábitos por su id (habit_id)
        habit = Habit.query.filter_by(habit_id=habit_id).first()
        # Se llama al servicio de validacion para corroborar que el hábito exista
        habit_validated = Validations.check_if_exists(habit, 'Habit')
        return habit_validated
