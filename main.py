import webapp2
import os
import jinja2
import helpers
import data
import datetime
import time
import validate
import json

# The path for our templates/views
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "views")
# Initialize the Jinja2 template engine
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.
                                       FileSystemLoader(TEMPLATE_PATH),
                                       autoescape=True)


class ViewHandler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.write(*args, **kwargs)

    @staticmethod
    def render_str(view, **kwargs):
        v = JINJA_ENVIRONMENT.get_template(view)
        return v.render(**kwargs)

    def render(self, view, **kwargs):
        self.write(self.render_str(view, **kwargs))

    def set_secure_cookie(self, name, val, remember):
        cookie_val = helpers.create_secure_val(val)
        if remember:
            expire_time = (datetime.datetime.utcnow() +
                           datetime.timedelta(days=200))
        else:
            expire_time = None
        self.response.set_cookie(name, value=cookie_val,
                                 expires=expire_time, path='/')

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and helpers.check_secure_val(cookie_val)

    def login(self, user, remember):
        self.set_secure_cookie('user_id', str(user.key().id()), remember)

    def logout(self):
        self.response.set_cookie('user_id', value='', max_age=None, path='/')

    def initialize(self, *args, **kwargs):
        webapp2.RequestHandler.initialize(self, *args, **kwargs)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and data.User.get_by_id(int(uid))


class MainPage(ViewHandler):
    def get(self):
        params = {}
        if self.user:
            params["user"] = self.user
        latest_posts = data.BlogPost.get_latest()
        if latest_posts:
            params["latest"] = latest_posts
            self.render("index.html", **params)


class SignupPage(ViewHandler):
    def get(self):
        if self.user:
            self.redirect('/')
        else:
            self.render("signup.html")

    def post(self):
        params = {}
        has_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        params["username"] = username
        params["email"] = email

        username_error = validate.is_valid_username(username)
        if username_error:
            params["error"] = username_error
            has_error = True

        password_error = validate.is_valid_password(password, verify)
        if password_error:
            params["error"] = password_error
            has_error = True

        email_error = validate.is_valid_email(email)
        if email_error:
            params["error"] = email_error
            has_error = True

        if has_error:
            self.render("signup.html", **params)
        else:
            user = data.User.create_user(username, password, email)
            if user:
                self.login(user, False)
                self.redirect('/welcome')
            else:
                params["error"] = "Unable to create user due to unknown error"
                self.render("signup.html", **params)


class WelcomePage(ViewHandler):
    def get(self):
        if self.user:
            self.render("welcome.html", username=self.user.username)
        else:
            self.redirect('/signup')


class LogoutPage(ViewHandler):
    def get(self):
        if self.user:
            self.logout()
            self.redirect('/')
        else:
            self.redirect('/')


class LoginPage(ViewHandler):
    def get(self):
        if self.user:
            self.redirect('/')
        else:
            self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        remember = self.request.get("remember")

        user = data.User.authenticate(username, password)
        if user:
            self.login(user, remember)
            self.redirect('/welcome')
        else:
            self.render("login.html", error="Invalid login", username=username)


class NewPostPage(ViewHandler):
    def get(self):
        if self.user:
            self.render("newpost.html", user=self.user)
        else:
            self.redirect('/login')

    def post(self):
        params = {}
        has_error = False
        subject = self.request.get("subject")
        content = self.request.get("content")
        params["subject"] = subject
        params["content"] = content
        subject_error = validate.is_valid_post_subject(subject)
        if subject_error:
            params["error"] = subject_error
            has_error = True

        content_error = validate.is_valid_post_content(content)
        if content_error:
            params["error"] = content_error
            has_error = True

        if has_error:
            self.render("newpost.html", **params)
        else:
            content = helpers.basic_escape(content)
            post = data.BlogPost.create(subject, content, self.user.username)
            if post:
                self.redirect('/post?id=%s' % str(post.key().id()))
            else:
                params["error"] = ("An unknown error "
                                   "occurred. Please try again later")
                self.render("newpost.html", **params)


