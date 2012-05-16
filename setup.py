#!/usr/bin/env bash

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
		elif( sys.argv[1] == '-c' ):
			print "Creating Tables..."
			t.get_connection()	
			t.create_table_customer()
		elif( sys.argv[1] == '-deleteCustomer' ):
			t.delete_table('Customer')
		elif( sys.argv[1] == '-deleteTracker' ):
			t.delete_table('Tracker')
		else:
			get_help_msg()
	else:
		get_help_msg()


if __name__ == '__main__':
	Run()