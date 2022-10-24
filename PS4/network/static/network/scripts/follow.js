document.addEventListener('DOMContentLoaded', () => {

  const followForm = document.querySelector("#follow-form");
  const follower   = document.querySelector('[name="follower"]');
  const followed   = document.querySelector('[name="followed"]');

  followForm.onsubmit = () => {
    fetch("/follow", {
      method: 'POST',
      headers: {
        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        follower: follower.value,
        followed: followed.value
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    });
    return false;
  };
})