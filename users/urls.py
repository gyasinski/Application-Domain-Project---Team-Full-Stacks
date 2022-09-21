from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_login_page),
    path('send-data/',views.get_login_data)
]