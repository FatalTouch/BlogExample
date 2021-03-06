(function ($) {
    'use strict';

    /** PAGE VARIABLES START **/

        // Current url of the page without hash strings
    var currentUrl = location.href.replace(location.hash, '');
    // Get The new comment submit button if it exists
    var buttonNewComment = document.getElementById('buttonNewComment');

    // Get all the elements which allow the user to edit the comment.
    var editCommentElements = document.getElementsByClassName('edit-comment');

    // Get all the elements which allow the user to delete the comments
    var deleteCommentElements = document.getElementsByClassName('delete-comment');

    // Element references to be used with the edit post functionality
    var editButton = document.getElementById('edit-button');
    var subjectElement = document.getElementsByName('subject')[0];
    var contentElement = document.getElementsByName('content')[0];
    var subjectElementMain = document.getElementsByClassName('subject')[0];
    var contentElementMain = document.getElementsByClassName('content')[0];
    var errorElement = document.getElementById('error');

    // Reference to cancel edit button
    var cancelEditButton = document.getElementById('cancel-edit');

    // Get our edit form element
    var form = document.getElementById('edit-form');

    // Get the confirm delete button
    var confirmDelete = document.getElementById('confirm-delete');

    // Get the like button element and total likes element
    var likeButton = document.getElementById('like-post');
    var totalLikesElement = document.getElementById('total-likes');

    /** PAGE VARIABLES END **/

        // Function to send an ajax request
    var sendAjaxRequest = function (url, parameters, successFunction, errorFunction) {

            var xmlhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new window.ActiveXObject('Microsoft.XMLHTTP');
            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                    var result = JSON.parse(xmlhttp.response);
                    if (result.success === 'true') {
                        successFunction(result);
                    }
                    else if (result.error) {
                        errorFunction(result);
                    }
                    else {
                        window.alert('Unknown error');
                    }
                }
            };

            xmlhttp.open('POST', url, true);
            xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xmlhttp.send(parameters);
        };



    // function that will be attached to delete button click event
    var deleteCommentHandler = function () {
        var commentId = this.getAttribute('data-comment');
        var url = '/comment/' + commentId + '/delete';
        var elementToDelete = document.getElementById('comment' + commentId);
        var onSuccess = function () {
            $(elementToDelete).remove();
        };

        var onError = function (response) {
            window.alert(response.error);
        };

        sendAjaxRequest(url, '', onSuccess, onError);
    };

    // function that will be attached on edit button click event
    var editCommentHandler = function () {

        // Lots of dynamic elements to be generated so we can use them
        // to allow users to edit their comments
        var commentId = this.getAttribute('data-comment');
        var divElement = document.createElement('div');
        divElement.setAttribute('class', 'col-xs-12');
        var editElement = document.createElement('textarea');
        editElement.setAttribute('class', 'form-control');
        divElement.appendChild(editElement);


        var saveSpan = document.createElement('span');
        var saveButton = document.createElement('button');
        saveButton.setAttribute('type', 'button');
        saveButton.innerHTML = 'Save';
        saveSpan.appendChild(saveButton);

        var cancelSpan = document.createElement('span');
        var cancelButton = document.createElement('button');
        cancelButton.setAttribute('type', 'button');
        cancelButton.innerHTML = 'Cancel';
        cancelSpan.appendChild(cancelButton);

        var errorSpan = document.createElement('span');
        errorSpan.setAttribute('class', 'text-danger');

        var elementToReplace = document.getElementById('comment' + commentId);
        editElement.value = elementToReplace.querySelector('p').innerHTML;

        editElement.parentNode.insertBefore(errorSpan, editElement.nextSibling);
        editElement.parentNode.insertBefore(cancelSpan, editElement.nextSibling);
        editElement.parentNode.insertBefore(saveSpan, editElement.nextSibling);

        elementToReplace.parentNode.replaceChild(divElement, elementToReplace);

        // Attach click event handler to dynamically generated cancel button
        cancelButton.addEventListener('click', function () {
            divElement.parentNode.replaceChild(elementToReplace, divElement);
        });

        // Attach click event handler to dynamically generated save button
        saveButton.addEventListener('click', function () {

            var onSuccess = function () {
                elementToReplace.querySelector('p').innerHTML = editElement.value;
                divElement.parentNode.replaceChild(elementToReplace, divElement);
            };

            var onError = function (response) {
                errorSpan.innerHTML = response.error;
            };

            var url = '/comment/' + commentId + '/edit';
            var parameters = 'comment=' + editElement.value;
            sendAjaxRequest(url, parameters, onSuccess, onError);
        });
    };

    // function that will be attached to confirm delete post event
    var confirmDeleteHandler = function () {
        var url = currentUrl + '/delete';
        var parameters = '';

        var onSuccess = function () {
            window.location = '/';
        };

        var onError = function (response) {
            window.alert(response.error);
        };

        sendAjaxRequest(url, parameters, onSuccess, onError);
    };


    // Function to append a new comment
    var appendNewComment = function (commentId, comment, username, created) {
        var html = '<div class="row comment">' +
            '<div id="comment' + commentId + '" class="col-xs-12 comment">' +
            '<h4 class="comment-user">' +
            username + '<span>' +
            '<time class="timeago"' +
            'datetime="' + created + '+00:00"></time>' +
            '</span>' +
            '</h4>' +
            '<p>' + comment + '</p>' +
            '<span><button type="button" class="delete-comment" data-comment="' +
            commentId + '">Delete</button></span>' +
            '<span><button type="button" class="edit-comment" data-comment="' +
            commentId + '">Edit</button></span>' +
            '</div>' +
            '</div>';
        $('#comments').prepend(html);
        $('time.timeago').timeago();
        $('.edit-comment:first-of-type').click(editCommentHandler);
        $('.delete-comment:first-of-type').click(deleteCommentHandler);
    };

    // Check if edit button was found and attach the handler
    if (editButton) {
        editButton.onclick = function () {

            // Hide the post that is originally shown
            var post = document.getElementsByClassName('post')[0];
            post.style.display = 'none';

            // Display our post editor
            var editForm = document.getElementsByClassName('edit-post')[0];
            editForm.style.display = 'block';

            // Copy subject value from unedited post
            subjectElement.value = document.getElementsByClassName('subject')[0].innerHTML;

            // Copy the content value from unedited post and replace html line breaks with newlines
            var content = document.getElementsByClassName('content')[0].innerHTML;
            content = content.replace(/<br>/g, '\n');
            contentElement.value = content;

        };
    }


    // Attach event handler if button exists and cancel the post editing
    // by showing the un-edited post and hiding the edit form.
    if (cancelEditButton) {
        cancelEditButton.onclick = function () {
            var post = document.getElementsByClassName('post')[0];
            post.style.display = 'block';

            var editForm = document.getElementsByClassName('edit-post')[0];
            editForm.style.display = 'none';
        };
    }

    // Attach to onsubmit if edit form exists
    if (form) {
        form.onsubmit = function () {

            // Variable to hold the values to be sent in the edit-post request
            var subject = subjectElement.value;
            var content = contentElement.value;

            var onSuccess = function () {
                contentElementMain.innerHTML = contentElement.value.replace(/\n/g, '<br>');
                subjectElementMain.innerHTML = subjectElement.value;
                var post = document.getElementsByClassName('post')[0];
                post.style.display = 'block';

                var editForm = document.getElementsByClassName('edit-post')[0];
                editForm.style.display = 'none';
            };

            var onError = function (response) {
                errorElement.innerHTML = response.error;
            };

            var url = currentUrl + '/edit';
            var parameters = 'subject=' + subject + '&content=' + content;
            sendAjaxRequest(url, parameters, onSuccess, onError);

            //return false so we don't submit the form as it is an ajax request!!
            return false;
        };
    }

    // Attach to confirm delete click event if it exists
    if (confirmDelete) {
        confirmDelete.addEventListener('click', confirmDeleteHandler);
    }
    // Attach to click event if the button exists on the page
    if (buttonNewComment) {
        var buttonNewCommentClick = function () {
            var commentElement = document.getElementById('comment');
            var comment = commentElement.value;
            var errorSpan = document.getElementById('errorNewComment');

            var onSuccess = function (data) {
                commentElement.value = '';
                appendNewComment(data.comment_id, data.comment, data.username, data.created);
            };

            var onError = function (response) {
                errorSpan.innerHTML = response.error;
            };
            var parameters = 'comment=' + comment;
            sendAjaxRequest(currentUrl + '/comment', parameters, onSuccess, onError);
        };
        buttonNewComment.addEventListener('click', buttonNewCommentClick);
    }


    // Attach to all edit comment elements on the page if any.
    if (editCommentElements && deleteCommentElements) {
        // Loop through all the editComment elements and attach to click event
        for (var i = 0; i < editCommentElements.length; i++) {
            editCommentElements[i].addEventListener('click', editCommentHandler);
            deleteCommentElements[i].addEventListener('click', deleteCommentHandler);
        }
    }



    // Attach to click event if the button exists
    if (likeButton) {
        likeButton.addEventListener('click', function () {

            // Get the current value of the button and total likes
            var status = likeButton.getAttribute('data-value');
            var action = '';
            var totalLikes = parseInt(totalLikesElement.innerHTML);

            // Make the action be opposite of what the current value is so it can act
            // as a toggle
            if (status === 'like') {
                action = 'unlike';
            }
            else if (status === 'unlike') {
                action = 'like';
            }
            else {
                return;
            }

            var onSuccess = function (data) {
                if (data.like_status === 'like') {
                    likeButton.setAttribute('class', 'btn btn-danger');
                    likeButton.setAttribute('data-value', 'like');
                    likeButton.innerHTML = '<i class=\"fa fa-thumbs-down\"></i> Unlike';
                    totalLikesElement.innerHTML = (totalLikes + 1).toString();
                }
                else if (data.like_status === 'unlike') {
                    likeButton.setAttribute('class', 'btn btn-success');
                    likeButton.setAttribute('data-value', 'unlike');
                    likeButton.innerHTML = '<i class=\"fa fa-thumbs-up\"></i> Like';
                    totalLikesElement.innerHTML = (totalLikes - 1).toString();
                }
            };

            var onError = function (response) {
                window.alert(response.error);
            };

            var url = currentUrl + '/like';
            var parameters = 'action=' + action;

            sendAjaxRequest(url, parameters, onSuccess, onError);
        });
    }


}(jQuery));