from django.urls import path
from . import views




urlpatterns = [

    path('journal_entry/', views.render_journal_entry_page),
    path('manager/unapproved_entries/', views.render_unapproved_entries_page),
    path('new_journal_entry_request/submit/', views.submit_request_for_new_journal_entry),
]