'use strict';

const Toast = Swal.mixin({
  toast: true,
  position: 'bottom-end',
  showConfirmButton: false,
  showCloseButton: true,
  timer: 3000,
  timerProgressBar: true,
  didOpen: toast => {
    toast.addEventListener('mouseenter', Swal.stopTimer);
    toast.addEventListener('mouseleave', Swal.resumeTimer);
  },
});

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
const dateText = document.querySelector('#textDate');

console.log('Data survey', dataSurvey);

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

if (dataSurvey.end_date !== '' && dataSurvey.end_date !== null && dataSurvey.end_date !== undefined) {
  dateText.textContent = 'Tiempo límite de formulario: ' + dataSurvey.end_date + ' (Actual)';
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
      if (result === 'Tiempo limite de encuesta modificado correctamente Asunto y mensaje actualizados') {
        Toast.fire({
          icon: 'success',
          title: 'Configuración guardada',
        });
      } else {
        Toast.fire({
          icon: 'error',
          title: 'Error inesperado:' + result,
        });
      }
    },
  });
};
