from handlers import ViewHandler
from utility import validate, helpers
import json
import entities


# Handler for editing posts
class EditPostHandler(ViewHandler):

    # This handler only accepts post requests and we make sure that comment is
    # valid and user is owner of the comment with the decorators and pass in
    # the json parameter to the decorator to send json response in case of
    # error
    @ViewHandler.is_post_owner("json")
    @ViewHandler.is_post_valid("json")
    def post(self, post_id):
        # Get the new comment from the request
        subject = self.request.get("subject")
        content = self.request.get("content")
        params = {}

        has_error = False
        # Check if the subject is valid
        subject_error = validate.is_valid_post_subject(subject)
        if subject_error:
            params["error"] = subject_error
            has_error = True

        # Check if the content is valid
        content_error = validate.is_valid_post_content(content)
        if content_error:
            params["error"] = content_error
            has_error = True

        # If there are any errors return the JSON response
        # with the errors
        if has_error:
            self.response.out.write(json.dumps(params))
        else:
            # Escape the content to sanitize html tags
            content = helpers.basic_escape(content)

            # Call the blog post edit method
            post = entities.BlogPost.edit(subject, content,
                                          post_id)

            # If truthy value is received the send success
            # true json response otherwise send an error
            # response
            if post:
                params["success"] = "true"
                self.response.out.write(json.dumps(params))
            else:
                # If we can't edit the post send an error json
                # response
                params["error"] = ("An unknown error "
                                   "occurred. Please "
                                   "try again later")
                self.response.out.write(json.dumps(params))
