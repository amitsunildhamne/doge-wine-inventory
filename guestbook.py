#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_WINE_TYPE = 'red'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def winebook_key(wine_type=DEFAULT_WINE_TYPE):
    """Constructs a Datastore key for a Guestbook entity.

    We use wine_type as the key.
    """
    return ndb.Key('Guestbook', wine_type)


def user_key(user_key):
    """Constructs a Datastore key for a Guestbook entity.

    We use wine_type as the key.
    """
    return ndb.Key('Cart', user_key)



# [START greeting]
class WineType(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    

class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)




class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    winetype = ndb.StructuredProperty(WineType)
    country = ndb.StringProperty(indexed=False)
    region = ndb.StringProperty(indexed=False)
    variety = ndb.StringProperty(indexed=False)
    winery = ndb.StringProperty(indexed=False)
    year = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    price = ndb.StringProperty(indexed=False)
    key = ndb.StringProperty(indexed=True)
# [END greeting]

class UserWine(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    winetype = ndb.StructuredProperty(WineType)
    country = ndb.StringProperty(indexed=False)
    region = ndb.StringProperty(indexed=False)
    variety = ndb.StringProperty(indexed=False)
    winery = ndb.StringProperty(indexed=False)
    year = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    price = ndb.StringProperty(indexed=False)
    quantity = ndb.IntegerProperty(indexed=False)
    key = ndb.StringProperty(indexed=True)
    keyToDel = ndb.KeyProperty(indexed=False)

class afterPurchase(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    winetype = ndb.StructuredProperty(WineType)
    country = ndb.StringProperty(indexed=False)
    region = ndb.StringProperty(indexed=False)
    variety = ndb.StringProperty(indexed=False)
    winery = ndb.StringProperty(indexed=False)
    year = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    price = ndb.StringProperty(indexed=False)
    quantity = ndb.IntegerProperty(indexed=False)
    tprice = ndb.IntegerProperty(indexed=False)
    key = ndb.StringProperty(indexed=True)
    keyToDel = ndb.KeyProperty(indexed=False)

class Query(ndb.Model):
    author = ndb.StructuredProperty(Author)
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    winetype = ndb.StructuredProperty(WineType)
    country = ndb.StringProperty(indexed=False)
    region = ndb.StringProperty(indexed=False)
    variety = ndb.StringProperty(indexed=False)
    winery = ndb.StringProperty(indexed=False)
    year = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    price = ndb.StringProperty(indexed=False)
    key = ndb.StringProperty(indexed=True)
    quantity = ndb.IntegerProperty(indexed=False)
    key = ndb.StringProperty(indexed=True)

# [START main_page]


# [END main_page]

# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        user1 = users.get_current_user()
        wine_type = wine_type.lower()
        greetings_query = Greeting.query(
            ancestor=winebook_key(wine_type)).order(-Greeting.date)
        greetings = greetings_query.fetch(1)
        err=""

        if(wine_type == ""):
            err="Error: Category must not be blank"
       

        

        if user1:
            user = users.get_current_user().email()
            identity=users.get_current_user().user_id()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
            'user': user,
            'identity':identity,
            'error1':err,
            'wine_type': urllib.quote_plus(wine_type),
           
        }
            
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
            'wine_type': urllib.quote_plus(wine_type),
            'error1':err

           
        }
        #template = JINJA_ENVIRONMENT.get_template('index.html')
        #self.response.write(template.render(template_values))

        template = JINJA_ENVIRONMENT.get_template('enter.html')
        self.response.write(template.render(template_values))

# [END main_page]


# [START guestbook]
class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        errq=""
        if(wine_type!=""):
            greeting = Greeting(parent=winebook_key(wine_type))
            greeting.country = self.request.get('country')
            greeting.region = self.request.get('region')
            greeting.variety = self.request.get('variety')
            greeting.winery = self.request.get('winery')
            greeting.year = self.request.get('year')
            greeting.price = self.request.get('price')
            key = greeting.put()
            temp=key.get()
            temp.key=str(key.id())
            temp.put()
        else:
            errq="Error: Category  must not be blank"
            wine_type=""
            query_params = {'wine_type': wine_type,'error1':errq}
            self.redirect('/enter?' + urllib.urlencode(query_params))
            return

        

        
       
        
           

        query_params = {'wine_type': wine_type,'error1':errq}
        self.redirect('/enter?' + urllib.urlencode(query_params))
