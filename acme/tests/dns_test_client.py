"""Client for Boulder's test DNS server.

USAGE:
  $ ./dns_test_client.py foo. bar
  $ dig -p 8053 @localhost foo TXT +tcp

For the server code see boulder/test/dns-test-srv/main.go.

"""
import logging
import sys

import requests

from acme import jose

DNS_ADDR = "localhost:8053"
HTTP_ADDR = "http://localhost:8055/set-txt"


class SetRequest(jose.JSONObjectWithFields):
    """setRequest message.

    Corresponds to `type setRequest struct`.

    """
    host = jose.Field('host')
    value = jose.Field('value')


def update(host, value):
    """Set TXT record to specific value."""
    request = SetRequest(host=host, value=value)
    response = requests.post(HTTP_ADDR, data=request.json_dumps())
    logging.debug(response)
    return response.ok


def main(args=sys.argv):
    """Run simple CLI interface."""
    assert len(args) == 3
    return not update(args[1], args[2])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
