from handlers import ViewHandler
import entities
import json


# Handler for likes
class LikesHandler(ViewHandler):

    # Only post handler for this one too
    def post(self):
        params = {}

        # Check if the user is logged in otherwise return json error
        # that the request is not authorized
        if self.user:
            post_id = self.request.get("post_id")
            action = self.request.get("action")

            # if both post_id and action exists otherwise return json
            # response with the errors
            if post_id and action:

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
                params["error"] = "No post id specified"
        else:
            params["error"] = "Request not authorized"
        self.response.write(json.dumps(params))
