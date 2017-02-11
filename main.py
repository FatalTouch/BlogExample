import webapp2
import os
import jinja2
import helpers
import data
import datetime
import time
import validate
import json


# JE = JINJA ENVIRONMENT
#


# The path for our templates/views
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "views")
# Initialize the Jinja2 template engine
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.
                                       FileSystemLoader(TEMPLATE_PATH),
                                       autoescape=True)


# Main view handler that inherits from the webapp2.RequestHandler
class ViewHandler(webapp2.RequestHandler):

    # write function that writes a response
    def write(self, *args, **kwargs):
        self.response.write(*args, **kwargs)

    # render_str function which gets the view from the directory configured
    # in the Jinja environment
    @staticmethod
    def render_str(view, **kwargs):
        v = JINJA_ENVIRONMENT.get_template(view)
        return v.render(**kwargs)

    # render function that takes in a view name and dictionary args that can
    # passed to jinja while rendering the view
    def render(self, view, **kwargs):
        self.write(self.render_str(view, **kwargs))

    # function to create a cookie for the user by using the name and values
    # provided to the function
    def set_secure_cookie(self, name, val, remember):
        cookie_val = helpers.create_secure_val(val)
        # Create a long term cookie if the user wishes to be signed-in
        if remember:
            expire_time = (datetime.datetime.utcnow() +
                           datetime.timedelta(days=30))
        else:
            expire_time = None
        self.response.set_cookie(name, value=cookie_val,
                                 expires=expire_time, path='/')

    # function to read a secure cookie and make sure the it isn't forged
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and helpers.check_secure_val(cookie_val)

    # function to login and set a cookie
    def login(self, user, remember):
        self.set_secure_cookie('user_id', str(user.key().id()), remember)

    # function to logout and delete the values in the cookie
    def logout(self):
        self.response.set_cookie('user_id', value='', max_age=None, path='/')

    # function that is called every time the page is initialized so we have
    # the user object on every page
    def initialize(self, *args, **kwargs):
        webapp2.RequestHandler.initialize(self, *args, **kwargs)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and data.User.get_by_id(int(uid))


# Handler for our main home page
class MainPage(ViewHandler):
    def get(self):
        params = {}
        # If user is authenticated set the user object in JE
        if self.user:
            params["user"] = self.user
        # Get all the latest posts and the object in JE
        latest_posts = data.BlogPost.get_latest()
        if latest_posts:
            params["latest"] = latest_posts
            # Render the index.html view with the params
            self.render("index.html", **params)


# Handler for our signup page
class SignupPage(ViewHandler):

    # Get request handler
    def get(self):
        # If user is already logged in, send back to home page otherwise
        # render the signup.html view
        if self.user:
            self.redirect('/')
        else:
            self.render("signup.html")

    # Post request handler
    def post(self):
        params = {}
        has_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        # Set the username and email the to be same as they are received
        params["username"] = username
        params["email"] = email

        # check if user name has any error
        username_error = validate.is_valid_username(username)
        if username_error:
            params["error"] = username_error
            has_error = True

        # check if password has any error
        password_error = validate.is_valid_password(password, verify)
        if password_error:
            params["error"] = password_error
            has_error = True

        # check if email has any error
        email_error = validate.is_valid_email(email)
        if email_error:
            params["error"] = email_error
            has_error = True

        # if there are errors on the page render back the signup.html
        # view and include the errors to be shown to the user
        if has_error:
            self.render("signup.html", **params)
        else:
            # If there are no errors then create a new user in the database
            user = data.User.create_user(username, password, email)
            if user:
                # Login the user and redirect them to welcome page
                self.login(user, False)
                self.redirect('/welcome')
            else:
                # Otherwise some db error occurred and we render the
                # signup.html view again
                params["error"] = "Unable to create user due to unknown error"
                self.render("signup.html", **params)


# Handler for the the welcome page
class WelcomePage(ViewHandler):
    def get(self):
        # If user is logged in render the welcome.html view
        # otherwise redirect them to the signup page
        if self.user:
            self.render("welcome.html", username=self.user.username)
        else:
            self.redirect('/signup')


# Handler for logout page
class LogoutPage(ViewHandler):
    def get(self):
        # If user is logged in call the logout method and redirect them to
        # the home page, otherwise just redirect them to home page
        if self.user:
            self.logout()
            self.redirect('/')
        else:
            self.redirect('/')


