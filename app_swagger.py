from flask import Flask
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

app = Flask(__name__)  # Flask app instance initiated
api = Api(app)  # Flask restful wraps Flask app around it.
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


class AwesomeResponseSchema(Schema):
    message_error = fields.Str(default='2000')
    message_description = fields.Str(default='Sucesso Returned')

class AwesomeRequestSchema(Schema):
    api_type = fields.String(required=True, description="API type of awesome API")


#  Restful way of creating APIs through Flask Restful
class AwesomeAPI(MethodResource, Resource):
    @doc(description='My First GET Awesome API.', tags=['Awesome'])
    @marshal_with(AwesomeResponseSchema)  # marshalling
#    @doc.response(200, 'Get AwaesomeAPI.')
    def get(self):
        '''
        Get method represents a GET API method
        '''
        return {'message': 'My First Awesome API'}

    @doc(description='My First GET Awesome API.', tags=['Awesome'])
    @use_kwargs(AwesomeRequestSchema, location=('json'))
    @marshal_with(AwesomeResponseSchema)  # marshalling
#    @api.response(201, 'Awaesome something created.')
    @marshal_with(AwesomeResponseSchema, code=201, description='Something created')
    @marshal_with(AwesomeResponseSchema, code=409, description='Something already created')
    def post(self):
        '''
        Get method represents a GET API method
        '''
        return {'message': 'My First Awesome API'}


api.add_resource(AwesomeAPI, '/awesome')
docs.register(AwesomeAPI)

if __name__ == '__main__':
    app.run(debug=True)
