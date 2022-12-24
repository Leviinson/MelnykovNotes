"""
Module was created to collect into it
business-logic from django-views.

Because the creator adheres to the principle, that
busines-logic must be in the MODEL layer, but not
in the CONTROLLER layer, that is represented in Django
by the name "View".
"""
import uuid
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

# for type hints
from django.http import HttpRequest
from django.db.models import (QuerySet,
                              Model)
from django.contrib.auth.models import AbstractBaseUser
# -----------------------------------------------------
from dateutil.relativedelta import relativedelta

from .models import Tasks
from .typehints import PeriodsOfTasks


def _define_period_for_time_delta(passed_period: PeriodsOfTasks) -> dict[str, int]:
    """
    Returns dict, that describes parameter for 'relativedelta' function.
    
    Parameters:
    -----------
        period: str
            abbreviature passed from request,
            all of this are described in SETTINGS module of
            this project.
    """
    match passed_period:
        case PeriodsOfTasks.this_day:
            period = "days"
          
        case PeriodsOfTasks.this_week:
            period = "weeks"
           
        case PeriodsOfTasks.this_month:
            period = "months"

        case PeriodsOfTasks.this_year:
            period = "years"
    
    return {period: 1}


def _is_user_owner(request: HttpRequest, user_uuid: uuid.UUID) -> bool:
    """
    Returns:
    --------
        boolean value, that represents meaning "is user owner or not"

    Parameters:
    -----------
        request: HtppRequest
        
        user_uuid: uuid.UUID
    """
    match request.user.uuid == user_uuid:  
        case True:
            is_owner = True

        case False:
            is_owner = False
    return is_owner


def _get_user_tasks_by_period_from_db(user_profile: AbstractBaseUser, period: PeriodsOfTasks) -> QuerySet:
    """
    Returns:
    --------
        user tasks by period from db: QuerySet[Tasks].
    
    Parameters:
    -----------
        user_profile: AbsctractBaseUser

        period: settings.SORT_TASKS_XX variable
    """
    if period == PeriodsOfTasks.all_time:
        user_tasks_by_period = Tasks.objects.filter(user_id = user_profile.pk)
    else:
        period_for_time_delta = _define_period_for_time_delta(period)
        user_datetime_now = timezone.now()
        last_date = timezone.now() + relativedelta(**period_for_time_delta)
        user_tasks_by_period = Tasks.objects.filter(user_id = user_profile.pk,
                                                    date_created__range = (user_datetime_now,
                                                                           last_date))
    return user_tasks_by_period


def get_user_tasks_by_period(request: HttpRequest,
                             period: settings.SORT_TASKS_TD,
                             user_uuid: uuid.UUID) -> dict[Model,
                                                           QuerySet,
                                                           QuerySet,
                                                           bool,
                                                           ]:
    """
    Returns:
    --------
        context for view with next keys:
            :dict_key: 'user' -- CustomUser model

            :dict_key: 'tasks' -- QuerySet[Tasks]
            
            :dict_key: 'friends' -- Queryset[UserModel.friends]

            :dict_key: 'owner' -- boolean value

    Parameters:
    -----------
        request: django.http.HttpRequest

        period: settings.SORT_TASKS_XX variable

        user_uuid: uuid.UUID 
    """
    users = get_user_model()
    user_profile = users.objects.get(uuid = user_uuid)
    is_owner = _is_user_owner(request, user_uuid)
    user_tasks_by_period = _get_user_tasks_by_period_from_db(user_profile = user_profile,
                                                             period = period)
    return {'user': user_profile,
            'tasks': user_tasks_by_period,
            'friends': user_profile.friends.all(),
            'owner': is_owner}