from django import forms  
from django.contrib.auth.models import User  
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control x1','placeholder':'Username'}),min_length=4, max_length=10)  
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control x2','placeholder':'Email'}))  
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Password'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x4','placeholder':'Confirm password'}), label='Password Confirmation')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control x5','placeholder':'first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control x6','placeholder':'last name'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)           
    
        return self.cleaned_data
    
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("The two password fields didnot match")  
        return password2  

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control x1','placeholder':'Username'}))  
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='Password')

class UserPasswordReset(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='New Password Confirmation')

class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x1','placeholder':'Password'}), label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='New Password Confirmation')
