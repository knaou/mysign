from django.db import models


class CertificateAuthority(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False, blank=True, default='')
    next_serial = models.IntegerField(null=False)
    key_pem = models.TextField(null=False)
    csr_pem = models.TextField(null=False)
    cert_pem = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Certificate(models.Model):
    certificate_authority = models.ForeignKey(CertificateAuthority, related_name='certificates', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False, blank=True, default='')
    serial = models.IntegerField(null=False)
    key_pem = models.TextField(null=False)
    csr_pem = models.TextField(null=False)
    cert_pem = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('certificate_authority', 'serial',)
