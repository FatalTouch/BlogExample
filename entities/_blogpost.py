from google.appengine.ext import db
import _comments
import _likes

# Blog post entity
class BlogPost(db.Model):
    # Information to store in the blog post entity
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    username = db.StringProperty(required=True)
    comment_count = db.IntegerProperty(default=0)

    # Method to create a blog post
    @classmethod
    def create(cls, subject, content, username):
        blogpost = cls(subject=subject, content=content, username=username)
        blogpost.put()
        return blogpost

    # Method to edit a blog post
    @classmethod
    def edit(cls, subject, content, post_id):
        blogpost = cls.get_by_id(int(post_id))
        if blogpost:
            blogpost.content = content
            blogpost.subject = subject
            blogpost.put()
            return True

    # Method to get 15 latest blog posts
    @classmethod
    def get_latest(cls):
        return db.GqlQuery("Select * From BlogPost "
                           "ORDER BY created desc limit 15")

    # Method to check if a blog post exists
    @classmethod
    def exists(cls, post_id):
        if post_id:
            if BlogPost.get_by_id(int(post_id)):
                return True
            else:
                return False
        else:
            return False

    # Method to delete a blog post and it's associated data
    @classmethod
    def delete_post(cls, post_id):
        comments = _comments.Comments.get_comments_by_post(post_id)
        for c in comments:
            c.delete()
        likes = _likes.Likes.get_likes_by_post(post_id)
        for l in likes:
            l.delete()
        cls.get_by_id(int(post_id)).delete()