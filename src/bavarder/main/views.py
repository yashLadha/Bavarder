import json
import codecs
import base64

from channels import Group
from django.shortcuts import render, redirect, HttpResponse

from .database.connection import MongoConn
from .forms import SignUpForm, LoginForm, MessageForm


def default_template(request):
    """Loads the index template"""
    db_check()
    if request.session.get('member'):
        user_obj = get_user(request)
        print(user_obj['name'])
    return render(request, 'index.html')


def get_user(request):
    email = request.session['member']
    user_obj = MongoConn.get_user(email)
    return user_obj


def db_check():
    """Check for the database instance connection"""
    value = MongoConn.check_database()
    if value:
        print('MongoConn created successfully')
    else:
        print('Unable to create object.')


def chat_view(request):
    """Chat view"""
    db_check()
    if request.session.get('member'):
        chat_form = MessageForm()
        user_obj = get_user(request)
        image = base64.b64encode(MongoConn.get_image(user_obj['image']).read()).decode('utf-8')
        return render(request, 'chat.html', {'message_forum': chat_form,
                'name': user_obj['name'],
                'sender_img': image}
            )
    return redirect("/")


def message_send(request):
    """Send message to the chat"""
    if request.method == 'POST':
        json_data = json.dumps(request.POST)
        json_data = json.loads(json_data)
        Group('chat').send(json_data)
        return HttpResponse(json_data)


def login_view(request):
    """Login View for authenticating user"""
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            print('Valid login form submitted')
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            status, obj = MongoConn.is_user(email, password)
            if status:
                print('User exists.')
                request.session['member'] = obj['email']  # User is added to the session
                return redirect('/')
            else:
                print('Invalid login attempt.')
                login_form = LoginForm()
                return render(request, 'login.html', {'form': login_form, 'status': False})
        else:
            print('Invalid form sent.')
    else:
        db_check()
        login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})


def signup_view(request):
    """Signup view for creating user"""
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST, request.FILES)
        if signup_form.is_valid():
            print('Valid Form Submitted')
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            conf_password = signup_form.cleaned_data['confirm_password']
            profile_image = request.FILES['profile_image']
            if password == conf_password:
                name = signup_form.cleaned_data['name']
                dob = signup_form.cleaned_data['dob']
                result, response = MongoConn.create_user(email, password, name, dob)
                if result and response == 0:
                    status, obj = MongoConn.is_user(email, password)
                    resp = MongoConn.insert_image(profile_image, obj)
                    if resp:
                        print("Profile image updated successfully")
                    request.session['member'] = obj['email']  # User is added to the session
                    return redirect('/')
                else:
                    signup_form = SignUpForm()
                    return render(request, 'signup.html', {
                        'form': signup_form,
                        'response': response
                    })
            return redirect('/')
    else:
        db_check()
        signup_form = SignUpForm()
    return render(request, 'signup.html', {'form': signup_form})
