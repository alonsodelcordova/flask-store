from apps.marshmallow import ma
from marshmallow import fields

class LoginInputSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class LoginOutputSchema(LoginInputSchema):
    id = fields.Integer()
    tipo = fields.Integer()
    is_active = fields.Boolean()
    token = fields.String()

login_input_schema = LoginInputSchema()
login_output_schema = LoginOutputSchema()
login_outputs_schemas = LoginOutputSchema(many=True)
