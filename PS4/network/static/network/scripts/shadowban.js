$(document).ready(function() {
  const shadowbanForm = document.querySelector("#shadowban-form");
  if (shadowbanForm) {
    console.log("Shadowban form accessible!");
    
    const targetId  = shadowbanForm.querySelector("[name=user_id]").value;
    const CSRFToken = shadowbanForm.querySelector("[name=csrfmiddlewaretoken]");
    const submitBtn = shadowbanForm.querySelector("#shadowban-button");

    console.log(targetId);
    shadowbanForm.onsubmit = () => {
      fetch(`/shadowban/${targetId}`, {
        method: 'POST',
        headers: {
          "X-CSRFToken" : CSRFToken.value,
          "Content-Type": "application/json"
        }
      })
      .then(response => response.json())
      .then(result => {
        submitBtn.value = (result['action'] === 'shadowbanned') ? "Remove shadowban" : "Shadowban"; 

        document.querySelectorAll(".post").forEach(post => {
          const author = post.querySelector(".author > a");

          if (author.innerHTML === result['target_name']) {
            if (result['action'] === 'shadowbanned') {
              post.classList.add("post-shadowbanned");
            } else if (result['action'] === 'shadowban removed') {
              post.classList.remove("post-shadowbanned");
            }
          } else {
            console.log("Warning: invalid shadowban action!");
          }
        })
      })
      return false;
    }
  } else {
    console.log("Shadowban form not accessible!");
  }
})