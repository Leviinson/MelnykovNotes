from django.urls import (
                        path,
                        include
                        )
from .views import func_stub_about
app_name = 'about_us'
urlpatterns = [
    path('', func_stub_about, name='about_main')
]