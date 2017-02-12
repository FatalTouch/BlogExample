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


    # Use the is_user_authenticated decorator to check if user is logged in
    @ViewHandler.is_post_valid()
    @ViewHandler.is_user_authenticated()
    # Post request handler
    def post(self, post_id):
        post = entities.BlogPost.get_by_id(int(post_id))
        params = {"post": post, "user": self.user}
        has_error = False

        # check if they are not the owner of the post and shw a like/dislike
        # button
        if not self.user.username == post.username:
            params["like_status"] = entities.Likes.get_status(
                self.user.username, post_id)
        action = self.request.get("action")

        # Check if the action is specified otherwise redirect to get
        # handler for the post
        if action:

            # If action is delete
            if action == "delete":

                # Get the post and check if the current user is the
                # owner then delete post otherwise render the response
                # from the get handler
                post = entities.BlogPost.get_by_id(int(post_id))
                if post.username == self.user.username:
                    entities.BlogPost.delete_post(post_id)

                    # wait 0.1 seconds so we can render the main page
                    # without the deleted object
                    time.sleep(0.1)
                    self.redirect('/')
                else:
                    self.get()
            # If action is edit

