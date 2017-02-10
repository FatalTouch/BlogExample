import re
import data
import helpers


# User Registration input validations
def is_valid_username(username):
    if username:
        user_re = re.compile(r"^[a-zA-Z0-9_-]{4,20}$")
        if user_re.match(username):
            if not data.User.check_username(username):
                return None
            else:
                return "Username already exists"
        else:
            return ("User name is not valid. Please make sure "
                    "it is between 4-20 characters and doesn't "
                    "contain any special symbols.")
    else:
        return "*Username can't be empty."


def is_valid_password(password, verify):
    if password and verify:
        if password != verify:
            return "Password and confirmation password do not match"
        else:
            password_re = re.compile(r"^.{6,30}$")
            if password_re.match(password):
                return None
            else:
                return ("Password is not valid. Please make sure it is "
                        "between 6-30 characters.")
    else:
        return "Password or confirmation password can't be empty."


def is_valid_email(email):
    if email:
        email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if email_re.match(email):
            return None
        else:
            return "Email address entered is not valid."
    else:
        return None


def is_valid_password_hash(username, password, h):
    salt = h.split('|')[1]
    return h == helpers.make_pw_hash(username, password, salt)


def is_valid_post_subject(subject):
    if subject:
        if len(subject) > 150:
            return "Subject can't contain more than 150 characters"
        else:
            return None
    else:
        return "*Post subject can't be empty"


def is_valid_post_content(content):
    if content:
        if len(content) > 5000:
            return "Content can't contain more than 5000 characters"
        else:
            return None
    else:
        return "*Post content can't be empty"


def is_valid_comment(comment):
    if comment:
        if len(comment) > 500:
            return "Comment can't contain more than 500 characters"
        else:
            return None
    else:
        return "*Comment can't be empty"
