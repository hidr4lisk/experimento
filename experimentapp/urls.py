from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-agent/', views.add_agent, name='add_agent'),
    path('edit-agent/<int:agent_id>/', views.edit_agent, name='edit_agent'),
    path('delete-agent/<int:agent_id>/', views.delete_agent, name='delete_agent'),
    path('add-record/', views.add_record, name='add_record'),
    path('edit-record/<int:record_id>/', views.edit_record, name='edit_record'),
    path('delete-record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('agent/<int:agent_id>/calendar/', views.agent_calendar, name='agent_calendar'),
    path('agent/<int:agent_id>/calendar-data/', views.agent_calendar_data, name='agent_calendar_data'),
    path('debug-db/', views.debug_db, name='debug_db'),
]
