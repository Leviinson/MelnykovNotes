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
from django.db.models import (Count,
                              DateField)
from django.db.models.functions import Trunc

# for type hints
from django.http import HttpRequest
from django.db.models import QuerySet
from django.contrib.auth.models import AbstractBaseUser
from MelnykovNotes.typehints import Period
# -----------------------------------------------------
from dateutil.relativedelta import relativedelta
import uuid


def _get_requested_user_profiles(sender_user: HttpRequest,
                                 requested_user_uuid: uuid.UUID,
                                 is_sender_user_owner: bool) -> tuple:
    """
    Returns:
    --------
        requested user object from db
    
    Parameters:
    -----------
        requested_user_uuid: uuid.UUID
    """
    if is_sender_user_owner:
        return sender_user
    requested_user = get_object_or_404(get_user_model(), uuid = requested_user_uuid)
    return requested_user


def _is_sender_user_owner(sender_user_uuid: uuid.UUID,
                          requested_user_uuid: uuid.UUID) -> bool:
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


def _define_period_parameter_for_relativedelta(relativedelta_parameter_title: str | None) -> dict[str, int]:
    """
    Returns:
    --------
        dict, that describes kwarg for 'dateutil.relativedelta.relativedelta' function.
    
    Parameters:
    -----------
        relativedelta_parameter_title: str | None (None because it's standard value)
    """
    assert relativedelta_parameter_title is not None, \
           "Here must be passed concrete period, not 'all time'." 
    return {relativedelta_parameter_title: 1} # 1 because we add one day/one month/one year to
                                              # actual date


def _get_add_periods_titles_and_abbreviatures(period_abbreviature: str) -> list[str]:
    """
    Returns:
    --------
        list of titles and abbreviatures of additional periods
    
    Parameters:
    -----------
        period_abbreviature: str
            described in the settings of project
    """
    periods_from_settings: dict = settings.DICT_OF_PERIODS.copy()
    periods_from_settings.pop(period_abbreviature)
    return [(period.title, period.abbreviature) for period in periods_from_settings.values()]


def _calculate_range_for_tasks(period_parameter_for_relativedelta: dict):
    """
    Returns:
    --------
        range of dates: between requested user time zone
        and requested period of tasks | datetime.datetime
    
    Parameters:
        period_parameter_for_relativedelta: dict
            looks like {"years": 1}
    """
    now = timezone.now()
    last_date = now - relativedelta(**period_parameter_for_relativedelta)
    return now, last_date


def _select_requested_user_tasks_from_db_wo_period(requested_user: AbstractBaseUser,
                                                   sender_user: AbstractBaseUser,
                                                   is_sender_user_owner: bool) -> QuerySet:
    """
    Returns:
    --------
        requested user tasks for all time [QuerySet]

    Parameters:
    -----------
        requested_user: AbstractBaseUser
        sender_user: AbstractBaseUser
        is_sender_user_owner: bool
    """
    
    if is_sender_user_owner:
        accessed_tasks = requested_user.tasks_set.all()
    else:
        public_tasks = requested_user.tasks_set.filter(is_private = False)
        private_tasks = requested_user.tasks_set.filter(pk__in = 
                                                        sender_user.admitted_tasks.values_list('task__pk', flat = True))
        accessed_tasks = public_tasks | private_tasks
    return accessed_tasks


def _select_requested_user_tasks_from_db_by_period(requested_user: AbstractBaseUser,
                                                   sender_user: AbstractBaseUser,
                                                   is_sender_user_owner: bool,
                                                   relativedelta_parameter_title: str | None) -> QuerySet:
    """
    Returns:
    --------
        requested user task for specified period [QuerySet]

    Parameters:
    -----------
        requested_user: AbstractBaseUser
        sender_user: AbstractBaseUser
        relativedelta_parameter_title: str | None (None because it's standard value)
        is_sender_user_owner: bool
    """
    period_parameter_for_relativedelta = _define_period_parameter_for_relativedelta(relativedelta_parameter_title)
    sender_user_datetime_now, last_date = _calculate_range_for_tasks(period_parameter_for_relativedelta)
    if is_sender_user_owner:
        accessed_tasks = requested_user.tasks_set.filter(date_created__range = (last_date,
                                                                                sender_user_datetime_now))
    else:
        public_tasks = requested_user.tasks_set.filter(is_private = False,
                                                       date_created__range = (last_date,
                                                                              sender_user_datetime_now))
        private_tasks = requested_user.tasks_set.filter(pk__in = sender_user.admitted_tasks.values_list('task__pk',
                                                                                                        flat = True),
                                                        date_created__range = (last_date,
                                                                               sender_user_datetime_now))
        accessed_tasks = public_tasks | private_tasks
    return accessed_tasks


