from google.appengine.ext import db
import _blogpost


# Likes entity
class Likes(db.Model):
    # Information stored in the likes entity
    username = db.StringProperty(required=True)
    post_id = db.IntegerProperty(required=True)
    value = db.BooleanProperty(required=True)

    # Method to create a new like and do a check before to make sure that
    # the person liking/unliking the post isn't the creator of the post
    @classmethod
    def create(cls, username, post_id, value):
        post = _blogpost.BlogPost.get_by_id(int(post_id))
        if post:
            if not post.username == username:
                db_likes = (cls.all().filter('post_id = ', int(post_id))
                            .filter('username = ', username)).get()
                if db_likes:
                    db_likes.value = value
                    db_likes.put()
                    return True
                else:
                    db_likes = cls(username=username, post_id=int(post_id),
                                   value=value)
                    db_likes.put()
                    return True

    # like method that calls the create method with a True value for like
    @classmethod
    def like(cls, username, post_id):
        return cls.create(username, post_id, True)

    # dislike method that calls the create method with a False value for like
    @classmethod
    def unlike(cls, username, post_id):
        return cls.create(username, post_id, False)

    # Get the current like status for a post by passing in username and postid
    @classmethod
    def get_status(cls, username, post_id):
        status = (cls.all().filter('post_id = ', int(post_id))
                  .filter('username = ', username)).get()

        if status:
            return status.value
        else:
            return False

    # Get all the likes by passing in a post_id
    @classmethod
    def get_likes_by_post(cls, post_id):
        return cls.all().filter('post_id = ', int(post_id))

    # Get the total likes for a post
    @classmethod
    def get_total_likes(cls, post_id):
        return (cls.all().filter('post_id = ', int(post_id))
                .filter('value = ', True)).count()