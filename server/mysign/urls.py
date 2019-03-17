from django.contrib import admin
from django.urls import path, include
import ca.urls as ca_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(ca_urls.api.urls))
]
