"""
this is templete Module

"""

import webapp2
from home import Home
from home import Logout
from post import Post
from allposts import *


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/post',Post),
    ('/allposts', Allposts),
    ('/logout', Logout),
    ('/comment',comment),
    ('/like',like),
    ('/dislike',dislike),
    ('/deletepost',deletepost),
    ('/editpost',editpost)
], debug=True)
        


 