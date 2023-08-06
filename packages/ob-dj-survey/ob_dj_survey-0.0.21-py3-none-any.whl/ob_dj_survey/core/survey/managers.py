import typing

from django.db import models

if typing.TYPE_CHECKING:
    from django.contrib.auth import get_user_model as User

    from ob_dj_survey.core.survey.models import Answer, Choice, Question, Survey  # noqa


class SurveyManager(models.Manager):
    def active(self) -> models.QuerySet["Survey"]:
        return self.filter(is_active=True)


class QuestionManager(models.Manager):
    def active(self) -> models.QuerySet["Question"]:
        return self.filter(is_active=True)


class AnswerManager(models.Manager):
    def get_survey_previous_answer(self, *args, **kwargs):
        """
        This should return the second the last submitted answer
        """
        obj = self.get(*args, **kwargs)

        survey_answers = self.filter(
            meta=obj.meta, created_by=obj.created_by, survey=obj.survey
        ).order_by("created_at")
        answers_count = survey_answers.count()

        return survey_answers[answers_count - 2] if answers_count > 1 else None

    def get_survey_answer(self, *args, **kwargs):
        """
        This should return the last submitted answer
        """
        obj = self.get(*args, **kwargs)
        return (
            self.filter(created_by=obj.created_by, survey=obj.survey, meta=obj.meta)
            .order_by("created_at")
            .last()
        )

    def create(
        self,
        survey: "Survey",
        answers: typing.List["Choice"] = None,
        created_by: "User" = None,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> "Answer":
        instance = super().create(survey=survey, created_by=created_by, *args, **kwargs)
        if answers:
            instance.submit(answers=answers)
        return instance


class ResponseManager(models.Manager):
    pass
