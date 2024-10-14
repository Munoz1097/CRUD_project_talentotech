from app import db
from app.models.habit_model import Habit

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
        new_habit = Habit(habit_name, time_of_day)

        # Agregar el nuevo hábito a la base de datos y confirmar la transacción
        db.session.add(new_habit)
        db.session.commit()

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
        habit = Habit.query.get(habit_id)

        if not habit:
            raise ValueError('Habit not found')

        # Actualizar el nombre del hábito si se proporciona
        if 'habit_name' in new_data:
            habit.habit_name = new_data['habit_name']

        # Actualizar el momento del día si se proporciona
        if 'time_of_day' in new_data:
            habit.time_of_day = new_data['time_of_day']

        # Guardar los cambios en la base de datos
        db.session.commit()

        return habit

    @staticmethod
    def delete_habit(habit_id):
        """
        Eliminar un hábito existente.

        Args:
            habit_id (int): El ID del hábito a eliminar.

        Raises:
            ValueError: Si el hábito no se encuentra.
        """
        habit = HabitService.get_habit_by_habit_id(habit_id)

        if not habit:
            raise ValueError('Habit not found')

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
    def get_habit_by_habit_id(habit_id):
        return Habit.query.filter_by(habit_id=habit_id).first()
