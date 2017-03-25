from handler import Handler

from users import Users 
from blog import Blog
from home import *


class Post(Handler):
    user=False
    """
     docs
    """ 
    def get(self):
        """
        docs
        """ 
        
        Post.user=check_secure_val(self.request.cookies.get('user_id', '0'))
        if Post.user:
            Post.user=Users.by_id(Post.user)

        if Post.user:
            self.render('writepost.html',name = Post.user.name)
        else:
            self.redirect('/')




    def post(self):
        """Create a blog-entry """
        if not Post.user:
            self.redirect('/home')
        else:
            title = self.request.get("title")
            article = self.request.get("article")
            if title and article and self.user:
                a = Blog.create_blog_entry(created_by=Post.user,
                                                     title=title,
                                                     article=article)
                self.redirect('/allposts?id=%s' % str(a.key().id()))