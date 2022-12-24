from django.contrib.auth import (login,
                                 logout)
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.views.generic import CreateView
from django.urls import (reverse,
                         reverse_lazy)
from django.http import (HttpRequest, HttpResponse,
                         HttpResponseRedirect)


from typing import (Any,
                    Dict)


from .forms import (RegisterUserForm,
                    LoginUserForm)
from .utils import AuthenticationMixin, MenuMixin


class RegisterUser(MenuMixin, AuthenticationMixin, CreateView):
    '''
    Registers user in database.
    '''
    form_class = RegisterUserForm
    success_url = reverse_lazy('authentication')
    template_name = 'authorization/user_registration_form.html'
    context_object_name = 'reg_form'


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''
        Supplements context dictionary with "title" attribute.
        '''
        main_context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_data(title = "Sign in")
        return main_context | mixin_context
        
    
    def form_valid(self, form: RegisterUserForm) -> HttpResponseRedirect:
        '''
        Saves new user in database,
        redirects to authentication form.
        '''
        form.save(commit = True)
        return super().form_valid(form = form)
    


class LoginUser(MenuMixin, AuthenticationMixin, LoginView):
    '''
    Authenticates user with database.
    '''
    template_name = 'authorization/user_authentication_form.html'
    form_class = LoginUserForm


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''
        Supplements context dictionary with "title" attribute.
        '''
        main_context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_data(title = "Sign up")
        return main_context | mixin_context

    def form_valid(self, form: LoginUserForm) -> HttpResponseRedirect:
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return HttpResponseRedirect(
            reverse_lazy(
                'profile:profile_page_with_period',
                args = [self.request.user.uuid, settings.SORT_TASKS_TD]
            )
        )


def logout_view(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('authentication'))