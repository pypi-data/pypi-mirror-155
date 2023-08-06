from django.apps import apps
from django.conf import settings
from django.core.checks import Error
from django.utils.module_loading import import_string

REQUIRED_INSTALLED_APPS = [
    "rest_framework",
]

REQUIRED_DEPENDENCIES = [
    "celery>=5",
]


def required_dependencies(app_configs, **kwargs):
    return []


def required_installed_apps(app_configs, **kwargs):
    return [
        Error(f"{app} is required in INSTALLED_APPS")
        for app in REQUIRED_INSTALLED_APPS
        if not apps.is_installed(app)
    ]


def required_settings(app_configs, **kwargs):
    return []


def serializer_validations(app_configs, **kwargs):

    if not settings.SERIALIZERS_MIXIN:
        return []

    for name, path in settings.SERIALIZERS_MIXIN.items():
        try:
            serializer_class = import_string(path)
            if isinstance(serializer_class, type):
                return []

            return [Error(f"{path} is not a class")]
        except ImportError:
            return [Error(f"{path} is not found")]
