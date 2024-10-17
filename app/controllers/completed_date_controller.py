from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields, marshal
from app.services.completed_date_service import CompletedDateService


completed_date_ns = Namespace('completed_dates', description='Operaciones relacionadas con las fechas en que se completan los hábitos asignados')

entry_completed_date_model = completed_date_ns.model('CompletedDates', {
    'completed_date': fields.Date(description='Fecha en que se completa el hábito'),
    'fk_assignment_id': fields.Integer(required=True, description='ID de la asignacion del hábito a un usuario')
})

get_completed_date_response_model = completed_date_ns.model('CompletedDateResponse', {
    'completed_date_id': fields.Integer(description='ID de la fecha en que se completo un hábito'),
    'completed_date': fields.Date(description='Fecha en que se completó un hábito asignado'),
    'fk_assignment_id': fields.Integer(description='ID de la asignacion del hábito a un usuario')
})

@completed_date_ns.route('/')
class CompletedDateResource(Resource):
    @completed_date_ns.doc('get_all_dates')
    def get(self):
        dates = CompletedDateService.get_all_dates()
        return marshal(dates, get_completed_date_response_model), 200

    @completed_date_ns.doc('create_completed_date')
    @completed_date_ns.expect(entry_completed_date_model, validate=True)
    def post(self):
        data= request.get_json()
        try:
            new_completed_date = CompletedDateService.create_completed_date(data['fk_assignment_id'], data['completed_date'])
            return make_response(jsonify(
                {'message': 'Date created successfully', 'date': new_completed_date.completed_date}), 201)
        except ValueError as e:
            return make_response(jsonify({'message': str(e)}), 422)
        
@completed_date_ns.route('/<int:fk_assignment_id>')
@completed_date_ns.param('fk_assignment_id', 'ID de la asignación')
class CompletedDateAssignmentResource(Resource):
    @completed_date_ns.doc('get_all_dates_by_assignment_id')
    def get(self, fk_assignment_id):
        dates = CompletedDateService.get_all_dates_by_assignment_id(fk_assignment_id)
        return marshal(dates, get_completed_date_response_model), 200