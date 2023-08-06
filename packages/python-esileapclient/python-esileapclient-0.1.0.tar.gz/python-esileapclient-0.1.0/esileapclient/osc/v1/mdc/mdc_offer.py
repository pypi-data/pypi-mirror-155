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
import random

import openstack
from osc_lib.command import command
from osc_lib import exceptions
from osc_lib import utils as oscutils

from esileapclient.v1 import client as esileapclient
from esileapclient.v1.lease import Lease as LEASE_RESOURCE
from esileapclient.v1.offer import Offer as OFFER_RESOURCE

LOG = logging.getLogger(__name__)


class MDCListOffer(command.Lister):
    """List offers across multiple data centers."""

    log = logging.getLogger(__name__ + ".MDCListOffer")
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(MDCListOffer, self).get_parser(prog_name)

        parser.add_argument(
            '--clouds',
            dest='clouds',
            metavar='<clouds>',
            nargs="+",
            help="Specify the cloud to use from clouds.yaml."
        )
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
            '--resource-type',
            dest='resource_type',
            required=False,
            help="Show all offers with given resource-type.")

        return parser

    def take_action(self, parsed_args):
        data = []

        cloud_regions = openstack.config.loader.OpenStackConfig().\
            get_all_clouds()
        if parsed_args.clouds:
            cloud_regions = filter(lambda c: c.name in parsed_args.clouds,
                                   cloud_regions)
        filters = {
            'status': parsed_args.status,
            'start_time': str(parsed_args.time_range[0]) if
            parsed_args.time_range else None,
            'end_time': str(parsed_args.time_range[1]) if
            parsed_args.time_range else None,
            'available_start_time': str(
                parsed_args.availability_range[0]) if
            parsed_args.availability_range else None,
            'available_end_time': str(parsed_args.availability_range[1]) if
            parsed_args.availability_range else None,
            'resource_type': parsed_args.resource_type,
        }

        for c in cloud_regions:
            client = esileapclient.Client(session=c.get_session())

            offers = client.offer.list(filters)
            for offer in offers:
                offer.cloud = c.name
                offer.region = c.config['region_name']
                data += [offer]

        columns = ['cloud', 'region'] + list(OFFER_RESOURCE.fields.keys())
        labels = ['Cloud', 'Region'] + list(OFFER_RESOURCE.fields.values())

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))


class MDCClaimOffer(command.Lister):
    """Claim offers across multiple data centers."""

    log = logging.getLogger(__name__ + ".MDCClaimOffer")
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(MDCClaimOffer, self).get_parser(prog_name)

        parser.add_argument(
            "node_count",
            metavar="<node_count>",
            help="Number of nodes to claim")
        parser.add_argument(
            'start_time',
            metavar='<start_time>',
            help="Time when the lease will start.")
        parser.add_argument(
            'end_time',
            metavar='<end_time>',
            help="Time when the lease will expire.")
        parser.add_argument(
            '--clouds',
            dest='clouds',
            metavar='<clouds>',
            nargs="+",
            help="Specify the cloud to use from clouds.yaml."
        )
        parser.add_argument(
            '--resource-type',
            dest='resource_type',
            required=False,
            help="Show all offers with given resource-type.")

        return parser

    def take_action(self, parsed_args):
        cloud_regions = openstack.config.loader.OpenStackConfig().\
            get_all_clouds()
        if parsed_args.clouds:
            cloud_regions = filter(lambda c: c.name in parsed_args.clouds,
                                   cloud_regions)
        node_count = int(parsed_args.node_count)
        filters = {
            'status': 'available',
            'available_start_time': str(parsed_args.start_time) if
            parsed_args.start_time else None,
            'available_end_time': str(parsed_args.end_time) if
            parsed_args.end_time else None,
            'resource_type': parsed_args.resource_type,
        }

        available_offers = []
        for c in cloud_regions:
            client = esileapclient.Client(session=c.get_session())
            offers = client.offer.list(filters)
            for offer in offers:
                offer.cloud_region = c
                offer.cloud = c.name
                offer.region = c.config['region_name']
                available_offers += [offer]

        if node_count > len(available_offers):
            raise exceptions.CommandError(
                "ERROR: Not enough offers found")

        offers_to_claim = random.sample(available_offers, node_count)
        leases = []
        for offer in offers_to_claim:
            client = esileapclient.Client(
                session=offer.cloud_region.get_session())
            try:
                lease = client.offer.claim(
                    offer.uuid,
                    **{'start_time': parsed_args.start_time,
                       'end_time': parsed_args.end_time})
                lease.cloud = offer.cloud
                lease.region = offer.region
                leases += [lease]
            except exceptions.CommandError:
                # offer is no longer available during this time range; continue
                # but let user know
                print("Offer %s is no longer available; continuing"
                      % offer.uuid)

        columns = ['cloud', 'region'] + list(LEASE_RESOURCE.fields.keys())
        labels = ['Cloud', 'Region'] + list(LEASE_RESOURCE.fields.values())

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in leases))
