from handlers import ViewHandler
from utility import validate
import json
import time
import entities


# Handler for comments
class NewCommentHandler(ViewHandler):

    # This one only contains post handler!
    @ViewHandler.is_post_valid('json')
    @ViewHandler.is_user_authenticated('json')
    def post(self, post_id, post):

        comment = self.request.get("comment")
        params = {"comment": comment}
        has_error = False

        # Check if the comment is valid
        comment_error = validate.is_valid_comment(comment)
        if comment_error:
            params["error"] = comment_error
            has_error = True

        # If there are any errors return the json response to the user
        if has_error:
            self.response.write(json.dumps(params))
        else:
            # Create the comment object in the database
            comment = (entities.Comments
                       .create(comment, self.user.username,
                               post_id))

            if comment:
                # wait 0.1 seconds so we can properly fetch the
                # newly created object from database
                time.sleep(0.1)

                params["success"] = "true"
                params["username"] = comment.username
                params["created"] = comment.created.strftime('%Y-%m-%d %H:%M:%S')
                params["comment_id"] = comment.key().id()
                self.response.write(json.dumps(params))
            else:
                params["error"] = "Unknown error"
                self.response.write(json.dumps(params))



