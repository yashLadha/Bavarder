from django.shortcuts import render, redirect

from .database.connection import MongoConn
from .forms import SignUpForm


def default_template(request):
    # TODO: Add user presence logic
    db_check()
    return render(request, 'index.html')


def db_check():
    value = MongoConn.check_database()
    if value:
        print('MongoConn created successfully')
    else:
        print('Unable to create object.')


def chat_view(request):
    db_check()
    return render(request, 'chat.html')


def login_view(request):
    # TODO: Add Login Logic
    db_check()
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            print('Valid Form Submitted')
            # TODO: Add user creation logic
            return redirect('/')
    else:
        db_check()
        signup_form = SignUpForm()
    return render(request, 'signup.html', {'form': signup_form})
