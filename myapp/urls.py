
from django.urls import path
from . import views
'''
urlpatterns = [
    # Existing APIs
    path('', views.index, name='home'),
    path('api/subjects/<str:branch_code>/<int:semester_num>/', views.get_subjects_with_pdfs, name='get_subjects'),
    path('api/student-notes/', views.api_student_notes, name='api_student_notes'),
    
    # NEW AUTH URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # NEW NOTES URLs
    path('notes/', views.notes_home, name='notes_home'),
    path('notes/upload/', views.upload_note_view, name='upload_note'),
    path('notes/my-notes/', views.my_notes_view, name='my_notes'),
    path('api/get-subjects/', views.get_subjects_ajax, name='get_subjects_ajax'),
]'''
#########################
from django.urls import path
from . import views

urlpatterns = [
    # Page views
    path('', views.index, name='index'),
    
    # API endpoints
    path('api/check-auth/', views.api_check_auth, name='api_check_auth'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),

    path('api/subjects/<str:branch_code>/<int:semester_num>/', views.get_subjects_with_pdfs, name='get_subjects'),
    path('api/student-notes/', views.api_student_notes, name='api_student_notes'),
    path('api/upload-note/', views.api_upload_note, name='api_upload_note'),
    path('api/my-notes/', views.api_my_notes, name='api_my_notes'),
   # path('api/delete-note/<int:note_id>/', views.api_delete_note, name='api_delete_note'),
]

