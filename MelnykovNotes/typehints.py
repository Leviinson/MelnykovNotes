from typing import NamedTuple

class Period(NamedTuple):
    abbreviature: str
    title: str
    relativedelta_parameter_title: str = None
    django_template__date_filter: str = None
    django_orm_date_truncation: str = None