# [END guestbook]

class Display(webapp2.RequestHandler):
     def get(self):
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        user1 = users.get_current_user()
        wine_type = wine_type.lower()
        greetings_query = Greeting.query(
            ancestor=winebook_key(wine_type)).order(-Greeting.date)
        greetings = greetings_query.fetch()

        if user1:
            user = users.get_current_user().email()
            identity=users.get_current_user().user_id()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
            'user': user,
            'identity':identity,
            'greetings': greetings,
            'wine_type': urllib.quote_plus(wine_type),
           
        }
            
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
            'greetings': greetings,
            'wine_type': urllib.quote_plus(wine_type),
           
        }


      
        template = JINJA_ENVIRONMENT.get_template('displayA.html')
        self.response.write(template.render(template_values))
       
       




class MO(webapp2.RequestHandler):
    def get (self):
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        
        greeting = Query(parent=winebook_key(wine_type))
        
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        
        template_values={
        'user': user,
        'url': url,
         'url_linktext': url_linktext,
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))




class Search2(webapp2.RequestHandler):
     def get(self):
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        user1 = users.get_current_user()
        wine_type = wine_type.lower()
        greetings_query = Query.query(
            ancestor=winebook_key(wine_type)).order(-Greeting.date)
        greetings = greetings_query.fetch(1)

        answers_query = Greeting.query(ancestor=winebook_key(wine_type)).order(-Greeting.date)
        answers = answers_query.fetch()

        output=[]
        err=''
        empty=False

        country=''
        region=''
        variety=''
        winery=''
        
        for r in greetings:
            country=r.country.lower()
            region=r.region.lower()
            variety=r.variety.lower()
            winery=r.winery.lower()

        for ans in answers:

            if(country == '' and region == '' and variety == '' and winery == ''):
                empty=True
                break
            elif((country == '' or (country in ans.country.lower())) and (region == '' or (region in ans.region.lower()))
                and (variety == '' or (variety in ans.variety.lower())) and (winery == '' or (winery in ans.winery.lower()))):
                output.append(ans)

        if(output == []):
            err='error'


        if user1:
            user = users.get_current_user().email()
            identity=users.get_current_user().user_id()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
            'user': user,
            'empty':empty,
            'error':err,
            'greetings': output,
            'wine_type': urllib.quote_plus(wine_type),
           
        }
            
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
            'wine_type': urllib.quote_plus(wine_type),
            'empty':empty,
            'error':err,
            'greetings': output,
            'wine_type': urllib.quote_plus(wine_type),

           
        }

        #template = JINJA_ENVIRONMENT.get_template('index.html')
        #self.response.write(template.render(template_values))

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))


class Search(webapp2.RequestHandler):
     def get(self):
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        user1 = users.get_current_user()
        wine_type = wine_type.lower()
        


        output=[]
        err=''

        if user1:
            user = users.get_current_user().email()
            identity=users.get_current_user().user_id()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
            'user': user,
            'empty':False,
            'error':err,
            'greetings': output,
            'wine_type': urllib.quote_plus(wine_type),
           
        }
            
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
            'wine_type': urllib.quote_plus(wine_type),
            'empty':False,
            'error':err,
            'greetings': output,
            'wine_type': urllib.quote_plus(wine_type),

           
        }


        #template = JINJA_ENVIRONMENT.get_template('index.html')
        #self.response.write(template.render(template_values))

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))


