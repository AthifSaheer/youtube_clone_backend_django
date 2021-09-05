from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # APPS URLS
    path('api/v1/user/', include('user.urls')),
    path('api/v1/studio/', include('studio.urls')),
    path('api/v1/admin/', include('admin_panel.urls')),
    path('', TemplateView.as_view(template_name='index.html'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
