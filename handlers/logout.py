from handlers import ViewHandler


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
