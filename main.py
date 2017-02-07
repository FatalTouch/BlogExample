import webapp2
import os
import jinja2
import helpers

from google.appengine.ext import db

# The path for our templates/views
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "views")
# Initialize the Jinja2 template engine
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.
                                       FileSystemLoader(TEMPLATE_PATH),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)


class User(db.Model):
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)


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

        username_error = helpers.is_valid_username(username)
        if username_error:
            params["error"] = username_error
            has_error = True

        password_error = helpers.is_valid_password(password, verify)
        if password_error:
            params["error"] = password_error
            has_error = True

        email_error = helpers.is_valid_email(email)
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
