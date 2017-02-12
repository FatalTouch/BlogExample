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
    ('/post/([0-9]+)', handlers.PostPage),
    ('/post/([0-9]+)/comment', handlers.comment1.NewCommentHandler),
    ('/comment/([0-9]+)/edit', handlers.comment1.EditCommentHandler),
    ('/comment', handlers.comment.CommentHandler),
    ('/likes', handlers.LikesHandler)
], debug=True)
