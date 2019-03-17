from django.test import TestCase

from ca.lib.sign.certificate import CertificateDefinition, Certificate
from ca.lib.sign.key import Key
from ca.lib.sign.request import Request

sample_key_pem = """-----BEGIN PRIVATE KEY-----
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
QqGM6jX3VDOr7ukJEUcCvRjoQ7TAPQ==
-----END PRIVATE KEY-----
"""

sample_request_pem = """-----BEGIN CERTIFICATE REQUEST-----
MIIE7zCCAtcCAQAwgakxCzAJBgNVBAYTAkpQMQ4wDAYDVQQIDAVTdGF0ZTEOMAwG
A1UEBwwFbG9jYWwxGjAYBgNVBAoMEU9yZ2FuaXphdGlvbiBOYW1lMSEwHwYDVQQL
DBhPcmdhbml6YXRpb25hbCBVbml0IE5hbWUxFDASBgNVBAMMC2V4YW1wbGUuY29t
MSUwIwYJKoZIhvcNAQkBFhZzaXRlbWFzdGVyQGV4YW1wbGUuY29tMIICIjANBgkq
hkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6O30aCTWbYFG9lg0EJLAIiCp6mvNkFmY
ZUz3+SyGaLg4Ojf5ilg19oZqeSQSUA+5jjBsUrHQF0UHdqZsno5LxbRqBN5OQl1g
lplC4DDwLoig/pWePIHsibxQ/yUtkMkXYO1vm9G8I1+SEQ/cEIuMlCfkV2OasL2G
k72LQ7AuGshWSihT79PhNFGdVQQPVZ9stOlnHtNvjZJ+UMbbWRnh9uHcHE+TdWmY
IxJkWp4H7eCxkAVQAsduKPcRFR2awhecVtuXdgAebfFRIutYZP0b3yE4DeaBY8JU
14nxLfmgtDFkIt85NpJRiegen0VFF4ekhXY4mk69Gp/Dx86Hig57fNLbl4l3SzDk
ba9Opbyn60oWsuRch4mVNFmvx1m7b4lYZEDeFn5azpk2hSQ0Cxeh54BkYsSNfwch
NO0NzLGmGKMVQckIMw+E8cdFcRSnfvrAPTC3r9cjRUcAhrKluv8+voQdGDDDqbec
8H6gT0wsJF7A3o9BbW0RY463CP5Ys3K2XOoVMbqhDHKYzkrojSrqtv9NUITDrUVS
AOb4WjVB/WhIADMaf1YUu9EOPtcX3oSeLUtAyPJEreekYtVToYfThiJq1h8HNHp+
62MnKfe7jW5YbB838BZSkKZqOPMYgH2yP4MgHMqieFz5rP3eWiCRAxKD/Ntpmpbk
xQcXM5nwhdkCAwEAAaAAMA0GCSqGSIb3DQEBCwUAA4ICAQDOifDJzfhPQIbaPCfe
zalXpoZbGCfz5HTai035yvy6oaPQ4xnh6vDI+GUwGXO1gfQhuSbKIx7zm2X8Avj1
jHtYLh7rOM5Yhi/i6QmFiu6Fu+NKhodL2RsypwWBsmOKELUPIhWQ3jVBRWzJSqMk
3gfpQ7xozjG0IYLd5Zfz4ye4PLDNtoR6w17Dy21BQ5J6WFktgZ/UFy5RO05WdZph
hcEsLfj4XuAFQrk2oc803cfYc37jfNHkhDYyJSDiJ99ga3J6nzyRBkFm0BZ09uvw
cLpDbIKvNglCnA0Ezm3Le5OGSxkHOk+LijYT64A22sZWQKPgm4+Gv9UL4fXfbcTX
mOIHeJ4U4W8K7kx0OpLvg565K+rOlRzKD/WD1+b0sCa28EYM5GyPOVEIYR/7C0zP
R8INKCbdHsdUMcXjakNMFFb5X5odawqOpYpybhTA0j1gt3WwyMS55JpNDUCbpmqJ
V5tRB02eYgUXEmPy6txk9CGWYWq2RRpJhvWy1mtVkCfzcKTUW7gaLK35bRBkBqMk
76O4UbphF/xydfJXg19E2t40yLXMEdhmcl5g/mMB/n5butIregRUn+Y24WM8J7qJ
ieWE4DtZ76Sw48wZA2C2DrWgR1ZPt5rQLHq/ptNmxtLha0nmM+wvNkX8pXbRDuSH
Itfd5rKre2Rl8DBH3ENEk/9R+g==
-----END CERTIFICATE REQUEST-----
"""

