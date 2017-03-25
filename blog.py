"""Enities used in myBlog."""

import datetime
from google.appengine.ext import db  
from users import Users



class Blog(db.Model):
    """Blog-entries."""
    title = db.StringProperty(required=True)
    article = db.TextProperty(required=True)
    created_by = db.ReferenceProperty(Users, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    
    last_modified = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_title(cls, title):
        
        blogEntry = Blog.all().filter('title =', title).get()
        return blogEntry

    @classmethod
    def get_by_id_str(cls, blog_id):
        return Blog.get_by_id(int(blog_id))

    @classmethod
    def create_blog_entry(cls, title, article, created_by):
        
        existingTitle = Blog.by_title(title)
        if not existingTitle:
            blogEntry = Blog(
                                   title=title,
                                   article=article,
                                   created_by=created_by)
            blogEntry.put()
            return blogEntry
class Comments(db.Model):
    """Comments for blog_entries"""

    commentBy = db.ReferenceProperty(Users, required=True)
    commentOn = db.ReferenceProperty(Blog, required=True)
    comment = db.TextProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)


    @classmethod
    def comment_on_post(cls, commentBy, commentOn, comment):
        """Create a comment."""
        comment = comment.strip()

        comment_entry = Comments(
            commentBy=commentBy,
            commentOn=commentOn,
            comment=comment)
        Comments.put()
        return comment_entry
    


    @classmethod
    def get_comments_on_post(cls, commentOn):
        """Return comments for the blog_post."""
        comments = Comments.all().filter(
            'commentOn = ', commentOn)
        return comments
class Like(db.Model):
    """Votes in the blog."""

    LikeBy = db.ReferenceProperty(Users, required=True)
    LikeOn = db.ReferenceProperty(Blog, required=True)
    LikeType = db.StringProperty(required=True, choices=('up', 'down'))


    @classmethod
    def get_likes_on_post(cls, likesOn):
        """Return up- and downvotes for the blog_post."""
        votes = {}
        votes['up'] = Like.all().filter(
            'LikeOn = ', likesOn).filter('LikeType = ', 'up').count()


        votes['down'] = Like.all().filter(
            'LikeOn = ', likesOn).filter('LikeType = ', 'down').count()
        return votes

    @classmethod
    def like_on_blog(cls, LikeOn, LikeBy, LikeType):
        """
        Update a vote, or create it if it doesn't exist.

        """
        if LikeOn.created_by.key().id() == LikeBy.key().id():
            return 'Cannot vote on own post'
        the_like = Like.all().filter(
            'LikeBy = ', LikeBy).filter(
                'LikeOn = ', LikeOn).get()
        if the_like:
            if the_like.LikeType == LikeType:
                the_like.delete()
            else:
                the_like.LikeType = LikeType
                the_like.put()
        else:
            the_like = Like(
                LikeBy=LikeBy,
                LikeOn=LikeOn,
                LikeType=LikeType).put()
        return the_like
