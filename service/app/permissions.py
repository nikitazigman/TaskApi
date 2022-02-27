import logging

from rest_framework import permissions

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        logger.debug(
            f"we got permission request from {request.user} of {obj.user_id} object {obj}"
        )
        return obj.user_id == request.user and super(IsOwner, self).has_object_permission(
            request, view, obj
        )
