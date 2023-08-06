import time
import pytest

import esileapclient.tests.functional.utils.esi_interfaces as esi
from esileapclient.tests.functional.base import ESIBaseTestClass
from esileapclient.tests.functional.utils.dummy_node import DummyNode


class SubleaseTests(ESIBaseTestClass):
    @classmethod
    def setUpClass(cls):
        super(SubleaseTests, cls).setUpClass()
        cls._init_dummy_project(cls, 'node', 'owner')
        cls._init_dummy_project(cls, 'sublessee', 'owner')
        cls._init_dummy_project(cls, 'project', 'lessee')

    def setUp(self):
        super(SubleaseTests, self).setUp()
        self.clients = SubleaseTests.clients
        self.users = SubleaseTests.users
        self.projects = SubleaseTests.projects
        self.dummy_node = DummyNode(SubleaseTests.config['dummy_node_dir'],
                                    self.projects['node']['id'])

    @pytest.mark.slow
    def test_offer_create_sublease(self):
        """ Tests that an owner of a project that has leased a node can
                create offers for said leased node.
            Test steps:
            1) (node-owner) Create a lease on an owned node, specifying
                the sublessee project as the lessee.
            2) Check that offer details were returned.
            3) Wait for the esi-leap manager service to move the lease from
                the created state to the active state.
            4) (sublessee-owner) Create an offer for the node leased to the
                sublessee in step 1.
            5) Check that offer details were returned.
            6) (cleanup) (node-owner) Delete the offer from step 3.
            7) (cleanup) (authorized-owner) Delete the lease from step 1. """
        lease = esi.lease_create(self.clients['node-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['sublessee']['name'],
                                 resource_type='dummy_node')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['node-owner'],
                        lease['uuid'])

        time.sleep(65)

        offer = esi.offer_create(self.clients['sublessee-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['sublessee-owner'],
                        offer['uuid'])

    @pytest.mark.slow
    def test_lease_create_sublease(self):
        """ Tests that an owner of a project that has leased a node can
                create a lease on said leased node.
            Test steps:
            1) (node-owner) Create a lease on an owned node, specifying
                the sublessee project as the lessee.
            2) Check that offer details were returned.
            3) Wait for the esi-leap manager service to move the lease from
                the created state to the active state.
            4) (sublessee-owner) Create a lease on the node leased to the
                sublessee in step 1.
            5) Check that lease details were returned.
            6) (cleanup) (sublessee-owner) Delete the lease from step 3.
            7) (cleanup) (node-owner) Delete the lease from step 1. """
        lease = esi.lease_create(self.clients['node-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['sublessee']['name'],
                                 resource_type='dummy_node')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['node-owner'],
                        lease['uuid'])

        time.sleep(65)

        sublease = esi.lease_create(self.clients['sublessee-owner'],
                                    self.dummy_node.uuid,
                                    self.projects['project']['name'],
                                    resource_type='dummy_node')
        self.assertNotEqual(sublease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['sublessee-owner'],
                        sublease['uuid'])

    @pytest.mark.slow
    def test_offer_claim_sublease(self):
        """ Tests that an offer for a subleased node can be claimed.
            Test steps:
            1) (node-owner) Create a lease on an owned node, specifying
                the sublessee project as the lessee.
            2) Check that lease details were returned.
            3) Wait for the esi-leap manager service to move the lease from
                the created state to the active state.
            4) (sublessee-owner) Create an offer for the node leased to the
                sublessee in step 1.
            5) Check that offer details were returned.
            6) (project-lessee) Claim the offer created in step 3.
            7( Check that lease details were returned.
            8) (cleanup) (project-lessee) Delete the lease from step 5.
            9) (cleanup) (sublessee-owner) Delete the offer from step 3.
            10) (cleanup) (node-owner) Delete the lease from step 1. """
        lease = esi.lease_create(self.clients['node-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['sublessee']['name'],
                                 resource_type='dummy_node')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['node-owner'],
                        lease['uuid'])

        time.sleep(65)

        offer = esi.offer_create(self.clients['sublessee-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['sublessee-owner'],
                        offer['uuid'])

        sublease = esi.offer_claim(self.clients['project-lessee'],
                                   offer['uuid'])
        self.assertNotEqual(sublease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['project-lessee'],
                        sublease['uuid'])

    @pytest.mark.slow
    def test_offer_show_sublease_parent_deleted(self):
        """ Tests that offers made for a leased node are deleted after the
                node owning project deletes the original lease.
            Test steps:
            1) (node-owner) Create a lease on an owned node, specifying the
                sublessee project as the lessee.
            2) Check that lease details were returned.
            3) Wait for the esi-leap manager service to move the lease from
                the created state to the active state.
            4) (sublessee-owner) Create an offer for the node leased to the
                sublessee in step 1.
            5) Check that offer details were returned.
            6) Delete the offer created in step 1.
            7) View the details of the offer created in step 4 to ensure the
                offer's status is 'deleted'.
            8) (sublessee-owner) If not, delete the offer manually. """
        lease = esi.lease_create(self.clients['node-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['sublessee']['name'],
                                 resource_type='dummy_node')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['node-owner'],
                        lease['uuid'],
                        fail_ok=True)

        time.sleep(65)
        offer = esi.offer_create(self.clients['sublessee-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['sublessee-owner'],
                        offer['uuid'],
                        fail_ok=True)

        esi.lease_delete(self.clients['node-owner'], lease['uuid'])
        details = esi.offer_show(self.clients['sublessee-owner'],
                                 offer['uuid'])
        self.assertEqual(details['status'], 'deleted')

    @pytest.mark.slow
    def test_lease_show_sublease_parent_deleted(self):
        """ Tests that leases made on a leased node are deleted after the
                node owning project deletes the original lease.
            Test steps:
            1) (node-owner) Create a lease on an owned node, specifying the
                sublessee project as the lessee.
            2) Check that lease details were returned.
            3) Wait for the esi-leap manager service to move the lease from
                the created state to the active state.
            4) (sublessee-owner) Create a lease on the node leased to the
                sublessee in step 1.
            5) Check that lease details were returned.
            6) Delete the original lease created in step 1.
            7) View the details of the lease created in step 4 to ensure the
                lease's status is 'deleted'.
            8) (sublessee-owner) If not, delete the lease manually. """
        lease = esi.lease_create(self.clients['node-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['sublessee']['name'],
                                 resource_type='dummy_node')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['node-owner'],
                        lease['uuid'],
                        fail_ok=True)

        time.sleep(65)
        sublease = esi.lease_create(self.clients['sublessee-owner'],
                                    self.dummy_node.uuid,
                                    self.projects['project']['name'],
                                    resource_type='dummy_node')
        self.assertNotEqual(sublease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['sublessee-owner'],
                        sublease['uuid'],
                        fail_ok=True)

        esi.lease_delete(self.clients['node-owner'], lease['uuid'])
        details = esi.lease_show(self.clients['sublessee-owner'],
                                 sublease['uuid'])
        self.assertEqual(details['status'], 'deleted')
