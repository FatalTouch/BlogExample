from google.appengine.ext import db
from utility import validate, helpers


# User entity
class User(db.Model):
    # Information to store in the user entity
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    # Class method that can be called to create a user
    @classmethod
    def create_user(cls, username, password, email=None):

        # Hash the pw before saving in database
        hashed_pw = helpers.make_pw_hash(username, password)

        # Save the username in lower case in database
        username = username.lower()

        # Check if email exists and convert it to lower case and save in db
        if email:
            email = email.lower()
            user = cls(username=username, pw_hash=hashed_pw, email=email)
        else:
            user = cls(username=username, pw_hash=hashed_pw)

        # Write the entity to database
        user.put()

        # Return the user that was created
        return user

    # Method to check if the username exists in the database
    @classmethod
    def check_username(cls, username):
        return cls.all().filter('username = ', username.lower()).get()

    # Method to authenticate the user by comparing the password and hashed
    # password
    @classmethod
    def authenticate(cls, username, password):
        username = username.lower()
        user = User.all().filter('username = ', username).get()
        if (user and validate.is_valid_password_hash
                (username, password, user.pw_hash)):
            return user
