(function () {
    var editButton = document.getElementById("edit-button");
    var subjectElement = document.getElementsByName('subject')[0];
    var contentElement = document.getElementsByName('content')[0];
    var postIdElement = document.getElementsByName('post_id')[0];
    var errorElement = document.getElementById('error');

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
                    console.log(xmlhttp.response)
                    var result = JSON.parse(xmlhttp.response);
                    if (result.success == "true") {
                        location.reload();
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

})();