class Seek(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        if(wine_type !=""):
            greeting = Query(parent=winebook_key(wine_type))
        else:
            return


        greeting.country = self.request.get('country')
        greeting.region = self.request.get('region')
        greeting.variety = self.request.get('variety')
        greeting.winery = self.request.get('winery')
        greeting.year = self.request.get('year')
        greeting.price = self.request.get('price')
        greeting.put()        

        query_params = {'wine_type': wine_type}
        self.redirect('/search2?' + urllib.urlencode(query_params))

class Cart(webapp2.RequestHandler):
    def get(self):
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        
        wine_type = wine_type.lower()
        
        user1 = users.get_current_user()
        if user1:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            user = users.get_current_user().email()
            identity=users.get_current_user().user_id() 
            greetings_query = UserWine.query(
            ancestor=user_key(user)).order(-Greeting.date)
            greetings = greetings_query.fetch()
            total=0
            for g in greetings:
                total+=g.quantity*int(g.price)

            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
            'user': user,
            'identity':identity,
            'greetings': greetings,
            'wine_type': urllib.quote_plus(wine_type),
            'total':total
           
        }
            
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            total=0
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
           
        }
        
        
       


        

      
        template = JINJA_ENVIRONMENT.get_template('cart.html')
        self.response.write(template.render(template_values))
       
       


