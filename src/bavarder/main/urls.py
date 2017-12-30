from django.urls import path
from .views import default_template, chat_view, login_view, signup_view, message_send

urlpatterns = [
    path('', default_template),
    path('chat/', chat_view),
    path('login/', login_view),
    path('signup/', signup_view),
    path('send/', message_send)
]
