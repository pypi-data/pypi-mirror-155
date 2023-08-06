import json
from django.http import HttpResponse
from django.template import Template, RequestContext
from django.views import View
from django.conf import settings
from openapi_django.openapi_utils.objects import OpenAPI


class OpenApiFile(View):
    def get(self, request):
        obj = OpenAPI.generate(root_urlconf=getattr(settings, "ROOT_URLCONF"), servers=['http://127.0.0.1:8000/'])
        response = HttpResponse(
            json.dumps(obj.json(), indent=2, ensure_ascii=False).encode('utf-8'), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="openapi.json"'
        return response


class OpenApiPage(View):
    def get(self, request):
        template = """
        <!DOCTYPE html>
        <html>
          <head>
            <title>Swagger</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" type="text/css" href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css" />
          </head>
          <body>
            <div id="swagger-ui"></div>
            <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
            <script>
            const ui = SwaggerUIBundle({
                url: "{file-url}file",
                dom_id: '#swagger-ui',
                presets: [
                  SwaggerUIBundle.presets.apis,
                  SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout",
                requestInterceptor: (request) => {
                  request.headers['X-CSRFToken'] = "{{ csrf_token }}"
                  return request;
                }
              })
            </script>
          </body>
        </html>
        """.replace("{file-url}", request.path)
        template = Template(template)
        context = RequestContext(request)
        return HttpResponse(template.render(context))
