document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function show_view(viewName, display='block') {
  // Hide all views
  document.querySelectorAll('.js-view').forEach(view => view.style.display = 'none');
  // Show the chosen view
  document.querySelector(`${viewName}`).style.display = display;
}

function compose_email(reply = false) {

  // Show compose view and hide other views
  show_view('#compose-view');

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = reply['sender']  || '';
  document.querySelector('#compose-subject').value    = reply['subject'] || '';
  document.querySelector('#compose-body').value       = reply['body']    || '';

  document.querySelector('#compose-form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject:    document.querySelector('#compose-subject').value,
        body:       document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
    });
    return false;
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  show_view('#emails-view');

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  const emailsView = document.querySelector('#emails-view');

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
  emails.forEach(email => {

    // Create necessary HTML elements for mailvox view
    const element        = document.createElement('div');
    const elementEmail   = document.createElement('div');
    const elementSubject = document.createElement('div');
    const elementTime    = document.createElement('div');

    // Provide each element a CSS class
    element       .classList.add('mailbox-element');
    elementEmail  .classList.add('mailbox-element-email');
    elementSubject.classList.add('mailbox-element-subject');
    elementTime   .classList.add('mailbox-element-time');

    // Provide each element their corresponding value
    if (`${mailbox}` === 'sent') {
      elementEmail.innerHTML = email['recipients'][0];
      if (email['recipients'].length > 1) {elementEmail.innerHTML += ' et al.'} 
    } else {
      elementEmail.innerHTML = email['sender'];
    }
    elementSubject.innerHTML = email['subject'];
    elementTime.innerHTML    = email['timestamp'];

    element.style.background = 'white';
    if (email['read']) {
      element.style.background = 'ghostwhite';
    }
    // Add elements to the mailbox view
    element.append(elementEmail);
    element.append(elementSubject);
    element.append(elementTime);

    element.addEventListener('click', () => load_email(email['id']));

    emailsView.append(element);

  });
  })
}

function load_email(emailId) {

  show_view('#single-email-view');

  const view = document.querySelector('#single-email-view');
  var read;
  
  // Purge the view
  view.innerHTML = '';

  fetch(`/emails/${emailId}`)
  .then(response => response.json())
  .then(email => {
    // After creating the view: if false, a PUT request will be mad to update the mail as read
    read = email['read'];

    // Create necessary HTML elements for single email view
    const emailSender     = document.createElement('div');
    const emailRecipients = document.createElement('div');
    const emailSubject    = document.createElement('div');
    const emailTimestamp  = document.createElement('div');
    const emailBody       = document.createElement('div');
    const archiveButton   = document.createElement('button');
    const replyButton     = document.createElement('button');

    // FIll the HTML elements with email data
    emailSender.innerHTML     = email['sender'];
    emailRecipients.innerHTML = email['recipients'];
    emailSubject.innerHTML    = email['subject'];
    emailTimestamp.innerHTML  = email['timestamp'];
    emailBody.innerHTML       = email['body'];
    archiveButton.innerHTML   = (email['archived']) ? 'Unarchive' : 'Archive';
    replyButton.innerHTML     = "Reply";

    // Add the HTML elements to the email view
    view.append(emailSender);
    view.append(emailRecipients);
    view.append(emailSubject);
    view.append(emailTimestamp);
    view.append(emailBody);
    view.append(archiveButton);
    view.append(replyButton);

    // Add onclick functionality to the archiveButton
    archiveButton.onclick = () => {
      fetch(`/emails/${emailId}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !(email['archived'])
        })
      })
      .then(() => load_mailbox('inbox'))
    };

    // Add onclick functionality to the replyButton
    replyButton.onclick = () => {
      reply = {
        'sender':  email['sender'],
        'subject': email['subject'].startsWith('Re:') ? email['subject'] : `Re: ${email['subject']}`,
        'body':    `On ${email['timestamp']} ${email['sender']} wrote:\r\n${email['body']}\r\n---------------\r\n` 
      };
      return compose_email(reply);
    }
  });

  // Set the email to read if it's not already read.
  if (!read) {
    fetch(`/emails/${emailId}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    });
  }
}
