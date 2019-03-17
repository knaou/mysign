from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Certificate)
admin.site.register(models.CertificateAuthority)
