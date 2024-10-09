from django.urls import path, include
from . import views

app_name = 'App_Survey'

urlpatterns = [
    path('', views.home, name='home'),
    path('submit_complain/', views.submit_complain, name='submit_complain'),
    path('submit_feedback/', views.submit_suggestion, name='submit_suggestion'),
    path('resolve-complain/<int:complain_id>/', views.resolve_complain, name='resolve_complain'),
    path('search-resolved/', views.search_resolved_complain, name='search_resolved_complain'),
    path('submission-complete/', views.submission_complete, name='submission_complete'),
    path('complain-submission/', views.complain_submission, name='complain_submission'),
    # path('survey/admin/', views.signin_user, name='signin'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('signout/', views.signout_user, name='signout'),
    path('complains/', views.complaint_list, name='complaint_list'),
    path('feedbacks/', views.suggestion_list, name='suggestion_list'),
    path('complaints/edit/<int:complain_id>/', views.edit_complain, name='edit_complain'),
    path('resolved/', views.resolved_feedback_list, name='resolved'),
    path('complain/<int:pk>/details/', views.complain_details, name='complain_details'),

    path('createuser/', views.register_user_profile, name='register_profile'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('profile/update/<int:user_id>/', views.update_profile, name='update_profile'),
    path('userprofiles/', views.user_profile_list, name='user_profile_list'),
    path('complaints/export/csv/', views.export_complaints_csv, name='export_complaints_csv'),
    path('feedbacks/export/csv/', views.export_feedback_csv, name='export_feedback_csv'),
    path('solutions/export/csv/', views.export_solution_csv, name='export_solution_csv'),
    path('complaints/export/pdf/', views.export_complaints_pdf, name='export_complaints_pdf'),
    # path('accounts/', include('allauth.urls')),
    
]
