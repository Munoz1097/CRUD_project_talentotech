from app import db, bcrypt
from app.models.user_model import User
from datetime import datetime


class UserService:
    @staticmethod
    def create_user(first_name, last_name, nickname, email, user_password):
        """
        Crear un nuevo usuario en el sistema.

        Args:
            first_name (str): El nombre del usuario.
            last_name (str): El apellido del usuario.
            nickname (str): Nombre de usuario del nuevo usuario.
            email (str): Correo electrónico del nuevo usuario.
            user_password (str): Contraseña en texto plano que será encriptada.

        Returns:
            User: El usuario creado.
        """
        # Generar un hash seguro de la contraseña con bcrypt
        hashed_password = bcrypt.generate_password_hash(user_password).decode('utf-8')

        # Guarda la fecha actual en la variable created_date para asignarla a la fecha de creación del usuario
        created_date = datetime.now()

        # Crear un nuevo objeto User con la contraseña hasheada y todos los demás datos necesarios
        user = User(first_name, last_name, nickname, email, user_password=hashed_password, user_status=True, user_created_date=created_date)

        # Añadir el nuevo usuario a la base de datos
        db.session.add(user)
        db.session.commit()

        return user  # Retornar el usuario recién creado

    @staticmethod
    def get_all_users():
        """
        Obtener todos los usuarios de la base de datos.

        Returns:
            List[User]: Lista de todos los usuarios en la base de datos.
        """
        # Recuperar todos los registros de la tabla User
        return User.query.all()

    @staticmethod
    def get_user_by_user_id(user_id):
        """
        Obtener un usuario por su id de usuario.

        Args:
            user_id (int): ID del usuario a buscar.

        Returns:
            User: El usuario encontrado o None si no existe.
        """
        # Filtrar usuarios por su id de usuario (user_id)
        return User.query.filter_by(user_id=user_id).first()

    @staticmethod
    def update_user(user_id, new_data):
        """
        Actualizar los datos de un usuario existente.

        Args:
            user_id (int): ID del usuario a actualizar.
            new_data (dict): Diccionario con los nuevos datos, como 'first_name', 'last_name', 'nickname', 'email', o 'user_password'.

        Returns:
            None

        Raises:
            ValueError: Si el usuario no es encontrado.
        """
        # Buscar al usuario por su id
        user = UserService.get_user_by_user_id(user_id)
        if not user:
            # Si no se encuentra el usuario, lanzar una excepción
            raise ValueError('User not found')

        # Si se proporciona un nuevo first_name, asigna el nuevo first_name
        if 'first_name' in new_data:
            user.first_name = new_data['first_name']

        # Si se proporciona un nuevo last_name, asigna el nuevo last_name
        if 'last_name' in new_data:
            user.last_name = new_data['last_name']

        # Si se proporciona un nuevo nickname, asigna el nuevo nickname
        if 'nickname' in new_data:
            user.nickname = new_data['nickname']

        # Si se proporciona un nuevo email, asigna el nuevo email
        if 'email' in new_data:
            user.email = new_data['email']

        # Si se proporciona una nueva contraseña, generar el hash y asigna la nueva contraseña
        if 'user_password' in new_data:
            user.user_password = bcrypt.generate_password_hash(new_data['user_password']).decode('utf-8')

        # Guardar los cambios en la base de datos
        db.session.commit()

    @staticmethod
    def delete_user(user_id):
        """
        Eliminar un usuario existente.

        Args:
            user_id (int): ID del usuario a eliminar.

        Returns:
            None

        Raises:
            ValueError: Si el usuario no es encontrado.
        """
        # Buscar al usuario por su ID
        user = UserService.get_user_by_user_id(user_id)
        if not user:
            # Si no se encuentra el usuario, lanzar una excepción
            raise ValueError('User not found')

        # Eliminar el usuario de la base de datos
        db.session.delete(user)
        db.session.commit()
