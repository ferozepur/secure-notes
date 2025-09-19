from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Note
from .forms import NoteForm

@login_required
def dashboard(request):
    notes = Note.objects.filter(owner=request.user)
    return render(request, 'notes/dashboard.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            return redirect('notes:dashboard')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Create'})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.owner != request.user:
        return HttpResponseForbidden("Not allowed")
    return render(request, 'notes/note_detail.html', {'note': note})

@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.owner != request.user:
        return HttpResponseForbidden("Not allowed")
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Update'})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.owner != request.user:
        return HttpResponseForbidden("Not allowed")
    if request.method == 'POST':
        note.delete()
        return redirect('notes:dashboard')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})
