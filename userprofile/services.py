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
from django.shortcuts import get_object_or_404

# for type hints
from django.http import HttpRequest
from django.db.models import QuerySet
from django.contrib.auth.models import AbstractBaseUser
# -----------------------------------------------------
from dateutil.relativedelta import relativedelta
import uuid


def _get_requested_user_profiles(requested_user_uuid: uuid.UUID) -> tuple:
    """
    Returns:
    --------
        requested user object from db
    
    Parameters:
    -----------
        requested_user_uuid: uuid.UUID
    """
    requested_user = get_object_or_404(get_user_model(), uuid = requested_user_uuid)
    return requested_user


def _is_sender_user_owner(sender_user_uuid: uuid.UUID,
                          requested_user_uuid: str) -> bool:
    """
    Returns:
    --------
        boolean value, that represents meaning "is user owner or not"

    Parameters:
    -----------
        sender_user_uuid: uuid.UUID
        requested_user_uuid: uuid.UUID
    """
    if sender_user_uuid == requested_user_uuid:  
        return True
    return False


def _define_period_parameter_for_relativedelta(period_entity_from_settings: str) -> dict[str, int]:
    """
    Returns:
    --------
        dict, that describes kwarg for 'relativedelta' function.
    
    Parameters:
    -----------
        period_entity_from_settings: dict
            settings.XXX_PERIOD value from settings of the project
            using for dateutil.relativedelta.relativedelta function
            key word argument (days/weeks/month/years etc.)
    """
    assert "__parameter_title" in period_entity_from_settings, \
           "Here must be passed concrete period, not 'all time'."
    period = period_entity_from_settings['__parameter_title']
    return {period: 1} # 1 because we add one day/one month/one year to
                       # actual date


def _get_add_periods_titles_and_abbreviatures(period_abbreviature: str) -> list[str]:
    """
    Returns:
    --------
        additional periods titles list
    
    Parameters:
    -----------
        period_abbreviature: str
            described in the settings of project
    """
    periods_from_settings: dict = settings.DICT_OF_PERIODS.copy()
    periods_from_settings.pop(period_abbreviature)
    titles = [periods_from_settings[period]['title'] for period in periods_from_settings]
    abbreviatures = [periods_from_settings[period]['abbreviature'] for period in periods_from_settings]
    return zip(titles, abbreviatures)


def _calculate_range_for_tasks(period_parameter_for_relativedelta: dict):
    """
    Returns:
    --------
        range of dates: between requested user time zone
        and requested period of tasks
    
    Parameters:
        period_parameter_for_relativedelta: dict
            looks like {"years": 1}
    """
    requested_user_datetime_now = timezone.now()
    last_date = requested_user_datetime_now + relativedelta(**period_parameter_for_relativedelta)
    return requested_user_datetime_now, last_date


def _select_requested_user_tasks_from_db_wo_period(requested_user,
                                                   sender_user):
    """
    Returns:
    --------
        requested user tasks for all time [QuerySet]

    Parameters:
    -----------
        requested_user: AbstractBaseUser
        sender_user: AbstractBaseUser
    """
    public_tasks = requested_user.tasks_set.filter(is_private = False).order_by('date_created')
    private_tasks = requested_user.tasks_set.filter(pk__in = 
                            sender_user.admitted_tasks.values_list('task__pk', flat = True)).order_by('date_created')
    return public_tasks | private_tasks


def _select_requested_user_tasks_from_db_by_period(requested_user: AbstractBaseUser,
                                                   sender_user: AbstractBaseUser,
                                                   period_entity_from_settings: dict):
    """
    Returns:
    --------
        requested user task for specified period [QuerySet]

    Parameters:
    -----------
        requested_user: AbstractBaseUser
        sender_user: AbstractBaseUser
        period_entity_from_settings: dict
    """
    period_parameter_for_relativedelta = _define_period_parameter_for_relativedelta(
                                                    period_entity_from_settings
                                                )
    sender_user_datetime_now, last_date = _calculate_range_for_tasks(period_parameter_for_relativedelta)
    public_tasks = requested_user.tasks_set.filter(is_private = False,
                                                   date_created__range = (sender_user_datetime_now,
                                                                               last_date)).order_by('date_created')
    if requested_user.uuid != sender_user.uuid:
        private_tasks = requested_user.tasks_set.filter(pk__in = sender_user.admitted_tasks.values_list('task__pk', flat = True),
                                                        date_created__range = (sender_user_datetime_now,
                                                                               last_date)).order_by('date_created')
    else:
        private_tasks = requested_user.tasks_set.filter(date_created__range = (sender_user_datetime_now,
                                                                               last_date)).order_by('date_created')
    return public_tasks | private_tasks


def _get_requested_user_tasks_by_period_and_access_from_db(requested_user: AbstractBaseUser,
                                                           sender_user: AbstractBaseUser,
                                                           period_entity_from_settings: dict) -> QuerySet:
    """
    Returns:
    --------
        user tasks by period from db: QuerySet[Tasks].
    
    Parameters:
    -----------
        requested_user: AbsctractBaseUser
        sender_user: AbstractBaseUser
        period_entity_from_settings: dict -- settings.XXX_PERIOD variable
    """
    if period_entity_from_settings['abbreviature'] == settings.ALL_TIME_PERIOD['abbreviature']:
        requested_user_tasks_by_period = _select_requested_user_tasks_from_db_wo_period(requested_user,
                                                                                        sender_user)
    else:
        requested_user_tasks_by_period = _select_requested_user_tasks_from_db_by_period(requested_user,
                                                                                        sender_user,
                                                                                        period_entity_from_settings)
    return requested_user_tasks_by_period


def get_context_for_userprofile_page(request: HttpRequest,
                                     period_abbreviature: str,
                                     requested_user_uuid: str):
    """
    Returns:
    --------
        context for view with next keys:
            :dict_key: 'user' -- CustomUser model
            :dict_key: 'tasks' -- QuerySet[Tasks]
            :dict_key: 'friends' -- Queryset[UserModel.friends]
            :dict_key: 'owner' -- boolean value
            :dict_key: 'selected_period_title' -- str
            :dict_key: 'additional_periods_titles_and_abbreviatures' -- list[str]

    Parameters:
    -----------
        request: django.http.HttpRequest

        period_abbreviature: str

        requested_user_uuid: uuid.UUID
    """
    requested_user = _get_requested_user_profiles(requested_user_uuid)
    is_sender_user_owner = _is_sender_user_owner(request.user.uuid, requested_user_uuid)
    period_entity_from_settings = settings.DICT_OF_PERIODS[period_abbreviature]
    selected_period_title = period_entity_from_settings['title']
    add_periods_titles_and_abbreviatures = _get_add_periods_titles_and_abbreviatures(period_abbreviature)
    requested_user_tasks_by_period_and_access = _get_requested_user_tasks_by_period_and_access_from_db(requested_user,
                                                                                                       request.user,
                                                                                                       period_entity_from_settings)                                                
    return {'user': requested_user,
            'tasks': requested_user_tasks_by_period_and_access,
            'friends': requested_user.friends.all(),
            'owner': is_sender_user_owner,
            'selected_period_title': selected_period_title,
            'additional_periods_titles_and_abbreviatures': add_periods_titles_and_abbreviatures}
