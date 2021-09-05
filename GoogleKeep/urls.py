from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from api import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = DefaultRouter()

router.register('NoteAPI',views.NoteViewSet, basename='Note')
router.register('ListAPI',views.ListViewSet, basename='List')
router.register('ImageListAPI',views.ImageListViewSet, basename='ImageList')
router.register('ListItemAPI',views.ListItemViewSet, basename='ListItem')
router.register('ImageAPI',views.ImageViewSet, basename='Image')
router.register('UserAPI',views.UserViewSet, basename='User')
router.register('UserAPI2',views.ExtendedUserViewSet, basename='ExUser')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('ChangePassword/', views.ChangePasswordView.as_view(), name='change-password'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
