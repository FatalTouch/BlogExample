from google.appengine.ext import db
import _blogpost


# Comments entity
class Comments(db.Model):
    # Information stored in the comments entity
    comment = db.StringProperty(required=True)
    username = db.StringProperty(required=True)
    post_id = db.IntegerProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    # Method to create a new comment
    @classmethod
    def create(cls, comment, username, post_id):
        comment = comment.replace('\n', ' ')
        comment = cls(comment=comment, username=username, post_id=int(post_id))
        comment.put()
        post = _blogpost.BlogPost.get_by_id(int(post_id))
        post.comment_count += 1
        post.put()
        return comment

    # Method to edit an existing comment
    @classmethod
    def edit(cls, comment, comment_id, username):
        comment = comment.replace('\n', ' ')
        db_comment = cls.get_by_id(int(comment_id))
        if db_comment.key().id() == int(comment_id):
            if not db_comment.username == username:
                return None
            db_comment.comment = comment
            db_comment.put()
            return True

    # Method to get all the comments by passing a post id ordered by
    # time they were created in descending order
    @classmethod
    def get_comments_by_post(cls, post_id):
        return cls.all().filter('post_id = ', int(post_id)).order('-created')

    # Method to delete a comment
    @classmethod
    def delete_comment(cls, comment_id):
        comment = cls.get_by_id(int(comment_id))
        post = _blogpost.BlogPost.get_by_id(comment.post_id)
        post.comment_count -= 1
        post.put()
        comment.delete()
