import tracker
import unittest
import uuid

class TestTracker(unittest.TestCase):
	
	def test_GetConnection(self):
		track = tracker.Tracker()
		track.GetConnection()
		
	def test_Track(self):
		#create a UID for the test
		myID = uuid.uuid1()			
		
		track = tracker.Tracker()

		track.GetConnection()	

		track.Track(str(myID),'search','mycampaign2','google')

		track.GetByUID(str(myID),'mycampaign2')

		print track.GetByUID('d3f00230-7bbe-11e1-b474-df1df9a2acb9','mycampaign')
		
		items = track.GetCustomersByCampaign(myID,'mycampaign2')
		
		#for item in items:
			#print item
		
		
if __name__ == '__main__':
	unittest.main()