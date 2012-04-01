import tracker
import unittest
import uuid

class TestTracker(unittest.TestCase):
	
	def test_GetConnection(self):
		track = tracker.Tracker()
		track.GetConnection()
		
	def test_Track(self):
		myID = uuid.uuid1()			
		track = tracker.Tracker()
		track.GetConnection()	
		print track.Track(str(myID),'ppc','mycampaign','google')
		print track.GetByUID(str(myID),'ppc')			
		
if __name__ == '__main__':
	unittest.main()