sample_cert_pem = """-----BEGIN CERTIFICATE-----
MIIGADCCA+gCAQAwDQYJKoZIhvcNAQELBQAwgakxCzAJBgNVBAYTAkpQMQ4wDAYD
VQQIDAVTdGF0ZTEOMAwGA1UEBwwFbG9jYWwxGjAYBgNVBAoMEU9yZ2FuaXphdGlv
biBOYW1lMSEwHwYDVQQLDBhPcmdhbml6YXRpb25hbCBVbml0IE5hbWUxFDASBgNV
BAMMC2V4YW1wbGUuY29tMSUwIwYJKoZIhvcNAQkBFhZzaXRlbWFzdGVyQGV4YW1w
bGUuY29tMB4XDTE5MDIwMzEyMjk0MloXDTI5MDEzMTEyMjk0MlowgakxCzAJBgNV
BAYTAkpQMQ4wDAYDVQQIDAVTdGF0ZTEOMAwGA1UEBwwFbG9jYWwxGjAYBgNVBAoM
EU9yZ2FuaXphdGlvbiBOYW1lMSEwHwYDVQQLDBhPcmdhbml6YXRpb25hbCBVbml0
IE5hbWUxFDASBgNVBAMMC2V4YW1wbGUuY29tMSUwIwYJKoZIhvcNAQkBFhZzaXRl
bWFzdGVyQGV4YW1wbGUuY29tMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKC
AgEA6O30aCTWbYFG9lg0EJLAIiCp6mvNkFmYZUz3+SyGaLg4Ojf5ilg19oZqeSQS
UA+5jjBsUrHQF0UHdqZsno5LxbRqBN5OQl1glplC4DDwLoig/pWePIHsibxQ/yUt
kMkXYO1vm9G8I1+SEQ/cEIuMlCfkV2OasL2Gk72LQ7AuGshWSihT79PhNFGdVQQP
VZ9stOlnHtNvjZJ+UMbbWRnh9uHcHE+TdWmYIxJkWp4H7eCxkAVQAsduKPcRFR2a
whecVtuXdgAebfFRIutYZP0b3yE4DeaBY8JU14nxLfmgtDFkIt85NpJRiegen0VF
F4ekhXY4mk69Gp/Dx86Hig57fNLbl4l3SzDkba9Opbyn60oWsuRch4mVNFmvx1m7
b4lYZEDeFn5azpk2hSQ0Cxeh54BkYsSNfwchNO0NzLGmGKMVQckIMw+E8cdFcRSn
fvrAPTC3r9cjRUcAhrKluv8+voQdGDDDqbec8H6gT0wsJF7A3o9BbW0RY463CP5Y
s3K2XOoVMbqhDHKYzkrojSrqtv9NUITDrUVSAOb4WjVB/WhIADMaf1YUu9EOPtcX
3oSeLUtAyPJEreekYtVToYfThiJq1h8HNHp+62MnKfe7jW5YbB838BZSkKZqOPMY
gH2yP4MgHMqieFz5rP3eWiCRAxKD/NtpmpbkxQcXM5nwhdkCAwEAAaM2MDQwDgYD
VR0PAQH/BAQDAgGGMBEGCWCGSAGG+EIBAQQEAwIABzAPBgNVHRMBAf8EBTADAQH/
MA0GCSqGSIb3DQEBCwUAA4ICAQCYHsO8hklGoUyzrEDrthO7V9TUoUFUTfIGA8Wf
D5wy8MpiCOQX3Y0Kz9Jr/mWSlTfYpq6fKvOyQiZAmWwRxDfteFNZdPJo+fAV4i2H
g9jqiElOe4zW2VHqMYBkm5oD0ZXb58QPZLMj4SjlEF501iPeGOup2inrxhnyedWi
tYZQygHSpT+QrXGFYKg2N31qBwihL8CYqSdT9fVUE9G7tHkg4k6JzFJumOIBXSom
AfxchAxz3ZFw6uMZbQF9458fgTuY965uCRRny6O7dCd1pvDSs74bydhJ2G6+/iij
LkMlo5lfz/EXTxyAAgPDtyhaLQDFS1nkUO+lw4sUJ2NFC7+y5XNVwP4rVzHvQbgO
dj6fmZVR03Ij2x7cyY3uVyhAun1kYGg0dX2OF1wAHHWNt4IvN6Gjb7tGDn9SPTUR
uUmMVDG2UQkyhzxQ6ySeEBe1G03ax7btgSXj+hF8k+UigVK8aVY0jlr8gTg0LTpp
z5SSgXCrJe8weI4XyKSiDPZPGH1WiEy60NkInfhUuYXT6OXMVwlujHNHI+1xGLea
fmMAY05UOR6/7dLhnacws0RoV2JdJnCaParw4Us/WB7Okc4PaHuTFMbDD1x6xClc
6ADh0uup8gKByc85vjYXEEc2JRofox/sbuKxA1i107H+L0O7faBcLmjekdd2vP2R
M+01AQ==
-----END CERTIFICATE-----
"""


