from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_login_page),
    path('send-data/',views.get_login_data),
    path('forgot-password/', views.render_forgot_password_page),
    path('forgot-password-send-info/', views.fp_get_creds)
]