from django.urls import path
from . import views




urlpatterns = [
    path('', views.render_create_chart_accts_page),
    path('post_account/', views.create_chart_of_accounts)
]


