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
	
	def test_Track(self):	
		myID = config.TEST_UID
		myCampaign = str(datetime.now())
		track = tracker.Tracker()
		track.Track(myID,'search',myCampaign,'google')
		track.Track(myID,'email',myCampaign,'exacttarget')
		track.Track(myID,'ppc',myCampaign,'google')
		track.Track(myID,'social',myCampaign,'facebook')
	
	def test_GetEvents(self):
		myID = config.TEST_UID
		track = tracker.Tracker()
		items = track.GetEvents(myID)	
			
		for item in items:
			print item['Timestamp'], item['Referrer']
			print '-------------------'
	

if __name__ == '__main__':
	unittest.main()