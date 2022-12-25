"""
Module was created to collect into it
business-logic from django-views.

Because the creator adheres to the principle, that
busines-logic must be in the MODEL layer, but not
in the CONTROLLER layer, that is represented in Django
by the name "View".
"""
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
import uuid
from copy import copy

from .models import Tasks


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


def _get_period_and_dict_key_from_settings(period_abbreviature: str) -> dict[str, dict]:
    """
    """
    for period_key in settings.TASKS_PERIODS:
        period_from_settings = settings.TASKS_PERIODS[period_key]
        if period_from_settings['abbreviature'] == period_abbreviature:
            return period_from_settings, period_key


def _define_period_parameter_for_relativedelta(period_from_settings: str) -> dict[str, int]:
    """
    Returns dict, that describes parameter for 'relativedelta' function.
    
    Parameters:
    -----------
        period: str
            abbreviature passed from request,
            all of this are implemented in SETTINGS module of
            this project.
    """
    assert "__parameter_title" in period_from_settings, \
           "Here must be passed concrete period, not 'all time'."
    period = period_from_settings['__parameter_title']
    return {period: 1}


def _get_selected_period_title(period_from_settings: str):
    '''
    Returns:
    --------
        selected period title, like: day, week, month etc.

    Parameters:
    -----------
        period: str
    '''
    return period_from_settings['title']


def _get_additional_periods_titles_and_abbreviatures(period_key_from_settings: str) -> list[str]:
    """
    Returns:
    --------
        additional periods titles list
    
    Parameters:
    -----------
        period: str
    """
    periods_from_settings = settings.TASKS_PERIODS.copy()
    periods_from_settings.pop(period_key_from_settings)
    titles = [settings.TASKS_PERIODS[period]['title'] for period in periods_from_settings]
    abbreviatures = [settings.TASKS_PERIODS[period]['abbreviature'] for period in periods_from_settings]
    return zip(titles, abbreviatures)


def _get_selected_and_additional_periods(period_from_settings: str,
                                         period_key_from_settings: str) -> tuple[str, list]:
    """
    """                         
    selected_period_title = _get_selected_period_title(period_from_settings)
    additional_periods_titles_and_abbreviatures = _get_additional_periods_titles_and_abbreviatures(period_key_from_settings)
    return selected_period_title, additional_periods_titles_and_abbreviatures


def _get_user_tasks_by_period_and_access_from_db(user: AbstractBaseUser,
                                      period_from_settings: dict) -> QuerySet:
    """
    Returns:
    --------
        user tasks by period from db: QuerySet[Tasks].
    
    Parameters:
    -----------
        user: AbsctractBaseUser

        period: settings.SORT_TASKS_XX variable
    """
    if period_from_settings['abbreviature'] == settings.TASKS_PERIODS['all_time']['abbreviature']:
        user_tasks_by_period = Tasks.objects.filter(user_id = user.pk)
    else:
        period_parameter_for_relativedelta = _define_period_parameter_for_relativedelta(
                                                    period_from_settings
                                                )
        user_datetime_now = timezone.now()
        last_date = timezone.now() + relativedelta(**period_parameter_for_relativedelta)
        user_tasks_by_period = Tasks.objects.filter(user_id = user.pk,
                                                    date_created__range = (user_datetime_now,
                                                                           last_date))
    return user_tasks_by_period    
    

def get_context_for_userprofile_page(request: HttpRequest,
                                     period_abbreviature: str,
                                     user_uuid: uuid.UUID):
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
    user = users.objects.get(uuid = user_uuid)
    is_owner = _is_user_owner(request, user_uuid)

    period_from_settings, \
    period_dict_key_from_settings = _get_period_and_dict_key_from_settings(period_abbreviature)

    selected_period_title, \
    additional_periods_titles_and_abbreviatures = _get_selected_and_additional_periods(period_from_settings,
                                                                                       period_dict_key_from_settings)
    user_tasks_by_period = _get_user_tasks_by_period_and_access_from_db(user,
                                                                        period_from_settings)                                                
    
    return {'user': user,
            'tasks': user_tasks_by_period,
            'friends': user.friends.all(),
            'owner': is_owner,
            'selected_period_title': selected_period_title,
            'additional_periods_titles_and_abbreviatures': additional_periods_titles_and_abbreviatures}
