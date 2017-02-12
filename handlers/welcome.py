from handlers import ViewHandler


# Handler for the the welcome page
class WelcomePage(ViewHandler):

    # Use the is_user_authenticated decorator to check if user is logged in
    @ViewHandler.is_user_authenticated()
    def get(self):
            self.render("welcome.html", username=self.user.username)
