from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('orders.urls')),
    path('', lambda request: JsonResponse({"message": "Welcome to the API!"})),
]

# Thêm dòng này để phục vụ file media trong môi trường phát triển
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
