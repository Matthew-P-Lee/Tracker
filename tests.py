#!/usr/bin/env python

import tracker
import unittest
import uuid
import config
from datetime import datetime
import pdb

class TestTracker(unittest.TestCase):
	
	def test_GetConnection(self):
		track = tracker.Tracker()
		track.GetConnection()
	
	def test_GetStatus(self):
		track = tracker.Tracker()
		track.Status()
	
	def test_SetEvent(self):	
		myID = config.TEST_UID
		myCampaign = str(datetime.now())
		track = tracker.Tracker()
		track.SetEvent(myID,'search',myCampaign,'google')
		track.SetEvent(myID,'email',myCampaign,'exacttarget')
		track.SetEvent(myID,'ppc',myCampaign,'bing')
		track.SetEvent(myID,'social',myCampaign,'facebook')
	
	def test_GetEvents(self):
		myID = config.TEST_UID
		track = tracker.Tracker()
		items = track.GetEvents(myID)	
			
		#for item in items:
		#	print item['Timestamp'], item['Referrer']
			
	def test_GetSetCustomer(self):
		track = tracker.Tracker()
		
		#set 2 different UID for the same client
		track.SetCustomer(1,config.TEST_UID)
		track.SetCustomer(1,config.TEST_UID2)
		track.SetCustomer(1,config.TEST_UID2)
		
		#should not add dupes
		track.SetCustomer(3,config.TEST_UID)
		track.SetCustomer(3,config.TEST_UID)
		track.SetCustomer(3,config.TEST_UID)
	
		i = track.GetCustomers(1)	
		v = track.GetCustomers(3)	

		assert(len(list(i)) == 2)
		assert(len(list(v)) == 1)

		#for i in items:
		#	print i['ClientId'],i['CustomerId']
				
	def test_GetEntriesByClient(self):
		track = tracker.Tracker()
		items = track.GetCustomers(1)			
		
		for i in items:
			items = track.GetEvents(i['CustomerId'])	

			assert(len(items) > 0)
		
		
		#for i in items:
		#	items = track.GetEvents(i['CustomerId'])	
			
		#	for item in items:
		#		print item['Timestamp'], item['Referrer']

	def test_DeleteCustomer(self):
		track = tracker.Tracker()
		
		items = list(track.GetCustomers(1))			
		items2 = list(track.GetCustomers(3))

		v = items.extend(items2)
		
		for i in v:
			track.DeleteEntries(i['customerId'])

		track.DeleteCustomers(3)
		track.DeleteCustomers(1)
		
			
if __name__ == '__main__':
	unittest.main()