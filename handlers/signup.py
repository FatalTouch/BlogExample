import entities
from handlers import ViewHandler
from utility import validate


# Handler for our signup page
class SignupPage(ViewHandler):

    # Get request handler
    def get(self):
        # If user is already logged in, send back to home page otherwise
        # render the signup.html view
        if not self.user:
            self.render("signup.html")
        else:
            self.redirect('/')

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
            user = entities.User.create_user(username, password, email)
            if user:
                # Login the user and redirect them to welcome page
                self.login(user, False)
                self.redirect('/welcome')
            else:
                # Otherwise some db error occurred and we render the
                # signup.html view again
                params["error"] = "Unable to create user due to unknown error"
                self.render("signup.html", **params)
