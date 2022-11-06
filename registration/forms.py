from django.contrib.auth.forms import UserCreationForm

class RegisterUserFrom(UserCreationForm):
    class Meta:
        fields = ('email', 'username')