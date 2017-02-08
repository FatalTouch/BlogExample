(function () {
    var form = document.getElementsByTagName('form')[0];
    var usernameElement = document.getElementsByName("username")[0];
    var passwordElement = document.getElementsByName("password")[0];
    var verifyElement = document.getElementsByName("verify")[0];
    var emailElement = document.getElementsByName("email")[0];
    var errorSpan = document.getElementById("error");

    form.onsubmit = function () {
        var username = usernameElement.value;
        var password = passwordElement.value;
        var verify = verifyElement.value;
        var email = emailElement.value;

        var userNameError = IsValidUserName(username);
        if (userNameError) {
            errorSpan.innerHTML = userNameError;
            return false;
        }

        var passwordError = IsValidPassword(password, verify);
        if (passwordError) {
            errorSpan.innerHTML = passwordError;
            return false;
        }

        var emailError = IsValidEmail(email);
        if (emailError) {
            errorSpan.innerHTML = emailError;
            return false;
        }
        return true;
    };

    var IsValidUserName = function (username) {
        if (username) {
            var userReg = new RegExp('^[a-zA-Z0-9_-]{4,20}$');
            if (userReg.exec(username)) {
                return null;
            }
            else {
                return ('User name is not valid. Please make sure it is between 4-20 characters and doesn\'t contain any special symbols.');
            }
        }
        else {
            return ('*Username can\'t be empty.');
        }
    };

    var IsValidPassword = function (password, verify) {
        if (password && verify) {
            if (password != verify) {
                return ('Password and confirmation password do not match');
            }
            else {
                var passReg = new RegExp('^.{6,30}$');
                if (passReg.exec(password)) {
                    return null;
                }
                else {
                    return ('Password is not valid. Please make sure it is between 6-30 characters.');
                }
            }
        }
        else {
            return ('Password or confirmation password can\'t be empty.');
        }
    };
    
    var IsValidEmail = function (email) {
        if(email){
            var emailReg = new RegExp('^[\\S]+@[\\S]+.[\\S]+$');
            if(emailReg.exec(email)){
                return null;
            }
            else{
                return('Email address entered is not valid');
            }

        }
        else{
            return null;
        }
    };
})();