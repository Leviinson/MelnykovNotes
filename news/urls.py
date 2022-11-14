from django.urls import (
                        path,
                        include
                        )
from .views import func_stub_news
app_name = 'main_news'
urlpatterns = [
    path('', func_stub_news, name='news_page')
]