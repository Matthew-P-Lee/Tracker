import boto
import config
import uuid
from datetime import datetime
		
#campaign and customer tracker code
class Tracker:
	awsKeyId = config.AWS_KEY_ID
	awsSecretKey = config.AWS_SECRET_KEY
	tableName = config.TRACKER_TABLE_NAME
	trackedrows = {}
	conn = None
	
	def __init__(self):
		self.conn = self.GetConnection()						
	
	#returns tracker data for a specific identifier	
	def GetByID(self, id):
		table = self.conn.get_table(self.tableName)
		
		item = table.get_item(
			hash_key=id
		)
		
		return item
		
	#gets the status of the tracker	
	def Status(self):
		msg = ''
				
		for table in self.conn.list_tables():
			msg = self.conn.describe_table(table)

		return msg		
			
	#tracks some data		
	def Track(self,customerId,channel,campaign,referer):		
		self.trackedrows = {
			'CustomerId':customerId,
			'Channel':channel,
			'Campaign':campaign,
			'Referrer':referer
		}

		table = self.conn.get_table(self.tableName)
				
			
		#save off the new record	
		item = table.new_item(
			hash_key=str(customerId),
			range_key=str(datetime.now()),
			attrs=self.trackedrows
		)
		
		item.put()
		
		return item	
			
	def GetEvents(self,id):
		conn = self.GetConnection()
		table = conn.get_table(self.tableName)
		
		items = table.query(
			hash_key=id,
		)
			
		return items
			
	def GetConnection(self):
		
		if self.conn is None:
			self.conn = boto.connect_dynamodb(
				aws_access_key_id=self.awsKeyId,
				aws_secret_access_key=self.awsSecretKey)
		
		return self.conn		
			
	def CreateTableTracker(self):
		table_schema = self.conn.create_schema(
			hash_key_name='CustomerId',
			hash_key_proto_value='N',
			range_key_name='Timestamp',
			range_key_proto_value='S'
		)
		
		table = self.conn.create_table(
			name=self.tableName,
			schema=table_schema,
			read_units=5,
			write_units=5
		)	
			
		return table
		
	def	DeleteTableTracker(self):
		table = self.conn.get_table(self.tableName)
		conn.delete_table(table)