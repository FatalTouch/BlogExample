from handlers import ViewHandler
import entities


# Handler for our main home page
class IndexPage(ViewHandler):
    def get(self):
        params = {}
        # If user is authenticated set the user object in JE
        if self.user:
            params["user"] = self.user
        # Get all the latest posts and the object in JE
        latest_posts = entities.BlogPost.get_latest()
        if latest_posts:
            params["latest"] = latest_posts
            # Render the index.html view with the params
            self.render("index.html", **params)
