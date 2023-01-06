from django.urls import (path,
                         include)
from .views import (show_userprofile,
                    page_not_found) 
app_name = 'userprofile'
urlpatterns = [
        path('<uuid:requested_user_uuid>/<slug:period_abbreviature>/', show_userprofile, name = 'profile_page_with_period'),
        path('<uuid:requested_user_uuid>/', show_userprofile, name = 'profile_page_without_period')
]

handler404 = page_not_found