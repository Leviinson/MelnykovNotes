from typing import (
                    Any,
                    Dict
                   )
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import CreateView

from django.urls import reverse_lazy


from .forms import (
                    RegisterUserForm,
                    LoginUserForm
                   )
from .utils import MenuMixin


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

    
    def form_valid(self, form: RegisterUserForm):
        form.save(commit = True)
        return redirect('authentication')


class LoginUser(MenuMixin, LoginView):
    '''
    Authenticates user with database.
    '''
    template_name = 'authorization/user_authentication_form.html'
    form_class = LoginUserForm
    next_page = 'registration'


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''
        Supplements context dictionary with "title" attribute.
        '''
        main_context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_data(title = "Sign up")
        return main_context | mixin_context