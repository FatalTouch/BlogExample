(function () {
    var editButton = document.getElementById("edit-button");


    editButton.onclick = function () {
        var post = document.getElementsByClassName('post')[0];
        post.style.display = "none";

        var editForm = document.getElementsByClassName('edit-post')[0];
        editForm.style.display = "block";
        var subjectElement = document.getElementsByName('subject')[0];
        subjectElement.value = document.getElementsByClassName('subject')[0].innerHTML;
        var contentElement = document.getElementsByName('content')[0];
        var content = document.getElementsByClassName('content')[0].innerHTML;
        content = content.replace(/<br>/g, '');
        contentElement.value = content;

    };

    var cancelEditButton = document.getElementById('cancel-edit');

    cancelEditButton.onclick = function () {
        var post = document.getElementsByClassName('post')[0];
        post.style.display = "block";

        var editForm = document.getElementsByClassName('edit-post')[0];
        editForm.style.display = "none";

    }
})();