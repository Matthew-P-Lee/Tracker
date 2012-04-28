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
		
	#returns tracker data for a specific identifier	
	def GetByID(self, id):
		conn = self.GetConnection()						
		table = conn.get_table(self.tableName)
		
		item = table.get_item(
			hash_key=id
		)
		
		return item
		
	#gets the status of the tracker	
	def Status(self):
		msg = ''
		conn = self.GetConnection()
				
		for table in conn.list_tables():
			msg = conn.describe_table(table)

		return msg		
			
	#tracks some data		
	def Track(self,customerId,channel,campaign,referer):
		
		#store it somewhere
		self.trackedrows = {
			'CustomerId':customerId,
			'Channel':channel,
			'Campaign':campaign,
			'Referrer':referer
		}

		#connect to dynamoDb	
		conn = self.GetConnection()
		table = conn.get_table(self.tableName)
				
			
		#save off the new record	
		item = table.new_item(
			hash_key=str(uuid.uuid1()),
			range_key=str(datetime.now()),
			attrs=self.trackedrows
		)
		
		item.put()
		
		return item	
			
	def GetCustomersByCampaign(self,id,campaignId):
		conn = self.GetConnection()
		table = conn.get_table(self.tableName)
		items = table.scan()
				
		for item in items:
			print item
			
	def GetConnection(self):
		conn = boto.connect_dynamodb(
			aws_access_key_id=self.awsKeyId,
			aws_secret_access_key=self.awsSecretKey)
		
		return conn		
			
	def CreateTableTracker(self):
		conn = self.GetConnection()
	
		table_schema = conn.create_schema(
			hash_key_name='CustomerId',
			hash_key_proto_value='N',
			range_key_name='TimeStamp',
			range_key_proto_value='S'
		)
		
		table = conn.create_table(
			name=self.tableName,
			schema=table_schema,
			read_units=5,
			write_units=5
		)	
			
		return table
		
	def	DeleteTableTracker(self):
		conn = self.GetConnection()
		table = conn.get_table(self.tableName)
		conn.delete_table(table)