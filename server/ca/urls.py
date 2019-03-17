from rest_framework import routers
from . import views

api = routers.DefaultRouter()
api.register('certificate_authoritys', views.CertificateAuthorityViewSet)
api.register('certificates', views.CertificateViewSet)
