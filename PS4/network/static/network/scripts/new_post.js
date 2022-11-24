$(document).ready(function () {
    const newPostView  = document.querySelector('#new-post-view');
    const newPostTitle = document.querySelector('#new-post-title');
    const newPostBody  = document.querySelector('#new-post-body');
    const newPostBtn   = document.querySelector('#new-post-btn');


    // Ensures that the input fields will be empty on loading the page
    newPostTitle.value = '';
    newPostBody.value  = '';
    
    newPostBtn.onclick = () => {
        console.log("New post button clicked.");
        newPostView.style.display = 'block';
    }
    
    newPostBody.addEventListener('keydown', (key) => {
        if (key.key === 'Enter') {
            let cursor = newPostBody.selectionStart;

            newPostBody.innerHTML =
                newPostBody.innerHTML.slice(0, cursor) +
                '\n' +
                newPostBody.innerHTML.slice(cursor);
        }
    })


    $("#new-post-form").submit(function () {
        fetch("/new-post", {
            method : 'POST',
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: newPostTitle.value,
                body : newPostBody.value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })
    })
})