from handlers import ViewHandler
from utility import validate
import json
import entities


# Handler for editing comments
class EditCommentHandler(ViewHandler):

    # This handler only accepts post requests and we make sure that comment is
    # valid and user is owner of the comment with the decorators and pass in
    # the json parameter to the decorator to send json response in case of
    # error
    @ViewHandler.is_comment_owner("json")
    @ViewHandler.is_comment_valid("json")
    def post(self, comment_id):
        # Get the new comment from the request
        comment = self.request.get("comment")
        params = {"comment": comment}

        # Check if the comment is valid or send back an error response in json
        comment_error = validate.is_valid_comment(comment)
        if comment_error:
            params["error"] = comment_error
            self.response.write(json.dumps(params))
        else:
            # Edit the comment object in the database
            comment_db = (entities.Comments
                          .edit(comment, comment_id, self.user.username))

            # if comment was edited then we check for a truthy value and
            # return the success json otherwise an error json
            if comment_db:
                params["success"] = "true"
                self.response.write(json.dumps(params))
            else:
                params["error"] = "Unknown error"
                self.response.write(json.dumps(params))
