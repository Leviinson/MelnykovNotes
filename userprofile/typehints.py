from django.conf import settings
from typing import NamedTuple

class PeriodsOfTasks(NamedTuple):
    this_day = settings.SORT_TASKS_TD
    this_week = settings.SORT_TASKS_TW
    this_month = settings.SORT_TASKS_TM
    this_year = settings.SORT_TASKS_TY
    all_time = settings.SORT_TASKS_AT
