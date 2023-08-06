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
from esileapclient.v1.offer import Offer as OFFER_RESOURCE

LOG = logging.getLogger(__name__)


class CreateOffer(command.ShowOne):
    """Create a new offer."""

    log = logging.getLogger(__name__ + ".CreateOffer")

    def get_parser(self, prog_name):
        parser = super(CreateOffer, self).get_parser(prog_name)

        parser.add_argument(
            "resource_uuid",
            metavar="<resource_uuid>",
            help="Resource UUID")
        parser.add_argument(
            '--end-time',
            dest='end_time',
            required=False,
            help="Time when the offer will expire and no longer be "
                 "'available'.")
        parser.add_argument(
            '--lessee',
            dest='lessee_id',
            required=False,
            help="Project subtree to which this offer will be limited.")
        parser.add_argument(
            '--name',
            dest='name',
            required=False,
            help="Name of the offer being created. ")
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
            help="Time when the offer will be made 'available'.")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease

        field_list = OFFER_RESOURCE._creation_attributes

        fields = dict((k, v) for (k, v) in vars(parsed_args).items()
                      if k in field_list and v is not None)

        if 'properties' in fields:
            fields['properties'] = json.loads(fields['properties'])

        offer = client.offer.create(**fields)

        data = dict([(f, getattr(offer, f, '')) for f in
                    OFFER_RESOURCE.fields])

        return self.dict2columns(data)


class ListOffer(command.Lister):
    """List offers."""

    log = logging.getLogger(__name__ + ".ListOffer")

    def get_parser(self, prog_name):
        parser = super(ListOffer, self).get_parser(prog_name)

        parser.add_argument(
            '--long',
            default=False,
            help="Show detailed information about the offers.",
            action='store_true')
        parser.add_argument(
            '--status',
            dest='status',
            required=False,
            help="Show all offers with given status.")
        parser.add_argument(
            '--time-range',
            dest='time_range',
            nargs=2,
            required=False,
            help="Show all offers with start and end times "
                 "which begin and end in the given range."
                 "Must pass in two valid datetime strings."
                 "Example: --time-range 2020-06-30T00:00:00"
                 "2021-06-30T00:00:00")
        parser.add_argument(
            '--availability-range',
            dest='availability_range',
            nargs=2,
            required=False,
            help="Show all offers with availabilities "
                 "which will have no conflicting leases within "
                 "the given range. Must pass in two valid datetime "
                 "strings."
                 "Example: --availability-range 2020-06-30T00:00:00"
                 "2021-06-30T00:00:00")
        parser.add_argument(
            '--project',
            dest='project_id',
            required=False,
            help="Show all offers owned by given project ID or name.")
        parser.add_argument(
            '--resource-type',
            dest='resource_type',
            required=False,
            help="Show all offers with given resource-type.")
        parser.add_argument(
            '--resource-uuid',
            dest='resource_uuid',
            required=False,
            help="Show all offers with given resource-uuid.")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease

        filters = {
            'status': parsed_args.status,

            'start_time': str(parsed_args.time_range[0]) if
            parsed_args.time_range else None,
            'end_time': str(parsed_args.time_range[1]) if
            parsed_args.time_range else None,

            'available_start_time': str(parsed_args.availability_range[0]) if
            parsed_args.availability_range else None,
            'available_end_time': str(parsed_args.availability_range[1]) if
            parsed_args.availability_range else None,

            'project_id': parsed_args.project_id,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid
        }

        data = client.offer.list(filters)

        if parsed_args.long:
            columns = OFFER_RESOURCE.detailed_fields.keys()
            labels = OFFER_RESOURCE.detailed_fields.values()
        else:
            columns = OFFER_RESOURCE.fields.keys()
            labels = OFFER_RESOURCE.fields.values()

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))


class ShowOffer(command.ShowOne):
    """Show offer details."""

    log = logging.getLogger(__name__ + ".ShowOffer")

    def get_parser(self, prog_name):
        parser = super(ShowOffer, self).get_parser(prog_name)
        parser.add_argument(
            "uuid",
            metavar="<uuid>",
            help="UUID of the offer")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease

        offer = client.offer.get(parsed_args.uuid)._info

        return zip(*sorted(offer.items()))


class DeleteOffer(command.Command):
    """Unregister offer"""

    log = logging.getLogger(__name__ + ".DeleteOffer")

    def get_parser(self, prog_name):
        parser = super(DeleteOffer, self).get_parser(prog_name)
        parser.add_argument(
            "uuid",
            metavar="<uuid>",
            help="Offer to delete (UUID)")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease
        client.offer.delete(parsed_args.uuid)
        print('Deleted offer %s' % parsed_args.uuid)


class ClaimOffer(command.ShowOne):
    """Claim an offer."""

    log = logging.getLogger(__name__ + ".ClaimOffer")

    def get_parser(self, prog_name):
        parser = super(ClaimOffer, self).get_parser(prog_name)

        parser.add_argument(
            "offer_uuid",
            metavar="<offer_uuid>",
            help="Resource type")
        parser.add_argument(
            '--end-time',
            dest='end_time',
            required=False,
            help="Time when the offer will expire and no longer be "
                 "'available'.")
        parser.add_argument(
            '--start-time',
            dest='start_time',
            required=False,
            help="Time when the offer will be made 'available'.")
        parser.add_argument(
            '--properties',
            dest='properties',
            required=False,
            help="Record arbitrary key/value resource property "
                 "information. Pass in as a json object.")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.lease

        field_list = LEASE_RESOURCE._creation_attributes

        fields = dict((k, v) for (k, v) in vars(parsed_args).items()
                      if k in field_list and v is not None)

        if 'properties' in fields:
            fields['properties'] = json.loads(fields['properties'])

        lease = client.offer.claim(parsed_args.offer_uuid, **fields)

        data = dict([(f, getattr(lease, f, '')) for f in
                    LEASE_RESOURCE.fields])

        return self.dict2columns(data)
