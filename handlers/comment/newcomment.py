from handlers import ViewHandler
from utility import validate
import json
import entities


# Handler for new comments
class NewCommentHandler(ViewHandler):

    # This handler only accepts post requests and we make sure that post is
    # valid and user is authenticated with the decorators and pass in the
    # json parameter to the decorator to send json response in case of error
    @ViewHandler.is_post_valid("json")
    @ViewHandler.is_user_authenticated("json")
    def post(self, post_id):
        # Get the comment from the request
        comment = self.request.get("comment")
        params = {"comment": comment}

        # Check if the comment is valid
        comment_error = validate.is_valid_comment(comment)
        if comment_error:
            params["error"] = comment_error
            self.response.write(json.dumps(params))
        else:
            # Create the comment object in the database
            comment = (entities.Comments
                       .create(comment, self.user.username,
                               post_id))

            # if comment was created then we return the relevant data in
            # json format to the user otherwise we return an error
            if comment:
                params["success"] = "true"
                params["username"] = comment.username
                params["created"] = (comment.created
                                     .strftime('%Y-%m-%d %H:%M:%S'))
                params["comment_id"] = comment.key().id()
                self.response.write(json.dumps(params))
            else:
                params["error"] = "Unknown error"
                self.response.write(json.dumps(params))
