#!/usr/bin/env python

import boto
import config
import uuid
import time
from datetime import datetime
from boto.dynamodb.condition import *

# Simple click and event tracker using AWS DynamoDB #
class Tracker:
	awsKeyId = config.AWS_KEY_ID
	awsSecretKey = config.AWS_SECRET_KEY
	trackedrows = {}
	conn = None
	
#	def __init__(self):
#		self.conn = self.get_connection()						
		
	def pytime_to_timestamp(self, pythondatetime):
		return time.mktime(pythondatetime.timetuple())
		
	#Tracks a click or trackable event
	def set_click(self,customerId,campaign,url):		
		conn = self.get_connection()
		
		self.trackedrows = {
			'CustomerId':customerId,
			'CampaignCode':campaign,
			'URL':url
		}

		table = conn.get_table(config.TRACKER_TABLE_NAME)
		
		#save off the new record	
		item = table.new_item(
			hash_key=str(customerId),
			range_key=str(self.pytime_to_timestamp(datetime.now())),
			attrs=self.trackedrows
		)
		
		item.put()
		
		return item	
	
	#Sets a customer record if none exists
	def set_customer(self,clientId,customerId):
		conn = self.get_connection()
		item = None
		
		#only set if doesnt exist already
		items = self.get_customers(clientId)
		
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
				range_key=str(self.pytime_to_timestamp(datetime.now())),
				attrs={
					'CustomerId':customerId
				}
			)
		
			print item.put()
		
		return item	
		
	def delete_customer(self,clientId):
		items = self.get_customers(clientId)
		
		for i in items:
			i.delete()
	
	def delete_click(self,customerId):
		events = self.get_clicks(customerId)
		
		for e in events:
			e.delete()
	
	#gets a list of unique customers for a specific client	
	def get_customers(self,clientId):
		conn = self.get_connection()
		table = conn.get_table(config.CUSTOMER_TABLE_NAME)
		
		items = table.query(
			hash_key=str(clientId),
		)
			
		return items
	
	#gets clicks for a customer
	def get_clicks(self,id):
		conn = self.get_connection()
		table = conn.get_table(config.TRACKER_TABLE_NAME)
			
		items = table.query(
			hash_key=id,
			range_key_condition=LT(
					str(self.pytime_to_timestamp(datetime.now()))
				)
		)
			
		#item = table.get_item(
		#	hash_key=id
		#)	
			
		return items	
			
	#Checks for an active connection and creates it if not 			
	def get_connection(self):
		conn = None
		
		if self.conn is None:
			conn = boto.connect_dynamodb(
				aws_access_key_id=self.awsKeyId,
				aws_secret_access_key=self.awsSecretKey)
		else:
			conn = self.conn
		
		return conn		
		
	#creates theGetConnection  event tracker table in DynamoDB		
	def create_table_tracker(self):
		conn = self.get_connection()	
		
		table_schema = conn.create_schema(
			hash_key_name='CustomerId',
			hash_key_proto_value='S',
			range_key_name='CreatedDate',
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
	def create_table_customer(self):
		conn = self.get_connection()	
		
		table_schema = conn.create_schema(
			hash_key_name='ClientId',
			hash_key_proto_value='S',
			range_key_name='CreatedDate',
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
	def	delete_table(self,tablename):
		conn = self.get_connection()			
		table = conn.get_table(tablename)
		conn.delete_table(table)