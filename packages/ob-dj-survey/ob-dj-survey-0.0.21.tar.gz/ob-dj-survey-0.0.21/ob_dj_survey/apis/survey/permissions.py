from rest_framework.permissions import BasePermission


class SurveyManagerPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Allows access only to survey managers.
        Managers can create, update and list surveys, other users can view details
        """
        user = request.user
        return (
            user
            and hasattr(user, "can_manage_survey")
            and user.can_manage_survey(request=request, view=view, obj=None)
        )

    def has_object_permission(self, request, view, obj):
        """
        controle who can see a specific survey.
        """
        user = request.user
        return (
            user
            and hasattr(user, "can_manage_survey")
            and user.can_manage_survey(request=request, view=view, obj=obj)
        )
