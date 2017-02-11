from handlers import ViewHandler


# Handler for the the welcome page
class WelcomePage(ViewHandler):
    def get(self):
        # If user is logged in render the welcome.html view
        # otherwise redirect them to the signup page
        if self.user:
            self.render("welcome.html", username=self.user.username)
        else:
            self.redirect('/signup')