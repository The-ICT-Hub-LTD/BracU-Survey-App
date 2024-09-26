from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Complain
from .forms import ComplainForm, ResolveForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import AdminLoginForm
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

def home(request):
    return render(request, 'students/home.html')

def submit_complain(request):
    if request.method == 'POST':
        form = ComplainForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = ComplainForm()
    return render(request, 'students/submit_complain.html', {'form': form})

# For admins to resolve complaints
@staff_member_required
def resolve_complain(request, complain_id):
    complain = get_object_or_404(Complain, id=complain_id)
    if request.method == 'POST':
        form = ResolveForm(request.POST, request.FILES, instance=complain)
        if form.is_valid():
            complain.is_resolved = True
            form.save()
            return redirect('App_Survey:admin_complain_list')
    else:
        form = ResolveForm(instance=complain)
    return render(request, 'students/resolve_complain.html', {'form': form, 'complain': complain})

# For students to search resolved complaints by student ID
# def search_resolved_complain(request):
#     if request.method == 'GET' and 'student_id' in request.GET:
#         student_id = request.GET.get('student_id')
#         complaints = Complain.objects.filter(student_id=student_id, is_resolved=True)
#         return render(request, 'students/resolved_complaints.html', {'complaints': complaints})
#     return render(request, 'students/resolved_complaints.html')

def search_resolved_complain(request):
    student_id = request.GET.get('student_id', '')
    complaints = Complain.objects.filter(student_id=student_id) if student_id else []
    return render(request, 'students/resolved_complaints.html', {'complaints': complaints, 'student_id': student_id})

def complain_success(request):
    return render(request, 'students/complain_success.html')



def is_admin(user):
    return user.is_staff

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('App_Survey:admin_dashboard')  

    if request.method == 'POST':
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None and user.is_staff: 
                login(request, user)
                return redirect('App_Survey:admin_dashboard')  
            else:
                messages.error(request, "Invalid credentials or you are not authorized.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AdminLoginForm()

    return render(request, 'App_Survey/signin.html', {'form': form})


@user_passes_test(is_admin) 
def admin_dashboard_view(request):
    return render(request, 'App_Survey/dashboard.html')

@login_required
def signout_user(request):
     logout(request)
     messages.warning(request, "You are Logged Out")
     return HttpResponseRedirect(reverse('App_Survey:admin_login'))


@staff_member_required
def complaint_list(request):
    complaints = Complain.objects.all()
    return render(request, 'App_Survey/complaint_list.html', {'complaints': complaints})

@staff_member_required
def edit_complain(request, complain_id):
    complain = get_object_or_404(Complain, id=complain_id)
    if request.method == 'POST':
        form = ResolveForm(request.POST, request.FILES, instance=complain)
        if form.is_valid():
            form.save()
            # messages.success(request, "Complain updated successfully.")
            return redirect('App_Survey:complaint_list')
    else:
        form = ResolveForm(instance=complain)

    # Updated check for AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('App_Survey/complain_edit_modal.html', {'form': form, 'complain': complain}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'App_Survey/complain_edit.html', {'form': form, 'complain': complain})