'use strict';

// import Swal from 'sweetalert2';

// const Toast = Swal.mixin({
//   toast: true,
//   position: 'top-end',
//   showConfirmButton: false,
//   timer: 3000,
//   timerProgressBar: true,
//   didOpen: toast => {
//     toast.addEventListener('mouseenter', Swal.stopTimer);
//     toast.addEventListener('mouseleave', Swal.resumeTimer);
//   },
// });

// Toast.fire({
//   icon: 'success',
//   title: 'Signed in successfully',
// });

const dataSurvey = data.dataSurvey;
let dataConfiguration = {
  mail_subject: dataSurvey.mail_subject,
  mail_body: dataSurvey.mail_body,
  end_date: dataSurvey.end_date,
  id: dataSurvey.id,
};

document.querySelector('.bodyConfiguration').style.opacity = 1;

const switchSubject = document.querySelector('#subject');
const textSubject = document.querySelector('#textSubject');
const switchBody = document.querySelector('#body');
const textBody = document.querySelector('#textBody');

console.log(dataSurvey);

const setDate = function (event) {
  dataConfiguration.end_date = event.target.value;
  console.log(dataConfiguration.end_date);
};

const setSubject = function (event) {
  dataConfiguration.mail_subject = event.target.value;
  console.log(dataConfiguration.mail_subject);
};

const setBody = function (event) {
  dataConfiguration.mail_body = event.target.value;
  console.log(dataConfiguration.mail_body);
};

if (dataSurvey.mail_subject !== '' && dataSurvey.mail_subject !== null && dataSurvey.mail_subject !== undefined) {
  switchSubject.checked = true;
  textSubject.value = dataSurvey.mail_subject;
  textSubject.classList.remove('visually-hidden');
}

if (dataSurvey.mail_body !== '' && dataSurvey.mail_body !== null && dataSurvey.mail_body !== undefined) {
  switchBody.checked = true;
  textBody.value = dataSurvey.mail_body;
  textBody.classList.remove('visually-hidden');
}

const showTextArea = event => {
  const switchEvent = event.target;
  const textEvent = switchEvent.getAttribute('id');
  if (textEvent === 'subject') {
    const textArea = document.querySelector('#textSubject');
    textArea.value = '';
    switchEvent.checked ? textArea.classList.remove('visually-hidden') : textArea.classList.add('visually-hidden');
  } else {
    const textArea = document.querySelector('#textBody');
    textArea.value = '';
    switchEvent.checked ? textArea.classList.remove('visually-hidden') : textArea.classList.add('visually-hidden');
  }
};

const sendConfiguration = () => {
  $.ajax({
    url: '/cambiar_configuracion_survey',
    type: 'POST',
    data: { surveyConfig: JSON.stringify(dataConfiguration) },
    success: function (result) {
      // delay();
      //if result === true pasa esto. Si no muestra la modal de error.
      // alert(result);
      // delay();
    },
  });
};
