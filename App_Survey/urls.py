from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit-complain/', views.submit_complain, name='submit_complain'),
    path('resolve-complain/<int:complain_id>/', views.resolve_complain, name='resolve_complain'),
    path('search-resolved/', views.search_resolved_complain, name='search_resolved_complain'),
    path('complain-success/', views.complain_success, name='complain_success'),
]