def _get_requested_user_tasks_grouped_by_period_and_access_from_db(requested_user: AbstractBaseUser,
                                                                   sender_user: AbstractBaseUser,
                                                                   is_sender_user_owner: bool,
                                                                   period_entity_from_settings: Period) -> QuerySet:
    """
    Returns:
    --------
        user tasks by period from db: QuerySet[Tasks].
    
    Parameters:
    -----------
        requested_user: AbsctractBaseUser
        sender_user: AbstractBaseUser
        is_sender_user_owner: bool
        period_entity_from_settings: MelnykovNotes.typehints.Period -- settings.THIS_XXX_PERIOD variable
    """
    if period_entity_from_settings.abbreviature == settings.ALL_TIME_PERIOD.abbreviature:
        accessed_tasks = _select_requested_user_tasks_from_db_wo_period(requested_user = requested_user,
                                                                        sender_user = sender_user,
                                                                        is_sender_user_owner = is_sender_user_owner)
    else:
        accessed_tasks = _select_requested_user_tasks_from_db_by_period(requested_user = requested_user,
                                                                        sender_user = sender_user,
                                                                        is_sender_user_owner = is_sender_user_owner,
                                                                        relativedelta_parameter_title = period_entity_from_settings.relativedelta_parameter_title)
    accessed_tasks_grouped_by_period = accessed_tasks.annotate(date = Trunc('date_created',
                                                                            period_entity_from_settings.django_orm_date_truncation,
                                                                            output_field = DateField())).values('date')
    number_of_accessed_tasks_grouped_by_period = accessed_tasks_grouped_by_period.annotate(number_of_tasks = Count('date')).order_by('date')
    return number_of_accessed_tasks_grouped_by_period[:7]


def get_context_for_userprofile_page(request: HttpRequest,
                                     period_abbreviature: str,
                                     requested_user_uuid: uuid.UUID):
    """
    Returns:
    --------
        context for view with next keys:
            :dict_key: 'user' -- CustomUser model
            :dict_key: 'number_of_tasks_by_period' -- QuerySet[Tasks]
            :dict_key: 'friends' -- Queryset[UserModel.friends]
            :dict_key: 'is_owner' -- boolean value
            :dict_key: 'selected_period_title' -- str
            :dict_key: 'additional_periods_titles_and_abbreviatures' -- list[str]
            :dict_key: 'date_filter' -- str (uses to asign value for "date" filter parameter of django templates)

    Parameters:
    -----------
        request: django.http.HttpRequest
    
        period_abbreviature: str

        requested_user_uuid: uuid.UUID
    """
    sender_user = request.user
    is_sender_user_owner = _is_sender_user_owner(sender_user.uuid, requested_user_uuid)
    requested_user = _get_requested_user_profiles(sender_user, requested_user_uuid, is_sender_user_owner)
    period_entity_from_settings: Period = settings.DICT_OF_PERIODS[period_abbreviature]
    selected_period_title = period_entity_from_settings.title
    add_periods_titles_and_abbreviatures = _get_add_periods_titles_and_abbreviatures(period_abbreviature)
    requested_user_tasks_by_period_and_access = _get_requested_user_tasks_grouped_by_period_and_access_from_db(requested_user,
                                                                                                       sender_user,
                                                                                                       is_sender_user_owner,
                                                                                                       period_entity_from_settings)
    return {'user': requested_user,
            'number_of_tasks_by_period': requested_user_tasks_by_period_and_access,
            'friends': requested_user.friends.values("username", "uuid").all(),
            'is_owner': is_sender_user_owner,
            'selected_period_title': selected_period_title,
            'additional_periods_titles_and_abbreviatures': add_periods_titles_and_abbreviatures,
            'date_filter': period_entity_from_settings.django_template__date_filter}
