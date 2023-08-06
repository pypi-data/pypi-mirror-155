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

import copy
import json
import mock

from osc_lib import exceptions

from esileapclient.osc.v1.mdc import mdc_offer
from esileapclient.tests.unit.osc.v1 import base
from esileapclient.tests.unit.osc.v1 import fakes


class TestMDCOffer(base.TestESILeapCommand):

    def setUp(self):
        super(TestMDCOffer, self).setUp()

        self.client_mock = self.app.client_manager.lease
        self.client_mock.reset_mock()


class TestMDCOfferList(TestMDCOffer):
    def setUp(self):
        super(TestMDCOfferList, self).setUp()

        class FakeCloudRegion(object):
            def __init__(self, name, region):
                self.name = name
                self.config = {'region_name': region}

            def get_session(self):
                return None

        self.cloud1 = FakeCloudRegion('cloud1', 'regionOne')
        self.cloud2 = FakeCloudRegion('cloud2', 'regionTwo')
        self.offer1 = base.FakeResource(copy.deepcopy(fakes.OFFER))
        self.offer2 = base.FakeResource(copy.deepcopy(fakes.OFFER))
        self.cmd = mdc_offer.MDCListOffer(self.app, None)

    @mock.patch('esileapclient.v1.client.Client')
    @mock.patch('openstack.config.loader.OpenStackConfig.get_all_clouds')
    def test_mdc_offer_list(self, mock_clouds, mock_client):
        mock_clouds.return_value = [self.cloud1, self.cloud2]
        mock_client.return_value = self.client_mock
        self.client_mock.offer.list.side_effect = [[self.offer1],
                                                   [self.offer2]]

        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

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
            'resource_type': parsed_args.resource_type,
        }

        self.client_mock.offer.list.assert_called_with(filters)

        collist = [
            "Cloud",
            "Region",
            "UUID",
            "Resource",
            "Lessee",
            "Start Time",
            "End Time",
            "Status",
            "Availabilities"
        ]

        self.assertEqual(collist, list(columns))

        datalist = (('cloud1', 'regionOne',
                     fakes.offer_uuid,
                     fakes.lease_resource,
                     fakes.offer_lessee,
                     fakes.lease_start_time,
                     fakes.lease_end_time,
                     fakes.lease_status,
                     json.loads(fakes.lease_availabilities)
                     ),
                    ('cloud2', 'regionTwo',
                     fakes.offer_uuid,
                     fakes.lease_resource,
                     fakes.offer_lessee,
                     fakes.lease_start_time,
                     fakes.lease_end_time,
                     fakes.lease_status,
                     json.loads(fakes.lease_availabilities)
                     ))
        self.assertEqual(datalist, tuple(data))

    @mock.patch('esileapclient.v1.client.Client')
    @mock.patch('openstack.config.loader.OpenStackConfig.get_all_clouds')
    def test_mdc_offer_list_filter(self, mock_clouds, mock_client):
        mock_clouds.return_value = [self.cloud1, self.cloud2]
        mock_client.return_value = self.client_mock
        self.client_mock.offer.list.return_value = [self.offer2]

        arglist = ['--clouds', 'cloud2']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

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
            'resource_type': parsed_args.resource_type,
        }

        self.client_mock.offer.list.assert_called_with(filters)

        collist = [
            "Cloud",
            "Region",
            "UUID",
            "Resource",
            "Lessee",
            "Start Time",
            "End Time",
            "Status",
            "Availabilities"
        ]

        self.assertEqual(collist, list(columns))

        datalist = (('cloud2', 'regionTwo',
                     fakes.offer_uuid,
                     fakes.lease_resource,
                     fakes.offer_lessee,
                     fakes.lease_start_time,
                     fakes.lease_end_time,
                     fakes.lease_status,
                     json.loads(fakes.lease_availabilities)
                     ),)
        self.assertEqual(datalist, tuple(data))


