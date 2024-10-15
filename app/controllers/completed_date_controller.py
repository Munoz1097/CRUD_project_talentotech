from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.completed_date_service import CompletedDateService


completed_date_ns = Namespace('completed_dates', description='Operaciones relacionadas con las fechas en que se completan los hábitos asignados')

completed_date_model = completed_date_ns.model('CompletedDates', {
    'completed_date': fields.DateTime(required=True, description='Fecha en que se completó un hábito asignado'),
    'fk_assignment_id': fields.Integer(required=True, description='ID de la asignacion del hábito a un usuario')
})

@completed_date_ns.route('/')
class CompletedDateResource(Resource):
    @completed_date_ns.doc('create_completed_date')
    @completed_date_ns.expect(completed_date_model, validate=True)
    @completed_date_ns.marshal_with(completed_date_model, code=201)
    def post(self):
        data= request.get_json()
        new_completed_date = CompletedDateService.create_completed_date(data['fk_assignment_id'])
        return new_completed_date