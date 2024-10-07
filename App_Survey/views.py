from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Complain, Profile, UserProfile
from .forms import ComplainForm, ResolveForm, FeedbackForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import AdminLoginForm, UserProfileCreationForm, ProfileForm
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
import csv
from django.http import HttpResponse
from django.db.models import Count
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from openpyxl import Workbook
from Core.settings import DEFAULT_FROM_EMAIL


def home(request):
    return render(request, 'students/home.html')

def submit_complain(request):
    if request.method == 'POST':
        form = ComplainForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form
            complain = form.save(commit=False)
            complain.is_feedback = False
            complain.save()

            # try:
            subject = f"New Feedback From Khabardabar Catering is Submitted by {complain.student_id}"
            message = f"Name: {complain.student_name}\n" \
                    f"ID: {complain.student_id}\n" \
                    f"Complain Category : {complain.category}\n" \
                    f"Invoice Number: {complain.invoice_no}\n" \
                    f"Feedback Details: {complain.problem_details}\n"                              
            recipients = ['testnetworkeverything@gmail.com','shovonmufrid98@gmail.com']
            
            # Send email
            send_mail(
                subject,
                message,
                DEFAULT_FROM_EMAIL,
                recipients,
                fail_silently=False
            )
            # except:
            #     pass

            return JsonResponse({'redirect_url': reverse('App_Survey:submission_complete')})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    
    form = ComplainForm()
    return render(request, 'students/feedback.html', {'form': form})

def submit_suggestion(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.is_feedback = True
            suggestion.save()
            return JsonResponse({'redirect_url': reverse('App_Survey:submission_complete')})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    
    form = FeedbackForm()
    return render(request, 'students/suggestion.html', {'form': form})


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


def submission_complete(request):
    return render(request, 'students/submission_complete.html')



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
    total_complain = Complain.objects.filter(is_feedback=False).count()
    total_feedback = Complain.objects.filter(is_feedback=True).count()
    total_complaints = total_complain + total_feedback
    current_user_email = request.user.email

    category_status_counts = {
        'Foreign_Material': 0,
        'Personal_Hygiene': 0,
        'Food_Quality': 0,
        'Others': 0
    }
    category_counts = Complain.objects.values('category').annotate(count=Count('category'))

    for category in category_counts:
        category_name = category['category']
        if category_name:  # Check if category is not None
            category_name = category_name.replace(' ', '_')
            if category_name in category_status_counts:
                category_status_counts[category_name] = category['count']


    context = {
        'total_active_profiles': total_active_profiles,
        'total_resolved_complaints': total_resolved_complaints,
        'total_unresolved_complaints': total_unresolved_complaints,
        'total_complaints': total_complaints,
        'current_user_email': current_user_email,  
        'category_status_counts': category_status_counts,
        'total_complain': total_complain,
        'total_feedback': total_feedback,

    }

    return render(request, 'App_Survey/dashboard.html', context)

@login_required
def signout_user(request):
     logout(request)
     messages.warning(request, "You are Logged Out")
     return HttpResponseRedirect(reverse('App_Survey:admin_login'))


@staff_member_required
def complaint_list(request):
    complaints = Complain.objects.filter(is_feedback=False).order_by('-id')

    # Get filter inputs
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    student_id = request.GET.get('student_id')
    category = request.GET.get('category') 

    # Filter by date range
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            complaints = complaints.filter(submitted_at__date__range=[start_date, end_date])
        except ValueError:
            pass 

    # Filter by student_id
    if student_id:
        complaints = complaints.filter(student_id__icontains=student_id)

    # Filter by category
    # if category and category != "None":
    if category:
        complaints = complaints.filter(category=category)

    # Pagination
    paginator = Paginator(complaints, 10) 
    page_number = request.GET.get('page')
    complaints = paginator.get_page(page_number)
    categories = Complain.CategoryStatus.choices 
    return render(request, 'App_Survey/complaint_list.html', {'complaints': complaints, 'categories': categories})

@staff_member_required
def suggestion_list(request):
    suggestions = Complain.objects.filter(is_feedback=True).order_by('-id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    student_id = request.GET.get('student_id')

    # Date range filter
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            suggestions = suggestions.filter(submitted_at__date__range=[start_date, end_date])
        except ValueError:
            pass 

    # Student ID filter
    if student_id:
        suggestions = suggestions.filter(student_id__icontains=student_id)

    # Pagination
    paginator = Paginator(suggestions, 10)
    page_number = request.GET.get('page')
    suggestions = paginator.get_page(page_number)

    categories = Complain.CategoryStatus.choices
    return render(request, 'App_Survey/feedback_list.html', {'complaints': suggestions,})

@staff_member_required
def edit_complain(request, complain_id):
    complain = get_object_or_404(Complain, id=complain_id)
    if request.method == 'POST':
        form = ResolveForm(request.POST, request.FILES, instance=complain)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True}) 
    else:
        form = ResolveForm(instance=complain)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('App_Survey/complain_edit_modal.html', {'form': form, 'complain': complain}, request=request)
        return JsonResponse({'html': html}) 

    return render(request, 'App_Survey/complain_edit.html', {'form': form, 'complain': complain})

