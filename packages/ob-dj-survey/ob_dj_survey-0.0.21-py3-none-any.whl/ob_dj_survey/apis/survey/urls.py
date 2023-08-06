from django.conf.urls import include
from django.urls import path
from rest_framework.routers import SimpleRouter

from ob_dj_survey.apis.survey.views import (
    AnswerView,
    QuestionActivationView,
    QuestionView,
    SurveyView,
)

app_name = "survey"

router = SimpleRouter(trailing_slash=False)

router.register(r"survey", SurveyView, basename="survey")

urlpatterns = [
    path("answers", AnswerView.as_view(), name="survey-answers"),
    path("question", QuestionView.as_view(), name="survey-question"),
    path(
        "question_activation/<int:pk>",
        QuestionActivationView.as_view(),
        name="survey-question-activation",
    ),
    path("", include(router.urls)),
]
