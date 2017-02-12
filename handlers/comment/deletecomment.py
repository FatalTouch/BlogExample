from handlers import ViewHandler
from google.appengine.ext import db
import json
import entities


# Handler for new comments
class DeleteCommentHandler(ViewHandler):

    # This handler only accepts post requests and we make sure that comment is
    # valid and user is owner of the comment with the decorators and pass in
    # the json parameter to the decorator to send json response in case of
    # error
    @ViewHandler.is_comment_owner("json")
    @ViewHandler.is_comment_valid("json")
    def post(self, comment_id):
        params = {}
        # Try to delete the comment and return an error in case
        # it is unsuccessful
        try:
            entities.Comments.delete_comment(comment_id)
            params["success"] = "true"
            self.response.write(json.dumps(params))
        except db.TransactionFailedError:
            params["error"] = "Cannot delete comment due to an unknown reason"
            self.response.write(json.dumps(params))
