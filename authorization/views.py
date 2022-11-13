from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import RegisterUserForm


# Create your views here.
def register_user(request):
    '''
    Returns empty registration form or
    registers user in database.
    '''
    reg_form = RegisterUserForm(request.POST or None)
    if reg_form.is_valid():
        reg_form.save(commit = True)
        return redirect('login')
    return render(request, 'registration/user_registration_form.html', context = {'reg_form': reg_form, 'title': 'Sign up'})

def login_user(request):
    return HttpResponse('Authenticate user')