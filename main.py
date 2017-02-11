import webapp2
import handlers

# Mapping urls to the specific handlers
app = webapp2.WSGIApplication([
    ('/', handlers.IndexPage),
    ('/signup', handlers.SignupPage),
    ('/login', handlers.LoginPage),
    ('/welcome', handlers.WelcomePage),
    ('/logout', handlers.LogoutPage),
    ('/newpost', handlers.NewPostPage),
    ('/post', handlers.PostPage),
    ('/comment', handlers.CommentHandler),
    ('/likes', handlers.LikesHandler)
], debug=True)
