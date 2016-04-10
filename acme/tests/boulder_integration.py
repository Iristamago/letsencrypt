"""Boulder integration testing."""
import logging
import os
import sys

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import OpenSSL

from acme import client
from acme import crypto_util
from acme import challenges
from acme import messages
from acme import jose

import dns_test_client


DIRECTORY_URL = os.environ.get("SERVER", "http://localhost:4000/directory")
BOULDER_MIN_KEY_BITS = 2048  # both for account and CSR


def supported_challb(authzr, expected):
    """Get a singleton combo challenge with expected type or fail."""
    for combo in authzr.body.combinations:
        first_challb = authzr.body.challenges[combo[0]]
        if len(combo) == 1 and isinstance(first_challb.chall, expected):
            return first_challb
    raise Exception("Expected {0!r} not found".format(supported.typ))


def test_dns_01_challenge(acme):
    """Test for dns-01 challenge."""
    domain = 'example1.com'  # example.com is ignored by Boulder
    authzr = acme.request_domain_challenges(domain)
    logging.debug(authzr)

    challb = supported_challb(authzr, challenges.DNS01)
    response, validation = challb.response_and_validation(acme.key)

    dns_test_client.update(
        host="{0}.".format(challb.validation_domain_name(domain)),
        value=validation,
    )
    acme.answer_challenge(challb, response)

    csr = crypto_util.gen_csr(
        crypto_util.gen_pkey(BOULDER_MIN_KEY_BITS), [domain])
    certr, _ = acme.poll_and_request_issuance(
        jose.util.ComparableX509(csr), [authzr])


def setup_registered_acme():
    """Setup registered ACME client."""
    # generate_private_key requires cryptography>=0.5
    key = jose.JWKRSA(key=rsa.generate_private_key(
        public_exponent=65537,
        key_size=BOULDER_MIN_KEY_BITS,
        backend=default_backend()))
    acme = client.Client(DIRECTORY_URL, key)
    regr = acme.register()
    logging.info('Auto-accepting TOS: %s', regr.terms_of_service)
    acme.agree_to_tos(regr)
    logging.debug(regr)
    return acme


def main(args=sys.argv):
    """Run all tests."""
    acme = setup_registered_acme()
    test_dns_01_challenge(acme)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
