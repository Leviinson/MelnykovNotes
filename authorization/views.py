from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import RegisterUserForm


# Create your views here.
def register_user(request):

    if request.method == 'POST':
        dict_form_form = {
            'username': request.POST['username'],
            'email': request.POST['email'],
            'email_conf': request.POST['email_conf'],
            'password': request.POST['password'],
            'password_conf': request.POST['password_conf']
        }
        reg_form = RegisterUserForm(dict_form_form)
        if reg_form.is_valid():
            reg_form.save(commit = True)
            return redirect('login')
    else:
        reg_form = RegisterUserForm()
        
    return render(request, 'registration/user_registration_form.html', context = {'reg_form': reg_form, 'title': 'Sign up'})

def login_user(request):
    return HttpResponse('Authenticate user')