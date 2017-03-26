from google.appengine.ext import db

from handler import Handler
from users import Users 
from home import *
from blog import *
import logging


class Allposts(Handler):
    user=False
    def get(self):
        
    
        id=self.request.get('id')

        Allposts.user=check_secure_val(self.request.cookies.get('user_id', '0'))
        logging.info("Allposts.user")
        logging.info(Allposts.user)
        l=0
        if Allposts.user:
            if type(Allposts.user) is not Users:

                Allposts.user=Users.by_id(Allposts.user)
            b=Blog.get_by_id_str(id)
                         
            if(self.request.get('id') and b):
                posts =[]
                blog=Blog.get_by_id_str(id)
                posts.insert(0,blog)
                l=1

            else :

                posts = Blog.all().order('-created')
                l=posts.count()



        
        likes =[]
        comments =[]
        if Allposts.user:
            
            
            i=0
            for post in posts :
                comment = Comments.get_comments_on_post(post)
                like = Like.get_likes_on_post(post)
                likes.insert(i,like)
                comments.insert(i,comment)
                
                i=i+1
                logging.info("Allposts.user.name")
            
            self.render('posts.html',user=Allposts.user,name = Allposts.user.name,posts=posts,comments=comments,likes=likes ,l=l)
        else:
            self.redirect('/')




    #     arts = db.GqlQuery("SELECT * FROM Art "
    #                       "ORDER BY created DESC ")
    #     self.render('ascii_art.html',arts = arts)
   
    # def post(self):
    #     title = self.request.get('title')
    #     art = self.request.get('art')
    #     if (title and art):
    #         a = Art(title=title, art=art)
    #         a.put()
    #         self.redirect('/asciichan')
    #     else:
    #         error = "we need both title and art !!!"
    #         arts = db.GqlQuery("SELECT * FROM Art "
    #                       "ORDER BY created DESC ")
    #         self.render('ascii_art.html', arts = arts, error=error, title=title, art=art)
class comment(Allposts):
    def get(self):
        Allposts.get(self)
    def post(self):
        comment=self.request.get('theComment')
        thepost=self.request.get('thepost')

        user_id = self.request.cookies.get('user_id', '0')
        user=check_secure_val(user_id)

        if(user):
            Auser=Users.by_id(user)
        
            comment = comment.strip()
            b=Blog.get_by_id_str(thepost)
            if b: 

                comment_entry = Comments(
                    commentBy=Auser,
                    commentOn=b,
                    comment=comment)
                comment_entry.put()
        self.redirect('/')
        

class like(Allposts):
    def get(self):
        id=self.request.get('lid')
        user_id = self.request.cookies.get('user_id', '0')
        user=check_secure_val(user_id)

        if(user):
            Auser=Users.by_id(user)
            if Auser :
                b=Blog.get_by_id_str(id)
                if b:
                    Like.like_on_blog(b,Auser,'up')
        self.redirect('/')

    
        


class dislike(Allposts):
    def get(self):
        id=self.request.get('did')
        user_id = self.request.cookies.get('user_id', '0')
        user=check_secure_val(user_id)

        if(user):
            Auser=Users.by_id(user)
            if Auser :
                b=Blog.get_by_id_str(id)
                if b:
                    Like.like_on_blog(b,Auser,'down')
        self.redirect('/')


class deletepost(Allposts):
     def get(self):
        id=self.request.get('deleteid')
        user_id = self.request.cookies.get('user_id', '0')
        user=check_secure_val(user_id)

        if(user):
            Auser=Users.by_id(user)

            b=Blog.get_by_id_str(id)
            
            if (b and int(user)==int(Blog.get_by_id_str(id).created_by.key().id())):
                Blog.get_by_id_str(id).delete()
        self.redirect('/')



