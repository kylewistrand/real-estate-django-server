from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(label='username', max_length=30, required=True)
    password = forms.CharField(label='password', max_length=30, widget=forms.PasswordInput, required=True)
    passwordConf = forms.CharField(label='passwordConf', max_length=30, widget=forms.PasswordInput ,required=True)
    email = forms.EmailField(label='email', max_length=30, required=True)
    first_name = forms.CharField(label='first_name', max_length=30, required=True)
    last_name = forms.CharField(label="last_name", max_length=30, required=True)

class SigninForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(label='Password', max_length=30, required=True, widget=forms.PasswordInput)
