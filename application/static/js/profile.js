'use strict';

let selected = '';

let btnDeactivate;
let btnActivate;

if (role !== 'admin') {
  btnDeactivate = document.querySelector('.btnDeactivate');
  btnActivate = document.querySelector('.btnActivate');

  data.dataUser.estado ? btnDeactivate.classList.remove('d-none') : btnActivate.classList.remove('d-none');
}

const dataUser = data.dataUser;
let img = '';

if (avatar !== null) {
  img = avatar;
} else {
  img = role === 'admin' ? '/static/resources/user_blue.png' : '/static/resources/user_red.png';
}
document.querySelector('.profileImgProfile').setAttribute('src', img);

const htmlvar = `<div class="container d-flex flex-column gap-3">
<div class="row">
  <div class="col">
    <img id="avatar1" class="img-fluid avatar" onclick="selectAvatar(event)"src="/static/resources/avatares/user1.png">
  </div>
  <div class="col">
    <img id="avatar2" class="img-fluid avatar" onclick="selectAvatar(event)"src="/static/resources/avatares/user2.png">
  </div>
  <div class="col">
    <img id="avatar3" class="img-fluid avatar" onclick="selectAvatar(event)"src="/static/resources/avatares/user3.png">
  </div>
  <div class="col">
    <img id="avatar4" class="img-fluid avatar" onclick="selectAvatar(event)"src="/static/resources/avatares/user4.png">
  </div>

</div>
<div class="row">
  <div class="col">
    <img id="avatar5" class="img-fluid avatar" onclick="selectAvatar(event)"src="/static/resources/avatares/user5.png">
  </div>
  <div class="col">
    <img id="avatar6" class="img-fluid avatar" onclick="selectAvatar(event)"src="/static/resources/avatares/user6.png">
  </div>
  <div class="col">
    <img id="avatar7" class="img-fluid avatar" onclick="selectAvatar(event)"src="/static/resources/avatares/user7.png">
  </div>
  <div class="col">
    <img id="avatar8" class="img-fluid avatar" onclick="selectAvatar(event)"src="/static/resources/avatares/user8.png">
  </div>

</div>
</div>`;

const selectAvatar = event => {
  if (selected !== '') {
    document.querySelector(`#avatar${selected}`).classList.remove('selected');
  }

  const img = event.target;
  img.classList.add('selected');
  selected = img.attributes[0].value.slice(6);
};

const setImage = () => {
  document.querySelector('.profileImgProfile').setAttribute('src', `/static/resources/avatares/user${selected}.png`);
  document.querySelector('.profileImg').setAttribute('src', `/static/resources/avatares/user${selected}.png`);
  selected = '';
};

async function delay() {
  await new Promise(done => setTimeout(() => done(), 2000));
  return true;
}

const initModal = () => {
  Swal.fire({
    title: 'Selecciona tu avatar',
    html: htmlvar,
    showCloseButton: false,
    showCancelButton: true,
    focusConfirm: false,
    reverseButtons: true,
    confirmButtonText: 'Guardar',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: '#58d68d',
    cancelButtonColor: '#ff3e69',
    showLoaderOnConfirm: true,
    preConfirm: () => {
      const sendData = { user: dataUser.email, url: `/static/resources/avatares/user${selected}.png` };
      if (selected === '') {
        Swal.showValidationMessage(`No has seleccionado un avatar`);
      } else {
        return fetch(`/change_avatar`, {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
          },
          body: JSON.stringify(sendData),
        })
          .then(responseServer => {
            if (!responseServer.ok) {
              throw responseServer.statusText;
            }
            return responseServer.json();
          })
          .then(data => {
            if (data !== 'avatar cambiado correctamente') {
              throw data;
            }
          })
          .catch(error => {
            Swal.showValidationMessage(`Solicitud fallida: ${error}`);
          });
      }
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then(result => {
    if (result.isConfirmed) {
      Swal.fire('Excelente!', 'Avatar guardado correctamente.', 'success');
      setImage();
    }
  });
  selected = '';
};

const activate = function () {
  const response = {
    email: dataUser.email,
    state: true,
  };

  $.ajax({
    url: '/state_user',
    type: 'POST',
    data: { response: JSON.stringify(response) },
    success: function (result) {},
  });
  btnActivate.classList.add('d-none');
  btnDeactivate.classList.remove('d-none');
};

const deactivate = function () {
  const response = {
    email: dataUser.email,
    state: false,
  };

  $.ajax({
    url: '/state_user',
    type: 'POST',
    data: { response: JSON.stringify(response) },
    success: function (result) {},
  });
  btnDeactivate.classList.add('d-none');
  btnActivate.classList.remove('d-none');
};

const containerSurvey = document.querySelector('.surveyBody');

const initSurvey = function () {
  for (const survey of dataUser.encuestas) insertRowSurvey(survey);
};

const insertRowSurvey = function (survey) {
  containerSurvey.insertAdjacentHTML(
    'beforeend',
    `
    <tr>
      <td>${survey.title}</td>
      <td>
        ${survey.date}
      </td>
    </tr>
  `
  );
};

initSurvey();
