from django import forms


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Enter Email')
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Re-Enter Password', widget=forms.PasswordInput())
    name = forms.CharField(label='Enter Name')
    dob = forms.DateField(label='Enter D.O.B.', widget=forms.SelectDateWidget(years=[y for y in range(1930, 2050)]))


class LoginForm(forms.Form):
    email = forms.EmailField(label='Enter Email')
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput())
