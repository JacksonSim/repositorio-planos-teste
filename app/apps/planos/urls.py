# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cidade=<slug:slug>/', views.planos_by_city, name='planos_by_city'),
    # ... outras URLs ...
]