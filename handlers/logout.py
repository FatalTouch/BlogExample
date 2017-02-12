from handlers import ViewHandler


# Handler for logout page
class LogoutPage(ViewHandler):

    # Use the is_user_authenticated decorator to check if user is logged in
    @ViewHandler.is_user_authenticated()
    def get(self):
        # call the logout method and redirect user to the home page
        self.logout()
        self.redirect('/')
