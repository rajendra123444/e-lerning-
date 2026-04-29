from django.shortcuts import render
from django.http import JsonResponse
from .models import Branch, Subject, UnitPDF

def index(request):
    branches = Branch.objects.all()
    return render(request, 'index.html', {'branches': branches})

def get_subjects_with_pdfs(request, branch_code, semester_num):
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
        return JsonResponse({'error': str(e)}, status=400)