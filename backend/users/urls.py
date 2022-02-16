from django.conf import settings
from django.urls import path, include

from . import views

urlpatterns = [
    path('create/pre_register', views.CreatePreRegister.as_view()),
]
