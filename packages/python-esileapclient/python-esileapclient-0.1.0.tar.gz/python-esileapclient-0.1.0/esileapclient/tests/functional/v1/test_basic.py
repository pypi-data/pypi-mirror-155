import pytest
from tempest.lib.exceptions import CommandFailed
from tempest.lib.common.utils import data_utils

import esileapclient.tests.functional.utils.esi_interfaces as esi
from esileapclient.tests.functional.base import ESIBaseTestClass
from esileapclient.tests.functional.utils.dummy_node import DummyNode


class BasicTests(ESIBaseTestClass):
    @classmethod
    def setUpClass(cls):
        super(BasicTests, cls).setUpClass()
        cls._init_dummy_project(cls, 'parent', 'owner')
        cls._init_dummy_project(cls, 'child', 'lessee', parent='parent')

    def setUp(self):
        super(BasicTests, self).setUp()
        self.clients = BasicTests.clients
        self.users = BasicTests.users
        self.projects = BasicTests.projects
        self.dummy_node = DummyNode(BasicTests.config['dummy_node_dir'],
                                    self.projects['parent']['id'])

    def test_offer_create_basic(self):
        """ Tests that a node owner can create and delete an offer for a node
                that they own.
            Test steps:
            1) Create an offer for an owned node.
            2) Check that offer details were returned.
            3) (cleanup) Delete the offer created in step 1. """
        offer = esi.offer_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['parent-owner'],
                        offer['uuid'])

    def test_offer_list_basic(self):
        """ Tests basic functionality of "esi offer list" when executed by
                both node owners and lessees with access to offers.
            Test steps:
            1) (owner) Create an offer for an owned node.
            2) Check that offer details were returned.
            3) (owner) Check that the output of 'offer list' contains the new
                offer.
            4) (lessee) Check that the output of 'offer list' contains the
                new offer.
            5) (cleanup) (owner) Delete the offer created in step 1. """
        offer = esi.offer_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node',
                                 lessee=self.projects['child']['name'])
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['parent-owner'],
                        offer['uuid'])

        for client_name in 'parent-owner', 'child-lessee':
            listings = esi.offer_list(self.clients[client_name])
            self.assertNotEqual(listings, [])
            self.assertIn(offer['uuid'], [x['UUID'] for x in listings])

    def test_offer_show_basic(self):
        """ Tests basic functionality of "esi offer show" when executed by
                both node owners and lessees with access to offers.
            Test steps:
            1) (owner) Create an offer for an owned node.
            2) Check that offer details were returned.
            3) (owner) Check that the output of 'offer show' contains the
                details of the offer.
            4) (lessee) Check that the output of 'offer show' contains the
                details of the new offer.
            5) (cleanup) (owner) Delete the offer created in step 1. """
        offer = esi.offer_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node',
                                 lessee=self.projects['child']['name'])
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['parent-owner'],
                        offer['uuid'])

        for client_name in 'parent-owner', 'child-lessee':
            details = esi.offer_show(self.clients[client_name], offer['uuid'])
            for field in offer.keys():
                self.assertEqual(offer[field], details[field])

    def test_offer_claim_basic(self):
        """ Tests that a lessee can claim an offer made available to them
                and delete the created lease when finished.
            Test steps:
            1) (owner) Create an offer for an owned node.
            2) Check that offer details were returned.
            3) (lessee) Claim the offer created in step 1.
            4) Check that lease details were returned.
            5) (cleanup) (lessee) Delete the lease created in step 3.
            6) (cleanup) (owner) Delete the offer created in step 1. """
        offer = esi.offer_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node',
                                 lessee=self.projects['child']['name'])
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['parent-owner'],
                        offer['uuid'])

        lease = esi.offer_claim(self.clients['child-lessee'],
                                offer['uuid'])
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['child-lessee'],
                        lease['uuid'])

    def test_lease_create_basic(self):
        """ Tests that a node owner can create and delete a lease on a node
                that they own.
            Test steps:
            1) Create a lease on an owned node.
            2) Check that lease details were returned.
            3) (cleanup) Delete the lease created in step 1. """
        lease = esi.lease_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['child']['name'],
                                 resource_type='dummy_node',
                                 start_time='9999-01-01')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['parent-owner'],
                        lease['uuid'])

    def test_lease_list_basic(self):
        """ Tests basic functionality of "esi lease list" when executed by
                a node owner.
            Test steps:
            1) Create a lease on an owned node.
            2) Check that lease details were returned.
            3) Check that the output of 'lease list' contains the new lease.
            4) (cleanup) Delete the lease created in step 1. """
        lease = esi.lease_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['child']['name'],
                                 resource_type='dummy_node',
                                 start_time='9999-01-01')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['parent-owner'],
                        lease['uuid'])

        listings = esi.lease_list(self.clients['parent-owner'])
        self.assertNotEqual(listings, [])
        self.assertIn(lease['uuid'], [x['UUID'] for x in listings])

    def test_lease_show_basic(self):
        """ Tests basic functionality of "esi lease show" when executed by
                both node owners and the lessee of the lease.
            Test steps:
            1) (owner) Create a lease on an owned node.
            2) Check that offer details were returned.
            3) (owner) Check that the output of 'offer show' contains the
                details of the offer.
            4) (lessee) Check that the output of 'offer show' contains the
                details of the new offer.
            5) (cleanup) (owner) Delete the offer created in step 1. """
        lease = esi.lease_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['child']['name'],
                                 resource_type='dummy_node',
                                 start_time='9999-01-01')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['parent-owner'],
                        lease['uuid'])

        for client_name in 'parent-owner', 'child-lessee':
            details = esi.lease_show(self.clients[client_name], lease['uuid'])
            for field in lease.keys():
                self.assertEqual(lease[field], details[field])

    def test_lease_show_offer_deleted(self):
        """ Tests that leases created thru claiming an offer are deleted after
                the claimed offer has been deleted.
            Test steps:
            1) (owner) Create an offer for an owned node.
            2) Check that offer details were returned.
            3) (lessee) Claim the offer created in step 1.
            4) Check that lease details were returned.
            5) (owner) Delete the offer created in step 1.
            6) View the details of the lease created in step 4 to ensure the
                lease's status is 'deleted'.
            7) (lessee) If not, delete the lease manually. """
        offer = esi.offer_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node',
                                 lessee=self.projects['child']['name'])
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['parent-owner'],
                        offer['uuid'],
                        fail_ok=True)

        lease = esi.offer_claim(self.clients['child-lessee'],
                                offer['uuid'])
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['child-lessee'],
                        lease['uuid'],
                        fail_ok=True)

        esi.offer_delete(self.clients['parent-owner'], offer['uuid'])
        details = esi.lease_show(self.clients['child-lessee'], lease['uuid'])
        self.assertEqual(details['status'], 'deleted')

    @pytest.mark.negative
    def test_offer_show_invalid_id(self):
        """ Tests that "esi offer show" properly handles being passed an
                offer uuid that does not exist.
            Test steps:
            1) Attempt to show details of an offer that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr. """
        fake_name = data_utils.rand_name('does-not-exist', prefix='')
        e = self.assertRaises(CommandFailed,
                              esi.offer_show,
                              self.clients['parent-owner'],
                              fake_name)
        self.assertIn('Offer with name or uuid %s not found.' % fake_name,
                      e.stderr.decode())

    @pytest.mark.negative
    def test_lease_show_invalid_id(self):
        """ Tests that "esi lease show" properly handles being passed a
                lease uuid that does not exist.
            Test steps:
            1) Attempt to show details of a lease that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr. """
        fake_name = data_utils.rand_name('does-not-exist', prefix='')
        e = self.assertRaises(CommandFailed,
                              esi.lease_show,
                              self.clients['parent-owner'],
                              fake_name)
        self.assertIn('Lease with name or uuid %s not found.' % fake_name,
                      e.stderr.decode())

    @pytest.mark.negative
    def test_offer_delete_invalid_id(self):
        """ Tests that "esi offer delete" properly handles being passed an
                offer uuid that does not exist.
            Test steps:
            1) Attempt to delete an offer that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr. """
        fake_name = data_utils.rand_name('does-not-exist', prefix='')
        e = self.assertRaises(CommandFailed,
                              esi.offer_delete,
                              self.clients['parent-owner'],
                              fake_name)
        self.assertIn('Offer with name or uuid %s not found.' % fake_name,
                      e.stderr.decode())

    @pytest.mark.negative
    def test_lease_delete_invalid_id(self):
        """ Tests that "esi lease delete" properly handles being passed a
                lease uuid that does not exist.
            Test steps:
            1) Attempt to delete a lease that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr. """
        fake_name = data_utils.rand_name('does-not-exist', prefix='')
        e = self.assertRaises(CommandFailed,
                              esi.lease_delete,
                              self.clients['parent-owner'],
                              fake_name)
        self.assertIn('Lease with name or uuid %s not found.' % fake_name,
                      e.stderr.decode())

    @pytest.mark.negative
    def test_offer_claim_invalid_id(self):
        """ Tests that "esi offer claim" properly handles being passed an
                offer uuid that does not exist.
            Test steps:
            1) Attempt to claim an offer that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr. """
        fake_name = data_utils.rand_name('does-not-exist', prefix='')
        e = self.assertRaises(CommandFailed,
                              esi.offer_claim,
                              self.clients['child-lessee'],
                              fake_name)
        self.assertIn('Offer with name or uuid %s not found.' % fake_name,
                      e.stderr.decode())

    @pytest.mark.negative
    def test_create_invalid_node(self):
        """ Tests that "esi [offer/lease] create" properly handles being
                passed a resource node uuid that does not exist.
            Test steps:
            1) Attempt to create an offer for a node that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr.
            4) Attempt to create a lease for a node that does not exist.
            5) Check that the command failed. (returned non-zero exit code)
            6) Check that the proper error message was sent to stderr. """
        fake_name = data_utils.rand_name('does-not-exist', prefix='')
        e = self.assertRaises(CommandFailed,
                              esi.offer_create,
                              self.clients['parent-owner'],
                              fake_name,
                              resource_type='dummy_node')
        self.assertIn('No such file or directory', e.stderr.decode())

        e = self.assertRaises(CommandFailed,
                              esi.lease_create,
                              self.clients['parent-owner'],
                              fake_name,
                              self.projects['child']['name'],
                              resource_type='dummy_node')
        self.assertIn('No such file or directory', e.stderr.decode())

    @pytest.mark.negative
    def test_create_invalid_resource_type(self):
        """ Tests that "esi [offer/lease] create" properly handles being
                passed a resource type that does not exist.
            Test steps:
            1) Attempt to create an offer for a node with a resource type
                that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr.
            4) Attempt to create a lease on a node with a resource type
                that does not exist.
            5) Check that the command failed. (returned non-zero exit code)
            6) Check that the proper error message was sent to stderr. """
        fake_node = data_utils.rand_name('does-not-exist', prefix='')
        fake_type = data_utils.rand_name('does-not-exist', prefix='')

        e = self.assertRaises(CommandFailed,
                              esi.offer_create,
                              self.clients['parent-owner'],
                              fake_node,
                              resource_type=fake_type)
        self.assertIn('%s resource type unknown.' % fake_type,
                      e.stderr.decode())

        e = self.assertRaises(CommandFailed,
                              esi.lease_create,
                              self.clients['parent-owner'],
                              fake_node,
                              self.projects['child']['name'],
                              resource_type=fake_type)
        self.assertIn('%s resource type unknown.' % fake_type,
                      e.stderr.decode())
