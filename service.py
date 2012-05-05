# simple web tracking and redirection via rest server
import web
import tracker
import uuid
import config

#Mappings for web.py and any other HTTP related stuff
urls = (
	'/', 'status',
	'/track', 'track',
	'/getbyuid', 'getByUID',
	)

app = web.application(urls, globals())
tracker = tracker.Tracker()

class getByUID:
	def GET(self):
		i = web.input(id=config.TEST_UID)		
		return tracker.GetByID(i.id)
		
class status:
	def GET(self):
		return tracker.Status()

class track:
	def GET(self):
		#?channel='ppc'&campaign='mycampaign'
		i = web.input(channel = 'undefined channel',
						campaign = 'undefined campaign')
		
		#handy way to get HTTP environment variables
		referer = web.ctx.env.get('HTTP_REFERER', 
									'undefined referer')		
		
		#get the custId from the cookie or create a new one
		custId = self.SetCustomerCookie(str(uuid.uuid1()))
		
		#invoke the tracker
		return tracker.Track(custId,i.channel,i.campaign,referer)
	
	#get/set the master customerId cookie
	def SetCustomerCookie(self,defaultCookieValue):
		cookieName = 'bolCustId'
		cookieDuration = 3600
		
		#see if the user has a custId set in a cookie already, 
		cookie = web.cookies().get(cookieName)					
				
		#set it if they dont	
		if cookie is None:
			web.setcookie(cookieName,defaultCookieValue,cookieDuration)
			cookieValue = defaultCookieValue
		else:
			cookieValue = str(cookie)			

		return cookieValue

if __name__ == "__main__":
    app.run()		