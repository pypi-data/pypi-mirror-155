from dateutil.parser import parse
from django.utils.translation import gettext_lazy as _
from django_countries import countries


def question_answer_validation(validationerr, question, choices=None, values=None):
    """Validate choices given to answer a specific question."""

    if not choices and not values:
        validationerr(
            _(f"No answer given for question: {question.title}"),
        )

    if question.type in ["radio", "select", "select_multiple"]:
        if values:
            raise validationerr(
                _(f"You can't answer a {question.type} question type with a value.")
            )

        if not choices:
            raise validationerr(
                _(f"You can't answer a {question.type} question type without choices.")
            )

        for choice in choices:
            if choice.id not in question.choices.values_list("id", flat=True):
                raise validationerr(
                    _(f"{choice.title} is not a valid choice for {question.title}.")
                )

    if question.type not in [
        "radio",
        "select",
        "select_multiple",
    ]:
        if choices:
            raise validationerr(
                _(f"You can't answer a {question.type} question type with choices.")
            )

        if not values:
            raise validationerr(
                _(f"You can't answer a {question.type} question type without values.")
            )

        if question.type == "yes_no":
            for value in values:
                if value.lower() not in ["yes", "no"]:
                    raise validationerr(
                        _(f"{question.type} question type accept yes or no as answer.")
                    )
        if question.type == "integer":
            for value in values:
                if not str(value).isnumeric():
                    raise validationerr(
                        _(f"{question.type} question type accept integer as answer.")
                    )

        if question.type == "country":
            for value in values:
                if value not in [*countries.countries.keys()]:
                    raise validationerr(
                        _(
                            f"{question.type} question type accept country code as answer."
                        )
                    )

        if question.type == "float":
            for value in values:
                try:
                    float(value)
                except ValueError:
                    raise validationerr(
                        _(f"{question.type} question type accept float as answer.")
                    )

        if question.type == "date":
            for value in values:
                try:
                    parse(value, fuzzy=False)
                except ValueError:
                    raise validationerr(
                        _(f"{question.type} question type accept date as answer.")
                    )
