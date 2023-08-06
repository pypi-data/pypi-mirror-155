from django.contrib import admin

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


class QuestionChoiceMembershipInlineAdmin(admin.TabularInline):
    model = QuestionChoiceMembership
    extra = 1


class SurveyQuestionMembershipInlineAdmin(admin.TabularInline):
    model = SurveyQuestionMembership
    extra = 0


class QuestionInlineAdmin(admin.TabularInline):
    model = Question
    extra = 0


class SectionInlineAdmin(admin.TabularInline):
    model = Section
    extra = 0


class SurveyInlineAdmin(admin.TabularInline):
    model = Survey
    extra = 0


class ResponseInlineAdmin(admin.TabularInline):
    model = Response
    extra = 0


class AnswerInlineAdmin(admin.TabularInline):
    model = Answer
    extra = 0


class ResponsesAnswersInline(admin.TabularInline):
    model = Response


@admin.register(Section)
class SectionAdmin(
    admin.ModelAdmin,
):
    list_display = ["id", "name", "description", "meta", "created_at"]
    inlines = [QuestionInlineAdmin]


@admin.register(Survey)
class SurveyAdmin(
    admin.ModelAdmin,
):
    list_display = ["id", "name", "meta", "created_at"]
    inlines = [SurveyQuestionMembershipInlineAdmin, AnswerInlineAdmin]


@admin.register(Choice)
class ChoiceAdmin(
    admin.ModelAdmin,
):
    list_display = ["id", "title", "description", "created_at"]
    list_filter = [
        "questions",
        "questions__surveys",
    ]


@admin.register(Question)
class QuestionAdmin(
    admin.ModelAdmin,
):
    list_display = ["id", "title", "type", "section", "meta", "created_at"]
    inlines = [QuestionChoiceMembershipInlineAdmin, ResponseInlineAdmin]
    list_filter = ["surveys", "section"]


@admin.register(Response)
class ResponseAdmin(
    admin.ModelAdmin,
):
    list_display = [
        "id",
        "question",
        "choice",
        "value",
        "meta",
        "updated_at",
        "created_at",
    ]
    list_display_links = ["question"]
    list_editable = ["choice", "value"]
    list_filter = ["question", "choice"]


@admin.register(Answer)
class AnswerAdmin(
    admin.ModelAdmin,
):
    list_display = ["id", "status", "updated_at", "created_at"]
    inlines = [
        ResponsesAnswersInline,
    ]
    list_filter = [
        "survey",
        "responses",
    ]
