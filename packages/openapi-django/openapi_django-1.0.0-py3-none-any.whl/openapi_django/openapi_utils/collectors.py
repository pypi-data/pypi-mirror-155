import os
import re

from django.urls import URLPattern, URLResolver


def normalize_str_route(_url_pattern: URLPattern):
    return re.sub(r'<([a-zA-Z]+):([a-zA-Z0-9-_]+)>', r"{\g<2>}", _url_pattern.pattern._route)


def detect_urlpatterns(resolver):
    return \
        resolver.urlconf_name.urlpatterns if isinstance(resolver, URLResolver) else \
        [resolver]


def generate_route(resolver, pattern, url_pattern):
    if isinstance(resolver, URLResolver):
        return os.path.join(pattern._route, normalize_str_route(url_pattern))
    return pattern._route


def collect_routes(all_resolver):
    from openapi_django.openapi_utils.objects import Method, Route
    paths = []
    for resolver in all_resolver:
        if hasattr(resolver, 'app_name'):
            if resolver.app_name == 'admin':
                continue
        pattern = resolver.pattern
        urlpatterns = detect_urlpatterns(resolver)
        for url_pattern in urlpatterns:
            route = Route(route=generate_route(resolver=resolver, pattern=pattern, url_pattern=url_pattern))
            module_name, *submodule, view_name = url_pattern.lookup_str.split(".")
            _view_module = __import__(module_name)
            obj = _view_module
            for item in submodule:
                obj = getattr(obj, item)

            view = getattr(obj, view_name)
            for method_name in view.http_method_names:
                if hasattr(view, method_name):
                    try:
                        data = getattr(view, method_name)("openapi")
                    except Exception as e:
                        print(e)
                        continue
                    route.methods.append(Method.from_data(method_name=method_name, data=data))
            paths.append(route)
    return paths
