# simple web tracking and redirection via rest server
import web
import tracker
import uuid
import config

#Mappings for web.py and any other HTTP related stuff
urls = (
	'/', 'status',
	'/track', 'track',
	'/history', 'GetByCustomerID',
	)

app = web.application(urls, globals())
tracker = tracker.Tracker()

class GetByCustomerID:
	def GET(self):
		#get the custId from the cookie or create a new one
		cookieName = 'customer_id'
		
		#see if the user has a custId set in a cookie already, 
		cookie = web.cookies().get(cookieName)					
		return tracker.get_clicks(str(cookie))
		
class status:
	def GET(self):
		render = web.template.render('templates')
		return render.index()

class track:
	def GET(self):
		
		i = web.input(campaign = 'undefined campaign',client = '0')
		
		#handy way to get HTTP environment variables
		referer = web.ctx.env.get('HTTP_REFERER', 
									'undefined referrer')		

		#get the custId from the cookie or create a new one
		customer_id = self.set_customerCookie(str(uuid.uuid1()))
		
		#invoke the tracker
		return tracker.set_click(customer_id,i.campaign,i.client,referer)

	#get/set the master customerId cookie
	def set_customerCookie(self,defaultCookieValue):
		cookieName = 'customer_id'
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
