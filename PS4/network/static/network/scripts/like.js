$(document).ready(function() {
  const likeForms = document.querySelectorAll("form.like-form");

  likeForms.forEach(likeForm => {
    const likeDiv      = likeForm.parentElement;
    const likesCounter = likeDiv.querySelector('.likes-counter');
    
    likeForm.onsubmit = function() {
      fetch(this.action, {
        method: 'POST',
        headers: {
          "X-CSRFToken" : this.querySelector('[name=csrfmiddlewaretoken]').value,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
        })
      }) // end: fetch
      .then(response => response.json())
      .then(result => {
        likesCounter.innerHTML = result['likes'] == 1 ? '1 like' : `${result['likes']} likes`;
      });
      
      return false;
    } // end: likeForm.onsubmit
    
  }) // end: likeForms.forEach
  
}) // end: $(document).ready