@staff_member_required
def resolved_feedback_list(request):
    complaint = Complain.objects.filter(is_resolved=True).order_by('-id')
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


# ############## Profile ###################

def register_user_profile(request):
    if request.method == 'POST':
        user_form = UserProfileCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Create and save the UserProfile
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            # Get the automatically created Profile and update it with form data
            profile = user.profile  # This profile is created by the signal
            profile_form = ProfileForm(request.POST, instance=profile)
            
            if profile_form.is_valid():
                profile_form.save()

            messages.success(request, "User profile created successfully!")
            # return redirect('App_Survey:view_profile', user_id=user.id)
            return redirect('App_Survey:user_profile_list')

    else:
        user_form = UserProfileCreationForm()
        profile_form = ProfileForm()

    return render(request, 'profile/create_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# View a specific UserProfile and Profile
@login_required
def view_profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    profile = get_object_or_404(Profile, user=user_profile)

    return render(request, 'profile/view_profile.html', {
        'user_profile': user_profile,
        'profile': profile
    })

# Update Profile
@login_required
def update_profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    profile = user_profile.profile

    if request.method == 'POST':
        user_form = UserProfileCreationForm(request.POST, instance=user_profile)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('App_Survey:view_profile', user_id=user_profile.id)

    else:
        user_form = UserProfileCreationForm(instance=user_profile)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

def user_profile_list(request):
    user_profiles = UserProfile.objects.all()
    return render(request, 'profile/profile_list.html', {'user_profiles': user_profiles})

# Download CSV


@staff_member_required
def export_complaints_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="complaints.csv"'
    writer = csv.writer(response)
    writer.writerow(['SL', 'Name', 'UID', 'Category', 'Feedback', 'Status', 'Issued'])

    # Retrieve date range from the request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter complaints by date range if provided
    complaints = Complain.objects.filter(is_feedback=False).order_by('-id')
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            complaints = complaints.filter(submitted_at__date__range=[start_date, end_date])
        except ValueError:
            pass

    # Write the data rows
    for idx, complain in enumerate(complaints, start=1):
        writer.writerow([
            idx,
            complain.student_name,
            complain.student_id,
            complain.category,
            complain.problem_details,
            complain.feedback_status,
            complain.submitted_at
        ])

    return response

@staff_member_required
def export_solution_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="solution.csv"'
    writer = csv.writer(response)
    writer.writerow(['SL', 'Name', 'UID', 'Category', 'Feedback', 'Status', 'Issued', 'Solution', 'Resolved Date'])

    # Get the complaints data
    complaints = Complain.objects.filter(is_resolved=True).order_by('-resolved_at')

    # Write the data rows
    for idx, complain in enumerate(complaints, start=1):
        writer.writerow([
            idx,
            complain.student_name,
            complain.student_id,
            complain.category,
            complain.problem_details,
            # complain.complain_image.url if complain.complain_image else 'No image',
            complain.feedback_status,
            complain.submitted_at,
            complain.solution_details,
            complain.resolved_at,
        ])

    return response

@staff_member_required
def export_feedback_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback.csv"'
    writer = csv.writer(response)
    writer.writerow(['SL', 'Name', 'UID', 'Feedback', 'Status', 'Issued', 'Solution', 'Resolved Date'])

    # Get the complaints data
    complaints = Complain.objects.filter(is_feedback=True).order_by('-id')

    # Write the data rows
    for idx, complain in enumerate(complaints, start=1):
        writer.writerow([
            idx,
            complain.student_name,
            complain.student_id,
            complain.problem_details,
            complain.feedback_status,
            complain.submitted_at,
            complain.solution_details,
            complain.resolved_at,
        ])

    return response


@staff_member_required
def export_complaints_pdf(request):
    # Create a HttpResponse object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="complaints.pdf"'

    # Create a PDF object using ReportLab
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Complaints Report")

    # Set initial y-position for the table
    y = height - 80
    p.setFont("Helvetica", 12)

    # Get complaints data
    complaints = Complain.objects.all().order_by('-id')

    # Add table headers
    headers = ['SL', 'Name', 'UID', 'Category', 'Feedback', 'Status', 'Issued']
    p.drawString(30, y, ' | '.join(headers))

    y -= 20

    # Add data rows
    for idx, complain in enumerate(complaints, start=1):
        row = f"{idx} | {complain.student_name} | {complain.student_id} | {complain.category} | {complain.problem_details} | {complain.feedback_status} | {complain.submitted_at}"
        p.drawString(30, y, row)
        y -= 20
        if y < 40:  # Create a new page if space is running out
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()

    return response