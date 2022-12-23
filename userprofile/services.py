
from django.conf import settings
from django.utils import timezone
from typing import Dict
import datetime
from dateutil.relativedelta import relativedelta

def calculate_time_delta(period: str) -> datetime.date:
    """
    Calculates period for tasks,
    that view must return.
    
    Returns datetime.date object that represents
    this day/week/month/year

    Parameters:
    -----------
        period: str
            abbreviature passed from request,
            all of this are described in SETTINGS module of
            this project.
    """
    tasks_period = define_period_for_relativedelta(period)
    today_date = timezone.now()
    relative_delta = relativedelta(*tasks_period) 
    time_delta = today_date - relative_delta
    return time_delta

def define_period_for_relativedelta(passed_period: str) -> Dict[str, int]:
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
        case settings.SORT_TASKS_LD:
            period = {"days": 0}
          
        case settings.SORT_TASKS_LW:
            period = {"weeks": 0}
           
        case settings.SORT_TASKS_LM:
            period = {"months": 0}

        case settings.SORT_TASKS_LY:
            period = {"years": 0}
    return period
