'use strict';

const showTextArea = event => {
  const switchEvent = event.target;
  const textEvent = switchEvent.getAttribute('id');
  if (textEvent === 'subject') {
    const textArea = document.querySelector('#textSubject');
    switchEvent.checked ? textArea.classList.remove('visually-hidden') : textArea.classList.add('visually-hidden');
  } else {
    const textArea = document.querySelector('#textBody');
    switchEvent.checked ? textArea.classList.remove('visually-hidden') : textArea.classList.add('visually-hidden');
  }
};
