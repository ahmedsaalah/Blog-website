from string import letters
from handler import Handler
import re
import random
import hashlib
import hmac
import logging
from users import Users 
from google.appengine.ext import db

secret="$@l@h_4991_@hMeD"
def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
    else:
         return False


def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)



def validate_username(Username):
    user = db.GqlQuery("SELECT * FROM Users Where username = '%s'" % (str(Username)))
    return user


def check_user(Username,pw):
    user = db.GqlQuery("SELECT * FROM Users Where username = '%s' and password = '%s' " % (str(Username),))
    return user


def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
        if not salt:
            salt = make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return '%s,%s' % (salt, h)

class Home (Handler):
    def get(self):
        user_id = self.request.cookies.get('user_id', '0')
        self.getUserByCookie(user_id)

    def getUserByCookie(self,user_id):
        user=check_secure_val(user_id)

        if(user):
            UserData=Users.by_id(user)
            
            if(UserData is not None):
                self.redirect("/allposts")
        
        self.render('home.html')






    def signup(self):
        error_email=""
        error_name=""
        error_pw=""
        name = self.request.get("name")
        pw = self.request.get("pw")
        pw2 = self.request.get("pw2")

        if ( not self.verify_passwords_matches(pw,pw2)):
            error_pw=" pw not match"
        
        email=""
        if (Users.by_name(name) is None):
            e="s"
        else:
            error_name="name used"
            



        
        if ( error_name=="" and error_pw==""):
            hashpw = make_pw_hash(name,pw)
            user = Users(name=name,email=email,password=hashpw)
            user.put()
            self.login(user)
            logging.info(user)
            self.redirect("/allposts")
        else:
             self.render("home.html",error_email=error_email,error_name=error_name,error_pw=error_pw)






    def signin(self):
        username = self.request.get("name")
        password = self.request.get("pw")
        

   
        


        if (Users.login(username,password)):

            self.login(Users.login(username,password))
            logging.info("useerr")
            logging.info(Users.login(username,password).name)
            self.redirect('/allposts')
             
        else :
            self.render("home.html",error="Not valid User")
            




    
    def verify_passwords_matches(self,password1, password2):
         """Check that the passwords matches eachother."""
         return password1 == password2

    
    


    def post(self):
         submit = self.request.get("submit")
         if (submit == "signup"):
            self.signup()
         if (submit == "signin"):
            self.signin()
    def make_secure_val(val):
         return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

    def check_secure_val(secure_val):
        val = secure_val.split('|')[0]
        if secure_val == make_secure_val(val):
            return val

    def set_secure_cookie(self, name, val):
            cookie_val = make_secure_val(val)
            self.response.headers.add_header(
                'Set-Cookie',
                '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
    def delete_cookie(self, name):
        """Delete a cookie from the browser."""
        self.set_cookie(name,0, -999)




class Logout (Home):
    """Logout user."""

    def get(self):
        """Delete usercookie to logout user."""
        self.delete_cookie('user_id')
        self.redirect('/')
    def delete_cookie(self, name):
        """Delete a cookie from the browser."""
        self.response.headers.add_header(
        'Set-Cookie',
        '%s=%s; Path=/' % ("user_id", "0|0"))




