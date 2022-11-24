$(document).ready(function() {



  /**************************************************
  ***                  Variables                  ***
  ***************************************************/


  const CSRFToken = document.querySelector("#reactions-csrf-token > [name=csrfmiddlewaretoken]")
  const posts     = document.querySelectorAll('.post');
  
  const reactionsInterfaceContainer = document.querySelector("#reactions-interface-container");
  const reactionsInterface = reactionsInterfaceContainer.querySelector('#reactions-interface');




  /**************************************************
  ***                  Variables                  ***
  ***************************************************
  ***                  Functions                  ***
  ***************************************************/



  function createReactionsInterface(postId, activeReaction) {
    const post      = document.querySelector(`#post-${postId}`);
    const reactions = JSON.parse(sessionStorage.getItem('knownReactions'));

    reactionsInterface.innerHTML = '';
    reactionsInterfaceContainer.style.display = 'block';


    Object.entries(reactions).forEach(([id, _]) => {
      const reaction = document.createElement('div');

      reaction.setAttribute ( 'title', reactions[id]['reaction']);
      reaction.classList.add( 'reaction-category');
      reaction.dataset.id   =  parseInt(id);
      reaction.innerHTML    = `<span class="reaction-emoji">${reactions[id]['emoji']}</span>`
      if (activeReaction === reaction.title) { reaction.classList.add('reaction-active'); }

      reactionsInterface.append(reaction);
    })

    reactionsInterface.childNodes.forEach(reaction => {
      $(reaction).click(function(){
        fetch(`/react/${postId}`, {
          method : 'POST',
          headers: {
            "X-CSRFToken" : CSRFToken.value,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            "id"   : reaction.dataset.id,
            "title": reaction.title
          })
        })
        .then(response => response.json())
        .then(_ => {
          console.log(result)
          getReactions(post);
          // Both will close the reactions interface, the second one is just a fallback. View "./util.js" for more details.
          $('#add-reactions-close-btn').click() || reactionsInterfaceContainer.click(); 
        })
      })
    })
  }


  function updateKnownReactions() {
    fetch('/get-rcategories')
    .then(response => response.json())
    .then(result => {      
      sessionStorage.setItem('knownReactions', JSON.stringify(result));
    });
  }


  function getReactions(post) {
    fetch(`/get_reactions/${post.dataset.postid}`)
    .then(response => response.json())
    .then(result => {

      if ($.isEmptyObject(result)) {
        post.querySelector('.post-reactions').innerHTML =
          '<span class="no-reactions">No reactions</span>';

      } else {
        post.querySelector('.post-reactions').innerHTML = ''; // Clear reactions' field

        Object.keys(result).forEach(key => {
          let reaction = document.createElement("div");
          post.querySelector('.post-reactions').append(reaction);
          
          reaction.classList.add("reaction");
          reaction.setAttribute  ('title', key)
          reaction.innerHTML     = `<span class="reaction-emoji">${result[key]['emoji']}</span>`;
          reaction.dataset.count = result[key]['count'];
          if (result[key]['your_reaction']) {
            reaction.querySelector('span').classList.add("reaction-active");
            post.querySelector('.reaction-btn').dataset.reaction = key;
          }
        });
      }
    })
  }



  /**************************************************
  ***                   Functions                 ***
  ***************************************************
  ***                    Events                   ***
  ***************************************************/



  $('.reaction-btn').click(function () {
    let postId         = this.dataset.postid;         // Added for better readability.
    let activeReaction = this.dataset.reaction;
    
    createReactionsInterface(postId, activeReaction);
  });



  /**************************************************
  ***                    Events                   ***
  ***************************************************
  ***                  Executables                ***
  ***************************************************/



  posts.forEach(post => {
    getReactions(post);
  })

  updateKnownReactions();
  if (!sessionStorage.getItem('knownReactions')) {updateKnownReactions();}
})