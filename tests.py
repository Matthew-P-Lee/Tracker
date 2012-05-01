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
			
	def test_SetCustomer(self):
		track = tracker.Tracker()
		track.SetCustomer(1,config.TEST_UID)
		track.SetCustomer(2,config.TEST_UID)
		track.SetCustomer(3,config.TEST_UID)

	def test_GetCustomers(self):
		track = tracker.Tracker()
		items = track.GetCustomers(1)	
		
		#for i in items:
			#print i['ClientId'],i['CustomerId']
		
if __name__ == '__main__':
	unittest.main()