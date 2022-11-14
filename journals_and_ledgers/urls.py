from django.urls import path
from . import views




urlpatterns = [

    path('journal_entry/', views.render_journal_entry_page),
    path('manager/unapproved_entries/', views.render_unapproved_entries_page), #Review because of manager bit
    path('new_journal_entry_request/submit/', views.submit_request_for_new_journal_entry),
    path('new_journal_entry_request/approve/', views.commit_journal_entry_approval),
    path('new_journal_entry_request/reject/', views.reject_journal_entry),
    path('new_journal_entry_request/save_reject_id/', views.save_rejected_journal_entry_id),
    path('manager/rejected_journal_entry/', views.render_rejected_entries_page),
    path('manager/approved_journal_entry/', views.render_approved_entries_page),
    path('manager/journal_entry_results', views.search_journals_page, name='search_journals'),
]