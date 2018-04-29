import webapp2
import jinja2
import os
from google.appengine.api import mail

jinja_environment = jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class contact(webapp2.RequestHandler):
	template = jinja_environment.get_template('contact.html')
	def get(self):
		self.response.out.write(self.template.render())
	def post(self):
		# takes input from user
		userMail=self.request.get("mail")
		subject=self.request.get("subject")
		name=self.request.get("name")
		userMessage=self.request.get("message")
		message=mail.EmailMessage(sender="info@appspot.gserviceaccount.com",subject="Test")

		# not tested
		if not mail.is_email_valid(userMail):
		  self.response.out.write("Wrong email! Check again!")

		message.to=userMail
		message.body="""Thank you!
			 You have entered following information:
			 Your mail: %s
			 Subject: %s
			 Name: %s
			 Message: %s""" %(userMail,subject,name,userMessage)
		message.send()
		self.response.out.write("Message sent!")

app = webapp2.WSGIApplication([('/',contact)], debug=True)
