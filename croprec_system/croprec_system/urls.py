from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cropapp.urls')),  
]

if settings.DEBUG:
    try:
        doc_root = settings.STATICFILES_DIRS[0]
    except Exception:
        doc_root = settings.STATIC_ROOT
    urlpatterns += static(settings.STATIC_URL, document_root=doc_root)
