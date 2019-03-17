from ca.lib.sign.key import Key
from ca.lib.sign.request import Request

def request_params_from_request(req: Request):
    comp = req.get_components()
    return {k: comp[k] for k in ['C', 'ST', 'L', 'O', 'OU', 'CN', 'emailAddress'] if k in comp}


def private_key_from_params(params):
    p_pk = params['private_key']
    if p_pk == 'create':
        private_key = Key.create()
    elif p_pk == 'input':
        pem = params['private_key_pem']
        private_key = Key.from_pem(pem)
    else:
        raise Exception('Unexpected private key')
    return private_key


def csr_from_params(private_key, params):
    p_csr = params['csr']
    if p_csr == 'create':
        params = {
            "C": params['csr_C'],
            "ST": params['csr_ST'],
            "L": params['csr_L'],
            "O": params['csr_O'],
            "OU": params['csr_OU'],
            "CN": params['csr_CN'],
            "emailAddress": params['csr_emailAddress'],
        }
        valid_params = {k: params[k] for k in params if params[k] is not None and len(params[k]) > 0}
        csr = Request.create(private_key, valid_params)
    elif p_csr == 'input':
        pem = params['csr_pem']
        csr = Request.from_pem(pem)
    else:
        raise Exception('Unexpected csr')
    return csr

