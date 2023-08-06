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

import openstack
from osc_lib.command import command
from osc_lib import utils as oscutils

from esileapclient.v1 import client as esileapclient
from esileapclient.v1.lease import Lease as LEASE_RESOURCE

LOG = logging.getLogger(__name__)


class MDCListLease(command.Lister):
    """List leases across multiple data centers."""

    log = logging.getLogger(__name__ + ".MDCListLease")
    auth_required = False

    def get_parser(self, prog_name):
        parser = super(MDCListLease, self).get_parser(prog_name)

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
            help="Show all leases with given status.")
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
            '--resource-type',
            dest='resource_type',
            required=False,
            help="Show all leases with given resource-type.")

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
            'resource_type': parsed_args.resource_type,
        }

        for c in cloud_regions:
            client = esileapclient.Client(session=c.get_session())

            leases = client.lease.list(filters)
            for lease in leases:
                lease.cloud = c.name
                lease.region = c.config['region_name']
                data += [lease]

        columns = ['cloud', 'region'] + list(LEASE_RESOURCE.fields.keys())
        labels = ['Cloud', 'Region'] + list(LEASE_RESOURCE.fields.values())

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))
