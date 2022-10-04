from django.urls import path
from . import views




urlpatterns = [
    path('', views.render_create_chart_accts_page),
    path('delete_page/', views.render_delete_chart_accounts),
    path('post_account/', views.create_chart_of_accounts),
    path('delete_page/delete/', views.delete_chart_of_accounts),
]


