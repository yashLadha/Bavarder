from django import forms


class SignUpForm(forms.Form):
    """Model for the singup form"""
    email = forms.EmailField(label='Enter Email')
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Re-Enter Password', widget=forms.PasswordInput())
    name = forms.CharField(label='Enter Name')
    dob = forms.DateField(label='Enter D.O.B.',
                          widget=forms.SelectDateWidget(years=[y for y in range(1930, 2050)]))
    profile_image = forms.ImageField(label='Profile Image', required=True)


class LoginForm(forms.Form):
    """Model for the login form"""
    email = forms.EmailField(label='Enter Email')
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput())


class MessageForm(forms.Form):
    """Model for the message form"""
    message = forms.CharField(label='Message', max_length=1200)
