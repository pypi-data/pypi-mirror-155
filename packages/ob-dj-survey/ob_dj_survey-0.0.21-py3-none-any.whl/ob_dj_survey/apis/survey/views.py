import logging

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, permissions, viewsets

from ob_dj_survey.apis.survey.permissions import SurveyManagerPermission
from ob_dj_survey.apis.survey.serializers import (
    QuestionSerializer,
    SurveyAnswerSerializer,
    SurveyQuestionMembershipSerializer,
    SurveySerializer,
)
from ob_dj_survey.core.survey.models import (
    Answer,
    Question,
    Survey,
    SurveyQuestionMembership,
)
from ob_dj_survey.utils.serializers import CustomSerializerMixin, PatchUpdateMixin

logger = logging.getLogger(__name__)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="List Survey",
        operation_description="List Survey",
        tags=[
            "Survey",
        ],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Retrieve Survey",
        operation_description="retrieve survey",
        tags=[
            "Survey",
        ],
    ),
)
class SurveyView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    CustomSerializerMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated, SurveyManagerPermission]
    serializer_class = SurveySerializer
    queryset = Survey.objects.active()


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Survey Answer",
        operation_description="submit your answers",
        tags=[
            "Survey",
        ],
    ),
)
class AnswerView(CustomSerializerMixin, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SurveyAnswerSerializer
    queryset = Answer.objects.all()


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Survey Question",
        operation_description="Create new question",
        tags=[
            "Survey",
        ],
    ),
)
class QuestionView(CustomSerializerMixin, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, SurveyManagerPermission]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_summary="Activate/Deactivate Question",
        operation_description="Activate or deactivate a question",
        tags=[
            "Survey",
        ],
    ),
)
class QuestionActivationView(PatchUpdateMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, SurveyManagerPermission]
    serializer_class = SurveyQuestionMembershipSerializer
    queryset = SurveyQuestionMembership.objects.all()
