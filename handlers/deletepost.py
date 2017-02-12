from handlers import ViewHandler
from google.appengine.ext import db
import json
import entities
import time


# Handler for new comments
class DeletePostHandler(ViewHandler):

    # This handler only accepts post requests and we make sure that post is
    # valid and user is owner of the post with the decorators and pass in
    # the json parameter to the decorator to send json response in case of
    # error
    @ViewHandler.is_post_owner("json")
    @ViewHandler.is_post_valid("json")
    def post(self, post_id):
        params = {}
        # Try to delete the post and return an error in case
        # it is unsuccessful
        try:
            entities.BlogPost.delete_post(post_id)
            # Wait 0.1 second as user is instantly redirected back to home page
            # and the changes may have not reflected
            time.sleep(0.1)
            params["success"] = "true"
            self.response.write(json.dumps(params))
        except db.TransactionFailedError:
            params["error"] = "Cannot delete post due to an unknown reason"
            self.response.write(json.dumps(params))


