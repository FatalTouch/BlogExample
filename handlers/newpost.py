import entities
from handlers import ViewHandler
from utility import validate, helpers


# Handler for the new post page
class NewPostPage(ViewHandler):

    # Get request handler
    def get(self):
        # If the user is logged in render the newpost.html view otherwise
        # redirect them to login page
        if self.user:
            self.render("newpost.html", user=self.user)
        else:
            self.redirect('/login')

    # Post request handler
    def post(self):
        params = {}
        has_error = False
        subject = self.request.get("subject")
        content = self.request.get("content")
        params["subject"] = subject
        params["content"] = content

        # Check if the subject is valid
        subject_error = validate.is_valid_post_subject(subject)
        if subject_error:
            params["error"] = subject_error
            has_error = True

        # Check if the content is valid
        content_error = validate.is_valid_post_content(content)
        if content_error:
            params["error"] = content_error
            has_error = True

        # if there are any errors render the newpost.html view with
        # errors shown to the user
        if has_error:
            self.render("newpost.html", **params)
        else:
            # Escape the content to remove html tags and create a new blog
            # post in the db, if the post is created redirect the user to the
            # post page otherwise show an error
            content = helpers.basic_escape(content)
            post = entities.BlogPost.create(subject, content, self.user.username)
            if post:
                self.redirect('/post?id=%s' % str(post.key().id()))
            else:
                params["error"] = ("An unknown error "
                                   "occurred. Please try again later")
                self.render("newpost.html", **params)