from django.urls import (
                        path,
                        include
                        )
from .views import func_stub_userprofile
app_name = 'userprofile'
urlpatterns = [
    path('<uuid:user_uuid>/', func_stub_userprofile, name='profile_page')
]