import boto
import config
			
#campaign and customer tracker code
class Tracker:
	awsKeyId = config.AWS_KEY_ID
	awsSecretKey = config.AWS_SECRET_KEY
	tableName = 'Tracker'
	trackedrows = {}
		
	#returns tracker data for a specific identifier	
	def GetByUID(self, uid, campaign):
		#open a connection
		conn = self.GetConnection()						
		table = conn.get_table(self.tableName)
		
		item = table.get_item(
			hash_key=uid,
			range_key=campaign,
		)
		
		return item
		
	#gets the status of the tracker	
	def Status(self):
		msg = 'Tables: '
		
		#connect to dynamoDb	
		conn = self.GetConnection()
				
		for table in conn.list_tables():
			msg = conn.describe_table(table)

		return msg		
			
	#tracks some data		
	def Track(self,custId,channel,campaign,referer):
		
		#store it somewhere
		self.trackedrows = {
			'Channel':channel,
				
		}

		#connect to dynamoDb	
		conn = self.GetConnection()
		
		#create a table if one doesn't already exist	
		try:
			table = conn.get_table(self.tableName)
		except:
			table = self.CreateTable(self.tableName, conn)
			
		#save off the new record	
		item = table.new_item(
			hash_key=custId,
			range_key=campaign,
			attrs=self.trackedrows
		)
		
		item.put()
		
		return item	
		
	def GetCustomersByCampaign(self,id,campaignId):
		#connect to dynamoDb	
		conn = self.GetConnection()
		
		#create a table if one doesn't already exist	
		table = conn.get_table(self.tableName)
		
		items = table.scan()
				
		return items				
				
	def GetConnection(self):
		conn = boto.connect_dynamodb(
			aws_access_key_id=self.awsKeyId,
			aws_secret_access_key=self.awsSecretKey)
		
		return conn		
			
	def CreateTableTracker(self,tablename, conn):
		if conn is not None:
			table_schema = conn.create_schema(
					hash_key_name='CustomerId',
					hash_key_proto_value='S',
					range_key_name='Campaign',
					range_key_proto_value='S'
			)
		
			table = conn.create_table(
				name=tablename,
				schema=table_schema,
				read_units=10,
				write_units=10
			)	
			
		return table