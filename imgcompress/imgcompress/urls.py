from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from compressor import views
from rest_framework.routers import DefaultRouter
from compressor import views

router = DefaultRouter()
router.register('post_image',views.UploadModelViewSet,basename='post')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/',include(router.urls)),
    path('delete_old_media/',views.DeleteOldPhotosView.as_view()),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
