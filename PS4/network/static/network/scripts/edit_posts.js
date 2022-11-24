$(document).ready(function () {

  editButtons = document.querySelectorAll(".post-edit");

  editButtons.forEach(button => {
    button.onclick = () => {

      const editedPost     = button.parentNode;
      const title          = editedPost.querySelector(".post-title");
      const titleSpan      = editedPost.querySelector(".post-title > span");
      const body           = editedPost.querySelector(".post-body");
      const editForm       = editedPost.querySelector(".edit-form");
      const editFormInputs = editForm  .querySelector(".input-fields"); 

      // Closes the edit view. All the changes are discarded unless it is invoked
      //   after updating the titleSpan and body (which is only intended to happen
      //   when the database is being updated).
      function closeEditView() {
        editFormInputs.innerHTML = '';
        
        button.value        = 'Edit';
        button.innerHTML    = 'Edit';
        title.style.display = "Block";
        body.style.display  = "Block"; 
      }

   /************
    *** MAIN ***
    ************/

      // If the post isn't currently being edited, the edit button's value is 'Edit',
      //   which means clicking on it will begin editing
      if (button.value === 'Edit') {
        button.value     = 'Close';
        button.innerHTML = 'Close';
        
        // Create an input field for the edited post's title and set it initial value and attributes
        let titleField = document.createElement('input');
        titleField.classList.add('post-edit-title');
        titleField.setAttributes(
          { 'type' : 'text',
            'value': (titleSpan.classList.contains('no-title') ?
                            '' : titleSpan.innerHTML),
            'placeholder': 'Title (optional, up to 64 characters).',
            'maxlength'  : 64
          }
        );

        // Create an input field for the edited post's body and set it initial value and attributes
        let bodyField = document.createElement('textarea');
        bodyField.classList.add('post-edit-body');
        bodyField.setAttributes(
          { 'type'       : 'textarea',
            'placeholder': 'Type your post here (up to 4096 characters).',
            'style'      : `height: ${body.clientHeight + 25}px; padding: 5px;`, 
            'wrap'       : 'hard',
            'maxlength'  : 4096,
            'cols'       : 80
          }
        );
        // Fill the edit body textarea with the contents of the post and remove any <p> or </p> tags
        bodyField.value = body.innerHTML.replace(/<\/?p>/g, '')
                                        .replace(/<br(\s?\/)?>/g, '\n');        

        // Resizes the textarea on input so that it can fit all its content without leaving
        //   too much empty space
        bodyField.addEventListener('input', function() {
          if  (this.scrollHeight > this.clientHeight ||
                  (this.clientHeight + 20) > this.scrollHeight) { 
            
            // Prevents shrinking the textarea pixel by pixel on each input
            this.style.height = '0px';
            // Actually sets the size of the textarea
            this.style.height = `${this.scrollHeight}px`;
          }
        })
        
        // Prevents submitting the form if the 'enter' key is pressed down and
        //   allows the user to add a new line wherever the cursor is.
        bodyField.addEventListener('keydown', (key) => {
          if (key.key === 'Enter') {
            let cursor = bodyField.selectionStart;
            
            bodyField.innerHTML =
                bodyField.innerHTML.slice(0, cursor) +
                '\n' +
                bodyField.innerHTML.slice(cursor);
          }
        })


        // Create a submit button for the form
        const saveButton = document.createElement('input');
        saveButton.classList.add('btn', 'btn-outline-secondary', 'btn-sm');
        saveButton.setAttributes(
          { 'type' : 'submit',
            'value': 'Save'
          }
        );

        // Add the input fields and the save/submit button to the form and then
        //   place the form at the beginning of the post
        editFormInputs.append(titleField);
        editFormInputs.append(bodyField);
        editFormInputs.append(saveButton);
        
        // Hide the post's title and body so that the form appears to have taken their place
        title.style.display = "None";
        body.style.display  = "None";

        editForm.onsubmit = function() {
          fetch(this.action, {
            method: 'POST',
            headers: {
                "X-CSRFToken" : this.querySelector('[name=csrfmiddlewaretoken]').value,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title  : titleField.value,
                body   : bodyField.value,
                post_id: editForm.querySelector('[name=post-id]').value, // Sanity check
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            titleSpan.innerHTML = result['new_title'];
            body.innerHTML = '<p>' + 
                              result['new_body'].replace(/\n{2,}/g, '</p><p>')
                                                .replace(/\n/g,   '</br>') +
                              '</p>';

            if (titleSpan.innerHTML === '') {
              titleSpan.innerHTML = 'No title';
              titleSpan.classList.remove('has-title');
              titleSpan.classList.add   ('no-title');
            } else {
              titleSpan.classList.remove('no-title');
              titleSpan.classList.add   ('has-title');
            }

            closeEditView();
        })
          // Prevent page reload on form submit
          return false;
        }

      // If the post is currently being edited, clicking on the button will cancel
      //   the process and discard any changes
      } else {
        closeEditView()
      }
    }
  })
})