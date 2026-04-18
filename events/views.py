from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Event

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin, login_url='/login/')
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/list.html', {'events': events})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def event_add(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date', '')

        if not all([title, description, date]):
            messages.error(request, 'All fields are required.')
        else:
            Event.objects.create(title=title, description=description, date=date)
            messages.success(request, f'Event "{title}" created!')
            return redirect('event_list')

    return render(request, 'events/form.html')

@login_required
@user_passes_test(is_admin, login_url='/login/')
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date', '')

        if not all([title, description, date]):
            messages.error(request, 'All fields are required.')
        else:
            event.title = title
            event.description = description
            event.date = date
            event.save()
            messages.success(request, f'Event "{title}" updated!')
            return redirect('event_list')

    return render(request, 'events/form.html', {'event': event})

@login_required
@user_passes_test(is_admin, login_url='/login/')
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" deleted.')
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'event': event})
