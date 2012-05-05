#!/usr/bin/env python

import boto
import config
import uuid
from datetime import datetime


# Simple click and even tracker using AWS DynamoDB #
class Tracker:
	awsKeyId = config.AWS_KEY_ID
	awsSecretKey = config.AWS_SECRET_KEY
	trackedrows = {}
	conn = None
	
#	def __init__(self):
#		self.conn = self.GetConnection()						
		
	#Gets the status of the tracker	
	def Status(self):
		msg = ''
		conn = self.GetConnection()
				
		for table in conn.list_tables():
			msg = conn.describe_table(table)

		return msg		
			
	#Tracks a click or trackable event
	def SetEvent(self,customerId,channel,campaign,referer):		
		conn = self.GetConnection()
		
		self.trackedrows = {
			'CustomerId':customerId,
			'Channel':channel,
			'Campaign':campaign,
			'Referrer':referer
		}

		table = conn.get_table(config.TRACKER_TABLE_NAME)
		
		#save off the new record	
		item = table.new_item(
			hash_key=str(customerId),
			range_key=str(datetime.now()),
			attrs=self.trackedrows
		)
		
		item.put()
		
		return item	
	
	#Sets a customer record if none exists
	def SetCustomer(self,clientId,customerId):
		conn = self.GetConnection()
		item = None
		
		#only set if doesnt exist already
		items = self.GetCustomers(clientId)
		
		match = 0
		
		for i in items:
			if str(i['CustomerId']) == str(customerId): 
				match = 1
				item = i
		
		if not match:
			table = conn.get_table(config.CUSTOMER_TABLE_NAME)
		
			#save off the new record	
			item = table.new_item(
				hash_key=str(clientId),
				range_key=str(datetime.now()),
				attrs={
					'CustomerId':customerId
				}
			)
		
			item.put()
		
		return item	
		
	def DeleteCustomers(self,clientId):
		items = self.GetCustomers(clientId)
		
		for i in items:
			i.delete()
	
	def DeleteEvent(self,customerId):
		events = self.GetEvents(customerId)
		
		for e in events:
			e.delete()
	
	#gets a list of unique customers for a specific client	
	def GetCustomers(self,clientId):
		conn = self.GetConnection()
		table = conn.get_table(config.CUSTOMER_TABLE_NAME)
		
		items = table.query(
			hash_key=str(clientId),
		)
			
		return items
	
	#gets all events for a customer
	def GetEvents(self,id):
		conn = self.GetConnection()
		table = conn.get_table(config.TRACKER_TABLE_NAME)
		
		items = table.query(
			hash_key=id,
		)
			
		#item = table.get_item(
		#	hash_key=id
		#)	
			
		return items
				
	#Checks for an active connection and creates it if not 			
	def GetConnection(self):
		conn = None
		
		if self.conn is None:
			conn = boto.connect_dynamodb(
				aws_access_key_id=self.awsKeyId,
				aws_secret_access_key=self.awsSecretKey)
		else:
			conn = self.conn
		
		return conn		
		
	#creates the event tracker table in DynamoDB		
	def CreateTableTracker(self):
		conn = self.GetConnection()	
		
		table_schema = conn.create_schema(
			hash_key_name='CustomerId',
			hash_key_proto_value='S',
			range_key_name='Timestamp',
			range_key_proto_value='S'
		)
		
		table = conn.create_table(
			name=config.TRACKER_TABLE_NAME,
			schema=table_schema,
			read_units=5,
			write_units=5
		)	
			
		return table

	#creates the customer table in DynamoDB				
	def CreateTableCustomer(self):
		conn = self.GetConnection()	
		
		table_schema = conn.create_schema(
			hash_key_name='ClientId',
			hash_key_proto_value='N',
			range_key_name='Timestamp',
			range_key_proto_value='S'
		)
		
		table = conn.create_table(
			name=config.CUSTOMER_TABLE_NAME,
			schema=table_schema,
			read_units=5,
			write_units=5
		)	
			
		return table

	#deletes a dynamodb table... be careful!	
	def	DeleteTable(self,tablename):
		conn = self.GetConnection()			
		table = conn.get_table(tablename)
		conn.delete_table(table)
		
	