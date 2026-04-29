from django.db import models

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