# Handler for login page
class LoginPage(ViewHandler):
    # Get request handler
    def get(self):
        # If user is already logged in redirect them to home, otherwise
        # render the login.html view
        if self.user:
            self.redirect('/')
        else:
            self.render("login.html")

    # Post request handler
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        remember = self.request.get("remember")

        # Authenticate the user and if we get back a truthy response
        # login the user, otherwise render login.html view with the
        # error and passing back the username so it is preserved
        user = data.User.authenticate(username, password)
        if user:
            self.login(user, remember)
            self.redirect('/welcome')
        else:
            self.render("login.html", error="Invalid login", username=username)


# Handler for the new post page
class NewPostPage(ViewHandler):

    # Get request handler
    def get(self):
        # If the user is logged in render the newpost.html view otherwise
        # redirect them to login page
        if self.user:
            self.render("newpost.html", user=self.user)
        else:
            self.redirect('/login')

    # Post request handler
    def post(self):
        params = {}
        has_error = False
        subject = self.request.get("subject")
        content = self.request.get("content")
        params["subject"] = subject
        params["content"] = content

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

        # if there are any errors render the newpost.html view with
        # errors shown to the user
        if has_error:
            self.render("newpost.html", **params)
        else:
            # Escape the content to remove html tags and create a new blog
            # post in the db, if the post is created redirect the user to the
            # post page otherwise show an error
            content = helpers.basic_escape(content)
            post = data.BlogPost.create(subject, content, self.user.username)
            if post:
                self.redirect('/post?id=%s' % str(post.key().id()))
            else:
                params["error"] = ("An unknown error "
                                   "occurred. Please try again later")
                self.render("newpost.html", **params)


# Handler for the post page
class PostPage(ViewHandler):

    # Static method that gets the comments and likes for the post
    @staticmethod
    def get_comments_and_likes(params, post_id):
        comments = data.Comments.get_comments_by_post(post_id)
        if comments:
            params["comments"] = comments

        likes = data.Likes.get_total_likes(post_id)
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
            post = data.BlogPost.get_by_id(int(post_id))

            # If the user is logged in check if they are not the owner of the
            # post and show a like/dislike button
            if self.user:
                params["user"] = self.user
                if not self.user.username == post.username:
                    params["like_status"] = data.Likes.get_status(
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
        post = data.BlogPost.get_by_id(int(post_id))

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
                params["like_status"] = data.Likes.get_status(
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
                    if not data.BlogPost.exists(post_id):
                        params["comment_error"] = "Invalid action"
                        has_error = True

                    # If there are any errors render the post.html view with
                    # the errors shown to the user
                    if has_error:
                        self.get_comments_and_likes(params, post_id)
                        self.render("post.html", **params)
                    else:
                        # Create the comment object in the database
                        comment = (data.Comments
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
                        post = data.BlogPost.get_by_id(int(post_id))
                        if post.username == self.user.username:
                            data.BlogPost.delete_post(post_id)

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
                        post = data.BlogPost.get_by_id(int(post_id))
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
                            post = data.BlogPost.edit(subject, content,
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


# Handler for comments
class CommentHandler(ViewHandler):

    # This one only contains post handler!
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
                    comment = data.Comments.get_by_id(int(comment_id))

                    # Check if the current user is owner of the comment
                    if comment.username == self.user.username:

                        # Delete the comment and wait 0.1 seconds and redirect
                        # to the post
                        data.Comments.delete_comment(comment_id)
                        time.sleep(0.1)
                        self.redirect('/post?id=' + str(comment.post_id))
                    else:
                        self.redirect('/post?id=' + str(comment.post_id))
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
                if not data.BlogPost.exists(post_id):
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
                    comment = (data.Comments
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


# Handler for likes
class LikeHandler(ViewHandler):

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
                    result = data.Likes.like(self.user.username, post_id)
                    params["like_status"] = 'like'

                # If action is unlike then call the unlike method of Likes
                # entity
                elif action == 'unlike':
                    result = data.Likes.unlike(self.user.username, post_id)
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


# Mapping urls to the specific handlers
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', SignupPage),
    ('/login', LoginPage),
    ('/welcome', WelcomePage),
    ('/logout', LogoutPage),
    ('/newpost', NewPostPage),
    ('/post', PostPage),
    ('/comment', CommentHandler),
    ('/likes', LikeHandler)
], debug=True)
