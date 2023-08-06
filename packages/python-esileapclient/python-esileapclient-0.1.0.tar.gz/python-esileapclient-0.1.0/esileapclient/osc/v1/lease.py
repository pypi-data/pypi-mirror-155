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
import json

from osc_lib.command import command
from osc_lib import utils as oscutils

from esileapclient.v1.lease import Lease as LEASE_RESOURCE

LOG = logging.getLogger(__name__)


class CreateLease(command.ShowOne):
    """Create a new lease."""

    log = logging.getLogger(__name__ + ".CreateLease")

    def get_parser(self, prog_name):
        parser = super(CreateLease, self).get_parser(prog_name)

        parser.add_argument(
            "resource_uuid",
            metavar="<resource>",
            help="Resource UUID or name")
        parser.add_argument(
            'project_id',
            metavar="<project>",
            help="Project ID or name leasing the resource.")
        parser.add_argument(
            '--end-time',
            dest='end_time',
            required=False,
            help="Time when the lease will expire.")
        parser.add_argument(
            '--name',
            dest='name',
            required=False,
            help="Name of the lease being created. ")
        parser.add_argument(
            '--properties',
            dest='properties',
            required=False,
            help="Record arbitrary key/value resource property "
                 "information. Pass in as a json object.")
        parser.add_argument(
            '--resource-type',
            dest='resource_type',
            required=False,
            help="Use this resource type instead of the default.")
        parser.add_argument(
            '--start-time',
            dest='start_time',
            required=False,
            help="Time when the resource will become usable.")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.lease

        field_list = LEASE_RESOURCE._creation_attributes
        fields = dict((k, v) for (k, v) in vars(parsed_args).items()
                      if k in field_list and v is not None)

        if 'properties' in fields:
            fields['properties'] = json.loads(fields['properties'])

        lease = client.lease.create(**fields)

        data = dict([(f, getattr(lease, f, '')) for f in
                    LEASE_RESOURCE.fields])

        return self.dict2columns(data)


class ListLease(command.Lister):
    """List leases."""

    log = logging.getLogger(__name__ + ".ListLease")

    def get_parser(self, prog_name):
        parser = super(ListLease, self).get_parser(prog_name)

        parser.add_argument(
            '--long',
            default=False,
            help="Show detailed information about the leases.",
            action='store_true')
        parser.add_argument(
            '--all',
            default=False,
            help="Show all leases in the database. For admin use only.",
            action='store_true')
        parser.add_argument(
            '--status',
            dest='status',
            required=False,
            help="Show all leases with given status.")
        parser.add_argument(
            '--offer-uuid',
            dest='offer_uuid',
            required=False,
            help="Show all leases with given offer_uuid.")
        parser.add_argument(
            '--time-range',
            dest='time_range',
            nargs=2,
            required=False,
            help="Show all leases with start and end times "
                 "which begin and end in the given range."
                 "Must pass in two valid datetime strings."
                 "Example: --time-range 2020-06-30T00:00:00"
                 "2021-06-30T00:00:00")
        parser.add_argument(
            '--project',
            dest='project_id',
            required=False,
            help="Show all leases owned by given project ID or name.")
        parser.add_argument(
            '--owner',
            dest='owner_id',
            required=False,
            help="Show all leases relevant to an offer owner "
                 "by the owner's project ID or name.")
        parser.add_argument(
            '--resource-type',
            dest='resource_type',
            required=False,
            help="Show all leases with given resource-type.")
        parser.add_argument(
            '--resource-uuid',
            dest='resource_uuid',
            required=False,
            help="Show all leases with given resource-uuid.")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease

        filters = {
            'status': parsed_args.status,
            'offer_uuid': parsed_args.offer_uuid,
            'start_time': str(parsed_args.time_range[0]) if
            parsed_args.time_range else None,
            'end_time': str(parsed_args.time_range[1]) if
            parsed_args.time_range else None,
            'project_id': parsed_args.project_id,
            'owner_id': parsed_args.owner_id,
            'view': 'all' if parsed_args.all else None,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid
        }

        data = client.lease.list(filters)

        if parsed_args.long:
            columns = LEASE_RESOURCE.detailed_fields.keys()
            labels = LEASE_RESOURCE.detailed_fields.values()
        else:
            columns = LEASE_RESOURCE.fields.keys()
            labels = LEASE_RESOURCE.fields.values()

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))


class ShowLease(command.ShowOne):
    """Show lease details."""

    log = logging.getLogger(__name__ + ".ShowLease")

    def get_parser(self, prog_name):
        parser = super(ShowLease, self).get_parser(prog_name)
        parser.add_argument(
            "uuid",
            metavar="<uuid>",
            help="UUID of the lease")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease

        lease = client.lease.get(parsed_args.uuid)._info

        return zip(*sorted(lease.items()))


class DeleteLease(command.Command):
    """Unregister lease"""

    log = logging.getLogger(__name__ + ".DeleteLease")

    def get_parser(self, prog_name):
        parser = super(DeleteLease, self).get_parser(prog_name)
        parser.add_argument(
            "uuid",
            metavar="<uuid>",
            help="Lease to delete (UUID)")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease
        client.lease.delete(parsed_args.uuid)
        print('Deleted lease %s' % parsed_args.uuid)
