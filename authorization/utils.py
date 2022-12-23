from django.http import (HttpResponse,
                         HttpResponseRedirect)
from django.urls import reverse_lazy


menu = [
    {
        "title": "About us",
        "url": "about_us:about_main"
    },
    {
        "title": "News",
        "url": "main_news:news_page"
    }
]

class MenuMixin:
    '''
    Contains methods to supplement template context data.
    '''
    def get_user_data(self, **kwargs):
        '''
        Accepts supplemented additional context atributes,
        supplements additional context attributes with menu options,
        returns common context.
        '''
        context = kwargs
        #it's copy of menu because of possible customization of this menu
        navigation_menu = menu.copy()
        context['menu'] = navigation_menu
        return context

class AuthenticationMixin:
    """
    Mixin for LoginUser and RegisterUser class-based views.

    Attributes:
    -----------
        Doesn't have

    Methods:
    --------
        get(request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect
            Checks if user is authenticated,
            redirects to profile if it is.
            Else delegates to superclass (CreateView or LoginView).
    """
    def get(self, request, *args, **kwargs) -> HttpResponse | HttpResponseRedirect:
        """
        Checks if user is authenticated,
        redirects to profile if it is.
        Else delegates to superclass (CreateView or LoginView).
        """
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy(
                    'profile:profile_page',
                    args = [self.request.user.uuid]
                )
            )
        return super().get(request, *args, **kwargs)