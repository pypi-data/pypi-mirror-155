import copy

from esileapclient.osc.v1 import node
from esileapclient.tests.unit.osc.v1 import base
from esileapclient.tests.unit.osc.v1 import fakes


class TestNode(base.TestESILeapCommand):

    def setUp(self):
        super(TestNode, self).setUp()

        self.client_mock = self.app.client_manager.lease
        self.client_mock.reset_mock()


class TestNodeList(TestNode):

    def setUp(self):
        super(TestNodeList, self).setUp()

        self.client_mock.node.list.return_value = [
            base.FakeResource(copy.deepcopy(fakes.NODE))
        ]
        self.cmd = node.ListNode(self.app, None)

    def test_node_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
        }

        self.client_mock.node.list.assert_called_with(filters)

        collist = [
            "Name",
            "Owner",
            "Offer UUID",
            "Lease UUID",
            "Lessee"
        ]

        self.assertEqual(collist, list(columns))

        datalist = ((fakes.node_name,
                     fakes.node_owner,
                     '', '', ''
                     ),)
        self.assertEqual(datalist, tuple(data))

    def test_node_list_long(self):
        arglist = ['--long']
        verifylist = [('long', True)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        filters = {
        }

        self.client_mock.node.list.assert_called_with(filters)

        long_collist = [
            "Name",
            "UUID",
            "Owner",
            "Offer UUID",
            "Lease UUID",
            "Lessee",
            "Future Offers",
            "Future Leases"
        ]

        self.assertEqual(long_collist, list(columns))

        datalist = ((fakes.node_name,
                     fakes.node_uuid,
                     fakes.node_owner,
                     '', '', '', '', ''
                     ),)
        self.assertEqual(datalist, tuple(data))
