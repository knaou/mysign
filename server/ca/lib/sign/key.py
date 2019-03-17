from OpenSSL import crypto


class Key:
    @staticmethod
    def create(bits = 4096):
        pk = crypto.PKey()
        pk.generate_key(crypto.TYPE_RSA, bits)
        return Key(pk)

    @staticmethod
    def from_pem(pem, password = None):
        return Key(crypto.load_privatekey(
            crypto.FILETYPE_PEM,
            pem,
            password))

    def __init__(self, raw_key):
        self._key = raw_key

    def raw(self):
        return self._key

    def sign(self, data, digest = "sha256"):
        return crypto.sign(self._key, data, digest)

    def to_pem(self, cipher = None, passphrase = None):
        return crypto.dump_privatekey(
            crypto.FILETYPE_PEM,
            self._key,
            cipher,
            passphrase)

