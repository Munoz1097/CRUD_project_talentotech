from flask import request, jsonify,make_response
from flask_restx import Namespace, Resource, fields, marshal
from app.services.assignment_service import AssignmentService

assignment_ns = Namespace('assignments', description='Operaciones relacionadas a la asignación de hábitos por cada usuario')

entry_assignment_model = assignment_ns.model('Assignment', {
    'fk_user_id': fields.Integer(required=True, description='ID del usuario que asignó el hábito'),
    'fk_habit_id': fields.Integer(required=True, description='ID del hábito asignado')
})
get_assignment_response_model = assignment_ns.model('AssignmentResponse', {    
    'assignment_id': fields.Integer(description='ID de la asignación'),
    'created_date': fields.DateTime(description='Fecha de la asignación'),
    'assignment_status': fields.Boolean(description='Estado de la asignación (activado/desactivado)'),
    'fk_user_id': fields.Integer(description='ID del usuario que asignó el hábito'),
    'fk_habit_id': fields.Integer(description='ID del hábito asignado')
})

@assignment_ns.route('/')
class AssignmentResource(Resource):
    @assignment_ns.doc('created_assignment')
    @assignment_ns.expect(entry_assignment_model, validate=True) 
    def post(self):
        data = request.get_json()
        try:
            new_assignment = AssignmentService.create_assignment(data['fk_user_id'], data['fk_habit_id'])
            return make_response(jsonify({'message': f'Habit ID:{new_assignment.fk_habit_id} assigned to user ID:{new_assignment.fk_user_id} successfully'}), 201)
        except ValueError as e:
            # Si la asignacion ya existe se responde un mensaje de error con el codigo 422
            return make_response(jsonify({'message': str(e)}), 422)  
        
    @assignment_ns.doc('get_all_assignments')
    def get(self):
        """
        Obtener todos los usuarios
        ---
        Este método permite obtener una lista de todos los usuarios registrados en la base de datos.
        Responses:
        - 200: Retorna una lista de apodos de usuarios.
        """
        # Llama al servicio para obtener todos los usuarios
        assignments = AssignmentService.get_all_assignments()  
        # Usamos jsonify para garantizar que la lista de usuarios se retorne como un JSON válido.
        return marshal(assignments,get_assignment_response_model), 200
    

@assignment_ns.route('/<int:assignment_id>')
@assignment_ns.param('assignment_id', 'ID de la asignación')
class AssignmentDetailResource(Resource):
    @assignment_ns.doc('get_assignment_by_assignment_id')
    def delete(self, assignment_id):
        try:
            # Llama al servicio para eliminar la asignación
            AssignmentService.delete_assignment(assignment_id)  
            # Usamos jsonify para enviar un mensaje de éxito en formato JSON.
            return make_response(jsonify({'message': 'Assignment deleted successfully'}), 200)
        except ValueError as e:
            # Si el usuario no es encontrado, devolvemos un mensaje de error con el código 404
            return make_response(jsonify({'message': str(e)}), 404)

        
@assignment_ns.route('/<int:fk_user_id>')
@assignment_ns.param('fk_user_id', 'ID del usuario')
class AssignmentUserResource(Resource):
    @assignment_ns.doc('get_assignments_by_user_id')
    def get(self,fk_user_id):

        try:
            # Llama al servicio para obtener el la asignación asociada al ID del usuario
            assignment = AssignmentService.get_assignments_by_user_id(fk_user_id)  
            # Si la asignación se encuentra, aplicamos manualmente marshal para formatear la respuesta
            return marshal(assignment, get_assignment_response_model), 200
        except ValueError as e:
            # Si la asignación no es encontrada, devolvemos un mensaje de error con el código 404
            return make_response(jsonify({'message': str(e)}), 404)
        


