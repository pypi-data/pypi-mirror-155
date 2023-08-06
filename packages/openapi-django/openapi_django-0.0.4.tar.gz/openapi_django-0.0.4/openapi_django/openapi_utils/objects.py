from typing import List

from openapi_django.openapi_utils.collectors import collect_routes


class Components(object):
    def __init__(self):
        self.parameters = {}
        self.schemas = {}

    def json(self):
        return {
            "schemas": self.schemas,
            "parameters": self.parameters
        }

    def add_path_parameter(self, parameter):
        if parameter:
            schema = parameter.schema("#/components/schemas/{model}")['properties']
            for item in schema:
                self.parameters.update({
                    f"path_{item}": {
                        "in": "path",
                        "required": True,
                        "name": item,
                        "description": schema[item]['description'],
                        "schema": {
                            "type": schema[item]['type']
                        }
                    }
                })

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
    def __init__(self, method="get", parameters=None, return_class=None, description=None, path_parameters=None):
        self.method = method
        self.return_class = return_class
        self.description = description
        self.parameters = parameters
        self.path_parameters = path_parameters

    @classmethod
    def from_data(cls, method_name, data):
        data.update({"method": method_name})
        return cls(**data)

    def json(self):
        base = {
            "description": self.description,
            "summary": self.description,
            "parameters": self.collect_parameters(),
            "responses": {
                "200": {
                    "description": "OK"
                }
            }
        }

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
        return {
            "openapi": self.openapi_version,
            "info": {
                "title": self.title,
                "version": self.version
            },
            "servers": [{"url": item} for item in self.servers],
            "paths": dict([(path.route, path.json()) for path in self.routes]),
            "components": self.collect_components()
        }

    def collect_components(self):
        result = Components()
        for route in self.routes:
            for method in route.methods:
                result.add_schema(schema=method.return_class)
                result.add_path_parameter(parameter=method.path_parameters)
        return result.json()

    @classmethod
    def generate(cls, root_urlconf, servers=None):
        root_urlconf = __import__(root_urlconf)
        openapi = cls(servers=servers)
        openapi.routes = collect_routes(all_resolver=root_urlconf.urls.urlpatterns)
        return openapi
