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
    ('/post/([0-9]+)/edit', handlers.EditPostHandler),
    ('/post/([0-9]+)/delete', handlers.DeletePostHandler),
    ('/post/([0-9]+)/like', handlers.LikesHandler),
    ('/post/([0-9]+)/comment', handlers.comment.NewCommentHandler),
    ('/comment/([0-9]+)/edit', handlers.comment.EditCommentHandler),
    ('/comment/([0-9]+)/delete', handlers.comment.DeleteCommentHandler)

], debug=True)
