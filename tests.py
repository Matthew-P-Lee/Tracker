import tracker
import unittest

class TestTracker(unittest.TestCase):
	
	def test_GetConnection(self):
		track = tracker.Tracker()
		success = False
		try:			
			track.GetConnection()
			success = True
			print 'connection to DynamoDB success'
		except:
			print 'connection to DynamoDB failed'
			
		return success
		
if __name__ == '__main__':
	unittest.main()