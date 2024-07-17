from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
       super(RegisterUserForm, self).__init__(*args, **kwargs)
       self.fields['username'].label = 'Username'
       self.fields['password1'].label = 'Password'
       self.fields['password2'].label = 'Confirm Password'