from app import db
from sqlalchemy.sql import func

class User(db.Model):
    """
    Modelo que representa un usuario en el sistema.

    Cada usuario tiene un nombre de usuario, una contraseña encriptada y está asociado con un rol a través de una clave foránea.

    Atributos:
        id (int): Identificador único del usuario (clave primaria).
        username (str): Nombre de usuario, debe ser único.
        password (str): Contraseña encriptada del usuario.
        role_id (int): Clave foránea que referencia al rol asignado al usuario.
        role (Role): Relación con el modelo Role que indica el rol del usuario.
    """
    
    __tablename__ = 'users'  # Especifica el nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    user_id = db.Column(db.Integer, primary_key=True)  # Clave primaria de la tabla
    first_name = db.Column(db.String(100),nullable=False)  # Nombre de usuario, debe ser único y no nulo
    last_name =  db.Column(db.String(100),nullable=False)   # Contraseña encriptada del usuario, no puede ser nula
    username = db.Column(db.String(100),nullable=False, unique= True)  # Clave foránea hacia la tabla 'roles'
    email =  db.Column(db.String(100),nullable=False)
    user_password = db.Column(db.String(200),nullable=False)
    user_status = db.Column(db.Boolean ,nullable=False)
    user_created_date = db.Column(db.DateTime(timezone=True), default = func.now(), nullable= False)

    def __init__(self, first_name, last_name , username , email, user_password, user_status):
        """
        Constructor de la clase User.

        Args:
            username (str): El nombre de usuario.
            password (str): La contraseña encriptada.
            role_id (int): El ID del rol asociado.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.user_password = user_password
        self.user_status = user_status


