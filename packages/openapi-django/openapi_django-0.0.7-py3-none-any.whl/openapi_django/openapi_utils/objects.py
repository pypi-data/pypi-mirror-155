from enum import Enum
from typing import List

from openapi_django.openapi_utils.collectors import collect_routes


class ParameterType(Enum):
    PARAMETER = 'parameter'
    PATH_PARAMETER = 'path_parameter'
    BODY_PARAMETER = 'body_parameter'


class Parameter:
    def __init__(self, schema, name, parameter_type):
        self.schema = schema
        self.name = name
        self.parameter_type = parameter_type

    @property
    def _require(self):
        if 'required' in self.schema:
            return True if self.parameter_type == ParameterType.PATH_PARAMETER else self.name in self.schema['required']
        return False

    def json(self):
        return getattr(self, f'_{self.parameter_type.value}_json')

    @property
    def _parameter_json(self):
        base = {
            self.name: {
                "in": "query",
                "required": self._require,
                "name": self.name,
                "description": self.schema['properties'][self.name]['description'],
                "schema": {
                    "type": self.schema['properties'][self.name]['type']
                }
            }
        }
        return base

    @property
    def _path_parameter_json(self):
        return {
            f"path_{self.name}": {
                "in": "path",
                "required": True,
                "name": self.name,
                "description": self.schema['properties'][self.name]['description'],
                "schema": {
                    "type": self.schema['properties'][self.name]['type']
                }
            }
        }


class Components(object):
    def __init__(self):
        self.parameters = {}
        self.schemas = {}

    def json(self):
        return {
            "schemas": self.schemas,
            "parameters": self.parameters
        }

    def add_parameters(self, parameters, parameter_type):
        if parameters:
            schema = parameters.schema("#/components/schemas/{model}")
            for item in schema['properties']:
                obj = Parameter(schema=schema, name=item, parameter_type=parameter_type)
                self.parameters.update(obj.json())

    def add_schema(self, schema):
        if schema:
            _schema = schema.schema(ref_template='#/components/schemas/{model}').copy()
            if definitions := _schema.get('definitions'):
                for definition in definitions:
                    self.schemas.update({definition: definitions[definition]})
                _schema.pop('definitions')

            self.schemas.update({
                schema.__name__: _schema
            })


class Method(object):
    def __init__(
            self, method="get", parameters=None, return_class=None, description=None, path_parameters=None, body=None
    ):

        self.method = method
        self.return_class = return_class
        self.description = description
        self.parameters = parameters
        self.path_parameters = path_parameters
        self.body = body

    @classmethod
    def from_data(cls, method_name, data):
        data.update({"method": method_name})
        return cls(**data)

    def json(self):
        base = {
            "parameters": self.collect_parameters(),
            "responses": {
                "200": {
                    "description": "OK"
                }
            }
        }

        if self.description:
            base.update({
                "description": self.description,
                "summary": self.description
            })

        if self.body:
            base['requestBody'] = {"content": {"application/json": {"schema": {"type": "object","allOf": [
                {"$ref": f"#/components/schemas/{self.body.__name__}"}
            ]}}}}

        if self.return_class:
            base["responses"]["200"]["content"] = {
                "application/json": {
                    "schema": {
                        "$ref": f"#/components/schemas/{self.return_class.__name__}"
                    }
                }
            }
        return base

    def collect_parameters(self):
        result = []
        components_schema = "#/components/parameters/"
        if self.path_parameters:
            result.extend(
                [{"$ref": f"{components_schema}path_{item}"} for item in self.path_parameters.schema()['properties']])
        if self.parameters:
            result.extend(
                [{"$ref": f"{components_schema}{item}"} for item in self.parameters.schema()['properties']])
        return result

    def collect_body(self):
        result = []
        components_schema = "#/components/schemas/"
        if self.body:
            result.extend(
                [{"$ref": f"{components_schema}{item}"} for item in self.body.schema()['properties']])
        return result


class Route(object):
    def __init__(self, route: str):
        self.route = f'/{route}'
        self.methods: List[Method] = []

    def json(self):
        return dict([(item.method, item.json()) for item in self.methods])


class OpenAPI(object):
    def __init__(
            self, servers: List[str] = None, openapi_version="3.0.2", title="Openapi Documentation", version="1.0.0"):
        self.servers = servers if servers else ["http://test.test"]
        self.openapi_version = openapi_version
        self.title = title
        self.version = version

        self.routes: List[Route] = []
        self.tags = []

    def json(self):
        result = {
            "openapi": self.openapi_version,
            "info": {
                "title": self.title,
                "version": self.version
            },
            "servers": [{"url": item} for item in self.servers],
            "paths": dict([(path.route, path.json()) for path in self.routes]),
            "components": self.collect_components()
        }
        return result

    def collect_components(self):
        result = Components()
        for route in self.routes:
            for method in route.methods:
                result.add_schema(schema=method.return_class)
                result.add_parameters(parameters=method.path_parameters, parameter_type=ParameterType.PATH_PARAMETER)
                result.add_parameters(parameters=method.parameters, parameter_type=ParameterType.PARAMETER)
                result.add_schema(schema=method.body)
        return result.json()

    @classmethod
    def generate(cls, root_urlconf, servers=None):
        root_urlconf = __import__(root_urlconf)
        openapi = cls(servers=servers)
        openapi.routes = collect_routes(all_resolver=root_urlconf.urls.urlpatterns)
        return openapi
