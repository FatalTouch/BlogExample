(function () {
    var editButton = document.getElementById("edit-button");
    var subjectElement = document.getElementsByName('subject')[0];
    var contentElement = document.getElementsByName('content')[0];
    var subjectElementMain = document.getElementsByClassName('subject')[0];
    var contentElementMain = document.getElementsByClassName('content')[0];
    var postIdElement = document.getElementsByName('post_id')[0];
    var errorElement = document.getElementById('error');
    var editCommentElements = document.getElementsByClassName('edit-comment');

    if (editButton) {
        editButton.onclick = function () {
            var post = document.getElementsByClassName('post')[0];
            post.style.display = "none";

            var editForm = document.getElementsByClassName('edit-post')[0];
            editForm.style.display = "block";

            subjectElement.value = document.getElementsByClassName('subject')[0].innerHTML;

            var content = document.getElementsByClassName('content')[0].innerHTML;
            content = content.replace(/<br>/g, '');
            contentElement.value = content;

        };
    }

    var cancelEditButton = document.getElementById('cancel-edit');

    if (cancelEditButton) {
        cancelEditButton.onclick = function () {
            var post = document.getElementsByClassName('post')[0];
            post.style.display = "block";

            var editForm = document.getElementsByClassName('edit-post')[0];
            editForm.style.display = "none";
        }
    }

    var form = document.getElementById('edit-form');
    if (form) {
        form.onsubmit = function () {
            var xmlhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                    var result = JSON.parse(xmlhttp.response);
                    if (result.success == "true") {
                        contentElementMain.innerHTML = contentElement.value;
                        subjectElementMain.innerHTML = subjectElement.value
                        var post = document.getElementsByClassName('post')[0];
                        post.style.display = "block";

                        var editForm = document.getElementsByClassName('edit-post')[0];
                        editForm.style.display = "none";
                    }
                    else if (result.error) {
                        errorElement.innerHTML = result.error;
                    }
                    else {
                        errorElement.innerHTML = 'Unknown Error';
                    }
                }
            }

            var subject = subjectElement.value;
            var content = contentElement.value;
            var post_id = postIdElement.value;

            xmlhttp.open("POST", window.location.href, true);
            xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xmlhttp.send('action=edit&subject=' + subject + '&content=' + content + '&post_id=' + post_id);
            return false;
        }
    }

    if (editCommentElements) {
        for (var i = 0; i < editCommentElements.length; i++) {
            editCommentElements[i].addEventListener('click', function () {

                var comment_id = this.getAttribute('data-comment');
                var divElement = document.createElement('div');
                divElement.setAttribute('class', 'col-xs-12');
                var editElement = document.createElement('textarea');
                editElement.setAttribute('class', 'form-control');
                divElement.appendChild(editElement);


                var saveSpan = document.createElement('span');
                var saveButton = document.createElement('button');
                saveButton.setAttribute('type', 'button');
                saveButton.innerHTML = "Save";
                saveSpan.appendChild(saveButton);

                var cancelSpan = document.createElement('span');
                var cancelButton = document.createElement('button');
                cancelButton.setAttribute('type', 'button');
                cancelButton.innerHTML = "Cancel";
                cancelSpan.appendChild(cancelButton);

                var errorSpan = document.createElement('span');
                errorSpan.setAttribute('class', 'text-danger');

                var elementToReplace = document.getElementById('comment' + comment_id);
                editElement.value = elementToReplace.querySelector('p').innerHTML;

                editElement.parentNode.insertBefore(errorSpan, editElement.nextSibling);
                editElement.parentNode.insertBefore(cancelSpan, editElement.nextSibling);
                editElement.parentNode.insertBefore(saveSpan, editElement.nextSibling);

                elementToReplace.parentNode.replaceChild(divElement, elementToReplace);

                cancelButton.addEventListener('click', function () {
                    divElement.parentNode.replaceChild(elementToReplace, divElement);
                });

                saveButton.addEventListener('click', function () {
                    var xmlhttp = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
                    xmlhttp.onreadystatechange = function () {
                        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                            var result = JSON.parse(xmlhttp.response);
                            if (result.success == "true") {
                                elementToReplace.querySelector('p').innerHTML = editElement.value;
                                divElement.parentNode.replaceChild(elementToReplace, divElement);
                            }
                            else if (result.comment_error) {
                                errorSpan.innerHTML = result.comment_error;
                            }
                            else {
                                errorSpan.innerHTML = 'Unknown Error';
                            }
                        }
                    }

                    var post_id = postIdElement.value;

                    xmlhttp.open("POST", '/comment', true);
                    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    xmlhttp.send('action=edit&comment=' + editElement.value + '&comment_id=' + comment_id + '&post_id=' + post_id);
                    return false;
                });

            })

        }
    }

})();