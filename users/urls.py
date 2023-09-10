from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('userprofile-details/<int:user__pk>/', views.UserProfileDetail.as_view(), name='userprofile-details'),
    path('profilepictures/<int:pk>/', views.ProfilePictureDetail.as_view(), name='profilepicture-detail'),
    path('profile/', views.profile_view, name='profile')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)