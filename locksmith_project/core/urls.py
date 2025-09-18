from django.urls import path
from . import views

urlpatterns = [
    path('callback/', views.callback_view, name='callback_view'),
]