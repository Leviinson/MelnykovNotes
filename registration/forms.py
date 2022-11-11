from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError

from django import forms


from typing import Any
from typing import Dict


from .models import CustomUser



class RegisterUserForm(forms.ModelForm):

    email_conf = forms.EmailField(required = True, label = '')
    password_conf = forms.CharField(required = True, widget = forms.PasswordInput(), label = '')

    email_conf.widget.attrs.update({
        'placeholder': 'Repeat email',
        'id': 'usr-mail-repeat'
    })

    password_conf.widget.attrs.update({
        'placeholder': 'Repeat password',
        'id': 'usr-passw-repeat'
    })
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'email_conf', 'password', 'password_conf')
        labels = {
            field: '' for field in fields
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'id': 'usr-name'
            }),

            'email': forms.EmailInput(attrs = {
                'placeholder': 'Email',
                'id': 'usr-mail'
            }),

            'password': forms.PasswordInput(attrs = {
                'placeholder': 'Password',
                'id': 'usr-passw'
            })
        }
        
        

    def clean(self) -> Dict[str, Any]:
        '''Checks the identity of the entered mails and passwords.
        Return`s error text to the form if fields aren`t similar.'''
        cleaned_data = super().clean()
        passwords_and_emails = self._get_email_and_password_from_form(cleaned_data = cleaned_data)

        #equivalent for: '' in passwords_and_emails.values() or not Nont in password_and_emails.values()
        if not any(x in ('', None) for x in passwords_and_emails.values()): 
            
            if passwords_and_emails['email'] != passwords_and_emails['email_conf']:
                self.add_error('email_conf', ValidationError('Emails weren`t similar'))
            
            if passwords_and_emails['password'] != passwords_and_emails['password_conf']:
                self.add_error('password_conf', ValidationError('Passwords weren`t similar'))
                
        return cleaned_data


    def _get_email_and_password_from_form(self, cleaned_data: dict) -> Dict[str, str]:
        '''Returns dict with values from form fields:
            email, email_conf, password, password_conf.'''
        result = {}
        result['email'] = cleaned_data.get('email')
        result['email_conf'] = cleaned_data.get('email_conf')
        result['password'] = cleaned_data.get('password')
        result['password_conf'] = cleaned_data.get('password_conf')
        return result

    
    def save(self, commit = False):
        user: CustomUser  = super().save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
