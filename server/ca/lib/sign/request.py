
from .key import Key
from OpenSSL import crypto

class Request:
    @staticmethod
    def create_with_sample(key:Key, base_args):
        args = {
            "C": "US",
            "ST": "StateOrProvinceName",
            "L": "LocalityName",
            "O": "organizationName",
            "OU": "OrganizationalUnitName",
            "CN": "CommonName",
            "emailAddress": "sample@example.com"
        }
        for k in base_args:
            args[k] = base_args[k]
        return Request.create(key, args)

    # C or countryName – The country of the entity.
    # ST or stateOrProvinceName – The state or province of the entity.
    # L or localityName – The locality of the entity.
    # O or organizationName – The organization name of the entity.
    # OU or organizationalUnitName – The organizational unit of the entity.
    # CN or commonName – The common name of the entity.
    # emailAddress – The e-mail address of the entity.
    @staticmethod
    def create(key:Key, args:dict, digest='sha256'):
        csr = crypto.X509Req()
        n = csr.get_subject()
        for k in args:
            n.__setattr__(k, args[k])
        csr.set_pubkey(key.raw())
        csr.sign(key.raw(), digest)
        return Request(csr)

    @staticmethod
    def from_pem(pem):
        return Request(crypto.load_certificate_request(crypto.FILETYPE_PEM, pem))

    def __init__(self, raw_csr):
        self._csr = raw_csr

        # Decode All Components
        self._components = {}
        for (c, v) in raw_csr.get_subject().get_components():
            self._components[c.decode()] = v.decode()

    def raw(self):
        return self._csr

    def get_components(self):
        return self._components

    def to_pem(self):
        return crypto.dump_certificate_request(crypto.FILETYPE_PEM, self._csr)
