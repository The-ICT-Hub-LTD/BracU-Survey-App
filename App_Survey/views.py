from django.shortcuts import render, get_object_or_404, redirect
from .models import Complain
from .forms import ComplainForm, ResolveForm
from django.contrib.admin.views.decorators import staff_member_required

# For students to submit complaints

def submit_complain(request):
    if request.method == 'POST':
        form = ComplainForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('complain_success')
    else:
        form = ComplainForm()
    return render(request, 'submit_complain.html', {'form': form})

# For admins to resolve complaints
@staff_member_required
def resolve_complain(request, complain_id):
    complain = get_object_or_404(Complain, id=complain_id)
    if request.method == 'POST':
        form = ResolveForm(request.POST, request.FILES, instance=complain)
        if form.is_valid():
            complain.is_resolved = True
            form.save()
            return redirect('admin_complain_list')
    else:
        form = ResolveForm(instance=complain)
    return render(request, 'resolve_complain.html', {'form': form, 'complain': complain})

# For students to search resolved complaints by student ID
def search_resolved_complain(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student_id = request.GET.get('student_id')
        complaints = Complain.objects.filter(student_id=student_id, is_resolved=True)
        return render(request, 'resolved_complaints.html', {'complaints': complaints})
    return render(request, 'resolved_complaints.html')

# Success page after submitting a complaint
def complain_success(request):
    return render(request, 'complain_success.html')
