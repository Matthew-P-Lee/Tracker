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
		print 'setting up test data'
		cls.loadTestData()

	@classmethod
	def tearDownClass(cls):
		print 'tearing down test data'
#		cls.deleteTestData()
		

	@classmethod	
	def loadTestData(cls):
		track = tracker.Tracker()
		myCampaign = str(datetime.now())
		
		#set 2 different UID for the same client
		track.set_customer(1,config.TEST_UID)
		track.set_customer(1,config.TEST_UID2)
		track.set_customer(1,config.TEST_UID2)
		
		#should not add dupes
		track.set_customer(3,config.TEST_UID)
		track.set_customer(3,config.TEST_UID)
		track.set_customer(3,config.TEST_UID)
			
		#only load events if none
		items = track.get_clicks(config.TEST_UID)
		
		#pdb.set_trace()
		
		#create 4 test events for each UID
		if len(list(items)) == 0:		
			print track.set_click(
				config.TEST_UID,'1','1',config.TEST_URL)
			time.sleep(1)
			print track.set_click(
				config.TEST_UID,'2','1',config.TEST_URL)
			time.sleep(1)
			print track.set_click(
				config.TEST_UID,'3','1',config.TEST_URL)
			time.sleep(1)
			print track.set_click(
				config.TEST_UID,'4','1',config.TEST_URL)		 		
			time.sleep(1)
			print track.set_click(
				config.TEST_UID2,'5','1',config.TEST_URL)
			time.sleep(1)
			print track.set_click(
				config.TEST_UID2,'6','1',config.TEST_URL)
			time.sleep(1)
			print track.set_click(
				config.TEST_UID2,'7','1',config.TEST_URL)
			time.sleep(1)
			print track.set_click(
				config.TEST_UID2,'8','1',config.TEST_URL)		 

	@classmethod
	def deleteTestData(cls):
		track = tracker.Tracker()
		items = list(track.get_customers(1))			
		
		for i in items:
			track.delete_clicks(i['customer_id'])

		track.delete_customers(1)
		track.delete_customers(3)
		
	def test_get_clicks(self):
		track = tracker.Tracker()
		items = track.get_clicks(config.TEST_UID)	

		assert(len(list(items)) == 4)
		
	def test_get_customers(self):
		track = tracker.Tracker()
		
		c1 = track.get_customers(1)	
		c2 = track.get_customers(3)	

		assert(len(list(c1)) == 2)
		assert(len(list(c2)) == 1)
		
		for cust in c1:
			print cust['client_id'],cust['client_id']
		
	def test_GetItems(self):
		track = tracker.Tracker()
		items = track.get_customers(3)			
				
		for i in items:
			items2 = track.get_clicks(i['customer_id'])		
			assert(len(list(items2)) == 4)
		
			
										
if __name__ == '__main__':
	unittest.main()
	
