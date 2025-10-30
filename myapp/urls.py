from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('welcome/',views.welcome_view, name='welcome'),
    path('student/', views.StudentView, name='student'),
    path('books/', views.books_view, name='books'),
    path('register/', views.register_books_view, name='register'),
    path('stud_add/', views.stud_add, name='stud_add'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),

    #Logged In
    path('Logged/', views.Logged_view, name='Logged'),
    
    #admin
    path('Admin_list/', views.Admin_view, name='Admin_list'),
    path('Admin_reg/', views.Admin_reg_view, name='Admin_reg'),
    path('admin_status_change/<int:user_id>/<str:action>/', views.admin_status_change, name='admin_status_change'),
    path('admin_edit/<int:user_id>/', views.edit_admin, name='admin_edit'),
    path('admin_delete/<int:user_id>/', views.admin_delete, name='admin_delete'),
    path('admin_password/', views.admin_password, name='admin_password'),
    
    #quotes
    path('quotes_new/', views.quotes_new, name='quotes_new'),
    path('quotes_view/', views.quotes_view, name='quotes_view'),
    path('modify_quotes/<int:quote_id>/', views.modify_quotes, name='modify_quotes'),
    path('delete_quotes/<int:id>/', views.delete_quotes, name='delete_quotes'),

    #Sabhasad
    path('Sabhasad/', views.Sabhasad_view, name='Sabhasad'),
    path('Sabhasad_reg/', views.Sabhasad_reg, name='Sabhasad_reg'),
    path('delete_Sabhasad/<int:id>/', views.delete_Sabhasad, name='delete_Sabhasad'),
    path('sabhasad_modify/<int:id>/', views.sabhasad_modify, name='sabhasad_modify'),
    path('best_wish/', views.best_wish_view, name='best_wish'),
    path('send_single_message/<int:sabhasad_id>/', views.send_single_message, name='send_single_message'),
    path('store_message/', views.store_message, name='store_message'),
    path('sabhasad_filter/', views.sabhasad_filter, name='sabhasad_filter'),

    #Event
    path('Event/', views.Event_view, name='Event'),
    path('Birth_view/', views.Birth_view, name='Birth_view'),
    
    #IDcard
    path('card/', views.card_view, name='card'),
    path('fetch_by_id/', views.fetch_by_id, name='fetch_by_id'),
    
    
  
]
