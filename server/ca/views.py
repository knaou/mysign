from django.http import HttpResponse
import re
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ca.lib.params import private_key_from_params, csr_from_params
from ca.lib.sign.certificate import CertificateDefinition, Certificate
from ca.lib.sign.key import Key
from ca.lib.sign.request import Request
from ca.serializers import CertificateAuthoritySerializer, WizardSerializer, CertificateSerializer
from . import models


class CertificateAuthorityViewSet(viewsets.ModelViewSet):
    queryset = models.CertificateAuthority.objects.all()
    serializer_class = CertificateAuthoritySerializer

    @action(detail=False, methods=['post'])
    def wizard(self, request):
        wiz = WizardSerializer(data=request.data)
        wiz.is_valid(raise_exception=True)
        name = wiz.data['name']
        description = wiz.data['description']
        key = private_key_from_params(wiz.data)
        csr = csr_from_params(key, wiz.data)
        cert_def = CertificateDefinition(key, csr, csr, 0, minutes=10 * 365 * 24 * 60 * 60)
        cert_def.set_key_usage(digital_signature=True, crl_sign=True, key_cert_sign=True)
        # TODO: set from params
        cert_def.set_certType(sslCA=True, emailCA=True, objCA=True)
        cert_def.set_CA()
        cert = cert_def.sign()
        ca = models.CertificateAuthority.objects.create(
            name=name,
            description=description,
            next_serial=1,
            key_pem=key.to_pem().decode(),
            csr_pem=csr.to_pem().decode(),
            cert_pem=cert.to_pem().decode()
        )
        return Response(CertificateAuthoritySerializer(ca, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def certificates(self, request, pk=None):
        ca = models.CertificateAuthority.objects.get(pk=pk)
        certs = models.Certificate.objects.filter(certificate_authority=ca)
        return Response([CertificateSerializer(cert, context={'request': request}).data for cert in certs])

    @certificates.mapping.post
    def post_certificates(self, request, pk=None):
        ca = models.CertificateAuthority.objects.get(pk=pk)
        ca_key = Key.from_pem(ca.key_pem)
        ca_csr = Request.from_pem(ca.csr_pem)
        serial = ca.next_serial

        wiz = WizardSerializer(data=request.data)
        wiz.is_valid(raise_exception=True)

        name = wiz.data['name']
        description = wiz.data['description']
        key = private_key_from_params(wiz.data)
        csr = csr_from_params(key, wiz.data)
        cert_def = CertificateDefinition(ca_key, ca_csr, csr, serial)
        if 'sans' in wiz.data:
            sans = [x.strip() for x in re.split('[ ,]+', wiz.data['sans'])]
            if len(sans) > 0 and len(sans[0]) > 0:
                cert_def.set_SANs(sans)
        if 'usages' in wiz.data:
            usages = {u: True for u in wiz.data['usages']}
            cert_def.set_key_usage(**usages)
        if 'ext_usages' in wiz.data:
            ext_usages = {u: True for u in wiz.data['ext_usages']}
            cert_def.set_extended_key_usage(**ext_usages)
        # TODO: set from params
        cert_def.set_certType(server=True, client=True, objsign=True)
        cert = cert_def.sign()
        cert_obj = models.Certificate.objects.create(
            certificate_authority=ca,
            name=name,
            description=description,
            serial=serial,
            key_pem=key.to_pem().decode(),
            csr_pem=csr.to_pem().decode(),
            cert_pem=cert.to_pem().decode()
        )

        ca.next_serial += 1
        ca.save()

        return Response(CertificateSerializer(cert_obj, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def keyfile(self, request, pk=None):
        ca = models.CertificateAuthority.objects.get(pk=pk)
        response = HttpResponse(ca.key_pem, content_type="application/x-pem-file")
        response["Content-Disposition"] = "filename=key.pem"
        return response

    @action(detail=True, methods=['get'])
    def csrfile(self, request, pk=None):
        ca = models.CertificateAuthority.objects.get(pk=pk)
        response = HttpResponse(ca.csr_pem, content_type="application/x-pem-file")
        response["Content-Disposition"] = "filename=csr.pem"
        return response

    @action(detail=True, methods=['get'])
    def certfile(self, request, pk=None):
        ca = models.CertificateAuthority.objects.get(pk=pk)
        response = HttpResponse(ca.cert_pem, content_type="application/x-pem-file")
        response["Content-Disposition"] = "filename=cert.pem"
        return response


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = models.Certificate.objects.all()
    serializer_class = CertificateSerializer

    @action(detail=True, methods=['get'])
    def keyfile(self, request, pk=None):
        ca = models.Certificate.objects.get(pk=pk)
        response = HttpResponse(ca.key_pem, content_type="application/x-pem-file")
        response["Content-Disposition"] = "filename=key.pem"
        return response

    @action(detail=True, methods=['get'])
    def csrfile(self, request, pk=None):
        ca = models.Certificate.objects.get(pk=pk)
        response = HttpResponse(ca.csr_pem, content_type="application/x-pem-file")
        response["Content-Disposition"] = "filename=csr.pem"
        return response

    @action(detail=True, methods=['get'])
    def certfile(self, request, pk=None):
        ca = models.Certificate.objects.get(pk=pk)
        response = HttpResponse(ca.cert_pem, content_type="application/x-pem-file")
        response["Content-Disposition"] = "filename=cert.pem"
        return response
