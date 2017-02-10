//IIFE so we don't pollute the global namespace
(function () {
    'use strict';

    // Check if user name is between 4-20 characters and doesn't contain
    // any special character except - and _
    var isValidUserName = function (username) {
        if (username) {
            var userReg = new RegExp('^[a-zA-Z0-9_-]{4,20}$');
            if (userReg.exec(username)) {
                return null;
            } else {
                return ('User name is not valid. Please make sure it is between 4-20 characters' +
                        'and doesn\'t contain any special symbols.');
            }
        } else {
            return ('*Username can\'t be empty.');
        }
    },

        // Check if password is between 6-30 characters and matches with the verify password
        isValidPassword = function (password, verify) {
            if (password && verify) {
                if (password !== verify) {
                    return ('Password and confirmation password do not match');
                } else {
                    var passReg = new RegExp('^.{6,30}$');
                    if (passReg.exec(password)) {
                        return null;
                    } else {
                        return ('Password is not valid. Please make sure it is between 6-30 characters.');
                    }
                }
            } else {
                return ('Password or confirmation password can\'t be empty.');
            }
        },

        // function to validate the email, using a simple regex because we don't want
        // to block anyone with a "valid enough" email address
        isValidEmail = function (email) {
            if (email) {
                var emailReg = new RegExp('^[\\S]+@[\\S]+.[\\S]+$');
                if (emailReg.exec(email)) {
                    return null;
                } else {
                    return ('Email address entered is not valid');
                }

            } else {
                return null;
            }
        },

    // Variables for elements associated with form validation
        form = document.getElementsByTagName('form')[0],
        usernameElement = document.getElementsByName('username')[0],
        passwordElement = document.getElementsByName('password')[0],
        verifyElement = document.getElementsByName('verify')[0],
        emailElement = document.getElementsByName('email')[0],
        errorSpan = document.getElementById('error');

    //Attach on submit event handler to the form and validate data before submitting
    form.onsubmit = function () {

        // Variable to store value of the form validation elements
        var username = usernameElement.value,
            password = passwordElement.value,
            verify = verifyElement.value,
            email = emailElement.value,

            userNameError = isValidUserName(username),
            passwordError = isValidPassword(password, verify),
            emailError = isValidEmail(email);

        //Return false if any of the validation fails otherwise return true and submit the form
        if (userNameError) {
            errorSpan.innerHTML = userNameError;
            return false;
        }

        if (passwordError) {
            errorSpan.innerHTML = passwordError;
            return false;
        }

        if (emailError) {
            errorSpan.innerHTML = emailError;
            return false;
        }
        return true;
    };
}());