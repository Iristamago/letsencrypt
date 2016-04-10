"""Example script showing how to use acme client API."""
import logging
import os
import pkg_resources

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import OpenSSL

from acme import client
from acme import messages
from acme import jose


logging.basicConfig(level=logging.DEBUG)


DIRECTORY_URL = 'https://acme-staging.api.letsencrypt.org/directory'
BITS = 2048  # minimum for Boulder
DOMAIN = 'example1.com'  # example.com is ignored by Boulder

# generate_private_key requires cryptography>=0.5
key = jose.JWKRSA(key=rsa.generate_private_key(
    public_exponent=65537,
    key_size=BITS,
    backend=default_backend()))
acme = client.Client(DIRECTORY_URL, key)

regr = acme.register()
logging.info('Auto-accepting TOS: %s', regr.terms_of_service)
acme.agree_to_tos(regr)
logging.debug(regr)

authzr = acme.request_domain_challenges(DOMAIN)
logging.debug(authzr)

# challb = find_suitable_challb(authzr)
# response, validation = challb.response_and_validation(acme.key)
# solve_challb(challb, validation)
# acme.answer_challenge(challb, response)

authzr, authzr_response = acme.poll(authzr)

csr = OpenSSL.crypto.load_certificate_request(
    OpenSSL.crypto.FILETYPE_ASN1, pkg_resources.resource_string(
        'acme', os.path.join('testdata', 'csr.der')))
try:
    acme.request_issuance(jose.util.ComparableX509(csr), (authzr,))
except messages.Error as error:
    print ("This script is doomed to fail as no authorization "
           "challenges are ever solved. Moreover, sent CSR was for "
           "example.com rather than requested example1.com. Check "
           "commented code in the script. Error from server: {0}".format(error))
