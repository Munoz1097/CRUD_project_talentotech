from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.habit_service import HabitService

# Crear un espacio de nombres (namespace) para los hábitos
habit_ns = Namespace('habits', description='Operaciones relacionadas con los hábitos')

# Definir los valores válidos para 'time_of_day'
TIME_OF_DAY_VALUES = ['mañana', 'tarde', 'noche']

# Modelo de entrada para la creación de un nuevo hábito
habit_model = habit_ns.model('Habit', {
    'habit_name': fields.String(required=True, description='Nombre del hábito'),
    'time_of_day': fields.String(required=True, description='Momento del día (mañana, tarde, noche)', enum=TIME_OF_DAY_VALUES),
})

# Modelo de salida para la respuesta de las operaciones relacionadas con los hábitos
habit_response_model = habit_ns.model('HabitResponse', {
    'habit_id': fields.Integer(description='ID del hábito'),
    'habit_name': fields.String(description='Nombre del hábito'),
    'time_of_day': fields.String(description='Momento del día (mañana, tarde, noche)'),
    'habit_status': fields.Boolean(description='Estado del hábito (activo o inactivo)'),
})

# Definir el controlador de hábitos con decoradores para la documentación
@habit_ns.route('/')
class HabitResource(Resource):

    @habit_ns.doc('get_all_habits')
    def get(self):
        """
        Obtener todos los hábitos
        ---
        Este método permite obtener una lista de todos los hábitos registrados.

        Responses:
        - 200: Retorna una lista de todos los hábitos.
        """
        habits = HabitService.get_all_habits()  # Llama al servicio para obtener todos los hábitos
        return habits  # Retorna todos los hábitos en el formato estipulado

    @habit_ns.doc('create_habit')
    @habit_ns.expect(habit_model, validate=True)  # Decorador para esperar el modelo en la petición
    def post(self):
        """
        Crear un nuevo hábito
        ---
        Este método permite crear un nuevo hábito proporcionando los siguientes datos:
        - Nombre del hábito.
        - Momento del día.

        Body Parameters:
        - habit_name: Nombre del hábito a crear.
        - time_of_day: Momento del día (mañana, tarde, noche).

        Responses:
        - 201: Hábito creado con éxito.
        - 400: Si ocurre un error debido a un valor inválido.
        """
        data = request.get_json()  # Obtiene los datos en formato JSON del cuerpo de la solicitud

        # Validar el campo 'time_of_day'
        time_of_day = data.get('time_of_day')
        if time_of_day not in TIME_OF_DAY_VALUES:
            return jsonify({'message': f"Invalid value for 'time_of_day'. Allowed values are: {', '.join(TIME_OF_DAY_VALUES)}"}), 400
        
        new_habit = HabitService.create_habit(data['habit_name'], time_of_day)  # Crear el nuevo hábito
        return new_habit, 201  # Retornar el nuevo hábito creado

@habit_ns.route('/<int:habit_id>')
@habit_ns.param('habit_id', 'ID del hábito')
class HabitDetailResource(Resource):

    @habit_ns.doc('get_habit_by_id')
    @habit_ns.marshal_with(habit_response_model, code=200)  # Decorador para estipular el formato de la respuesta
    def get(self, habit_id):
        """
        Obtener un hábito por su ID
        ---
        Este método permite obtener todos los datos de un hábito basado en su ID.

        Responses:
        - 200: Retorna un JSON con todos los datos del hábito.
        - 404: Si el hábito no es encontrado.
        """
        habit = HabitService.get_habit_by_habit_id(habit_id)  # Llama al servicio para obtener el hábito asociado al ID
        if not habit:
            habit_ns.abort(404, 'Habit not found')  # Retornar error 404 si no se encuentra el hábito
        return habit  # Retorna todos los datos del hábito en el formato estipulado

    @habit_ns.doc('update_habit')
    @habit_ns.expect(habit_model, validate=False)  # Decorador para esperar el modelo en la petición
    def put(self, habit_id):
        """
        Actualizar un hábito existente
        ---
        Este método permite actualizar la información de un hábito basado en el ID del hábito.

        Path Parameters:
        - habit_id: El ID del hábito que se actualizará.

        Body Parameters:
        - habit_name: Nuevo nombre del hábito (opcional).
        - time_of_day: Nuevo momento del día (opcional).

        Responses:
        - 200: Hábito actualizado con éxito.
        - 404: Si el hábito no se encuentra.
        """
        new_data = request.get_json()  # Obtiene los nuevos datos para la actualización

        # Validar si se proporciona un nuevo valor para 'time_of_day' y si es válido
        if 'time_of_day' in new_data:
            time_of_day = new_data['time_of_day']
            if time_of_day not in TIME_OF_DAY_VALUES:
                return jsonify({'message': f"Invalid value for 'time_of_day'. Allowed values are: {', '.join(TIME_OF_DAY_VALUES)}"}), 400
        
        habit = HabitService.update_habit(habit_id, new_data)  # Actualizar el hábito con los nuevos datos
        return habit, 200  # Retornar el hábito actualizado

    @habit_ns.doc('delete_habit')
    def delete(self, habit_id):
        """
        Eliminar un hábito
        ---
        Este método permite eliminar un hábito existente basado en el ID del hábito.

        Path Parameters:
        - habit_id: El ID del hábito a eliminar.

        Responses:
        - 200: Hábito eliminado con éxito.
        - 404: Si el hábito no se encuentra.
        """
        HabitService.delete_habit(habit_id)  # Llama al servicio para eliminar el hábito
        return jsonify({'message': 'Habit deleted successfully'}), 200  # Retornar mensaje de éxito
