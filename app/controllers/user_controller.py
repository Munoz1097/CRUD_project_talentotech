from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.user_service import UserService

# Crear un espacio de nombres (namespace) para los usuarios
user_ns = Namespace('users', description='Operaciones relacionadas con los usuarios')

# Modelo de entrada de usuario para la documentación de Swagger
user_model = user_ns.model('User', {
    'first_name': fields.String(required=True, description='Nombre de usuario'),
    'last_name': fields.String(required=True, description='Apellido de usuario'),
    'username': fields.String(required=True, description='Apodo de usuario'),
    'email': fields.String(required=True, description='Email de usuario'),
    'user_password': fields.String(required=True, description='Contraseña'),
})

# Modelo de salida de usuario
user_response_model = user_ns.model('UserResponse', {
    'user_id': fields.Integer(description='ID de usuario'),
    'first_name': fields.String(description='Nombre de usuario'),
    'last_name': fields.String(description='Apellido de usuario'),
    'username': fields.String(description='Apodo de usuario'),
    'email': fields.String(description='Email de usuario'),
    'user_status': fields.Boolean(description='Estado del usuario (activo o inactivo)'),
    'user_created_date': fields.DateTime(description='Fecha y hora de creación del usuario')
})

# Definir el controlador de usuarios con decoradores para la documentación
@user_ns.route('/')
class UserResource(Resource):
    @user_ns.doc('get_all_users')
    def get(self):
        """
        Obtener todos los usuarios
        ---
        Este método permite obtener una lista de todos los usuarios registrados en la base de datos.

        Responses:
        - 200: Retorna una lista de nombres de usuarios.
        """
        users = UserService.get_all_users()  # Llama al servicio para obtener todos los usuarios
        # Usamos jsonify para garantizar que la lista de usuarios se retorne como un JSON válido.
        return jsonify({'users': [user.username for user in users]})  # Retorna solo los nombres de usuario
    
    @user_ns.doc('create_user')
    @user_ns.expect(user_model, validate=True)  # Decorador para esperar el modelo en la petición
    def post(self):
        """
        Crear un nuevo usuario
        ---
        Este método permite crear un nuevo usuario proporcionando los siguientes datos:
        - Nombre.
        - Apellido.
        - Apodo.
        - Email.
        - Contraseña.

        Body Parameters:
        - first_name: Nombre del usuario a crear. 
        - last_name: Apellido del usuario.
        - username: Apodo del usuario.
        - email: Correo electronico del usuario.
        - user_password: Contraseña del usuario.

        Responses:
        - 201: Usuario creado con éxito.
        - 400: Si ocurre un error durante la creación del usuario.
        """
        data = request.get_json()  # Obtiene los datos en formato JSON del cuerpo de la solicitud
        user = UserService.create_user(data['first_name'], data['last_name'], data['username'], data['email'], data['user_password'])
        # Usamos jsonify para asegurarnos de que la respuesta siga el formato JSON válido.
        return jsonify({'message': 'User created successfully', 'user': user.username})
    

@user_ns.route('/<int:user_id>')
@user_ns.param('user_id', 'ID del usuario')
class UserDetailResource(Resource):
    @user_ns.doc('get_user_by_user_id')
    @user_ns.marshal_with(user_response_model, code=200)  # Decorador para estipular el formato de la respuesta
    def get(self, user_id):
        """
        Obtener datos de usuario
        ---
        Este método permite obtener todos los datos de un usuario basado en su ID.

        Responses:
        - 200: Retorna un JSON con todos los datos del usuario.
        - 404: Si el usuario no es encontrado.
        """
        user = UserService.get_user_by_user_id(user_id)  # Llama al servicio para obtener el usuario asociado al ID
        return user  # Retorna todos los datos del usuario en el formato estipulado (user_response_model)

    @user_ns.doc('delete_user')
    def delete(self, user_id):
        """
        Eliminar un usuario
        ---
        Este método permite eliminar un usuario existente basado en el ID del usuario.

        Path Parameters:
        - user_id: El ID del usuario a eliminar.

        Responses:
        - 200: Usuario eliminado con éxito.
        - 404: Si el usuario no se encuentra.
        """
        UserService.delete_user(user_id)  # Llama al servicio para eliminar al usuario
        # Usamos jsonify para enviar un mensaje de éxito en formato JSON.
        return jsonify({'message': 'User deleted successfully'})

    @user_ns.doc('update_user')
    @user_ns.expect(user_model, validate=False)
    def put(self, user_id):
        """
        Actualizar un usuario
        ---
        Este método permite actualizar la información de un usuario basado en el ID del usuario.

        Path Parameters:
        - user_id: El ID del usuario que se actualizará.

        Body Parameters:
        - first_name: Nuevo nombre del usuario (opcional).
        - last_name: Nuevo apellido del usuario (opcional).
        - username: El nuevo nombre de usuario (opcional).
        - email: El nuevo Email del usuario (opcional).
        - user_password: La nueva contraseña (opcional).

        Responses:
        - 200: Usuario actualizado con éxito.
        - 404: Si el usuario no se encuentra.
        """
        new_data = request.get_json()  # Obtiene los nuevos datos para la actualización
        UserService.update_user(user_id, new_data)  # Llama al servicio para actualizar el usuario
        # Usamos jsonify para enviar un mensaje de éxito en formato JSON.
        return jsonify({'message': 'User updated successfully'})
