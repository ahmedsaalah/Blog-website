"""
Users entity

"""
from google.appengine.ext import db
import home
def users_key(group = 'default'):
    return db.Key.from_path('users', group)
class Users(db.Model):
    """
    User Class
    """
    name = db.StringProperty(required = True)
    password = db.TextProperty(required= True)
    email = db.StringProperty( required = False)
    created=db.DateTimeProperty( auto_now_add = True)

    
    @classmethod
    def by_name(cls, name):
        u = Users.all().filter('name =', name).get()
        return u

    @classmethod
    def by_id(cls, uid):
        return Users.get_by_id(int(uid))
    


    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and home.valid_pw(name, pw, u.password):
            return u
        else:
            return False
