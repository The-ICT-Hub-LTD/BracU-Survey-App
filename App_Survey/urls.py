from django.urls import path
from . import views

app_name = 'App_Survey'

urlpatterns = [
    path('', views.home, name='home'),
    path('submit-feedbacks/', views.submit_complain, name='submit_complain'),
    path('resolve-complain/<int:complain_id>/', views.resolve_complain, name='resolve_complain'),
    path('search-resolved/', views.search_resolved_complain, name='search_resolved_complain'),
    path('complain-success/', views.complain_success, name='complain_success'),
    # path('survey/admin/', views.signin_user, name='signin'),
    path('admin-login/', views.admin_login_view, name='admin_login'),  # Admin login URL
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('signout/', views.signout_user, name='signout'),
    path('feedbacks/', views.complaint_list, name='complaint_list'),
    path('complaints/edit/<int:complain_id>/', views.edit_complain, name='edit_complain'),
    path('resolved/', views.resolved_feedback_list, name='resolved'),
    path('complain/<int:pk>/details/', views.complain_details, name='complain_details'),

    path('createuser/', views.register_user_profile, name='register_profile'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('profile/update/<int:user_id>/', views.update_profile, name='update_profile'),
    path('userprofiles/', views.user_profile_list, name='user_profile_list'),
    
]
