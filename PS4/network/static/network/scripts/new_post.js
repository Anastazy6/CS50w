document.addEventListener("DOMContentLoaded", () => {

    const newPostView  = document.querySelector('#new-post-view');
    const newPostTitle = document.querySelector('#new-post-title');
    const newPostBody  = document.querySelector('#new-post-body')

    // Ensures that the input fields will be empty on loading the page
    newPostTitle.value = '';
    newPostBody.value  = '';

    function closeNewPostView() {
        newPostTitle.value = '';
        newPostBody.value  = '';
        newPostView.style.display = 'none';
    }
    
    document.querySelector('#new-post-btn').onclick = () => {
        newPostView.style.display = 'block';
    }

    document.querySelector("#new-post-close-btn").onclick = closeNewPostView;
    

    document.querySelector("#new-post-form").onsubmit = () => {
        fetch("/new-post", {
            method: 'POST',
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: newPostTitle.value,
                body:  newPostBody.value
            })
        })
        // return false;
    }
})