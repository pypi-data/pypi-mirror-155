import time
import pytest
from datetime import datetime, timedelta
from tempest.lib.exceptions import CommandFailed

import esileapclient.tests.functional.utils.esi_interfaces as esi
from esileapclient.tests.functional.base import ESIBaseTestClass
from esileapclient.tests.functional.utils.dummy_node import DummyNode


class TimeTests(ESIBaseTestClass):
    @classmethod
    def setUpClass(cls):
        super(TimeTests, cls).setUpClass()
        cls._init_dummy_project(cls, 'main', 'owner')
        cls._init_dummy_project(cls, 'subproj1', ['owner', 'lessee'],
                                parent='main')
        cls._init_dummy_project(cls, 'subproj2', 'lessee', parent='main')

    def setUp(self):
        super(TimeTests, self).setUp()
        self.clients = TimeTests.clients
        self.users = TimeTests.users
        self.projects = TimeTests.projects
        self.dummy_node = DummyNode(TimeTests.config['dummy_node_dir'],
                                    self.projects['main']['id'])

    def test_offer_claim_multiple(self):
        """ Tests that more that one lessee can claim the same offer provided
                that the times specified do not conflict.
            Test steps:
            1) (owner) Create an offer for an owned node.
            2) Check that offer details were returned.
            3) Record what the time will be in five minutes.
            4) (subproj1) Claim the offer from step 1, starting at the time
                recorded in step 3 and ending 30 minutes from then.
            5) Check that lease details were returned.
            6) (subproj2) Claim the offer from step 1, starting five minutes
                after the end time of the lease created in step 4 and ending
                30 minutes from then.
            7) Check that lease details were returned.
            8) (owner) Check that both leases show up when listing leases.
            9) (subproj2) (cleanup) Delete the lease created in step 6.
            10) (subproj1) (cleanup) Delete the lease created in step 4.
            11) (owner) (cleanup) Delete the offer created in step 1. """
        offer = esi.offer_create(self.clients['main-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['main-owner'],
                        offer['uuid'])

        time_now = datetime.now()
        lease1_start_time = time_now + timedelta(minutes=5)
        lease1_end_time = lease1_start_time + timedelta(minutes=30)
        lease2_start_time = lease1_end_time + timedelta(minutes=5)
        lease2_end_time = lease2_start_time + timedelta(minutes=30)

        lease1 = esi.offer_claim(self.clients['subproj1-lessee'],
                                 offer['uuid'],
                                 start_time=str(lease1_start_time),
                                 end_time=str(lease1_end_time))
        self.assertNotEqual(lease1, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['subproj1-lessee'],
                        lease1['uuid'])

        lease2 = esi.offer_claim(self.clients['subproj2-lessee'],
                                 offer['uuid'],
                                 start_time=str(lease2_start_time),
                                 end_time=str(lease2_end_time))
        self.assertNotEqual(lease2, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['subproj2-lessee'],
                        lease2['uuid'])

        listings = esi.lease_list(self.clients['main-owner'])
        uuid_listings = [x['UUID'] for x in listings]
        self.assertNotEqual(listings, [])
        for lease_id in lease1['uuid'], lease2['uuid']:
            self.assertIn(lease_id, uuid_listings)

    def test_offer_create_multiple(self):
        """ Tests that more than one offer can be created for the same
                resource provided that the times specified do not conflict.
            Test steps:
            1) Record what the time will be in five minutes.
            2) Create an offer for an owned node, starting at the time
                recorded in step 1 and ending 30 minutes from then.
            3) Check that offer details were returned.
            4) Create an offer for the same node, starting five minutes after
               the end time of the offer created in step 2 and ending 30
               minutes from then.
            5) Check that offer details were returned.
            6) Check that both offers show up when listing offers.
            7) (cleanup) Delete the offer created in step 4.
            8) (cleanup) Delete the offer created in step 2. """
        time_now = datetime.now()
        offer1_start_time = time_now + timedelta(minutes=5)
        offer1_end_time = offer1_start_time + timedelta(minutes=30)
        offer2_start_time = offer1_end_time + timedelta(minutes=5)
        offer2_end_time = offer2_start_time + timedelta(minutes=30)

        offer1 = esi.offer_create(self.clients['main-owner'],
                                  self.dummy_node.uuid,
                                  resource_type='dummy_node',
                                  start_time=str(offer1_start_time),
                                  end_time=str(offer1_end_time))
        self.assertNotEqual(offer1, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['main-owner'],
                        offer1['uuid'])

        offer2 = esi.offer_create(self.clients['main-owner'],
                                  self.dummy_node.uuid,
                                  resource_type='dummy_node',
                                  start_time=str(offer2_start_time),
                                  end_time=str(offer2_end_time))
        self.assertNotEqual(offer2, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['main-owner'],
                        offer2['uuid'])

        listings = esi.offer_list(self.clients['main-owner'])
        uuid_listings = [x['UUID'] for x in listings]
        self.assertNotEqual(listings, [])
        for offer_id in offer1['uuid'], offer2['uuid']:
            self.assertIn(offer_id, uuid_listings)

    def test_lease_create_multiple(self):
        """ Tests that more than one lease can be created for the same
                resource provided that the times specified do not conflict.
            Test steps:
            1) Record what the time will be in five minutes.
            2) Create a lease on an owned node, starting at the time recorded
                in step 1 and ending 30 minutes from then.
            3) Check that lease details were returned.
            4) Create a lease on the same node, starting five minutes after
               the end time of the lease created in step 2 and ending 30
               minutes from then.
            5) Check that lease details were returned.
            6) Check that both lease show up when listing leases.
            7) (cleanup) Delete the lease created in step 4.
            8) (cleanup) Delete the lease created in step 2. """
        time_now = datetime.now()
        lease1_start_time = time_now + timedelta(minutes=5)
        lease1_end_time = lease1_start_time + timedelta(minutes=30)
        lease2_start_time = lease1_end_time + timedelta(minutes=5)
        lease2_end_time = lease2_start_time + timedelta(minutes=30)

        lease1 = esi.lease_create(self.clients['main-owner'],
                                  self.dummy_node.uuid,
                                  self.projects['main']['name'],
                                  resource_type='dummy_node',
                                  start_time=str(lease1_start_time),
                                  end_time=str(lease1_end_time))
        self.assertNotEqual(lease1, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['main-owner'],
                        lease1['uuid'])

        lease2 = esi.lease_create(self.clients['main-owner'],
                                  self.dummy_node.uuid,
                                  self.projects['main']['name'],
                                  resource_type='dummy_node',
                                  start_time=str(lease2_start_time),
                                  end_time=str(lease2_end_time))
        self.assertNotEqual(lease2, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['main-owner'],
                        lease2['uuid'])

        listings = esi.lease_list(self.clients['main-owner'])
        uuid_listings = [x['UUID'] for x in listings]
        self.assertNotEqual(listings, [])
        for lease_id in lease1['uuid'], lease2['uuid']:
            self.assertIn(lease_id, uuid_listings)

    @pytest.mark.negative
    def test_offer_claim_conflict(self):
        """ Tests that two lessees cannot make overlapping claims on the
                same offer.
            Test steps:
            1) (owner) Create an offer for an owned node.
            2) Check that offer details were returned.
            3) Record the current time.
            4) (subproj1) Claim the offer from step 1, ending 30 minutes
                after the time recorded in step 3.
            5) Check that lease details were returned.
            6) (subproj2) Attempt to claim the offer from step 1, starting
                15 minutes after the time recorded in step 3, and ending 30
                minutes after that.
            7) Check that the command failed. (returned non-zero exit code)
            8) Check that the proper error message was sent to stderr.
            9) (subproj1) (cleanup) Delete the lease created in step 4.
            10) (owner) (cleanup) Delete the offer created in step 1. """
        offer = esi.offer_create(self.clients['main-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['main-owner'],
                        offer['uuid'])

        time_now = datetime.now()
        lease1_end_time = time_now + timedelta(minutes=30)
        lease2_start_time = time_now + timedelta(minutes=15)
        lease2_end_time = lease2_start_time + timedelta(minutes=30)

        lease1 = esi.offer_claim(self.clients['subproj1-lessee'],
                                 offer['uuid'],
                                 end_time=str(lease1_end_time))
        self.assertNotEqual(lease1, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['subproj1-lessee'],
                        lease1['uuid'])

        e = self.assertRaises(CommandFailed,
                              esi.offer_claim,
                              self.clients['subproj2-lessee'],
                              offer['uuid'],
                              start_time=str(lease2_start_time),
                              end_time=str(lease2_end_time))
        err = ('Offer %s has no availabilities at given time range %s, %s' %
               (offer['uuid'], str(lease2_start_time), str(lease2_end_time)))
        self.assertIn(err, e.stderr.decode())

    @pytest.mark.negative
    def test_offer_create_conflict(self):
        """ Tests that two overlapping offers cannot be created for the
                same node.
            Test steps:
            1) Record the current time.
            2) Create an offer for an owned node, ending 30 minutes after the
                time recorded in step 1.
            3) Check that offer details were returned.
            4) Attempt to create another offer for the same node as in step 2,
                starting 15 minutes after the time recorded in step 1, and
                ending 30 minutes after that.
            5) Check that the command failed. (returned non-zero exit code)
            6) Check that the proper error message was sent to stderr.
            7) (cleanup) Delete the offer created in step 2. """
        time_now = datetime.now()
        offer1_end_time = time_now + timedelta(minutes=30)
        offer2_start_time = time_now + timedelta(minutes=15)
        offer2_end_time = offer2_start_time + timedelta(minutes=30)

        offer1 = esi.offer_create(self.clients['main-owner'],
                                  self.dummy_node.uuid,
                                  resource_type='dummy_node',
                                  end_time=str(offer1_end_time))
        self.assertNotEqual(offer1, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['main-owner'],
                        offer1['uuid'])

        e = self.assertRaises(CommandFailed,
                              esi.offer_create,
                              self.clients['main-owner'],
                              self.dummy_node.uuid,
                              resource_type='dummy_node',
                              start_time=str(offer2_start_time),
                              end_time=str(offer2_end_time))
        self.assertIn('Time conflict for dummy_node %s.' %
                      self.dummy_node.uuid,
                      e.stderr.decode())

    @pytest.mark.negative
    def test_lease_create_conflict(self):
        """ Tests that two overlapping leases cannot be created on the
                same node.
            Test steps:
            1) Record the current time.
            2) Create a lease on an owned node, ending 30 minutes after the
                time recorded in step 1.
            3) Check that lease details were returned.
            4) Attempt to create another lease on the same node as in step 2,
                starting 15 minutes after the time recorded in step 1, and
                ending 30 minutes after that.
            5) Check that the command failed. (returned non-zero exit code)
            6) Check that the proper error message was sent to stderr.
            7) (cleanup) Delete the lease created in step 2. """
        time_now = datetime.now()
        lease1_end_time = time_now + timedelta(minutes=30)
        lease2_start_time = time_now + timedelta(minutes=15)
        lease2_end_time = lease2_start_time + timedelta(minutes=30)

        lease1 = esi.lease_create(self.clients['main-owner'],
                                  self.dummy_node.uuid,
                                  self.projects['main']['name'],
                                  resource_type='dummy_node',
                                  end_time=str(lease1_end_time))
        self.assertNotEqual(lease1, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['main-owner'],
                        lease1['uuid'])

        e = self.assertRaises(CommandFailed,
                              esi.lease_create,
                              self.clients['main-owner'],
                              self.dummy_node.uuid,
                              self.projects['main']['name'],
                              resource_type='dummy_node',
                              start_time=str(lease2_start_time),
                              end_time=str(lease2_end_time))
        self.assertIn('Time conflict for dummy_node %s.' %
                      self.dummy_node.uuid,
                      e.stderr.decode())

    @pytest.mark.negative
    def test_offer_claim_out_of_range(self):
        """ Tests to ensure offers cannot be claimed for a time period that
                is outside of the range of the offer's availability.
            Test steps:
            1) Record the current time.
            2) (owner) Create an offer for an owned node, starting 15 minutes
                after the time recorded in step 1, and ending 30 minutes
                after that.
            3) Check that offer details were returned.
            4) Repeat steps 5 thru 7 with the following ranges (times are
                relative to the time recorded in step 1):
                - 5 minutes after thru 20 minutes after
                - 20 minutes after thru 60 minutes after
                - 5 minutes after thru 60 minutes after
            5) (subproj1) Attempt to claim the offer created in step 2 for a
                time range outside of what was specified during creation.
            6) Check that the command failed. (returned non-zero exit code)
            7) Check that the proper error message was sent to stderr.
            8) (owner) (cleanup) Delete the offer created in step 2. """
        time_now = datetime.now()
        offer_start_time = time_now + timedelta(minutes=15)
        offer_end_time = time_now + timedelta(minutes=30)
        claim_time_early = time_now + timedelta(minutes=5)
        claim_time_valid = offer_start_time + timedelta(minutes=15)
        claim_time_late = offer_end_time + timedelta(minutes=15)

        offer = esi.offer_create(self.clients['main-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node',
                                 start_time=str(offer_start_time),
                                 end_time=str(offer_end_time))
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['main-owner'],
                        offer['uuid'])

        for (start, end) in ((claim_time_early, claim_time_valid),
                             (claim_time_valid, claim_time_late),
                             (claim_time_early, claim_time_late)):
            err = ('Offer %s has no availabilities at given time range %s, %s.'
                   % (offer['uuid'], str(start), str(end)))
            e = self.assertRaises(CommandFailed,
                                  esi.offer_claim,
                                  self.clients['subproj1-lessee'],
                                  offer['uuid'],
                                  start_time=str(start),
                                  end_time=str(end))
            self.assertIn(err, e.stderr.decode())

    @pytest.mark.negative
    @pytest.mark.slow
    def test_offer_create_sublease_out_of_range(self):
        """ Tests to ensure an offer for a leased node cannot be created for
                a time period outside of the original lease's availability.
            Test steps:
            1) Record the current time.
            2) (main-owner) Create a lease for an owned node, ending 30
                minutes after the time recorded in step 1.
            3) Check that lease details were returned.
            4) Wait for the esi-leap manager service to move the lease from
                the created state to the active state.
            5) (subproj1-owner) Attempt to create an offer on the node leased
                in step 2, starting 15 minutes after the time recorded in
                step 1, and ending 45 minutes after.
            6) Check that the command failed. (returned non-zero exit code)
            7) Check that the proper error message was sent to stderr.
            8) (main-owner) (cleanup) Delete the offer created in step 2. """
        time_now = datetime.now()
        lease_end_time = time_now + timedelta(minutes=30)
        offer_start_time = time_now + timedelta(minutes=15)
        offer_end_time = time_now + timedelta(minutes=45)

        lease = esi.lease_create(self.clients['main-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['subproj1']['name'],
                                 resource_type='dummy_node',
                                 end_time=str(lease_end_time))
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['main-owner'],
                        lease['uuid'])

        time.sleep(65)

        err = ('You do not have permissions on dummy_node %s for the time '
               'range %s - %s.') % (self.dummy_node.uuid,
                                    str(offer_start_time), str(offer_end_time))
        e = self.assertRaises(CommandFailed,
                              esi.offer_create,
                              self.clients['subproj1-owner'],
                              self.dummy_node.uuid,
                              resource_type='dummy_node',
                              start_time=str(offer_start_time),
                              end_time=str(offer_end_time))
        self.assertIn(err, e.stderr.decode())

    @pytest.mark.negative
    @pytest.mark.slow
    def test_offer_expire(self):
        """ Tests to ensure expired offers cannot be claimed and that they
                do not show up in the list of offers after expiring.
            Test steps:
            1) Record what the time will be in 30 seconds.
            2) (owner) Create an offer for an owned node that ends at the time
                recorded in step 1.
            3) Check that offer details were returned and that the offer's
                status is 'available'.
            4) Wait 100 seconds to allow the esi-leap manager to move the
                offer from the 'available' state to the 'expired' state.
            5) (owner) Check that state of the offer from step 2 is 'expired'.
            6) (subproj1) Attempt to claim the expired offer.
            7) Check that the command failed. (returned non-zero exit code)
            8) Check that the proper error message was sent to stderr.
            9) (subproj1) Check that the offer does not show up in the list
                of available offers.
            10) (owner) (cleanup) Delete the offer from step 2 if needed. """
        time_now = datetime.now()
        offer_end_time = time_now + timedelta(seconds=30)

        offer = esi.offer_create(self.clients['main-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node',
                                 lessee=self.projects['subproj1']['name'],
                                 end_time=str(offer_end_time))
        self.assertNotEqual(offer, {})
        # NOTE: this ensures the offer is deleted, ignoring failed attempts
        # to delete offers that expired correctly.
        self.addCleanup(esi.offer_delete,
                        self.clients['main-owner'],
                        offer['uuid'],
                        fail_ok=True)
        self.assertEqual(offer['status'], 'available')

        time.sleep(100)

        details = esi.offer_show(self.clients['main-owner'], offer['uuid'])
        self.assertEqual(details['status'], 'expired')

        e = self.assertRaises(CommandFailed,
                              esi.offer_claim,
                              self.clients['subproj1-lessee'],
                              offer['uuid'])
        self.assertIn('Offer with name or uuid %s not found.' % offer['uuid'],
                      e.stderr.decode())

        listings = esi.offer_list(self.clients['subproj1-lessee'])
        self.assertNotIn(offer['uuid'], [x['UUID'] for x in listings])

    @pytest.mark.negative
    @pytest.mark.slow
    def test_lease_expire(self):
        """ Tests to ensure expired leases do not show up in the list of
                leases after expiring.
            Test steps:
            1) Record what the time will be in 30 seconds.
            2) Create an lease on an owned node that ends at the time recorded
                in step 1.
            3) Check that lease details were returned and that the lease's
                status is either 'created' or 'active'.
            4) Wait 100 seconds to allow the esi-leap manager to move the
                lease into the 'expired' state.
            5) Check that state of the lease from step 2 is 'expired'.
            6) Check that the lease does not show up in the list
                of leases.
            7) (cleanup) Delete the lease from step 2 if needed. """
        time_now = datetime.now()
        lease_end_time = time_now + timedelta(seconds=30)

        lease = esi.lease_create(self.clients['main-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['main']['name'],
                                 resource_type='dummy_node',
                                 end_time=str(lease_end_time))
        self.assertNotEqual(lease, {})
        # NOTE: this ensures the lease is deleted, ignoring failed attempts
        # to delete leases that expired correctly.
        self.addCleanup(esi.lease_delete,
                        self.clients['main-owner'],
                        lease['uuid'],
                        fail_ok=True)
        self.assertIn(lease['status'], ('created', 'active'))

        time.sleep(100)

        details = esi.lease_show(self.clients['main-owner'], lease['uuid'])
        self.assertEqual(details['status'], 'expired')

        listings = esi.lease_list(self.clients['main-owner'])
        self.assertNotIn(lease['uuid'], [x['UUID'] for x in listings])
