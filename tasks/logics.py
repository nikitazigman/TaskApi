from typing import Union
import logging

from django.contrib.auth.models import User
from .models import List, Task


logger = logging.getLogger(__name__)


def filter_owner_data(user: User, queryset: Union[List, Task]) -> Union[List, Task]:
    """
        it filters given objects by it's owner
    :param user: from django User model
    :param queryset: Task or List models
    :return: filtered obj by given owner
    """

    logger.debug(f" filtered queryset {type(queryset.first()).__name__} by owner {user.username}: user_id = {user.id}")
    return queryset.filter(user_id=user)
