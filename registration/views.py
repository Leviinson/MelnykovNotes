from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

# Create your views here.
class RegisterUser(CreateView):
    form_class = UserCreationForm