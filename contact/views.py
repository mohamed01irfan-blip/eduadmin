from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Message as ContactMessage

def is_admin(user):
    return user.is_staff or user.is_superuser

def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('body', '').strip()

        if not all([name, email, subject, body]):
            messages.error(request, 'All fields are required.')
        else:
            ContactMessage.objects.create(name=name, email=email, subject=subject, body=body)
            messages.success(request, 'Message sent! We will get back to you soon.')
            return redirect('contact')

    return render(request, 'contact/form.html')

@login_required
@user_passes_test(is_admin, login_url='/login/')
def message_list(request):
    msgs = ContactMessage.objects.all()
    unread = ContactMessage.objects.filter(is_read=False).count()
    return render(request, 'contact/list.html', {'messages_list': msgs, 'unread': unread})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = True
    msg.save()
    return render(request, 'contact/detail.html', {'msg': msg})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def message_toggle_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save()
    return redirect('message_list')

@login_required
@user_passes_test(is_admin, login_url='/login/')
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message deleted.')
        return redirect('message_list')
    return render(request, 'contact/confirm_delete.html', {'msg': msg})
