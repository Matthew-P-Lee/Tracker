#!/usr/bin/env python

import tracker
import unittest
import uuid
import config
from datetime import datetime
import pdb

class TestTracker(unittest.TestCase):	
	
	@classmethod
	def setUpClass(cls):
		cls.loadTestData()

#	@classmethod
	def tearDownClass(cls):
		cls.deleteTestData()

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
		
		if len(list(items)) == 0:		
			print 'Loading test Events...'
			track.SetEvent(config.TEST_UID,'search',myCampaign,'google')
			track.SetEvent(config.TEST_UID,'email',myCampaign,'exacttarget')
			track.SetEvent(config.TEST_UID,'ppc',myCampaign,'bing')
			track.SetEvent(config.TEST_UID,'social',myCampaign,'facebook')		 		
			track.SetEvent(config.TEST_UID2,'search',myCampaign,'google')
			track.SetEvent(config.TEST_UID2,'email',myCampaign,'exacttarget')
			track.SetEvent(config.TEST_UID2,'ppc',myCampaign,'bing')
			track.SetEvent(config.TEST_UID2,'social',myCampaign,'facebook')		 

	@classmethod
	def deleteTestData(cls):
		print 'Deleting test database...'
		track = tracker.Tracker()
		items = list(track.GetCustomers(1))			
		
		for i in items:
			track.DeleteEvent(i['CustomerId'])

		track.DeleteCustomers(1)
		track.DeleteCustomers(3)
		
	def test_GetConnection(self):
		track = tracker.Tracker()
		track.GetConnection()
	
	def test_GetStatus(self):
		track = tracker.Tracker()
		track.Status()
		
	def test_GetEvents(self):
		myID = config.TEST_UID
		track = tracker.Tracker()
		items = track.GetEvents(myID)	
			
		#for item in items:
		#	print item['CustomerId'],item['Timestamp'], item['Referrer']
			
	def test_GetCustomer(self):
		track = tracker.Tracker()
		i = track.GetCustomers(1)	
		v = track.GetCustomers(3)	

		assert(len(list(i)) == 2)
		assert(len(list(v)) == 1)

		#for e in i:
		#	print e['ClientId'],e['CustomerId']
				
	def test_GetEntriesByClient(self):
		track = tracker.Tracker()
		items = track.GetCustomers(3)			
				
		for i in items:
			items2 = track.GetEvents(i['CustomerId'])		
			assert(len(list(items2)) >= 4)		
					
		#	for item in items:
		#		print item['Timestamp'], item['Referrer']
					
if __name__ == '__main__':
	unittest.main()
	