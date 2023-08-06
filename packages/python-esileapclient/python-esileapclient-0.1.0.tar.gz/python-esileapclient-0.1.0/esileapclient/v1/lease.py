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


class Lease(base.Resource):

    detailed_fields = {
        'end_time': "End Time",
        'expire_time': "Expire Time",
        'fulfill_time': "Fulfill Time",
        'name': "Name",
        'offer_uuid': "Offer UUID",
        'owner': "Owner",
        'owner_id': "Owner ID",
        'parent_lease_uuid': "Parent Lease UUID",
        'project': "Project",
        'project_id': "Project ID",
        'properties': "Properties",
        'resource': "Resource",
        'resource_type': "Resource Type",
        'resource_uuid': "Resource UUID",
        'start_time': "Start Time",
        'status': "Status",
        'uuid': "UUID",
    }

    fields = {
        'uuid': "UUID",
        'resource': "Resource",
        'project': "Project",
        'start_time': "Start Time",
        'end_time': "End Time",
        'offer_uuid': "Offer UUID",
        'status': "Status",
    }

    _creation_attributes = ['start_time', 'end_time', 'status', 'name',
                            'properties', 'project_id', 'resource_type',
                            'resource_uuid']

    def __repr__(self):
        return "<Lease %s>" % self._info


class LeaseManager(base.Manager):
    resource_class = Lease
    _resource_name = 'leases'

    def create(self, os_esileap_api_version=None, **kwargs):
        """Create a lease based on a kwargs dictionary of attributes.
        :returns: a :class: `Lease` object
        """

        lease = self._create(os_esileap_api_version=os_esileap_api_version,
                             **kwargs)

        return lease

    def list(self, filters, os_esileap_api_version=None):
        """Retrieve a list of leases.
        :returns: A list of leases.
        """

        resource_id = ""

        url_variables = LeaseManager._url_variables(filters)
        url = self._path(resource_id) + url_variables

        leases = self._list(url,
                            os_esileap_api_version=os_esileap_api_version)

        if type(leases) is list:
            return leases

    def get(self, lease_uuid):
        """Get a lease with the specified identifier.
        :param lease_uuid: The uuid of a lease.
        :returns: a :class:`Lease` object.
        """

        lease = self._get(lease_uuid)

        return lease

    def delete(self, lease_uuid):
        """Delete a lease with the specified identifier.
        :param lease_uuid: The uuid of a lease.
        :returns: a :class:`Lease` object.
        """

        self._delete(resource_id=lease_uuid)
