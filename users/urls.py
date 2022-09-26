from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_login_page),
    path('send-data/',views.get_login_data),
    path('create/', views.render_create_page),
    path('forgot-password/', views.render_forgot_password_page),
    path('forgot-password-send-info/', views.fp_get_creds),
    path('set-password/', views.render_setpass_page),

    path('admin/', views.render_admin_page),
    path('admin/view_all_users', views.render_viewusers_page),

    path('accountant/', views.render_accountant_page),

    path('manager/', views.render_manager_page),
]