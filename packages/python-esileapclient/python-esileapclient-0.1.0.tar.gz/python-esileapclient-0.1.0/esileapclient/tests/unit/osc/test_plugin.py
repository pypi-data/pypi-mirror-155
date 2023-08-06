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

import unittest.mock as mock
import testtools

from esileapclient.osc import plugin
from esileapclient.v1 import client

API_VERSION = '1'


class FakeClientManager(object):
    def __init__(self):
        self.identity = None
        self.auth_ref = None
        self.interface = 'public'
        self._region_name = 'RegionOne'
        self.session = 'fake session'
        self._api_version = {'lease': API_VERSION}


class MakeClientTest(testtools.TestCase):

    @mock.patch.object(client, 'Client')
    def test_make_client_explicit_version(self, mock_client):
        instance = FakeClientManager()
        plugin.make_client(instance)
        mock_client.assert_called_once_with(
            os_esileap_api_version=API_VERSION,
            session=instance.session,
            region_name=instance._region_name,
            endpoint_override=None)

    @mock.patch.object(client, 'Client')
    def test_make_client_latest(self, mock_client):
        instance = FakeClientManager()
        instance._api_version = {'lease': plugin.LATEST_VERSION}
        plugin.make_client(instance)
        mock_client.assert_called_once_with(
            os_esileap_api_version=plugin.LATEST_VERSION,
            session=instance.session,
            region_name=instance._region_name,
            endpoint_override=None)

    @mock.patch.object(client, 'Client')
    def test_make_client_v1(self, mock_client):
        instance = FakeClientManager()
        instance._api_version = {'lease': '1'}
        plugin.make_client(instance)
        mock_client.assert_called_once_with(
            os_esileap_api_version=plugin.LATEST_VERSION,
            session=instance.session,
            region_name=instance._region_name,
            endpoint_override=None)
