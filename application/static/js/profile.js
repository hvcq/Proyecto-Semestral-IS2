'use strict';

let selected = '';

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
      if (selected === '') {
        Swal.showValidationMessage(`No has seleccionado un avatar`);
      } else {
        return delay();
      }
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then(result => {
    // $.ajax({
    //   url: '/state_user',
    //   type: 'POST',
    //   data: { response: JSON.stringify(response) },
    //   success: function (result) {},
    // });
    if (result.isConfirmed) {
      if (selected) Swal.fire('Guardado!', 'Tu avatar fue guardado con exito.', 'success');
      // Swal.fire('Error!', 'Ha ocurrido un problema inesperado.', 'error');
      setImage();
    } else {
    }
  });
};

console.log(data);

const btnDeactivate = document.querySelector('.btnDeactivate');
const btnActivate = document.querySelector('.btnActivate');

data.dataUser.estado ? btnDeactivate.classList.remove('d-none') : btnActivate.classList.remove('d-none');

const dataUser = data.dataUser;

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
