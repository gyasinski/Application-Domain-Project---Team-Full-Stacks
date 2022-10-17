from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_login_page),
    path('send-data/',views.login_user),
    path('forgot-password/', views.render_forgot_password_page),
    path('forgot-password-send-info/', views.fp_get_creds),
    path('set-password/', views.render_setpass_page),
    path('administrator/', views.render_admin_page),
    path('administrator/create_user/', views.render_create_page),
    path('administrator/view_expired_passwords/', views.render_expired_passwords_page),
    path('administrator/unapproved_users/', views.render_unapproved_users_page),
    path('administrator/unapproved_users/approve_signal/', views.approved_user),
    path('administrator/unapproved_users/reject_signal/', views.reject_user),
    path('administrator/view_all_users/', views.render_viewusers_page),
    path('administrator/edit_user/', views.render_edituser_page),
    path('administrator/activate_user/<str:pk>/', views.toggle_active_status),
    path('administrator/suspend_user/', views.render_suspenduser_page),
    path('administrator/email_user/', views.render_emailuser_page),
    path('administrator/logout_user/', views.logout_user),
    path('new_user_request/', views.render_create_page),
    path('new_user_request/submit/', views.submit_request_for_new_account),
    path('accountant/', views.render_accountant_page),
    path('manager/', views.render_manager_page),
    path('view_accounts/', views.render_viewaccounts_page),

]