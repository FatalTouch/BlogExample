import datetime
import os
import jinja2
import webapp2
import entities
import json
import sys
import functools
from utility import helpers

# The path for our templates/views
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', "views")
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
        self.user = uid and entities.User.get_by_id(int(uid))

    # Function decorator to check if the user is authenticated which takes
    # an optional argument to specify the response type
    @staticmethod
    def is_user_authenticated(response_type=None):
        def user_authenticated(f):
            @functools.wraps(f)
            def wrap(self, *args, **kwargs):
                if self.user:
                    x = f(self, *args, **kwargs)
                else:
                    if response_type == 'json':
                        x = self.response.write(json.dumps({
                            "error": "User not authorized"
                        }))
                    else:
                        x = self.redirect('/login')
                return x
            return wrap
        return user_authenticated

    # Decorator to check if a post_id is valid and exists in the database
    # takes an optional argument to specify response type
    @staticmethod
    def is_post_valid(response_type=None):
        def post_valid(f):
            @functools.wraps(f)
            def wrap(self, post_id, *args, **kwargs):
                if helpers.is_valid_int64(post_id):
                    post = entities.BlogPost.get_by_id(int(post_id))
                    if post:
                        x = f(self, post_id, *args, **kwargs)
                    else:
                        if response_type == 'json':
                            x = self.response.write(json.dumps({
                                "error": "Invalid post id"
                            }))
                        else:
                            x = self.redirect('/')
                else:
                    x = self.redirect('/')
                return x
            return wrap
        return post_valid

    # Decorator to check if a comment_id is valid and exists in the database
    # takes an optional argument to specify response type
    @staticmethod
    def is_comment_valid(response_type=None):
        def comment_valid(f):
            @functools.wraps(f)
            def wrap(self, comment_id, *args, **kwargs):
                if helpers.is_valid_int64(comment_id):
                    comment = entities.Comments.get_by_id(int(comment_id))
                    if comment:
                        x = f(self, comment_id, *args, **kwargs)
                    else:
                        if response_type == 'json':
                            x = self.response.write(json.dumps({
                                "error": "Invalid comment id"
                            }))
                        else:
                            x = self.redirect('/')
                else:
                    x = self.redirect('/')
                return x
            return wrap
        return comment_valid

    # Decorator to check if the current user is owner of the current comment
    # takes an optional argument to specify response type
    @staticmethod
    def is_comment_owner(response_type=None):
        def comment_owner(f):
            @functools.wraps(f)
            def wrap(self, comment_id, *args, **kwargs):
                comment = entities.Comments.get_by_id(int(comment_id))
                if self.user:
                    if self.user.username == comment.username:
                        x = f(self, comment_id, *args, **kwargs)
                    else:
                        if response_type == 'json':
                            x = self.response.write(json.dumps({
                                "error": "Invalid user"
                            }))
                        else:
                            x = self.redirect('/')
                else:
                    if response_type == 'json':
                        x = self.response.write(json.dumps({
                            "error": "User not authorized"
                        }))
                    else:
                        x = self.redirect('/login')
                return x
            return wrap
        return comment_owner

    # Decorator to check if the current user is owner of the current comment
    # takes an optional argument to specify response type
    @staticmethod
    def is_post_owner(response_type=None):
        def post_owner(f):
            @functools.wraps(f)
            def wrap(self, post_id, *args, **kwargs):
                post = entities.BlogPost.get_by_id(int(post_id))
                if self.user:
                    if self.user.username == post.username:
                        x = f(self, post_id, *args, **kwargs)
                    else:
                        if response_type == 'json':
                            x = self.response.write(json.dumps({
                                "error": "Invalid user"
                            }))
                        else:
                            x = self.redirect('/')
                else:
                    if response_type == 'json':
                        x = self.response.write(json.dumps({
                            "error": "User not authorized"
                        }))
                    else:
                        x = self.redirect('/login')
                return x
            return wrap
        return post_owner
