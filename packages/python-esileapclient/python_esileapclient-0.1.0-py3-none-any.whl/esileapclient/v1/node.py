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

from esileapclient.common import base

LOG = logging.getLogger(__name__)


class Node(base.Resource):

    detailed_fields = {
        'name': "Name",
        'uuid': "UUID",
        'owner': "Owner",
        'offer_uuid': "Offer UUID",
        'lease_uuid': "Lease UUID",
        'lessee': "Lessee",
        'future_offers': "Future Offers",
        'future_leases': "Future Leases"
    }

    fields = {
        'name': "Name",
        'owner': "Owner",
        'offer_uuid': "Offer UUID",
        'lease_uuid': "Lease UUID",
        'lessee': "Lessee"
    }

    _creation_attributes = ['name', 'uuid', 'owner', 'offer_uuid',
                            'lessee', 'lease_uuid', 'future_offers',
                            'future_leases']

    def __repr__(self):
        return "<Node %s>" % self._info


class NodeManager(base.Manager):
    resource_class = Node
    _resource_name = 'nodes'

    def list(self, filters, os_esileap_api_version=None):
        """Retrieve a list of nodes.
        :returns: A list of nodes.
        """

        resource_id = ""

        url_variables = NodeManager._url_variables(filters)
        url = self._path(resource_id) + url_variables

        nodes = self._list(url, os_esileap_api_version=os_esileap_api_version)

        if type(nodes) is list:
            return nodes
