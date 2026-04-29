from django.contrib import admin
from .models import Branch, Semester, Subject, UnitPDF

class UnitPDFInline(admin.TabularInline):
    model = UnitPDF
    extra = 1

class SubjectAdmin(admin.ModelAdmin):
    inlines = [UnitPDFInline]
    list_display = ['name', 'semester']
    list_filter = ['semester__branch', 'semester__semester_number']

class SemesterAdmin(admin.ModelAdmin):
    list_display = ['branch', 'semester_number']
    list_filter = ['branch']

admin.site.register(Branch)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(UnitPDF)