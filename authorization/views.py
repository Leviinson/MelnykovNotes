from typing import (
                    Any,
                    Dict
                   )
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView

from django.urls import reverse, reverse_lazy


from .forms import (
                    RegisterUserForm,
                    LoginUserForm
                   )
from .utils import MenuMixin

app_name = 'auth'
class RegisterUser(CreateView, MenuMixin):
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

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('userprofile:profile_page'))
        return super().get(*args, **kwargs)
        
        
    
    def form_valid(self, form: RegisterUserForm):
        '''
        Saves new user in database,
        redirects to authentication form.
        '''
        form.save(commit = True)
        return redirect('authentication')
    


class LoginUser(LoginView, MenuMixin):
    '''
    Authenticates user with database.
    '''
    template_name = 'authorization/user_authentication_form.html'
    form_class = LoginUserForm
    next_page = 'userprofile:profile_page'


    def get(self, *args, **kwargs):
        '''
        Redirects the user to their profile if they are authenticated,
        otherwise returns the standard behavior of the LoginView class's get method. 
        '''
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('userprofile:profile_page'))
        return super().get(*args, **kwargs)


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''
        Supplements context dictionary with "title" attribute.
        '''
        main_context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_data(title = "Sign up")
        return main_context | mixin_context