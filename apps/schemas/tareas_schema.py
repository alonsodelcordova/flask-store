from apps.marshmallow import ma
from marshmallow import fields

class TareaInputSchema(ma.Schema):
    tarea = fields.String(required=True)
    descripcion = fields.String(required=True)
    tipo = fields.Integer(required=True)

class TareaOutputSchema(TareaInputSchema):
    id = fields.Integer()
    is_active = fields.Boolean()
    usuario_id = fields.Integer()


tarea_input_schema = TareaInputSchema()
tarea_output_schema = TareaOutputSchema()
tarea_outputs_schemas = TareaOutputSchema(many=True)