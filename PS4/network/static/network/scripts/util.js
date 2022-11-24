/**
 *  Source: https://stackoverflow.com/a/12274886
 *  Allows to set multiple attributes to an element at once.
 *  
 */
Element.prototype.setAttributes = function(attributes) {
  for (let index in attributes) {
    if ((index === 'styles' || index === 'style') && typeof attributes[index] === 'object') {
      for (let property in attributes[index]) {
        this.style[property] = attributes[index][property];
      }
    } else if (index === 'html') {
      this.innerHTML = attributes[index];
    } else {
      this.setAttribute(index, attributes[index]);
    }
  }
}


$(document).ready(function () {
  
  $('.add-stuff-button').each(function() {
    const background = this.querySelector(".add-stuff-btn-background");
    const border     = this.querySelector(".add-stuff-btn-border");

    this.onmouseover = () => {
      background.style.fill = "springgreen";
      border    .style.fill = "forestgreen";
    }

    this.onmouseout = () => {
      background.style.fill = "powderblue";
      border    .style.fill = "aqua";
    }
  })

  /**************************************************
  ***                                             ***
  ***           Views-closing functions           ***
  ***                                             ***
  ***************************************************/

  function closeReactionsInterface() {
    $("#reactions-interface").innerHTML = '';
    $("#reactions-interface-container").css('display', 'none');
  }

  $('#add-reactions-close-btn').click(function() {
    closeReactionsInterface();
  })

  $("#reactions-interface-container").click(function(event) {
    // Ensure that the event won't trigger if a child node is clicked.
    if (this === event.target) { closeReactionsInterface(); }
  })

  function closeNewPostView() {
    $("#new-post-title").value = '';
    $("#new-post-body").value  = '';
    $("#new-post-view").css('display', 'none');
  }

  $("#new-post-close-btn").click(function() {
    closeNewPostView();
  })

  $("#new-post-view").click(function(event) {
    // Ensure that the event won't trigger if a child node is clicked.
    if (this === event.target) { closeNewPostView() };
  })

  // For the Escape key to close both New Post and Reactions Interface views
  //   both closing functions have to be assigned to a single .onkeydown event.
  //   Otherwise the second event assignment will replace the first one.     
  window.onkeydown = (key) => {
    if (key.code === "Escape") {
      closeReactionsInterface();
      closeNewPostView();
    }
  }
})