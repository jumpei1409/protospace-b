from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', include('prototypes.urls')),
    path('users/', include('users.urls')),
    path('prototypes/<int:pk>/comments/',include('comments.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)