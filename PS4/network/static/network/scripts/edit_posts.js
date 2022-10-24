document.addEventListener('DOMContentLoaded', () => {

  editButtons = document.querySelectorAll(".post-edit");

  editButtons.forEach(button => {
    button.onclick = () => {
      const editedPost = button.parentNode;
      const title      = editedPost.querySelector(".post-title");
      const titleSpan  = editedPost.querySelector(".post-title > span");
      if (title.classList.contains('no-title')) {
        console.log("It has no title!");
      }
      const body  = editedPost.querySelector(".post-body");
      console.log(`Title: "${titleSpan.innerHTML}";\nBody: "${body.innerHTML}";`);

      let editForm = document.createElement('form');
      
      let titleField = document.createElement('input');
      titleField.setAttribute('type', 'text');
      titleField.setAttribute('value', titleSpan.innerHTML);
      titleField.setAttribute('placeholder', 'Title (optional, up to 64 characters).')

      let bodyField = document.createElement('input');
      bodyField.setAttribute('type', 'textarea');
      bodyField.setAttribute('value', body.innerHTML);
      bodyField.setAttribute('placeholder', 'Type your post here (up to 4096 characters).');

      const saveButton = document.createElement('input');
      saveButton.setAttribute('type', 'submit');
      saveButton.setAttribute('value', 'Save');

      editForm.append(titleField);
      editForm.append(bodyField);
      editForm.append(saveButton);

      editedPost.prepend(editForm);
      title.style.display = "None";
      body.style.display  = "None";

      editForm.onsubmit = () => {
        console.log('Tried to submit the edit form');
        return False
      }





    }
  })
})