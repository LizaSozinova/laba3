from django.urls import path
from calculator import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница с калькулятором
]