class Add(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        
        user = users.get_current_user().email()
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        if(user!=""):
            greeting = UserWine(parent=user_key(user))
            greeting.country = self.request.get('country')
            greeting.region = self.request.get('region')
            greeting.variety = self.request.get('variety')
            greeting.winery = self.request.get('winery')
            greeting.year = self.request.get('year')
            greeting.price = self.request.get('price')
            greeting.user = user
            greeting.identity = self.request.get('identity')
            greeting.quantity = int(self.request.get('quantity'))
            greeting.key = self.request.get('key')
            

            greetings_query = UserWine.query(
            ancestor=user_key(user)).order(-Greeting.date)
            greetings1 = greetings_query.fetch()
            flag=0

            for ans in greetings1:

                if(greeting.key == ans.key):
                    t=ans.keyToDel.get()
                    t.quantity += greeting.quantity
                    t.put()
                    flag=1

            if(flag==0):
                temp=greeting.put()
                gret=temp.get()
                gret.keyToDel=temp
                gret.put()

            

        

        
       
        
           

        query_params = {'wine_type': wine_type}
        self.redirect('/display?' + urllib.urlencode(query_params))

class DelCart(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        user = users.get_current_user().email()
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        greeting = UserWine(parent=user_key(user))
        greeting.key = self.request.get('key')

        greetings_query = UserWine.query(
            ancestor=user_key(user)).order(-Greeting.date)
        greetings1 = greetings_query.fetch()

        #find a match. get it's key and delete
        
        for ans in greetings1:

            if(greeting.key == ans.key):
                t=ans.keyToDel
                t.delete()
                break

        

        template_values = {
            'user': user,
            'greetings': greetings1,
            'wine_type': urllib.quote_plus(wine_type),
           
        }


             

        query_params = {'user': user}
        self.redirect('/cart?' + urllib.urlencode(query_params))

class Chcart(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        user = users.get_current_user().email()
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        if(user!=""):
            greeting = UserWine(parent=user_key(user))
            greeting.country = self.request.get('country')
            greeting.region = self.request.get('region')
            greeting.variety = self.request.get('variety')
            greeting.winery = self.request.get('winery')
            greeting.year = self.request.get('year')
            greeting.price = self.request.get('price')
            greeting.user = user
            greeting.identity = self.request.get('identity')
            greeting.quantity = int(self.request.get('quantity'))
            greeting.key = self.request.get('key')
            

        greetings_query = UserWine.query(
            ancestor=user_key(user)).order(-Greeting.date)
        greetings1 = greetings_query.fetch()

        #find a match. get it's key and delete
        
        for ans in greetings1:

            if(greeting.key == ans.key):
                t=ans.keyToDel.get()
                t.quantity = greeting.quantity
                t.put()
                

        

        template_values = {
            'user': user,
            'greetings': greetings1,
            'wine_type': urllib.quote_plus(wine_type),
           
        }


             

        query_params = {'user': user}
        self.redirect('/cart?' + urllib.urlencode(query_params))


class Purchase(webapp2.RequestHandler):

    def get(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
       
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)

        
        user1 = users.get_current_user()
       


        
        if user1:
            user = users.get_current_user().email()
            identity=users.get_current_user().user_id()
            greetings_query = UserWine.query(
            ancestor=user_key(user)).order(-Greeting.date)
            greetings1 = greetings_query.fetch()
            output=[]
            for ans in greetings1:
                cart_purchase = afterPurchase(parent=user_key(user))
                cart_purchase.user=user
                cart_purchase.country = ans.country
                cart_purchase.region = ans.region
                cart_purchase.variety = ans.variety
                cart_purchase.winery = ans.winery
                cart_purchase.year = ans.year
                cart_purchase.price = ans.price
                cart_purchase.tprice = int(ans.price) * ans.quantity
                cart_purchase.quantity = ans.quantity
                cart_purchase.key = ans.key
                cart_purchase.identity = ans.identity
                output.append(cart_purchase)
                cart_purchase.put()
                ans.keyToDel.delete()
                greetings_query = afterPurchase.query(
                ancestor=user_key(user)).order(-Greeting.date)
                greetings2 = greetings_query.fetch()
                url = users.create_logout_url(self.request.uri)
                url_linktext = 'Logout'
                template_values = {
                    'user': user,
                    'user1':user1,
                    'greetings': greetings2,
                    'url':url,
                    'url_linktext':url_linktext,
                    'wine_type': urllib.quote_plus(wine_type),
                   
                }
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext
           
        }

        #find a match. get it's key and delete
        
            



        


             

        template = JINJA_ENVIRONMENT.get_template('thankyou.html')
        self.response.write(template.render(template_values))

class Pur(webapp2.RequestHandler):
     def get(self):
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        user1 = users.get_current_user()
       


        
        if user1:
            user = users.get_current_user().email()
            identity=users.get_current_user().user_id()
            wine_type = wine_type.lower()
            greetings_query = afterPurchase.query(
                ancestor=user_key(user)).order(-Greeting.date)
            greetings = greetings_query.fetch()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext,
            'user': user,
            'identity':identity,
            'greetings': greetings,
            'wine_type': urllib.quote_plus(wine_type),
           
        }
            
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            template_values = {
            'user1':user1,
            'url':url,
            'url_linktext':url_linktext
           
        }



       
      
        template = JINJA_ENVIRONMENT.get_template('purchase.html')
        self.response.write(template.render(template_values))


class AddS(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        
        user = users.get_current_user().email()
        wine_type = self.request.get('wine_type',
                                          DEFAULT_WINE_TYPE)
        if(user!=""):
            greeting = UserWine(parent=user_key(user))
            greeting.country = self.request.get('country')
            greeting.region = self.request.get('region')
            greeting.variety = self.request.get('variety')
            greeting.winery = self.request.get('winery')
            greeting.year = self.request.get('year')
            greeting.price = self.request.get('price')
            greeting.user = user
            greeting.identity = self.request.get('identity')
            greeting.quantity = int(self.request.get('quantity'))
            greeting.key = self.request.get('key')
            

            greetings_query = UserWine.query(
            ancestor=user_key(user)).order(-Greeting.date)
            greetings1 = greetings_query.fetch()
            flag=0

            for ans in greetings1:

                if(greeting.key == ans.key):
                    t=ans.keyToDel.get()
                    t.quantity += greeting.quantity
                    t.put()
                    flag=1

            if(flag==0):
                temp=greeting.put()
                gret=temp.get()
                gret.keyToDel=temp
                gret.put()

            

        

        
       
        
           

        query_params = {'wine_type': wine_type}
        self.redirect('/search2?' + urllib.urlencode(query_params))
       
       
# [END guestbook]

# [END main_page]

# [START app]
app = webapp2.WSGIApplication([
    (r'/',MO),
    (r'/enter',MainPage),
    (r'/sign',Guestbook),
    (r'/display',Display),
    (r'/search',Search),
    (r'/search2',Search2),
    (r'/seek',Seek),
    (r'/cart',Cart),
    (r'/add',Add),
    (r'/cartdel',DelCart),
    (r'/cartchQ',Chcart),
    (r'/purchase',Purchase),
    (r'/purchase2',Pur),
    (r'/addfromS',AddS)
], debug=True)
# [END app]
