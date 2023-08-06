import typing

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ob_dj_survey.core.survey.managers import (
    AnswerManager,
    QuestionManager,
    ResponseManager,
    SurveyManager,
)
from ob_dj_survey.utils.models import DjangoModelCleanMixin
from ob_dj_survey.utils.validations import question_answer_validation


class Section(DjangoModelCleanMixin, models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(
        null=True,
        blank=True,
        help_text=_("The meta field is used to maintain meta data for sections. "),
        default=dict,
    )

    def __str__(self):
        return f"(PK={self.id}) {self.name}"


class Choice(DjangoModelCleanMixin, models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(
        null=True,
        blank=True,
        help_text=_("The meta field is used to maintain meta data for survey choice"),
        default=dict,
    )

    def __str__(self):
        return f"(PK={self.id}) {self.title}"


class QuestionChoiceMembership(DjangoModelCleanMixin, models.Model):
    question = models.ForeignKey(
        "survey.Question",
        on_delete=models.CASCADE,
        related_name="choices_membership",
    )
    choice = models.ForeignKey(
        "survey.Choice",
        on_delete=models.CASCADE,
        related_name="questions_membership",
    )
    order = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )

    class Meta:
        ordering = [
            "order",
        ]

    def __str__(self):
        return f"(PK={self.id}) Question({self.question_id}) Choice({self.choice_id})"


class Question(DjangoModelCleanMixin, models.Model):
    class QuestionTypes(models.TextChoices):
        TEXT = "text", _("text (multiple line)")
        SHORT_TEXT = "short-text", _("short text (one line)")
        RADIO = "radio", _("radio")
        YES_NO = "yes_no", _("Yes/No")
        SELECT = "select", _("select")
        SELECT_IMAGE = "select_image", _("Select Image")
        SELECT_MULTIPLE = "select_multiple", _("Select Multiple")
        INTEGER = "integer", _("integer")
        FLOAT = "float", _("float")
        DATE = "date", _("date")
        COUNTRY = "country", _("country")

    title = models.CharField(max_length=200)
    type = models.CharField(
        max_length=100, choices=QuestionTypes.choices, default=QuestionTypes.RADIO.value
    )
    choices = models.ManyToManyField(
        Choice,
        blank=True,
        related_name="questions",
        through=QuestionChoiceMembership,
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="questions",
        null=True,
        blank=True,
    )
    meta = models.JSONField(
        null=True,
        blank=True,
        help_text=_("The meta field is used to maintain meta data for questions"),
        default=dict,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return f"(PK={self.id}) {self.title}"


class SurveyQuestionMembership(DjangoModelCleanMixin, models.Model):
    question = models.ForeignKey(
        "survey.Question",
        on_delete=models.CASCADE,
        related_name="surveys_membership",
    )
    survey = models.ForeignKey(
        "survey.Survey", on_delete=models.CASCADE, related_name="questions_membership"
    )
    order = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = [
            "order",
        ]

    def __str__(self):
        return f"(PK={self.id}) Survey({self.survey_id}) Question({self.question_id})"


class Survey(DjangoModelCleanMixin, models.Model):
    class SubmissionType(models.TextChoices):
        FULL = "full", _("Full")
        PARTIAL = "partial", _("Partial")

    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    submission_type = models.CharField(
        max_length=10, choices=SubmissionType.choices, default=SubmissionType.PARTIAL
    )
    questions = models.ManyToManyField(
        Question,
        blank=True,
        related_name="surveys",
        through=SurveyQuestionMembership,
    )
    meta = models.JSONField(
        null=True,
        blank=True,
        help_text=_("The meta field is used to maintain meta data for survey"),
        default=dict,
    )
    callback = models.JSONField(
        null=True,
        blank=True,
        help_text=_(
            "The callback field is used to maintain callback to other apps "
            "(For example, if survey medical_record require to callback another app and pass "
            "survey response parameters)"
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def activate(self) -> typing.NoReturn:
        if self.is_active:
            raise ValidationError(_("Survey is already active"))
        self.is_active = True
        self.save()

    objects = SurveyManager()

    def __str__(self):
        return f"(PK={self.id}) {self.name}"


class Answer(DjangoModelCleanMixin, models.Model):
    class Status(models.TextChoices):
        COMPLETED = "completed", _("Completed")
        PARTIAL = "partial", _("Partial")

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="answers")
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PARTIAL
    )
    meta = models.JSONField(
        null=True,
        blank=True,
        help_text=_("The meta field is used to maintain meta data for survey answers"),
        default=dict,
    )
    created_by = models.ForeignKey(
        get_user_model(), blank=True, null=True, on_delete=models.CASCADE
    )  # Anonymous
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    class Meta:
        verbose_name = _("Survey Answers")
        verbose_name_plural = _("Survey Answers")

    def __str__(self):
        return f"(PK={self.pk}) {self.__class__.__name__}"

    def is_completed(self):
        answered_questions_ids = self.responses.values_list(
            "question_id", flat=True
        ).distinct()
        questions_ids = set(
            self.survey.questions.filter(
                surveys_membership__is_active=True
            ).values_list("id", flat=True)
        )
        unanswered_questions = questions_ids.difference(answered_questions_ids)
        return len(unanswered_questions) == 0

    def submit(
        self,
        answers: typing.List["Choice"],
    ):
        if self.survey.is_active is False:
            raise ValidationError("You can't submit inactive survey.")

        # remove only the submitted answers so we can recreate them with new values
        questions_ids = [answer["question_id"].id for answer in answers]
        Response.objects.filter(question_id__in=questions_ids, answer=self).delete()

        validated_answers = []
        for answer in answers:
            # If Answer Object is Dict
            if isinstance(answer, dict):
                values = answer.pop("values", [])
                choices = answer.pop("choices_ids", [])
                meta = answer.pop("meta", {})
                question = answer["question_id"]
                validated_answers.extend(
                    Response.objects.create(
                        question=question,
                        choice=choice,
                        meta=meta,
                        answer=self,
                    )
                    for choice in choices
                )
                validated_answers.extend(
                    Response.objects.create(
                        question=question, value=value, meta=meta, answer=self
                    )
                    for value in values
                )

        # we could have answers more than questions when we have questions
        # with type `SELECT` that have multiple answers for each question.
        if self.is_completed():
            self.status = self.Status.COMPLETED
        elif self.survey.submission_type != Survey.SubmissionType.FULL.value:
            self.status = self.Status.PARTIAL
        else:
            raise ValidationError(_("This Survey should be Fully Answered."))
        self.save()

    def reset_survey_answers(self):
        # clean-up - delete all answers
        Response.objects.filter(
            answer__created_by=self.created_by, answer__survey=self.survey
        ).delete()
        Answer.objects.filter(
            created_by=self.created_by,
            survey=self.survey,
        ).delete()


class Response(DjangoModelCleanMixin, models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="responses",
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    value = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta = models.JSONField(
        null=True,
        blank=True,
        help_text=_("The meta field is used to maintain meta data for survey response"),
        default=dict,
    )

    objects = ResponseManager()

    def __str__(self):
        return f"(PK={self.pk}) {self.__class__.__name__}"

    def _validate_question(self):
        question_membership = self.answer.survey.questions_membership.filter(
            question_id=self.question_id
        ).first()
        if not question_membership:
            raise ValidationError(
                _(
                    f"The question {self.question.title} is not in the survey's questions."
                )
            )

        if not question_membership.is_active:
            raise ValidationError(
                _(f"This question {self.question.title} is not active.")
            )

    def _validate_yes_no_question(self):
        if (
            self.question.type == self.question.QuestionTypes.YES_NO.value
            and self.value.lower()
            not in (
                "yes",
                "no",
            )
        ):
            raise ValidationError(
                _(f"The answer for {self.question.title} can accept yes/no values")
            )

    def clean(self) -> None:
        question_answer_validation(
            validationerr=ValidationError,
            question=self.question,
            choices=[self.choice] if self.choice else None,
            values=[self.value] if self.value else None,
        )
        self._validate_question()
        self._validate_yes_no_question()
