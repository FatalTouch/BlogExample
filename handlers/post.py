import json
import time
import entities
from handlers import ViewHandler
from utility import validate, helpers


# Handler for the post page
class PostPage(ViewHandler):

    # Static method that gets the comments and likes for the post
    @staticmethod
    def get_comments_and_likes(params, post_id):
        comments = entities.Comments.get_comments_by_post(post_id)
        if comments:
            params["comments"] = comments

        likes = entities.Likes.get_total_likes(post_id)
        if likes:
            params["total_likes"] = likes
        else:
            params["total_likes"] = 0

    # Get request handler
    def get(self):
        # Get the post_id
        post_id = self.request.get("id")

        # If there's no post id redirect to home
        if not post_id:
            self.redirect('/')
        else:
            params = {}

            # Get the post from the database
            post = entities.BlogPost.get_by_id(int(post_id))

            # If the user is logged in check if they are not the owner of the
            # post and show a like/dislike button
            if self.user:
                params["user"] = self.user
                if not self.user.username == post.username:
                    params["like_status"] = entities.Likes.get_status(
                        self.user.username, post_id)

            # If post exists get the comments and total likes for the post
            # and render the post.html view with the post and comments data,
            # otherwise redirect to home page
            if post:
                params["post"] = post
                self.get_comments_and_likes(params, post_id)
                self.render("post.html", **params)
            else:
                self.redirect('/')

    # Post request handler
    def post(self):
        params = {}

        # Check if the post_id is present otherwise redirect to hoem page
        post_id = self.request.get("id")
        if not post_id:
            self.redirect('/')

        # Get the post object from the database
        post = entities.BlogPost.get_by_id(int(post_id))

        if post:
            params["post"] = post
        else:
            # If the post object is not in the db then redirect to home page
            self.redirect('/')

        # check if the user is logged in otherwise redirect to login page
        if self.user:
            has_error = False
            params["user"] = self.user

            # If the user is logged in check if they are not the owner of the
            # post and show a like/dislike button
            if not self.user.username == post.username:
                params["like_status"] = entities.Likes.get_status(
                    self.user.username, post_id)
            action = self.request.get("action")

            # Check if the action is specified otherwise redirect to get
            # handler for the post
            if action:

                # If action is comment
                if action == "comment":
                    post_id = self.request.get("post_id")
                    comment = self.request.get("comment")
                    params["comment"] = comment

                    # Check if the comment is valid
                    comment_error = validate.is_valid_comment(comment)
                    if comment_error:
                        params["comment_error"] = comment_error
                        has_error = True

                    # Check if the blog post exists
                    if not entities.BlogPost.exists(post_id):
                        params["comment_error"] = "Invalid action"
                        has_error = True

                    # If there are any errors render the post.html view with
                    # the errors shown to the user
                    if has_error:
                        self.get_comments_and_likes(params, post_id)
                        self.render("post.html", **params)
                    else:
                        # Create the comment object in the database
                        comment = (entities.Comments
                                   .create(comment, self.user.username,
                                           post_id))

                        # if the comment object was created then set the
                        # comment box to be blank again otherwise render
                        # the post.html view with errors
                        if comment:
                            params["comment"] = ""

                            # wait 0.1 seconds so we can properly fetch the
                            # newly created object from database
                            time.sleep(0.1)

                            self.get_comments_and_likes(params, post_id)
                            self.render("post.html", **params)
                        else:
                            self.get_comments_and_likes(params, post_id)
                            params["comment_error"] = "Unknown error"
                            self.render("post.html", **params)

                # If action is delete
                elif action == "delete":
                    # Get the post_id from the request
                    post_id = self.request.get("post_id")

                    # if post_id is provided then continue otherwise
                    # render the response from get handler
                    if post_id:

                        # Get the post and check if the current user is the
                        # owner then delete post otherwise render the response
                        # from the get handler
                        post = entities.BlogPost.get_by_id(int(post_id))
                        if post.username == self.user.username:
                            entities.BlogPost.delete_post(post_id)

                            # wait 0.1 seconds so we can render the main page
                            # without the deleted object
                            time.sleep(0.1)
                            self.redirect('/')
                        else:
                            self.get()
                    else:
                        self.get()

                # If action is edit
                elif action == "edit":

                    # Get the post id
                    post_id = self.request.get("post_id")
                    if post_id:

                        # Get the post object from the db
                        post = entities.BlogPost.get_by_id(int(post_id))
                        params = {}
                        has_error = False
                        subject = self.request.get("subject")
                        content = self.request.get("content")

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

                        # Check if the current user is owner of the post
                        if not (self.user.username == post.username):
                            params["error"] = "Authorization error"
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
                                # Wait 0.1 seconds although i think this can be
                                # omitted here since we don't reload the page
                                time.sleep(0.1)
                                params["success"] = "true"
                                self.response.out.write(json.dumps(params))
                            else:
                                # If we can't edit the post send an error json
                                # response
                                params["error"] = ("An unknown error "
                                                   "occurred. Please "
                                                   "try again later")
                                self.response.out.write(json.dumps(params))
                    else:
                        self.redirect('/')
            else:
                self.get()
        else:
            self.redirect('/login')
