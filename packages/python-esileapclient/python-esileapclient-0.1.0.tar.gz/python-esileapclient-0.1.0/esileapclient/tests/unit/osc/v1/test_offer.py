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
from osc_lib.tests import utils as osctestutils

from esileapclient.osc.v1 import offer
from esileapclient.tests.unit.osc.v1 import base
from esileapclient.tests.unit.osc.v1 import fakes


class TestOffer(base.TestESILeapCommand):

    def setUp(self):
        super(TestOffer, self).setUp()

        self.client_mock = self.app.client_manager.lease
        self.client_mock.reset_mock()


class TestOfferCreate(TestOffer):

    def setUp(self):
        super(TestOfferCreate, self).setUp()

        self.client_mock.offer.create.return_value = (
            base.FakeResource(copy.deepcopy(fakes.OFFER))
        )

        # Get the command object to test
        self.cmd = offer.CreateOffer(self.app, None)

    def test_offer_create(self):

        arglist = [
            fakes.lease_resource_uuid,
            '--end-time', fakes.lease_end_time,
            '--lessee', fakes.offer_lessee_id,
            '--name', fakes.offer_name,
            '--properties', fakes.lease_properties,
            '--resource-type', fakes.lease_resource_type,
            '--start-time', fakes.lease_start_time,
        ]

        verifylist = [
            ('end_time', fakes.lease_end_time),
            ('lessee_id', fakes.offer_lessee_id),
            ('name', fakes.offer_name),
            ('properties', fakes.lease_properties),
            ('resource_type', fakes.lease_resource_type),
            ('resource_uuid', fakes.lease_resource_uuid),
            ('start_time', fakes.lease_start_time),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        args = {
            'end_time': fakes.lease_end_time,
            'lessee_id': fakes.offer_lessee_id,
            'name': fakes.offer_name,
            'properties': json.loads(fakes.lease_properties),
            'resource_type': fakes.lease_resource_type,
            'resource_uuid': fakes.lease_resource_uuid,
            'start_time': fakes.lease_start_time,
        }

        self.client_mock.offer.create.assert_called_once_with(**args)


class TestOfferList(TestOffer):
    def setUp(self):
        super(TestOfferList, self).setUp()

        self.client_mock.offer.list.return_value = [
            base.FakeResource(copy.deepcopy(fakes.OFFER))
        ]
        self.cmd = offer.ListOffer(self.app, None)

    def test_offer_list(self):
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
            'project_id': parsed_args.project_id,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid
        }

        self.client_mock.offer.list.assert_called_with(filters)

        collist = [
            "UUID",
            "Resource",
            "Lessee",
            "Start Time",
            "End Time",
            "Status",
            "Availabilities"
        ]

        self.assertEqual(collist, list(columns))

        datalist = ((fakes.offer_uuid,
                     fakes.lease_resource,
                     fakes.offer_lessee,
                     fakes.lease_start_time,
                     fakes.lease_end_time,
                     fakes.lease_status,
                     json.loads(fakes.lease_availabilities)
                     ),)
        self.assertEqual(datalist, tuple(data))

    def test_offer_list_long(self):
        arglist = ['--long']
        verifylist = [('long', True)]

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
            'project_id': parsed_args.project_id,
            'resource_type': parsed_args.resource_type,
            'resource_uuid': parsed_args.resource_uuid
        }

        self.client_mock.offer.list.assert_called_with(filters)

        long_collist = [
            "Availabilities",
            "End Time",
            "Lessee",
            "Lessee ID",
            "Name",
            "Parent Lease UUID",
            "Project",
            "Project ID",
            "Properties",
            "Resource",
            "Resource Type",
            "Resource UUID",
            "Start Time",
            "Status",
            "UUID",
        ]

        self.assertEqual(long_collist, list(columns))

        datalist = ((json.loads(fakes.lease_availabilities),
                     fakes.lease_end_time,
                     fakes.offer_lessee,
                     fakes.offer_lessee_id,
                     fakes.offer_name,
                     fakes.parent_lease_uuid,
                     fakes.lease_project,
                     fakes.lease_project_id,
                     json.loads(fakes.lease_properties),
                     fakes.lease_resource,
                     fakes.lease_resource_type,
                     fakes.lease_resource_uuid,
                     fakes.lease_start_time,
                     fakes.lease_status,
                     fakes.offer_uuid
                     ),)
        self.assertEqual(datalist, tuple(data))


class TestOfferShow(TestOffer):
    def setUp(self):
        super(TestOfferShow, self).setUp()

        self.client_mock.offer.get.return_value = \
            base.FakeResource(copy.deepcopy(fakes.OFFER))

        self.cmd = offer.ShowOffer(self.app, None)

    def test_offer_show(self):
        arglist = [fakes.offer_uuid]
        verifylist = [('uuid', fakes.offer_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.client_mock.offer.get.assert_called_once_with(
            fakes.offer_uuid)

        collist = (
            "availabilities",
            "end_time",
            "lessee",
            "lessee_id",
            "name",
            "parent_lease_uuid",
            "project",
            "project_id",
            "properties",
            "resource",
            "resource_type",
            "resource_uuid",
            "start_time",
            "status",
            "uuid",
        )

        self.assertEqual(collist, columns)

        datalist = (json.loads(fakes.lease_availabilities),
                    fakes.lease_end_time,
                    fakes.offer_lessee,
                    fakes.offer_lessee_id,
                    fakes.offer_name,
                    fakes.parent_lease_uuid,
                    fakes.lease_project,
                    fakes.lease_project_id,
                    json.loads(fakes.lease_properties),
                    fakes.lease_resource,
                    fakes.lease_resource_type,
                    fakes.lease_resource_uuid,
                    fakes.lease_start_time,
                    fakes.lease_status,
                    fakes.offer_uuid
                    )
        self.assertEqual(datalist, tuple(data))

    def test_offer_show_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)


class TestOfferDelete(TestOffer):
    def setUp(self):
        super(TestOfferDelete, self).setUp()

        self.cmd = offer.DeleteOffer(self.app, None)

    def test_offer_delete(self):
        arglist = [fakes.offer_uuid]
        verifylist = [('uuid', fakes.offer_uuid)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        self.client_mock.offer.delete.assert_called_once_with(
            fakes.offer_uuid)

    def test_offer_delete_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)


class TestOfferClaim(TestOffer):
    def setUp(self):
        super(TestOfferClaim, self).setUp()

        self.cmd = offer.ClaimOffer(self.app, None)

    def test_offer_claim(self):
        arglist = [
            fakes.offer_uuid,
            '--end-time', fakes.lease_end_time,
            '--properties', fakes.lease_properties,
            '--start-time', fakes.lease_start_time,
        ]
        verifylist = [
            ('offer_uuid', fakes.offer_uuid),
            ('end_time', fakes.lease_end_time),
            ('properties', fakes.lease_properties),
            ('start_time', fakes.lease_start_time),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)

        lease_args = {
            'end_time': fakes.lease_end_time,
            'properties': json.loads(fakes.lease_properties),
            'start_time': fakes.lease_start_time,
        }

        self.client_mock.offer.claim.assert_called_once_with(
            fakes.offer_uuid, **lease_args)

    def test_offer_claim_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)
