from handlers import ViewHandler
import entities
import json


# Handler for likes
class LikesHandler(ViewHandler):

    @ViewHandler.is_post_valid('json')
    @ViewHandler.is_user_authenticated('json')
    # Only post requests for this handler
    def post(self, post_id):
        params = {}
        action = self.request.get("action")
        # if action exists otherwise return json
        # response with the errors
        if action:
            # if action is like then call the like method of Likes entity
            if action == 'like':
                result = entities.Likes.like(self.user.username, post_id)
                params["like_status"] = 'like'

            # If action is unlike then call the unlike method of Likes
            # entity
            elif action == 'unlike':
                result = entities.Likes.unlike(self.user.username, post_id)
                params["like_status"] = 'unlike'
            # If like/unlike was successful then return json success = true
            # otherwise return json with the error
            if result:
                params["success"] = "true"
            else:
                params["error"] = "Unknown error"
        else:
            params["error"] = "Invalid action"
        self.response.write(json.dumps(params))
