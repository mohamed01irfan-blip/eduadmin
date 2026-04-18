from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from students.models import Student, DEPARTMENT_CHOICES
from events.models import Event
from contact.models import Message
import json

def is_admin(user):
    return user.is_staff or user.is_superuser

def login_view(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('dashboard')
        return redirect('student_portal')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if is_admin(user):
                return redirect('dashboard')
            return redirect('student_portal')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not all([username, email, password1, password2]):
            messages.error(request, 'All fields are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')
    
    return render(request, 'core/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin, login_url='/login/')
def dashboard_view(request):
    # Stats
    total_students = Student.objects.count()
    total_events = Event.objects.count()
    total_messages = Message.objects.count()
    unread_messages = Message.objects.filter(is_read=False).count()

    # Chart: students by department
    dept_data = Student.objects.values('department').annotate(count=Count('department'))
    dept_labels = [dict(DEPARTMENT_CHOICES).get(d['department'], d['department']) for d in dept_data]
    dept_counts = [d['count'] for d in dept_data]

    # Chart: students by year
    year_data = Student.objects.values('year').annotate(count=Count('year')).order_by('year')
    year_labels = [f"Year {d['year']}" for d in year_data]
    year_counts = [d['count'] for d in year_data]

    # Recent data
    recent_students = Student.objects.order_by('-created_at')[:5]
    recent_events = Event.objects.order_by('-created_at')[:5]
    recent_messages = Message.objects.order_by('-created_at')[:5]

    context = {
        'total_students': total_students,
        'total_events': total_events,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'dept_labels': dept_labels,
        'dept_counts': dept_counts,
        'year_labels': year_labels,
        'year_counts': year_counts,
        'recent_students': recent_students,
        'recent_events': recent_events,
        'recent_messages': recent_messages,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def student_portal_view(request):
    """Simple portal for non-admin users"""
    return render(request, 'core/student_portal.html')
