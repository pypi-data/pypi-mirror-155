from django.urls import path

from openapi_django.views import OpenApiFile, OpenApiPage

urlpatterns = [
    path('file', OpenApiFile.as_view()),
    path('', OpenApiPage.as_view()),
]
