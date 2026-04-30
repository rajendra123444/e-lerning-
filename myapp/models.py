from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone





#################################
class Branch(models.Model):
    BRANCH_CHOICES = [
        ('CS', 'Computer Science'),
        ('ME', 'Mechanical Engineering'),
        ('Civil', 'Civil Engineering'),
        ('ET', 'Electronics Engineering'),
    ]
    code = models.CharField(max_length=10, choices=BRANCH_CHOICES, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Semester(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='semesters')
    semester_number = models.IntegerField()

    class Meta:
        unique_together = ('branch', 'semester_number')

    def __str__(self):
        return f"{self.branch.name} - Sem {self.semester_number}"

class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ('semester', 'name')

    def __str__(self):
        return self.name

class UnitPDF(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='units')
    unit_number = models.IntegerField()
    title = models.CharField(max_length=200, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/')

    class Meta:
        unique_together = ('subject', 'unit_number')

    def __str__(self):
        return f"{self.subject.name} - Unit {self.unit_number}"
    
    # ========== NEW MODELS FOR USER NOTES ==========

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"

class UserNote(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to='notes/covers/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='notes/pdfs/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.uploaded_by.username}"

    @property
    def uploaded_by_name(self):
        if self.uploaded_by.get_full_name():
            return self.uploaded_by.get_full_name()
        return self.uploaded_by.username