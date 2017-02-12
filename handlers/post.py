import json
import time
import entities
from handlers import ViewHandler
from utility import validate, helpers


# Handler for the post page
class PostPage(ViewHandler):

    # Static method that gets the comments and likes for the post
    @staticmethod
    def get_comments_and_likes(params, post_id):
        comments = entities.Comments.get_comments_by_post(post_id)
        if comments:
            params["comments"] = comments

        likes = entities.Likes.get_total_likes(post_id)
        if likes:
            params["total_likes"] = likes
        else:
            params["total_likes"] = 0

    @ViewHandler.is_post_valid()
    # Get request handler
    def get(self, post_id):
        post = entities.BlogPost.get_by_id(int(post_id))
        params = {"post": post}
        # If the user is logged in check if they are not the owner of the
        # post and show a like/dislike button
        if self.user:
            params["user"] = self.user
            if not self.user.username == post.username:
                params["like_status"] = entities.Likes.get_status(
                    self.user.username, post_id)

        self.get_comments_and_likes(params, post_id)
        self.render("post.html", **params)
