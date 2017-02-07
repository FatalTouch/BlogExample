import webapp2
import os
import jinja2
import re

from google.appengine.ext import ndb

# The path for our templates/views
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "views")
# Initialize the Jinja2 template engine
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.
                                       FileSystemLoader(TEMPLATE_PATH),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


class ViewHandler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.write(*args, **kwargs)

    @staticmethod
    def render_str(view, **kwargs):
        v = JINJA_ENVIRONMENT.get_template(view)
        return v.render(**kwargs)

    def render(self, view, **kwargs):
        self.write(self.render_str(view, **kwargs))


# User Registration input validations

def is_valid_username(username):
    if username:
        user_re = re.compile(r"^[a-zA-Z0-9_-]{4,20}$")
        if user_re.match(username):
            return None
        else:
            return ("User name is not valid. Please make sure "
                    "it is between 4-20 characters and doesn't "
                    "contain any special symbols.")
    else:
        return "*Username can't be empty."


def is_valid_password(password, verify):
    if password and verify:
        if password != verify:
            return "Password and confirmation password do not match"
        else:
            password_re = re.compile(r"^.{6,30}$")
            if password_re.match(password):
                return None
            else:
                return ("Password is not valid. Please make sure it is "
                        "between 6-30 characters.")
    else:
        return "Password or confirmation password can't be empty."


def is_valid_email(email):
    if email:
        email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-"
                              r"9-.]+$)")
        if email_re.match(email):
            return None
        else:
            return "Email address entered is not valid."
    else:
        return None


class SignupPage(ViewHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
        params = {}
        has_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        params["username"] = username
        params["email"] = email

        username_error = is_valid_username(username)
        if username_error:
            params["error"] = username_error
            has_error = True

        password_error = is_valid_password(password, verify)
        if password_error:
            params["error"] = password_error
            has_error = True

        email_error = is_valid_email(email)
        if email_error:
            params["error"] = email_error
            has_error = True

        if has_error:
            self.render("signup.html", **params)
        else:
            self.render("signup.html", **params)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', SignupPage)
], debug=True)
