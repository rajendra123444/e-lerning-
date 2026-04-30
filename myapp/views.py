from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import Branch, Subject, UnitPDF, UserNote
import json
from datetime import datetime

# ========== PAGE VIEWS ==========

def index(request):
    """Main page"""
    return render(request, 'index.html')

# ========== AUTH API (WITH CSRF EXEMPT FOR TESTING) ==========

@csrf_exempt
def api_register(request):
    """Handle user registration"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            
            # Check if user exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'Username already exists'})
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email already registered'})
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Login the user
            login(request, user)
            
            return JsonResponse({
                'success': True, 
                'user': username, 
                'full_name': user.get_full_name()
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def api_login(request):
    """Handle user login"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True, 
                    'user': username, 
                    'full_name': user.get_full_name()
                })
            else:
                return JsonResponse({'success': False, 'error': 'Invalid username or password'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def api_logout(request):
    """Handle user logout"""
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def api_check_auth(request):
    """Check if user is authenticated"""
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'username': request.user.username,
            'full_name': request.user.get_full_name()
        })
    return JsonResponse({'authenticated': False})

# ========== NOTES API ==========

def api_student_notes(request):
    """Get all student notes"""
    try:
        notes = UserNote.objects.all().order_by('-created_at')
        data = []
        for note in notes:
            data.append({
                'id': note.id,
                'title': note.title,
                'description': note.description or '',
                'cover_photo_url': note.cover_photo.url if note.cover_photo else None,
                'pdf_url': note.pdf_file.url,
                'uploaded_by_name': note.uploaded_by_name,
                'uploaded_by_username': note.uploaded_by.username,
                'created_date': note.created_at.strftime('%d %b %Y'),
            })
        return JsonResponse({'notes': data})
    except Exception as e:
        return JsonResponse({'notes': [], 'error': str(e)})

@login_required
@csrf_exempt
def api_upload_note(request):
    """Upload a new note"""
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            pdf_file = request.FILES.get('pdf_file')
            cover_photo = request.FILES.get('cover_photo')
            
            if not title:
                return JsonResponse({'success': False, 'error': 'Title is required'})
            
            if not pdf_file:
                return JsonResponse({'success': False, 'error': 'PDF file is required'})
            
            if not pdf_file.name.endswith('.pdf'):
                return JsonResponse({'success': False, 'error': 'Only PDF files are allowed'})
            
            note = UserNote.objects.create(
                title=title,
                description=description,
                pdf_file=pdf_file,
                cover_photo=cover_photo,
                uploaded_by=request.user
            )
            
            return JsonResponse({
                'success': True, 
                'note': {
                    'id': note.id,
                    'title': note.title,
                    'description': note.description,
                    'pdf_url': note.pdf_file.url,
                    'cover_photo_url': note.cover_photo.url if note.cover_photo else None,
                    'uploaded_by_name': note.uploaded_by_name,
                    'created_date': note.created_at.strftime('%d %b %Y'),
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def api_my_notes(request):
    """Get current user's notes"""
    try:
        notes = UserNote.objects.filter(uploaded_by=request.user).order_by('-created_at')
        data = []
        for note in notes:
            data.append({
                'id': note.id,
                'title': note.title,
                'description': note.description or '',
                'cover_photo_url': note.cover_photo.url if note.cover_photo else None,
                'pdf_url': note.pdf_file.url,
                'created_date': note.created_at.strftime('%d %b %Y'),
            })
        return JsonResponse({'notes': data})
    except Exception as e:
        return JsonResponse({'notes': [], 'error': str(e)})

# ========== SUBJECT API ==========

def get_subjects_with_pdfs(request, branch_code, semester_num):
    """Get subjects and PDFs for a branch and semester"""
    try:
        branch = Branch.objects.get(code=branch_code)
        semester = branch.semesters.get(semester_number=semester_num)
        subjects = semester.subjects.all()
        
        data = []
        for subject in subjects:
            units = subject.units.all().order_by('unit_number')
            unit_data = [{
                'unit_number': u.unit_number,
                'title': u.title or f"Unit {u.unit_number}",
                'pdf_url': u.pdf_file.url
            } for u in units]
            
            data.append({
                'subject_name': subject.name,
                'units': unit_data
            })
        return JsonResponse({'subjects': data})
    except Exception as e:
        return JsonResponse({'subjects': [], 'error': str(e)})