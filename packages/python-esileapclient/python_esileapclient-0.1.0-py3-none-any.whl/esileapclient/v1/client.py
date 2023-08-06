#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import logging


from esileapclient.common import http
from esileapclient.common.http import DEFAULT_VER
from esileapclient.v1 import lease
from esileapclient.v1 import node
from esileapclient.v1 import offer

LOG = logging.getLogger(__name__)


class Client(object):
    """Client for the ESI-Leap v1 API.
    :param session: A keystoneauth Session object (must be provided as
        a keyword argument).
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new client for the ESI-Leap v1 API."""

        if 'os_esileap_api_version' not in kwargs:
            kwargs['os_esileap_api_version'] = DEFAULT_VER

        if not args and not kwargs.get('session'):
            raise TypeError("A session is required for creating a client, "
                            "use esileapclient.client.get_client to create "
                            "it automatically")

        self.http_client = http._construct_http_client(*args, **kwargs)
        self.lease = lease.LeaseManager(self.http_client)
        self.node = node.NodeManager(self.http_client)
        self.offer = offer.OfferManager(self.http_client)