class KeyTests(TestCase):
    def test_new_key(self):
        key = Key('something')
        self.assertIs(key.raw(), 'something')

    def test_create_key(self):
        key = Key.create(4096)
        self.assertIsNotNone(key.raw())

    def test_from_pem(self):
        key = Key.from_pem(sample_key_pem)
        pem = key.to_pem()
        self.assertEqual(sample_key_pem, pem.decode())

class RequestTests(TestCase):
    def test_new_request_with_sample(self):
        key = Key.create()
        req = Request.create_with_sample(key, {'C': 'ZZ'})
        self.assertEqual(req.get_components()['C'], 'ZZ')

    def test_from_pem(self):
        req = Request.from_pem(sample_request_pem)
        pem = req.to_pem()
        self.assertEqual(sample_request_pem, pem.decode())

class CertificateTests(TestCase):
    def setUp(self):
        self._key = Key.create()
        self._req = Request.create_with_sample(self._key, {})

    def test_simple_sign(self):
        cdef = CertificateDefinition(self._key, self._req, self._req, 1)
        self.assertIsInstance(cdef.sign(), Certificate)

    def test_sign_with_certType(self):
        cdef = CertificateDefinition(self._key, self._req, self._req, 1)
        cdef.set_certType(
            server=True,
            client=True,
            email=True,
            objsign=True,
            sslCA=True,
            emailCA=True,
            objCA=True
        )
        self.assertIsInstance(cdef.sign(), Certificate)

    def test_sign_with_CA(self):
        cdef = CertificateDefinition(self._key, self._req, self._req, 1)
        cdef.set_CA()
        self.assertIsInstance(cdef.sign(), Certificate)

    def test_sign_with_CRL(self):
        cdef = CertificateDefinition(self._key, self._req, self._req, 1)
        cdef.set_CRL('https://example.com/')
        self.assertIsInstance(cdef.sign(), Certificate)

    def test_sign_with_extended_key_usage(self):
        cdef = CertificateDefinition(self._key, self._req, self._req, 1)
        cdef.set_extended_key_usage(
            server_auth=True,
            client_auth=True,
            code_signing=True,
            email_protection=True,
            time_stamping=True,
            ms_sgc=True,
            ns_sgc=True,
            ms_smartcard_login=True
        )
        self.assertIsInstance(cdef.sign(), Certificate)

    def test_sign_with_key_usage(self):
        cdef = CertificateDefinition(self._key, self._req, self._req, 1)
        cdef.set_key_usage(
            digital_signature=True,
            non_repudiation=True,
            key_encipherment=True,
            data_encipherment=True,
            key_agreement=True,
            key_cert_sign=True,
            crl_sign=True,
            encipher_only=True,
            decipher_only=True
        )
        self.assertIsInstance(cdef.sign(), Certificate)

    def test_sign_with_OCSP(self):
        cdef = CertificateDefinition(self._key, self._req, self._req, 1)
        cdef.set_OCSP('https://example.com/')
        self.assertIsInstance(cdef.sign(), Certificate)

    def test_sign_with_SANs(self):
        cdef = CertificateDefinition(self._key, self._req, self._req, 1)
        cdef.set_SANs(['IP:128.0.0.1', 'DNS:example.com'])
        self.assertIsInstance(cdef.sign(), Certificate)

    def test_from_pem(self):
        cert = Certificate.from_pem(sample_cert_pem)
        pem = cert.to_pem()
        self.assertEqual(sample_cert_pem, pem.decode())
