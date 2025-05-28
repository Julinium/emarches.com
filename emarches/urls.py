from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500

from base import views

handler400 = "base.views.custom_400_view" # Bad request
handler403 = "base.views.custom_403_view" # Forbidden
handler404 = "base.views.custom_404_view" # Not found
handler500 = "base.views.custom_500_view" # Internal server error

urlpatterns = []

urlpatterns += i18n_patterns(
    path('', include('base.urls')),
    path('crm/', include('crm.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('cons/', include('portal.urls')),
)

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
