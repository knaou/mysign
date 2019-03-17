
from .key import Key
from .request import Request
from OpenSSL import crypto

class CertificateDefinition:
    def __init__(self,
                 issuer_key: Key, issuer_csr: Request,
                 request_csr: Request,
                 serial,
                 minutes: int = 10 * 365 * 24 * 60 * 60,
                 digest: str = "sha256"):

        self._issuer_key = issuer_key
        self._digest = digest
        self._extensions = {}

        cert = crypto.X509()
        cert.set_version(2)
        cert.set_serial_number(serial)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(minutes)
        cert.set_issuer(issuer_csr.raw().get_subject())
        cert.set_subject(request_csr.raw().get_subject())
        cert.set_pubkey(request_csr.raw().get_pubkey())
        self._cert = cert

    def set_extension(self, key, value, critical=False):
        self._extensions[key] = (value, critical)
        return self

    def set_CA(self):
        return self.set_extension("basicConstraints", "CA:TRUE", True)

    def set_SANs(self, sans):
        return self.set_extension("subjectAltName", ", ".join(sans))

    def set_key_usage(self,
                      digital_signature=False,
                      non_repudiation=False,
                      key_encipherment=False,
                      data_encipherment=False,
                      key_agreement=False,
                      key_cert_sign=False,
                      crl_sign=False,
                      encipher_only=False,
                      decipher_only=False):
        usages = []
        if digital_signature:
            usages.append("digitalSignature")
        if non_repudiation:
            usages.append("nonRepudiation")
        if key_encipherment:
            usages.append("keyEncipherment")
        if data_encipherment:
            usages.append("dataEncipherment")
        if key_agreement:
            usages.append("keyAgreement")
        if key_cert_sign:
            usages.append("keyCertSign")
        if crl_sign:
            usages.append("cRLSign")
        if encipher_only:
            usages.append("encipherOnly")
        if decipher_only:
            usages.append("decipherOnly")
        if len(usages) == 0:
            raise Exception('No usages')
        return self.set_extension("keyUsage", ", ".join(usages), True)

    def set_extended_key_usage(self,
                               server_auth=False,
                               client_auth=False,
                               code_signing=False,
                               email_protection=False,
                               time_stamping=False,
                               ms_sgc=False,
                               ns_sgc=False,
                               ms_smartcard_login=False
                               ):
        usages = []
        if server_auth:
            usages.append("serverAuth")
        if client_auth:
            usages.append("clientAuth")
        if code_signing:
            usages.append("codeSigning")
        if email_protection:
            usages.append("emailProtection")
        if time_stamping:
            usages.append("timeStamping")
        if ms_sgc:
            usages.append("msSGC")
        if ns_sgc:
            usages.append("nsSGC")
        if ms_smartcard_login:
            usages.append("msSmartcardLogin")
        if len(usages) == 0:
            raise Exception('No usages')
        return self.set_extension("extendedKeyUsage", ", ".join(usages))

    def set_certType(self,
                     server=False,
                     client=False,
                     email=False,
                     objsign=False,
                     sslCA=False,
                     emailCA=False,
                     objCA=False):
        types = []
        if server:
            types.append("server")
        if client:
            types.append("client")
        if email:
            types.append("email")
        if objsign:
            types.append("objsign")
        if sslCA:
            types.append("sslCA")
        if emailCA:
            types.append("emailCA")
        if objCA:
            types.append("objCA")

        if len(types) == 0:
            raise Exception('No types')
        return self.set_extension("nsCertType", ", ".join(types))

    def set_CRL(self, uri):
        return self.set_extension("crlDistributionPoints", "URI:" + uri)

    def set_OCSP(self, uri):
        return self.set_extension("authorityInfoAccess", "OCSP;URI: " + uri)

    def sign(self):
        if len(self._extensions) > 0:
            exts = []
            for k in self._extensions:
                v, c = self._extensions[k]
                exts.append(crypto.X509Extension(k.encode(), c, v.encode()))
            self._cert.add_extensions(exts)
        self._cert.sign(self._issuer_key.raw(), self._digest)

        return Certificate(self._cert)


class Certificate:
    @staticmethod
    def from_pem(pem):
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem)
        return Certificate(cert)

    def __init__(self, cert):
        self._cert = cert

    def raw(self):
        return self._cert

    def to_pem(self):
        return crypto.dump_certificate(crypto.FILETYPE_PEM, self._cert)

