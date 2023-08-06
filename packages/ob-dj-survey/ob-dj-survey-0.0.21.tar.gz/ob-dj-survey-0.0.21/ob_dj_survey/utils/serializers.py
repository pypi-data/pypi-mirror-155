from django.conf import settings
from rest_framework.mixins import UpdateModelMixin

from ob_dj_survey.utils.helpers import import_from_string


class EmptyClass:
    pass


class CustomSerializerMixin:
    def get_serializer_class(self):
        SerializerClass = super().get_serializer_class()
        serializer_mixin = getattr(settings, "SERIALIZERS_MIXIN", {})
        MixinClass = (
            import_from_string(serializer_mixin.get(SerializerClass.__name__))
            or EmptyClass
        )

        class CustomizedSerializerClass(MixinClass, SerializerClass):
            pass

        return CustomizedSerializerClass


class PatchUpdateMixin(UpdateModelMixin):
    def patch(self, request, *args, **kwargs):
        kwargs.update({"partial": True})
        return super().partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
