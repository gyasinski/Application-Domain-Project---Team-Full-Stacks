from django.urls import path
from . import views




urlpatterns = [
    path('', views.render_create_chart_accts_page),
    path('view_event_log/',views.render_event_log),
    path('account/<str:acct_id>',views.render_single_account),
    path('account/pdf/<str:acct_id>/',views.render_to_pdf),
    path('delete_page/', views.render_delete_chart_accounts),
    path('post_account/', views.create_chart_of_accounts),
    path('delete_page/delete/', views.delete_chart_of_accounts),
    path('administrator/edit_account/', views.render_edit_chart_accounts),
    path('view_accounts/', views.render_viewaccounts_page),
    path('search/', views.search_account_results, name='search'),
]


