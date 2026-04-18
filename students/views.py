from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Student, DEPARTMENT_CHOICES, YEAR_CHOICES

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin, login_url='/login/')
def student_list(request):
    search = request.GET.get('search', '')
    dept_filter = request.GET.get('department', '')
    year_filter = request.GET.get('year', '')

    students = Student.objects.all()
    if search:
        students = students.filter(name__icontains=search) | students.filter(email__icontains=search)
    if dept_filter:
        students = students.filter(department=dept_filter)
    if year_filter:
        students = students.filter(year=year_filter)

    context = {
        'students': students,
        'departments': DEPARTMENT_CHOICES,
        'years': YEAR_CHOICES,
        'search': search,
        'dept_filter': dept_filter,
        'year_filter': year_filter,
        'total': students.count(),
    }
    return render(request, 'students/list.html', context)

@login_required
@user_passes_test(is_admin, login_url='/login/')
def student_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        department = request.POST.get('department', '')
        year = request.POST.get('year', '')
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        errors = []
        if not all([name, department, year, email, phone]):
            errors.append('All fields are required.')
        if Student.objects.filter(email=email).exists():
            errors.append('A student with this email already exists.')

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            Student.objects.create(
                name=name, department=department, year=int(year),
                email=email, phone=phone
            )
            messages.success(request, f'Student "{name}" added successfully!')
            return redirect('student_list')

    context = {'departments': DEPARTMENT_CHOICES, 'years': YEAR_CHOICES}
    return render(request, 'students/form.html', context)

@login_required
@user_passes_test(is_admin, login_url='/login/')
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        department = request.POST.get('department', '')
        year = request.POST.get('year', '')
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        errors = []
        if not all([name, department, year, email, phone]):
            errors.append('All fields are required.')
        if Student.objects.filter(email=email).exclude(pk=pk).exists():
            errors.append('Another student with this email already exists.')

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            student.name = name
            student.department = department
            student.year = int(year)
            student.email = email
            student.phone = phone
            student.save()
            messages.success(request, f'Student "{name}" updated successfully!')
            return redirect('student_list')

    context = {
        'student': student,
        'departments': DEPARTMENT_CHOICES,
        'years': YEAR_CHOICES
    }
    return render(request, 'students/form.html', context)

@login_required
@user_passes_test(is_admin, login_url='/login/')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f'Student "{name}" deleted.')
        return redirect('student_list')
    return render(request, 'students/confirm_delete.html', {'student': student})
