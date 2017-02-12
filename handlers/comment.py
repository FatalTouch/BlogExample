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

            # If action is edit
            elif action == "edit":
                has_error = False
                params = {}
                comment_id = self.request.get("comment_id")
                post_id = self.request.get("post_id")
                comment = self.request.get("comment")

                # Send back all the data received
                params["comment_id"] = comment_id
                params["comment"] = comment
                params["post_id"] = post_id

                # check if the comment is valid
                comment_error = validate.is_valid_comment(comment)
                if comment_error:
                    params["comment_error"] = comment_error
                    has_error = True

                # check if the blog post exists
                if not entities.BlogPost.exists(post_id):
                    params["comment_error"] = "Invalid action"
                    has_error = True

                # If there are any errors return the json response with
                # the the errors
                if has_error:
                    self.response.write(json.dumps(params))
                else:
                    # Edit the comment by calling edit method on Comments
                    # entity, wait 0.1 second although this can be omitted
                    # and return the json response with success = true
                    comment = (entities.Comments
                               .edit(comment, comment_id, self.user.username))
                    if comment:
                        time.sleep(0.1)
                        params["success"] = "true"
                        self.response.write(json.dumps(params))
                    else:
                        # If comment was not modified then return json response
                        # with the error
                        params["comment_error"] = "Unknown error"
                        self.response.write(json.dumps(params))
            else:
                self.redirect('/')
        else:
            self.redirect('/')
