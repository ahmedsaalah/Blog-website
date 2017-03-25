"""
Post entity

"""
from google.appengine.ext import db
from users import *

class Post(db.Model):
    title = db.StringProperty(required=True)
    article = db.TextProperty(required=True)
    created_by = db.ReferenceProperty(Users, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_title(cls, title):
        """Retrieve a blogentry by its title."""
        blogEntry = Post.all().filter('title =', title).get()
        return blogEntry

    @classmethod
    def get_by_id_str(cls, blog_id):
        """Return a blog_entry from blog_id(str) if valid."""
        if blog_id.isdigit():
            return BlogEntity.get_by_id(int(blog_id), parent=blog_key())
