import pytest
from tempest.lib.exceptions import CommandFailed

import esileapclient.tests.functional.utils.esi_interfaces as esi
from esileapclient.tests.functional.base import ESIBaseTestClass
from esileapclient.tests.functional.utils.dummy_node import DummyNode


class PolicyTests(ESIBaseTestClass):
    @classmethod
    def setUpClass(cls):
        super(PolicyTests, cls).setUpClass()
        cls._init_dummy_project(cls, 'authorized', 'owner')
        cls._init_dummy_project(cls, 'unauthorized', ['owner', 'lessee'])

    def setUp(self):
        super(PolicyTests, self).setUp()
        self.clients = PolicyTests.clients
        self.users = PolicyTests.users
        self.projects = PolicyTests.projects
        self.dummy_node = DummyNode(PolicyTests.config['dummy_node_dir'],
                                    self.projects['authorized']['id'])

    @pytest.mark.negative
    def test_offer_create_lessee(self):
        """ Tests that a lessee cannot create an offer.
            Test steps:
            1) Attempt to create an offer as a lessee.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr. """
        e = self.assertRaises(CommandFailed,
                              esi.offer_create,
                              self.clients['unauthorized-lessee'],
                              self.dummy_node.uuid,
                              resource_type='dummy_node')
        self.assertIn('Access was denied to esi_leap:offer:create.',
                      e.stderr.decode())

    @pytest.mark.negative
    def test_create_lessee(self):
        """ Tests that a lessee cannot create a lease.
            Test steps:
            1) Attempt to create a lease as a lessee (using lease create).
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr. """
        e = self.assertRaises(CommandFailed,
                              esi.lease_create,
                              self.clients['unauthorized-lessee'],
                              self.dummy_node.uuid,
                              self.projects['unauthorized']['name'],
                              resource_type='dummy_node')
        self.assertIn('Access was denied to esi_leap:lease:create.',
                      e.stderr.decode())

    @pytest.mark.negative
    def test_offer_delete_lessee(self):
        """ Tests that a lessee cannot delete an offer.
            Test steps:
            1) (authorized-owner) Create an offer for an owned node for the
                unauthorized project.
            2) Check that lease details were returned.
            3) (unauthorized-lessee) Attempt to delete the new offer.
            4) Check that the command failed. (returned non-zero exit code)
            5) Check that the proper error message was sent to stderr.
            6) (authorized-owner) (cleanup) Delete the offer from step 1. """
        offer = esi.offer_create(self.clients['authorized-owner'],
                                 self.dummy_node.uuid,
                                 lessee=self.projects['unauthorized']['name'],
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['authorized-owner'],
                        offer['uuid'])

        e = self.assertRaises(CommandFailed,
                              esi.offer_delete,
                              self.clients['unauthorized-lessee'],
                              offer['uuid'])
        self.assertIn('Access was denied to offer %s.' % offer['uuid'],
                      e.stderr.decode())

    @pytest.mark.negative
    def test_offer_create_unauthorized(self):
        """ Tests that an owner can't create an offer for a node that they
                do not own.
            Test steps:
            1) (unauthorized-owner) Attempt to create an offer for the dummy
                node owned by the authorized project.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr. """
        e = self.assertRaises(CommandFailed,
                              esi.offer_create,
                              self.clients['unauthorized-owner'],
                              self.dummy_node.uuid,
                              resource_type='dummy_node')
        self.assertIn('Access was denied to dummy_node %s.' %
                      self.dummy_node.uuid, e.stderr.decode())

    @pytest.mark.negative
    def test_lease_create_unauthorized(self):
        """ Tests that an owner can't create a lease on a node that they
                do not own.
            Test steps:
            1) (unauthorized-owner) Attempt to create a lease on the dummy
                node owned by the authorized project.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr. """
        e = self.assertRaises(CommandFailed,
                              esi.lease_create,
                              self.clients['unauthorized-owner'],
                              self.dummy_node.uuid,
                              self.projects['unauthorized']['name'],
                              resource_type='dummy_node')
        self.assertIn('Access was denied to dummy_node %s.' %
                      self.dummy_node.uuid, e.stderr.decode())

    @pytest.mark.negative
    def test_offer_delete_unauthorized(self):
        """ Tests that an owner can't delete an offer that they do not have
                access to.
            Test steps:
            1) (authorized-owner) Create an offer for an owned node.
            2) Check that offer details were returned.
            3) (unauthorized-owner) Attempt to delete the offer from step 1.
            4) Check that the command failed. (returned non-zero exit code)
            5) Check that the proper error message was sent to stderr.
            6) (authorized-owner) (cleanup) Delete the offer from step 1. """
        offer = esi.offer_create(self.clients['authorized-owner'],
                                 self.dummy_node.uuid,
                                 lessee=self.projects['authorized']['name'],
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['authorized-owner'],
                        offer['uuid'])

        e = self.assertRaises(CommandFailed,
                              esi.offer_delete,
                              self.clients['unauthorized-owner'],
                              offer['uuid'])
        self.assertIn('Access was denied to offer %s.' % offer['uuid'],
                      e.stderr.decode())

    @pytest.mark.negative
    def test_lease_delete_unauthorized(self):
        """ Tests that an owner can't delete a lease that they do not have
                access to.
            Test steps:
            1) (authorized-owner) Create a lease on an owned node.
            2) Check that lease details were returned.
            3) (unauthorized-owner) Attempt to delete the lease from step 1.
            4) Check that the command failed. (returned non-zero exit code)
            5) Check that the proper error message was sent to stderr.
            6) (authorized-owner) (cleanup) Delete the lease from step 1. """
        lease = esi.lease_create(self.clients['authorized-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['authorized']['name'],
                                 resource_type='dummy_node')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['authorized-owner'],
                        lease['uuid'])

        e = self.assertRaises(CommandFailed,
                              esi.lease_delete,
                              self.clients['unauthorized-owner'],
                              lease['uuid'])
        self.assertIn('Access was denied to lease %s.' % lease['uuid'],
                      e.stderr.decode())

    @pytest.mark.negative
    def test_offer_claim_unauthorized(self):
        """ Tests that a lessee can't claim an offer that they don't have
                access to.
            Test steps:
            1) (authorized-owner) Create an offer for an owned node,
                specifying a lessee that isn't the unauthorized project.
            2) Check that offer details were returned.
            3) (unauthorized-lessee) Attempt to claim the offer from step 1.
            4) Check that the command failed. (returned non-zero exit code)
            5) Check that the proper error message was sent to stderr.
            6) (authorized-owner) (cleanup) Delete the offer from step 1. """
        offer = esi.offer_create(self.clients['authorized-owner'],
                                 self.dummy_node.uuid,
                                 lessee=self.projects['authorized']['name'],
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['authorized-owner'],
                        offer['uuid'])

        e = self.assertRaises(CommandFailed,
                              esi.offer_claim,
                              self.clients['unauthorized-lessee'],
                              offer['uuid'])
        self.assertIn('Access was denied to offer %s.' % offer['uuid'],
                      e.stderr.decode())
