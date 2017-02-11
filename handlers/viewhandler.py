import datetime
import os
import jinja2
import webapp2
import entities
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