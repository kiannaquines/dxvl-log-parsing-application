from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from app.models import DXVLUsers
from django import forms

class RegisterUserForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
       super(RegisterUserForm, self).__init__(*args, **kwargs)
       self.fields['username'].label = 'Username'
       self.fields['password1'].label = 'Password'
       self.fields['password2'].label = 'Confirm Password'

       self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder': 'Username'})
       self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder': 'Password','aria-describedby':'password'})
       self.fields['password2'].widget.attrs.update({'class': 'form-control','placeholder': 'Confirm Password'})

    class Meta:
        model = DXVLUsers
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class EditUserForm(ModelForm):
    def __init__(self,*args,**kwargs):
       super(EditUserForm, self).__init__(*args, **kwargs)
       self.fields['username'].label = 'Username'
       self.fields['first_name'].label = 'First Name'
       self.fields['last_name'].label = 'Last Name'
       self.fields['email'].label = 'Email'
       self.fields['user_address'].label = 'Address'
       self.fields['user_mobile_number'].label = 'Phone Number'
       self.fields['is_active'].label = 'User Status'
       self.fields['is_superuser'].label = 'Superuser Status'
       self.fields['is_staff'].label = 'Staff Status'
       self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder': 'Username'})
       self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder': 'First Name'})
       self.fields['last_name'].widget.attrs.update({'class': 'form-control','placeholder': 'Last Name'})
       self.fields['email'].widget.attrs.update({'class': 'form-control','placeholder': 'Email'})
       self.fields['user_address'].widget.attrs.update({'class': 'form-control','rows':'3','placeholder': 'Address'})
       self.fields['user_mobile_number'].widget.attrs.update({'class': 'form-control','placeholder': 'Phone Number' })
       self.fields['is_active'].widget.attrs.update({'class': 'form-check-input',})
       self.fields['is_superuser'].widget.attrs.update({'class': 'form-check-input'})
       self.fields['is_staff'].widget.attrs.update({'class': 'form-check-input'})


    class Meta:
        model = DXVLUsers
        fields = ['username', 'first_name', 'last_name', 'email','user_address', 'user_mobile_number', 'is_active', 'is_superuser', 'is_staff',]
        exclude = ['password1', 'password2',]
        