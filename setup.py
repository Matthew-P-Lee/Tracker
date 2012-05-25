#!/usr/bin/env python

import tracker
import sys

def get_help_msg():
	print 'Args: -d to delete, -c to create'

def Run():
	t = tracker.Tracker()
	
	if (len(sys.argv) > 1):
		if( sys.argv[1] == '-d' ):
			print "Deleting Tables..."
			t.delete_table('Tracker')
			t.delete_table('Customer')
			t.delete_table('Campaign')		
		elif( sys.argv[1] == '-c' ):
			print "Creating Tables..."
			t.create_table('Tracker','customer_id')
			t.create_table('Customer','client_id')
			t.create_table('Campaign','campaign_id')		
		elif( sys.argv[1] == '-deleteCustomer' ):
			t.delete_table('Customer')
		elif( sys.argv[1] == '-deleteTracker' ):
			t.delete_table('Tracker')
		elif( sys.argv[1] == '-deleteCampaign' ):
			t.delete_table('Campaign')
		else:
			get_help_msg()
	else:
		get_help_msg()


if __name__ == '__main__':
	Run()
