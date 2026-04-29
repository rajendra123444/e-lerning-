from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('api/subjects/<str:branch_code>/<int:semester_num>/', views.get_subjects_with_pdfs, name='get_subjects'),
]