from app import db

class Validations():
    @staticmethod
    def check_if_exists(obj, type_obj):
        """
        Validacion de existencia de un objeto

        Args:
            obj: Objeto con todos sus atributos.
            str: clase del objeto
        
        Returns:
            User: retorna el objeto.
            ValueError: {type_obj} not found, si el usuario no existe.
        """
        if not obj:
            raise ValueError(f'{type_obj} not found')
        return obj
    
    @staticmethod
    def check_field_existence(attribute, value, name):
        """
        Validación de existencia de un campo.

        Args:
            attribute: El atributo a validar.
            value: El valor esperado del atributo.
            name: nombre de lo que se va a comparar

        Returns:
            boolean: si existe el campo retorna True
        """
        if db.session.query(db.exists().where(attribute == value)).scalar():
            raise ValueError(f'{name} already exists. Please choose a different one.') 
        
    @staticmethod
    def check_habit_pair_existence(attribute1, value1, attribute2, value2):
        """
        Validación de existencia de combinacion de combinacion entre nombre y jornanda de un hábito.

        Args:
            attribute1: El primer atributo a validar.
            value1: El primer valor esperado del atributo.
            attribute1: El segundo atributo a validar.
            value1: El segundo valor esperado del atributo.

        Returns:
            boolean: si existe la combinacion de campos retorna True
        """
        if db.session.query(db.exists().where(db.and_( attribute1 == value1, attribute2 == value2))).scalar():
            raise ValueError('A habit with the same name and time of day already exists. Please choose a different habit name or time slot.')