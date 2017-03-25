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
            if self.request.get('post_id'):
                blog = Blog.get_by_id_str(self.request.get('post_id'))
                self.render('writepost.html',name = Post.user.name, blog=blog, post_id = self.request.get('post_id'))
            else:
                self.render('writepost.html',name = Post.user.name)
                
        else:
            self.redirect('/')




    def post(self):
        """Create a blog-entry """
        Post.user=check_secure_val(self.request.cookies.get('user_id', '0'))
        if not Post.user:
            self.redirect('/')
        else:

            title = self.request.get("title")
            article = self.request.get("article")
                
            if title and article and self.user:
                if self.request.get('post_id'):
                     blog = Blog.get_by_id_str(self.request.get('post_id'))
                     blog.title = title
                     blog.article = article
                     blog.put()
                     self.redirect('/')
                else:
                    logging.info(Post.user)
                    logging.info(title)
                    logging.info(article)
                    a = Blog.create_blog_entry(created_by=Users.by_id(Post.user),
                                                        title=title,
                                                        article=article)
                    self.redirect('/allposts?id=%s' % str(a.key().id()))