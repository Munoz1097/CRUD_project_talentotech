from app import db

class User(db.Model):
    """
    Modelo que representa un usuario en el sistema.

    Cada usuario tiene un nombre de usuario, nombre, apellido, correo electrónico, contraseña encriptada y un estado que indica si el usuario está activo. También se registra la fecha de creación del usuario.

    Atributos:
        user_id (int): Identificador único del usuario (clave primaria).
        first_name (str): Nombre del usuario.
        last_name (str): Apellido del usuario.
        username (str): Nombre de usuario, debe ser único.
        email (str): Correo electrónico del usuario, debe ser único.
        user_password (str): Contraseña encriptada del usuario.
        user_status (bool): Estado del usuario, indica si está activo o inactivo (True = activo, False = inactivo).
        user_created_date (datetime): Fecha de creación del usuario.
    """

    __tablename__ = 'users'  # Especifica el nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    user_id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    first_name = db.Column(db.String(100), nullable=False)  # Nombre del usuario, no puede ser nulo
    last_name = db.Column(db.String(100), nullable=False)  # Apellido del usuario, no puede ser nulo
    username = db.Column(db.String(100), unique=True, nullable=False)  # Nombre de usuario, debe ser único y no nulo
    email = db.Column(db.String(100), unique=True, nullable=False)  # Correo electrónico del usuario, debe ser único y no nulo
    user_password = db.Column(db.String(200), nullable=False)  # Contraseña encriptada del usuario, no puede ser nula
    user_status = db.Column(db.Boolean, default=True, nullable=False)  # Estado del usuario, por defecto es activo
    user_created_date = db.Column(db.DateTime, nullable=False)  # Fecha de creación del usuario, no puede ser nula

    def __init__(self, first_name, last_name, username, email, user_password, user_status, user_created_date):
        """
        Constructor de la clase User.

        Args:
            first_name (str): El nombre del usuario.
            last_name (str): El apellido del usuario.
            username (str): El nombre de usuario, debe ser único.
            email (str): El correo electrónico del usuario, debe ser único.
            user_password (str): La contraseña encriptada del usuario.
            user_status (bool): El estado del usuario (activo/inactivo).
            user_created_date (datetime): La fecha de creación del usuario.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.user_password = user_password
        self.user_status = user_status
        self.user_created_date = user_created_date
