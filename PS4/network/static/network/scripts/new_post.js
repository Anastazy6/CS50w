document.addEventListener("DOMContentLoaded", () => {
    console.log("Content loaded.");

    const newPostView       = document.querySelector('#new-post-view');
    const newPostTitle      = document.querySelector('#new-post-title');
    const newPostBody       = document.querySelector('#new-post-body');
    const newPostBtn        = document.querySelector('#new-post-btn');
    const newPostBtnBack    = document.querySelector("#new-post-btn-background");
    const newPostBodyBorder = document.querySelector("#new-post-btn-border");

    // Ensures that the input fields will be empty on loading the page
    newPostTitle.value = '';
    newPostBody.value  = '';

    function closeNewPostView() {
        newPostTitle.value = '';
        newPostBody.value  = '';
        newPostView.style.display = 'none';
    }
    
    newPostBtn.onclick = () => {
        console.log("New post button clicked.");
        newPostView.style.display = 'block';
    }

    newPostBtn.onmouseover = () => {
        newPostBtnBack.style.fill    = "springgreen";
        newPostBodyBorder.style.fill = "forestgreen";
    }

    newPostBtn.onmouseout = () => {
        newPostBtnBack.style.fill    = "powderblue";
        newPostBodyBorder.style.fill = "aqua";
    }

    document.querySelector("#new-post-close-btn").onclick = closeNewPostView;
    
    window.onkeydown = (key) => {
        if (key.code === "Escape" && newPostView.style.display !== 'none') {
            closeNewPostView();
        }
    }

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
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })
    }
})