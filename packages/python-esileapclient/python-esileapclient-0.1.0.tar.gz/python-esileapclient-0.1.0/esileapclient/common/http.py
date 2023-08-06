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

from keystoneauth1 import adapter
from oslo_serialization import jsonutils

DEFAULT_VER = '1.0'
LOG = logging.getLogger(__name__)

USER_AGENT = 'python-esileapclient'


class SessionClient(adapter.LegacyJsonAdapter):
    """HTTP client based on Keystone client session."""

    def __init__(self,
                 os_esileap_api_version,
                 **kwargs):
        self.os_esileap_api_version = os_esileap_api_version

        super(SessionClient, self).__init__(**kwargs)

        endpoint = self.get_endpoint()

        if endpoint is None:
            # placeholder for actual error handling
            raise Exception('The Lease API endpoint cannot be detected and '
                            'was not provided explicitly')

    def _http_request(self, url, method, **kwargs):

        kwargs.setdefault('user_agent', USER_AGENT)
        kwargs.setdefault('auth', self.auth)

        if getattr(self, 'os_esileap_api_version', None):
            kwargs['headers'].setdefault('X-OpenStack-ESI-Leap-API-Version',
                                         self.os_esileap_api_version)

        endpoint_filter = kwargs.setdefault('endpoint_filter', {})
        endpoint_filter.setdefault('interface', self.interface)
        endpoint_filter.setdefault('service_type', self.service_type)
        endpoint_filter.setdefault('region_name', self.region_name)

        resp = self.session.request(url, method,
                                    raise_exc=False, **kwargs)

        return resp

    def json_request(self, method, url, **kwargs):

        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type', 'application/json')
        kwargs['headers'].setdefault('Accept', 'application/json')

        if 'body' in kwargs:
            kwargs['data'] = jsonutils.dump_as_bytes(kwargs.pop('body'))

        resp = self._http_request(url, method, **kwargs)

        body = resp.content
        content_type = resp.headers.get('content-type', None)

        if content_type is None:
            return resp, list()

        if 'application/json' in content_type:

            try:
                body = resp.json()
            except ValueError:
                LOG.error('Could not decode response body as JSON')
        else:
            body = None

        return resp, body


def _construct_http_client(session,
                           os_esileap_api_version=DEFAULT_VER,
                           **kwargs):

    kwargs.setdefault('service_type', 'lease')
    kwargs.setdefault('user_agent', 'python-esileapclient')
    kwargs.setdefault('interface', kwargs.pop('endpoint_type',
                                              'publicURL'))

    return SessionClient(os_esileap_api_version=os_esileap_api_version,
                         session=session,
                         **kwargs
                         )
