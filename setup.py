#!/usr/bin/env bash

import tracker
import sys

def PrintHelpMsg():
	print 'Args: -d to delete, -c to create'

def Run():
	t = tracker.Tracker()
	
	if (len(sys.argv) > 1):
		if( sys.argv[1] == '-d' ):
			print "Deleting Tables..."
			t.DeleteTable('Tracker')
			t.DeleteTable('Customer')
		elif( sys.argv[1] == '-c' ):
			print "Creating Tables..."
			t.CreateTableTracker()	
			t.CreateTableCustomer()
		elif( sys.argv[1] == '-deleteCustomer' ):
			t.DeleteTable('Customer')
		elif( sys.argv[1] == '-deleteTracker' ):
			t.DeleteTable('Tracker')
		else:
			PrintHelpMsg()
	else:
		PrintHelpMsg()


if __name__ == '__main__':
	Run()