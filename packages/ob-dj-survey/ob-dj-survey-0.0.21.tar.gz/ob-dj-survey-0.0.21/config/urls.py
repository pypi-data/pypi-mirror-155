import os

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(SchemaGenerator, self).get_schema(request, public)
        schema.basePath = os.path.join(schema.basePath, "docs/")
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        basePath="/",
        license=openapi.License(name="Privately owned"),
    ),
    public=True,
    urlconf="config.urls",
    permission_classes=(permissions.AllowAny,),
    generator_class=SchemaGenerator,
)

urlpatterns = [
    re_path(
        r"^$",
        lambda request: HttpResponse("Alive !"),
        name="ping",
    ),
    re_path(
        r"^docs/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("admin/", admin.site.urls),
    path(
        "",
        include("ob_dj_survey.apis.survey.urls", namespace="survey"),
    ),
]
urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]
