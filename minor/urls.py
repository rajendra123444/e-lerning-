"""
URL configuration for minor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for minor project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [


    # Admin
    path('admin/', admin.site.urls),

    # Authentication (login, logout, register)
    path('accounts/', include('accounts.urls')),

    # Optional combined auth page (template may not exist)
    path('auth/', TemplateView.as_view(template_name='registration/common_auth.html'), name='common_auth'),




    # Main pages – all with proper names
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('notes/', TemplateView.as_view(template_name='notes.html'), name='notes'),
    path('syllabus/', TemplateView.as_view(template_name='syllabus.html'), name='syllabus'),
    path('books/', TemplateView.as_view(template_name='books.html'), name='books'),
    path('pyq/', TemplateView.as_view(template_name='pyq.html'), name='pyq'),
    path('doubts/', TemplateView.as_view(template_name='doubts.html'), name='doubts'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),

    # Search (template already has JS-based ?q= searching)
    path('search/', TemplateView.as_view(template_name='search.html'), name='search'),

    # Optional: allow direct .html access (for compatibility)
    path('index.html', TemplateView.as_view(template_name='index.html')),
    path('notes.html', TemplateView.as_view(template_name='notes.html')),
    path('syllabus.html', TemplateView.as_view(template_name='syllabus.html')),
    path('books.html', TemplateView.as_view(template_name='books.html')),
    path('pyq.html', TemplateView.as_view(template_name='pyq.html')),
    path('doubts.html', TemplateView.as_view(template_name='doubts.html')),
    path('profile.html', TemplateView.as_view(template_name='profile.html')),

    # API endpoints (must be defined in api/urls.py)
    path('api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    