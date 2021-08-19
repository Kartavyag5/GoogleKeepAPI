from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()

router.register('NoteAPI',views.NoteViewSet, basename='Note')

router.register('UserAPI',views.UserViewSet, basename='User')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('api/', include('api.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
