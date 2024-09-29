from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Complain, Profile
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
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
    # user_log = UserLog.objects.filter(user=request.user).order_by('-timestamp')
    # paginator = Paginator(user_log, 10)
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
    total_active_profiles = Profile.objects.filter(user__is_active=True).count()
    total_resolved_complaints = Complain.objects.filter(is_resolved=True).count()
    total_unresolved_complaints = Complain.objects.filter(is_resolved=False).count()
    total_complaints = total_resolved_complaints + total_unresolved_complaints

    context = {
        'total_active_profiles': total_active_profiles,
        'total_resolved_complaints': total_resolved_complaints,
        'total_unresolved_complaints': total_unresolved_complaints,
        'total_complaints': total_complaints,
    }

    return render(request, 'App_Survey/dashboard.html', context)

@login_required
def signout_user(request):
     logout(request)
     messages.warning(request, "You are Logged Out")
     return HttpResponseRedirect(reverse('App_Survey:admin_login'))


@staff_member_required
def complaint_list(request):
    complaint = Complain.objects.all().order_by('-id')
    paginator = Paginator(complaint, 10) 
    page_number = request.GET.get('page')
    complaints = paginator.get_page(page_number)
    return render(request, 'App_Survey/complaint_list.html', {'complaints': complaints})

@staff_member_required
def edit_complain(request, complain_id):
    complain = get_object_or_404(Complain, id=complain_id)
    if request.method == 'POST':
        form = ResolveForm(request.POST, request.FILES, instance=complain)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # Respond with success
    else:
        form = ResolveForm(instance=complain)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('App_Survey/complain_edit_modal.html', {'form': form, 'complain': complain}, request=request)
        return JsonResponse({'html': html})  # Return the modal content

    return render(request, 'App_Survey/complain_edit.html', {'form': form, 'complain': complain})

@staff_member_required
def resolved_feedback_list(request):
    complaint = Complain.objects.filter(is_resolved=True).order_by('-resolved_at')
    paginator = Paginator(complaint, 10) 
    page_number = request.GET.get('page')
    complaints = paginator.get_page(page_number)
    
    return render(request, 'App_Survey/feedback_solved.html', {'complaints': complaints, })


def complain_details(request, pk):
    complain = get_object_or_404(Complain, pk=pk)
    data = {
        'student_name': complain.student_name,
        'student_id': complain.student_id,
        'problem_details': complain.problem_details,
        'complain_image': complain.complain_image.url if complain.complain_image else None,
        'submitted_at': complain.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
    }
    return JsonResponse(data)

# View to get complaint details (AJAX call)
# def get_complain_details(request):
#     if request.method == "GET" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         complain_id = request.GET.get('id')
#         complain = get_object_or_404(Complain, id=complain_id)
#         response_data = {
#             'id': complain.id,
#             'solution_details': complain.solution_details,
#             'feedback_status': complain.feedback_status,
#             'resolved_at': complain.resolved_at.isoformat() if complain.resolved_at else '',
#         }
#         return JsonResponse(response_data)
#     return JsonResponse({'error': 'Invalid request'}, status=400)

# @csrf_exempt
# def update_complain(request):
#     if request.method == "POST":
#         complain_id = request.POST.get('complain_id')
#         complain = get_object_or_404(Complain, id=complain_id)
#         complain.solution_details = request.POST.get('solution_details')
#         complain.feedback_status = request.POST.get('feedback_status')
        
#         resolved_at = request.POST.get('resolved_at')
#         if resolved_at:
#             complain.resolved_at = resolved_at
        
#         if 'resolved_image' in request.FILES:
#             complain.resolved_image = request.FILES['resolved_image']

#         complain.is_resolved = True if complain.feedback_status == 'Solved' else False
#         complain.save()

#         return JsonResponse({'success': True})
    
#     return JsonResponse({'success': False}, status=400)
