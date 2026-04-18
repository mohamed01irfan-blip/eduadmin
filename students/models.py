from django.db import models

DEPARTMENT_CHOICES = [
    ('CS', 'Computer Science'),
    ('EE', 'Electrical Engineering'),
    ('ME', 'Mechanical Engineering'),
    ('CE', 'Civil Engineering'),
    ('BIO', 'Biotechnology'),
    ('MBA', 'Business Administration'),
    ('ARTS', 'Arts & Humanities'),
    ('MATH', 'Mathematics'),
]

YEAR_CHOICES = [
    (1, '1st Year'),
    (2, '2nd Year'),
    (3, '3rd Year'),
    (4, '4th Year'),
]

class Student(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_department_display()}"

    def get_year_display_label(self):
        labels = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th'}
        return f"{labels.get(self.year, str(self.year))} Year"
