from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()

router.register('NoteAPI',views.NoteViewSet, basename='Note')
router.register('ListAPI',views.ListViewSet, basename='List')
router.register('ImageListAPI',views.ImageListViewSet, basename='ImageList')
router.register('ListItemAPI',views.ListItemViewSet, basename='ListItem')
router.register('ImageAPI',views.ImageViewSet, basename='Image')

router.register('UserAPI',views.UserViewSet, basename='User')
router.register('UserAPI2',views.ExtendedUserViewSet, basename='ExUser')
router.register('RegisterAPI',views.RegisterViewSet, basename='Register')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('api/', include('api.urls')),
   
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
