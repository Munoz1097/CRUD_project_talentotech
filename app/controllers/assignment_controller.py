from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.assignment_service import AssignmentService

assignment_ns = Namespace('assignments', description='Operaciones relacionadas a la asignación de hábitos por cada usuario')

assignment_model = assignment_ns.model('Assignment', {
    'fk_user_id': fields.Integer(required=True, description='ID del usuario que asignó el hábito'),
    'fk_habit_id': fields.Integer(required=True, description='ID del hábito asignado')
})

@assignment_ns.route('/')
class AssignmentResource(Resource):

    @assignment_ns.doc('created_assignment')
    @assignment_ns.expect(assignment_model, validate=True) 
    @assignment_ns.marshal_with(assignment_model, code=201)
    def post(self):
        data = request.get_json()
        new_assignment = AssignmentService.create_assignment(data['fk_user_id'], data['fk_habit_id'])
        return new_assignment