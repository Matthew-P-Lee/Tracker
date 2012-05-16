#!/usr/bin/env python

import tracker
import unittest
import uuid
import config
from datetime import datetime
import pdb
import time

class TestTracker(unittest.TestCase):	
	
	@classmethod
	def setUpClass(cls):
		cls.deleteTestData()
		cls.loadTestData()

#	@classmethod
#	def tearDownClass(cls):
#		cls.deleteTestData()

	@classmethod	
	def loadTestData(cls):
		track = tracker.Tracker()
		myCampaign = str(datetime.now())
		
		#set 2 different UID for the same client
		track.SetCustomer(1,config.TEST_UID)
		track.SetCustomer(1,config.TEST_UID2)
		track.SetCustomer(1,config.TEST_UID2)
		
		#should not add dupes
		track.SetCustomer(3,config.TEST_UID)
		track.SetCustomer(3,config.TEST_UID)
		track.SetCustomer(3,config.TEST_UID)
			
		#only load events if none
		items = track.GetEvents(config.TEST_UID)
		
		#pdb.set_trace()
		
		#create 4 test events for each UID
		if len(list(items)) == 0:		
			print track.SetEvent(config.TEST_UID,'1',config.TEST_URL)
			time.sleep(1)
			print track.SetEvent(config.TEST_UID,'2',config.TEST_URL)
			time.sleep(1)
			print track.SetEvent(config.TEST_UID,'3',config.TEST_URL)
			time.sleep(1)
			print track.SetEvent(config.TEST_UID,'4',config.TEST_URL)		 		
			time.sleep(1)
			print track.SetEvent(config.TEST_UID2,'5',config.TEST_URL)
			time.sleep(1)
			print track.SetEvent(config.TEST_UID2,'6',config.TEST_URL)
			time.sleep(1)
			print track.SetEvent(config.TEST_UID2,'7',config.TEST_URL)
			time.sleep(1)
			print track.SetEvent(config.TEST_UID2,'8',config.TEST_URL)		 

	@classmethod
	def deleteTestData(cls):
		track = tracker.Tracker()
		items = list(track.GetCustomers(1))			
		
		for i in items:
			track.DeleteEvent(i['CustomerId'])

		track.DeleteCustomers(1)
		track.DeleteCustomers(3)
		
	def test_GetEvents(self):
		track = tracker.Tracker()
		items = track.GetEvents(config.TEST_UID)	

		assert(len(list(items)) == 4)
		
	def test_GetCustomers(self):
		track = tracker.Tracker()
		
		c1 = track.GetCustomers(1)	
		c2 = track.GetCustomers(3)	

		assert(len(list(c1)) == 2)
		assert(len(list(c2)) == 1)
		
		for cust in c1:
			print cust['ClientId'],cust['CustomerId']
		
	def test_GetItems(self):
		track = tracker.Tracker()
		items = track.GetCustomers(3)			
				
		for i in items:
			items2 = track.GetEvents(i['CustomerId'])		
			assert(len(list(items2)) == 4)
		
			
										
if __name__ == '__main__':
	unittest.main()
	