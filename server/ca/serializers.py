from rest_framework import serializers

from ca.lib.params import request_params_from_request
from ca.lib.sign.certificate import Certificate
from ca.lib.sign.request import Request
from . import models


class CertificateAuthoritySummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CertificateAuthority
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'url')


class CertificateAuthoritySerializer(serializers.ModelSerializer):
    request = serializers.SerializerMethodField()

    def get_request(self, ca:models.CertificateAuthority):
        csr = Request.from_pem(ca.csr_pem)
        return request_params_from_request(csr)

    class Meta:
        model = models.CertificateAuthority
        fields = ('id', 'name', 'description', 'request', 'next_serial', 'created_at', 'updated_at', 'url')
        read_only_fields = ('id', 'request', 'next_serial', 'created_at', 'updated_at')


class CertificateSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Certificate
        fields = ('id', 'name', 'description', 'serial', 'created_at', 'updated_at', 'url')
        read_only_fields = ('id', 'serial', 'created_at', 'updated_at')


class CertificateSerializer(serializers.ModelSerializer):
    certificate_authority = CertificateAuthoritySummarySerializer(read_only=True)
    request = serializers.SerializerMethodField()

    def get_request(self, ca:models.CertificateAuthority):
        csr = Request.from_pem(ca.csr_pem)
        return request_params_from_request(csr)

    class Meta:
        model = models.Certificate
        fields = ('id', 'certificate_authority', 'name', 'description', 'request', 'serial', 'created_at', 'updated_at', 'url')
        read_only_fields = ('id', 'certificate_authority', 'request', 'serial', 'created_at', 'updated_at')


class WizardSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1024, allow_blank=True, required=False)

    private_key = serializers.CharField(max_length=10)
    private_key_pem = serializers.CharField(max_length=255, allow_blank=True, required=False)

    csr = serializers.CharField(max_length=10)
    csr_C = serializers.CharField(max_length=255, allow_blank=True, required=False)
    csr_ST = serializers.CharField(max_length=255, allow_blank=True, required=False)
    csr_L = serializers.CharField(max_length=255, allow_blank=True, required=False)
    csr_O = serializers.CharField(max_length=255, allow_blank=True, required=False)
    csr_OU = serializers.CharField(max_length=255, allow_blank=True, required=False)
    csr_CN = serializers.CharField(max_length=255, allow_blank=True, required=False)
    csr_emailAddress = serializers.CharField(max_length=255, allow_blank=True, required=False)
    csr_pem = serializers.CharField(max_length=255, allow_blank=True, required=False)

    sans = serializers.CharField(max_length=1024, allow_blank=True, required=False)
    usages = serializers.ListField(child=serializers.CharField(max_length=64), required=False)
    ext_usages = serializers.ListField(child=serializers.CharField(max_length=64), required=False)

    def validate(self, attrs):
        errors = {}
        if attrs['private_key'] != 'create' and attrs['private_key'] != 'input':
            errors['private_key'] = 'must be create or input'
        if attrs['private_key'] == 'input' and (attrs['private_key_pem'] == None or attrs['private_key_pem'] == ""):
            errors['private_key_pem'] = 'must be set'
        if attrs['csr'] != 'create' and attrs['csr'] != 'input':
            errors['csr'] = 'must be create or input'
        if attrs['csr'] == 'input' and (attrs['csr_pem'] == None or attrs['csr_pem'] == ""):
            errors['csr_pem'] = 'This field is required.'
        if attrs['csr'] == 'create' and (attrs['csr_C'] == None or attrs['csr_C'] == ""):
            errors['csr_C'] = 'This field is required.'
        if attrs['csr'] == 'create' and (attrs['csr_ST'] == None or attrs['csr_ST'] == ""):
            errors['csr_ST'] = 'This field is required.'
        if attrs['csr'] == 'create' and (attrs['csr_L'] == None or attrs['csr_L'] == ""):
            errors['csr_L'] = 'This field is required.'
        if attrs['csr'] == 'create' and (attrs['csr_O'] == None or attrs['csr_O'] == ""):
            errors['csr_O'] = 'This field is required.'
        if attrs['csr'] == 'create' and (attrs['csr_OU'] == None or attrs['csr_OU'] == ""):
            errors['csr_OU'] = 'This field is required.'
        if attrs['csr'] == 'create' and (attrs['csr_CN'] == None or attrs['csr_CN'] == ""):
            errors['csr_CN'] = 'This field is required.'
        if attrs['csr'] == 'create' and (attrs['csr_emailAddress'] == None or attrs['csr_emailAddress'] == ""):
            errors['csr_emailAddress'] = 'This field is required.'

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return attrs

