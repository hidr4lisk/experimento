from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ping/', lambda r: HttpResponse("PONG"), name='ping'),
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
    path('trigger-population/', views.trigger_population, name='trigger_population'),
    path('debug-db/', views.debug_db, name='debug_db'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('add-user/', views.add_user, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user_role, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]
