import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ob_dj_survey.apis.user.serializers import UserSerializer
from ob_dj_survey.core.survey.models import (
    Answer,
    Choice,
    Question,
    QuestionChoiceMembership,
    Response,
    Section,
    Survey,
    SurveyQuestionMembership,
)
from ob_dj_survey.utils.validations import question_answer_validation

logger = logging.getLogger(__name__)


class SectionSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)

    class Meta:
        model = Section
        fields = (
            "id",
            "name",
            "description",
            "meta",
        )


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "title", "description", "meta", "created_at")


class QuestionChoiceMembershipSerializer(serializers.ModelSerializer):
    choice = ChoiceSerializer()

    class Meta:
        model = QuestionChoiceMembership
        fields = ("id", "order", "choice")


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceMembershipSerializer(
        many=True, required=False, source="choices_membership"
    )
    section = SectionSerializer(read_only=True)
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(), write_only=True, required=False
    )

    class Meta:
        ref_name = "QuestionSerializer"
        model = Question
        fields = (
            "id",
            "title",
            "type",
            "section",
            "section_id",
            "meta",
            "created_at",
            "choices",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
        }

    def validate(self, attrs: dict):
        if "choices_membership" in attrs and attrs["type"] not in [
            "radio",
            "select",
            "select_multiple",
        ]:
            raise ValidationError(_("This question type doesn't accept choices!"))

        if "choices_membership" not in attrs and attrs["type"] in [
            "radio",
            "select",
            "select_multiple",
        ]:
            raise ValidationError(_("Choices required for this question type!"))
        return super().validate(attrs)

    def create(self, validated_data):
        choices = validated_data.pop("choices_membership", [])
        instance = Question.objects.create(**validated_data)
        for choice_membership in choices:
            choice_data = choice_membership["choice"]
            choice = Choice.objects.get_or_create(
                title=choice_data["title"],
                description=choice_data["description"],
                defaults={"meta": choice_data.get("meta", {})},
            )[0]
            QuestionChoiceMembership.objects.create(
                choice=choice,
                question=instance,
                order=choice_membership.get("order", 1),
            )
        return instance


class SurveyQuestionMembershipSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        ref_name = "SurveyQuestionMembershipSerializer"
        model = SurveyQuestionMembership
        fields = ("id", "order", "is_active", "question")


class SurveySerializer(serializers.ModelSerializer):
    questions = SurveyQuestionMembershipSerializer(
        many=True, source="questions_membership"
    )

    class Meta:
        ref_name = "SurveySerializer"
        model = Survey
        fields = (
            "id",
            "name",
            "questions",
            "created_at",
            "meta",
            "is_active",
        )


class AnswersSerializer(serializers.Serializer):
    """
        * Serializer for Submitting Answers

    - Answers Example :
        "answers": [
            {"question": question_1.pk, "choices": [ab_choice.pk]},
            { "question": question_2.pk, "choices": [fish_choice.pk], "values": ["Gluten"],},
            ....
    """

    question_id = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), required=True
    )
    choices_ids = serializers.PrimaryKeyRelatedField(
        queryset=Choice.objects.all(), many=True, required=False
    )
    values = serializers.ListField(required=False)
    meta = serializers.JSONField(required=False)

    def validate(self, attrs):
        if not attrs.get("choices_ids") and not attrs.get("values"):
            raise serializers.ValidationError(_("No Answers Provided"))
        return super().validate(attrs)


class ResponseSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    choice = ChoiceSerializer(read_only=True)

    class Meta:
        model = Response
        fields = (
            "id",
            "question",
            "choice",
            "value",
            "meta",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, attrs):
        return super().validate(attrs)


class SurveyAnswerSerializer(serializers.ModelSerializer):
    answers = AnswersSerializer(many=True, write_only=True)
    survey_id = serializers.PrimaryKeyRelatedField(
        queryset=Survey.objects.all(), write_only=True
    )

    responses = ResponseSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    survey = SurveySerializer(read_only=True)

    class Meta:
        ref_name = "AnswerSerializer"
        model = Answer
        fields = (
            "id",
            "survey",
            "survey_id",
            "responses",
            "answers",
            "status",
            "meta",
            "created_by",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, attrs):
        questions = attrs["survey_id"].questions.values_list("id", flat=True)
        for answer in attrs["answers"]:
            if answer["question_id"].id not in questions:
                raise ValidationError(_("You tried to answer the wrong question !"))

            question_answer_validation(
                ValidationError,
                question=answer["question_id"],
                choices=answer.get("choices_ids"),
                values=answer.get("values"),
            )

        submitted_question = [a["question_id"].id for a in attrs["answers"]]
        if len(submitted_question) != len(set(submitted_question)):
            raise ValidationError(
                _("You sent two diffrent response for the same question !")
            )

        attrs["created_by"] = self.context["request"].user
        return super().validate(attrs)

    def create(self, validated_data):
        filter_kwargs = {
            "survey_id": validated_data["survey_id"].id,
            "created_by": validated_data["created_by"],
        }
        if "meta" in validated_data:
            filter_kwargs["meta"] = validated_data["meta"]
        # if it's the first try create new instance, otherwise update the existing one
        instance, _ = Answer.objects.get_or_create(**filter_kwargs)

        instance.submit(answers=validated_data["answers"])
        instance.refresh_from_db()
        return instance
