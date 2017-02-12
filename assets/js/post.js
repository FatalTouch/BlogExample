(function ($) {
    'use strict';

    var currentUrl = location.href.replace(location.hash, '');
    // Element references to be used with the edit post functionality
    var editButton = document.getElementById('edit-button');
    var subjectElement = document.getElementsByName('subject')[0];
    var contentElement = document.getElementsByName('content')[0];
    var subjectElementMain = document.getElementsByClassName('subject')[0];
    var contentElementMain = document.getElementsByClassName('content')[0];
    var postIdElement = document.getElementsByName('post_id')[0];
    var errorElement = document.getElementById('error');

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

    // Reference to cancel edit button
    var cancelEditButton = document.getElementById('cancel-edit');

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

    // Get our edit form and attach onsubmit event handler if it exists
    var form = document.getElementById('edit-form');
    if (form) {
        form.onsubmit = function () {

            // Create new ajax request with fallback to ActiveXobject
            var xmlhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new window.ActiveXObject('Microsoft.XMLHTTP');

            // Attach to onreadystatechange event handler and check for readystate and response
            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                    // Parse the Json result
                    var result = JSON.parse(xmlhttp.response.toString());

                    // Check if operation was successful and copy the new content to be the originial
                    // content so we don't have to refresh the page.
                    if (result.success === 'true') {
                        contentElementMain.innerHTML = contentElement.value.replace(/\n/g, '<br>');
                        subjectElementMain.innerHTML = subjectElement.value;
                        var post = document.getElementsByClassName('post')[0];
                        post.style.display = 'block';

                        var editForm = document.getElementsByClassName('edit-post')[0];
                        editForm.style.display = 'none';
                    }

                    // Show the error if any error is in the response from server
                    else if (result.error) {
                        errorElement.innerHTML = result.error;
                    }
                    else {
                        errorElement.innerHTML = 'Unknown Error';
                    }
                }
            };

            // Variable to hold the values to be sent in the edit-post request
            var subject = subjectElement.value;
            var content = contentElement.value;
            var postId = postIdElement.value;

            // Set the headers, method and other stuff for the request and send it with the
            // parameters required by the server
            xmlhttp.open('POST', window.location.href, true);
            xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xmlhttp.send('action=edit&subject=' + subject + '&content=' + content);

            //return false so we don't submit the form as it is an ajax request!!
            return false;
        };
    }


    // Get the like button element and total likes element
    var likeButton = document.getElementById('like-post');
    var totalLikesElement = document.getElementById('total-likes');

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

            // Send an Ajax request and manipulate the button to be reversed upon each request.
            // so it can act as a toggle button for changing the like/unlike on server and also
            // decrease and increase the total likes by 1
            var xmlhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new window.ActiveXObject('Microsoft.XMLHTTP');
            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                    var result = JSON.parse(xmlhttp.response);
                    if (result.success === 'true') {
                        if (result.like_status === 'like') {
                            likeButton.setAttribute('class', 'btn btn-danger');
                            likeButton.setAttribute('data-value', 'like');
                            likeButton.innerHTML = '<i class=\"fa fa-thumbs-down\"></i> Unlike';
                            totalLikesElement.innerHTML = totalLikes + 1;
                        }
                        else if (result.like_status === 'unlike') {
                            likeButton.setAttribute('class', 'btn btn-success');
                            likeButton.setAttribute('data-value', 'unlike');
                            likeButton.innerHTML = '<i class=\"fa fa-thumbs-up\"></i> Like';
                            totalLikesElement.innerHTML = totalLikes - 1;
                        }
                    }
                    else if (result.error) {
                        window.alert(result.error);
                    }
                    else {
                        window.alert('Unknown error');
                    }
                }
            };

            var postId = postIdElement.value;

            xmlhttp.open('POST', '/likes', true);
            xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xmlhttp.send('&post_id=' + postId + '&action=' + action);
        });
    }

    // Get The new comment submit button if it exists
    var buttonNewComment = document.getElementById('buttonNewComment')

    // Get all the elements which allow the user to edit the comment.
    var editCommentElements = document.getElementsByClassName('edit-comment');

    // Function to send an ajax request
    var SendAjaxRequest = function (url, parameters, successFunction, errorFunction) {

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

    // Function to append a new comment
    var appendNewComment = function (comment_id, comment, username, created) {
        var html = '<div class="row comment">' +
            '<div id="comment' + comment_id + '" class="col-xs-12 comment">' +
            '<h4 class="comment-user">' +
            username + '<span>' +
            '<time class="timeago"' +
            'datetime="' + created + '+00:00"></time>' +
            '</span>' +
            '</h4>' +
            '<p>' + comment + '</p>' +
            '<form action="/comment" method="post">' +
            '<input type="hidden" value="' + comment_id + '" name="comment_id">' +
            '<span><button type="submit" value="delete" name="action">Delete</button></span>' +
            '<span><button type="button" class="edit-comment" data-comment="' + comment_id + '" value="edit"' +
            'name="action">Edit</button></span>' +
            '</form>' +
            '</div>' +
            '</div>';
        $('#comments').prepend(html);
        $('time.timeago').timeago();
        $('.edit-comment:first-of-type').click(editCommentHandler);
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

            var parameters = "comment=" + editElement.value;
            SendAjaxRequest('/comment/' + commentId + '/edit', parameters, onSuccess, onError);
        });
    };


    // Attach to click event if the button exists on the page
    if (buttonNewComment) {
        var buttonNewCommentClick = function () {
            var commentElement = document.getElementById('comment');
            var comment = commentElement.value;
            var errorSpan = document.getElementById('errorNewComment');

            var onSuccess = function (data) {
                commentElement.value = '';
                appendNewComment(data.comment_id, data.comment, data.username, data.created);
            }

            var onError = function (response) {
                errorSpan.innerHTML = response.error
            }
            var parameters = "comment=" + comment;
            SendAjaxRequest(currentUrl + '/comment', parameters, onSuccess, onError);
        }
        buttonNewComment.addEventListener('click', buttonNewCommentClick);
    }


    // Attach to all edit elements on the page if any.
    if (editCommentElements) {
        // Loop through all the editComment elements and attach to click event
        for (var i = 0; i < editCommentElements.length; i++) {
            editCommentElements[i].addEventListener('click', editCommentHandler);

        }
    }

}(jQuery));