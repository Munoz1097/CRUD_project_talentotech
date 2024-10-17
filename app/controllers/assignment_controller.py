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
    'create_date': fields.DateTime(description='Fecha de la asignación'),
    'assignment_status': fields.Boolean(description='Estado de la asignación (activado/desactivado)'),
    'fk_user_id': fields.Integer(description='ID del usuario que asignó el hábito'),
    'fk_habit_id': fields.Integer(description='ID del hábito asignado')
})

@assignment_ns.route('/')
class AssignmentResource(Resource):

    @assignment_ns.doc('created_assignment')
    @assignment_ns.expect(entry_assignment_model, validate=True) 
    @assignment_ns.marshal_with(entry_assignment_model, code=201)
    def post(self):
        data = request.get_json()
        new_assignment = AssignmentService.create_assignment(data['fk_user_id'], data['fk_habit_id'])
        return new_assignment
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

        
@assignment_ns.route('/<int:fk_user_id>')
@assignment_ns.param('fk_user_id', 'ID del usuario')


class AssignmentDetailResource(Resource):
    @assignment_ns.doc('get_assignments_by_user_id')
    def get(self,fk_user_id):
        assignments = AssignmentService.get_assignments_by_user_id(fk_user_id)  # Llama al servicio para obtener el hábito asociado al ID
        if not assignments:
            assignments.abort(404, 'Habit not found')  # Retornar error 404 si no se encuentra el hábito
        return assignments # Retorna todos los datos del hábito en el formato estipulado