class PostPage(ViewHandler):
    def get(self):
        post_id = self.request.get("id")
        if not post_id:
            self.redirect('/')
        else:
            params = {}
            if self.user:
                params["user"] = self.user
            post = data.BlogPost.get_by_id(int(post_id))
            if post:
                params["post"] = post
                comments = data.Comments.get_comments_by_post(post_id)
                if comments:
                    params["comments"] = comments
                self.render("post.html", **params)
            else:
                self.redirect('/')

    def post(self):
        params = {}
        post_id = self.request.get("id")
        if not post_id:
            self.redirect('/')
        post = data.BlogPost.get_by_id(int(post_id))
        if post:
            params["post"] = post
        else:
            self.redirect('/')
        if self.user:
            has_error = False
            params["user"] = self.user
            action = self.request.get("action")
            if action:
                if action == "comment":
                    post_id = self.request.get("post_id")
                    comment = self.request.get("comment")
                    params["comment"] = comment
                    comment_error = validate.is_valid_comment(comment)
                    if comment_error:
                        params["comment_error"] = comment_error
                        has_error = True
                    if not data.BlogPost.exists(post_id):
                        params["comment_error"] = "Invalid action"
                        has_error = True
                    if has_error:
                        comments = data.Comments.get_comments_by_post(post_id)
                        if comments:
                            params["comments"] = comments
                        self.render("post.html", **params)
                    else:
                        comment = (data.Comments
                                   .create(comment, self.user.username,
                                           post_id))
                        if comment:
                            params["comment"] = ""
                            time.sleep(0.1)
                            params["comments"] = (data.Comments
                                                  .get_comments_by_post
                                                  (post_id))
                            self.render("post.html", **params)
                        else:
                            comments = (data.Comments
                                        .get_comments_by_post(post_id))
                            if comments:
                                params["comments"] = comments
                            params["comment_error"] = "Unknown error"
                            self.render("post.html", **params)
                elif action == "delete":
                    post_id = self.request.get("post_id")
                    if post_id:
                        post = data.BlogPost.get_by_id(int(post_id))
                        if post.username == self.user.username:
                            data.BlogPost.delete_post(post_id)
                            time.sleep(0.1)
                            self.redirect('/')
                        else:
                            self.get()
                    else:
                        self.get()
                elif action == "edit":
                    post_id = self.request.get("post_id")
                    if post_id:
                        post = data.BlogPost.get_by_id(int(post_id))
                        params = {}
                        has_error = False
                        subject = self.request.get("subject")
                        content = self.request.get("content")
                        subject_error = validate.is_valid_post_subject(subject)
                        if subject_error:
                            params["error"] = subject_error
                            has_error = True

                        content_error = validate.is_valid_post_content(content)
                        if content_error:
                            params["error"] = content_error
                            has_error = True

                        if not (self.user.username == post.username):
                            params["error"] = "Authorization error"
                            has_error = True

                        if has_error:
                            self.response.out.write(json.dumps(params))
                        else:
                            content = helpers.basic_escape(content)
                            post = data.BlogPost.edit(subject, content, post_id)
                            if post:
                                time.sleep(0.1)
                                params["success"] = "true"
                                self.response.out.write(json.dumps(params))
                            else:
                                params["error"] = ("An unknown error "
                                                   "occurred. Please try again later")
                                self.response.out.write(json.dumps(params))
        else:
            self.redirect('/login')


class CommentHandler(ViewHandler):
    def post(self):
        action = self.request.get("action")
        if action:
            if action == "delete":
                comment_id = self.request.get("comment_id")
                if comment_id:
                    comment = data.Comments.get_by_id(int(comment_id))
                    if comment.username == self.user.username:
                        data.Comments.delete_comment(comment_id)
                        time.sleep(0.1)
                        self.redirect('/post?id=' + str(comment.post_id))
                    else:
                        self.redirect('/post?id=' + str(comment.post_id))
                else:
                    self.redirect('/')
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', SignupPage),
    ('/login', LoginPage),
    ('/welcome', WelcomePage),
    ('/logout', LogoutPage),
    ('/newpost', NewPostPage),
    ('/post', PostPage),
    ('/comment', CommentHandler)
], debug=True)