class TestMDCOfferClaim(TestMDCOffer):
    def setUp(self):
        super(TestMDCOfferClaim, self).setUp()

        class FakeCloudRegion(object):
            def __init__(self, name, region):
                self.name = name
                self.config = {'region_name': region}

            def get_session(self):
                return None

        self.cloud1 = FakeCloudRegion('cloud1', 'regionOne')
        self.cloud2 = FakeCloudRegion('cloud2', 'regionTwo')
        self.offer1 = base.FakeResource(copy.deepcopy(fakes.OFFER))
        self.offer2 = base.FakeResource(copy.deepcopy(fakes.OFFER))
        self.offer3 = base.FakeResource(copy.deepcopy(fakes.OFFER))
        self.lease1 = base.FakeResource(copy.deepcopy(fakes.LEASE))
        self.lease2 = base.FakeResource(copy.deepcopy(fakes.LEASE))
        self.lease3 = base.FakeResource(copy.deepcopy(fakes.LEASE))
        self.cmd = mdc_offer.MDCClaimOffer(self.app, None)

    @mock.patch('esileapclient.v1.client.Client')
    @mock.patch('openstack.config.loader.OpenStackConfig.get_all_clouds')
    def test_mdc_offer_claim(self, mock_clouds, mock_client):
        mock_clouds.return_value = [self.cloud1, self.cloud2]
        mock_client.return_value = self.client_mock
        self.client_mock.offer.list.side_effect = [[self.offer1, self.offer2],
                                                   [self.offer3]]
        self.client_mock.offer.claim.side_effect = [self.lease1, self.lease2,
                                                    self.lease3]

        arglist = ['3', fakes.lease_start_time, fakes.lease_end_time]
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        list_filters = {
            'status': 'available',
            'available_start_time': str(parsed_args.start_time),
            'available_end_time': str(parsed_args.end_time),
            'resource_type': parsed_args.resource_type,
        }

        self.client_mock.offer.list.assert_called_with(list_filters)
        self.client_mock.offer.claim.assert_called_with(
            fakes.offer_uuid,
            start_time=str(parsed_args.start_time),
            end_time=str(parsed_args.end_time))

        collist = [
            "Cloud",
            "Region",
            "UUID",
            "Resource",
            "Project",
            "Start Time",
            "End Time",
            "Offer UUID",
            "Status"
        ]

        self.assertEqual(collist, list(columns))

        cloud1_lease = ('cloud1', 'regionOne',
                        fakes.lease_uuid,
                        fakes.lease_resource,
                        fakes.lease_project,
                        fakes.lease_start_time,
                        fakes.lease_end_time,
                        fakes.offer_uuid,
                        fakes.lease_status,
                        )
        cloud2_lease = ('cloud2', 'regionTwo',
                        fakes.lease_uuid,
                        fakes.lease_resource,
                        fakes.lease_project,
                        fakes.lease_start_time,
                        fakes.lease_end_time,
                        fakes.offer_uuid,
                        fakes.lease_status,
                        )

        parsed_data = tuple(data)
        self.assertEqual(3, len(parsed_data))
        self.assertEqual(2, parsed_data.count(cloud1_lease))
        self.assertEqual(1, parsed_data.count(cloud2_lease))

    @mock.patch('esileapclient.v1.client.Client')
    @mock.patch('openstack.config.loader.OpenStackConfig.get_all_clouds')
    def test_mdc_offer_claim_filter(self, mock_clouds, mock_client):
        mock_clouds.return_value = [self.cloud1, self.cloud2]
        mock_client.return_value = self.client_mock
        self.client_mock.offer.list.return_value = [self.offer1, self.offer2]
        self.client_mock.offer.claim.side_effect = [self.lease1, self.lease2]

        arglist = ['2', fakes.lease_start_time, fakes.lease_end_time,
                   '--clouds', 'cloud1']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        list_filters = {
            'status': 'available',
            'available_start_time': str(parsed_args.start_time),
            'available_end_time': str(parsed_args.end_time),
            'resource_type': parsed_args.resource_type,
        }

        self.client_mock.offer.list.assert_called_with(list_filters)
        self.client_mock.offer.claim.assert_called_with(
            fakes.offer_uuid,
            start_time=str(parsed_args.start_time),
            end_time=str(parsed_args.end_time))

        collist = [
            "Cloud",
            "Region",
            "UUID",
            "Resource",
            "Project",
            "Start Time",
            "End Time",
            "Offer UUID",
            "Status"
        ]

        self.assertEqual(collist, list(columns))

        cloud1_lease = ('cloud1', 'regionOne',
                        fakes.lease_uuid,
                        fakes.lease_resource,
                        fakes.lease_project,
                        fakes.lease_start_time,
                        fakes.lease_end_time,
                        fakes.offer_uuid,
                        fakes.lease_status,
                        )

        parsed_data = tuple(data)
        self.assertEqual(2, len(parsed_data))
        self.assertEqual(2, parsed_data.count(cloud1_lease))

    @mock.patch('esileapclient.v1.client.Client')
    @mock.patch('openstack.config.loader.OpenStackConfig.get_all_clouds')
    def test_mdc_offer_claim_not_enough_offers(self, mock_clouds, mock_client):
        mock_clouds.return_value = [self.cloud1, self.cloud2]
        mock_client.return_value = self.client_mock
        self.client_mock.offer.list.side_effect = [[self.offer1, self.offer2],
                                                   [self.offer3]]

        arglist = ['4', fakes.lease_start_time, fakes.lease_end_time]
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError,
                          self.cmd.take_action, parsed_args)

        list_filters = {
            'status': 'available',
            'available_start_time': str(parsed_args.start_time),
            'available_end_time': str(parsed_args.end_time),
            'resource_type': parsed_args.resource_type,
        }

        self.client_mock.offer.list.assert_called_with(list_filters)
