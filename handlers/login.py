from handlers import ViewHandler
import entities


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
        user = entities.User.authenticate(username, password)
        if user:
            self.login(user, remember)
            self.redirect('/welcome')
        else:
            self.render("login.html", error="Invalid login", username=username)

