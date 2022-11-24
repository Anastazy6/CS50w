$(document).ready(function () {

  // Form and its values
  const followForm   = document.querySelector("#follow-form");
  const follower     = document.querySelector('[name="follower"]').value;
  const followed     = document.querySelector('[name="followed"]').value;
  const followMethod = document.querySelector('#follow-method');

  // Followers and following counters
  const followersCounter = document.querySelector('#followers-counter');
  const followingCounter = document.querySelector('#following-counter');

  followForm.onsubmit = () => {
    fetch("/follow", {
      method : 'POST',
      headers: {
        "X-CSRFToken" : document.querySelector('[name=csrfmiddlewaretoken]').value,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        follower: follower,
        followed: followed
      })
    })
    .then(response => response.json())
    .then(result => {
      if (result['success']) {
        // TODO: Przemyśleć, być może dałoby radę zrobić to za pomocą jednego fetcha, zamiast dwóch.
        //   Odciążyło by to serwer.
        fetch(`/follow?follower=${follower}&followed=${followed}`)
        .then(response => response.json())
        .then(result => {
          followersCounter.innerHTML = result['followers'];
          followingCounter.innerHTML = result['following'];
          followMethod.innerHTML     = result['follow_method'];
        })
      }
    });
    return false;
  };
})