
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App_Survey.urls')),
    # path('api/admin_panel/', include('admin_panel.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    #  "google_sso/", include("django_google_sso.urls", namespace="django_google_sso")
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)