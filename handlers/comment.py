from handlers import ViewHandler
from utility import validate
import json
import time
import entities


# Handler for comments
class CommentHandler(ViewHandler):

    # This one only contains post handler!
    @ViewHandler.is_user_authenticated()
    def post(self):
        action = self.request.get("action")

        # Check if action is present otherwise redirect to home page
        if action:

            # If action is delete
            if action == "delete":
                comment_id = self.request.get("comment_id")

                # Check if comment_id is present, otherwise redirect
                # to home page
                if comment_id:

                    # Get the comment object from db
                    comment = entities.Comments.get_by_id(int(comment_id))

                    # Check if the current user is owner of the comment
                    if comment.username == self.user.username:

                        # Delete the comment and wait 0.1 seconds and redirect
                        # to the post
                        entities.Comments.delete_comment(comment_id)
                        time.sleep(0.1)
                        self.redirect('/post/' + str(comment.post_id))
                    else:
                        self.redirect('/post/' + str(comment.post_id))
                else:
                    self.redirect('/')

            else:
                self.redirect('/')
        else:
            self.redirect('/')
