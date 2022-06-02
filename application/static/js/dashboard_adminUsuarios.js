'use strict';

//FILTER

let containerUsers = document.querySelector('.users');
const totalUsers = document.querySelector('.totalUsers');
const theadUsers = document.querySelector('.theadUsers');

totalUsers.textContent = data.dataUsers.length + ' Total';

let users = data.dataUsers;

let idMax = -1;

users.map(element => {
  if (element.id_user > idMax) idMax = element.id_user;
});

users.sort(function (a, b) {
  return a.name > b.name;
});

const init = function () {
  for (const user of users) insertRow(user);
};

const insertRow = function (user) {
  containerUsers.insertAdjacentHTML(
    'beforeend',
    `
    <tr id="User${user.id_user}">
      <td scope="row">
        <input class="form-check-input" type="checkbox">
      </td>
      <td filtroTitle="true">${user.name}</td>
      <td>
        ${user.lastName}
      </td>
      <td>
        ${user.email}
      </td>
      <td>
        ${user.age}
      </td>
      <td>
        ${user.rut}
      </td>
      <td>
        <small class="d-flex justify-content-center fw-semibold ${
          user.state ? ' text-success bg-success border-success' : ' text-danger bg-danger border-danger'
        } bg-opacity-10 border border-opacity-10 rounded-2 ps-2 pe-2 pt-1 pb-1" style="width: 40%">
        ${user.state ? 'Activo' : 'Inactivo'}</small>
      </td>
      <td class="text-center">
        <div class="btn-group dropstart">
          <button class="btn btn-secondary rounded-circle btn-circle p-1" type="button" id="dropdownCenterBtn" data-bs-toggle="dropdown" aria-expanded="false">
            <img class="imgDot" src="/static/resources/dots.png" alt="">
          </button>
          <ul class="dropdown-menu slideInAction animate" aria-labelledby="dropdownCenterBtn" idUser="${users.id_user}" style="z-index: 10000;">
            <li><a typeButton="POST" class="dropdown-item" onclick="showModalSure(event)">Dar de baja</a></li>
            <li><a typeButton="DELETE" class="dropdown-item" onclick="showModalSure(event)">Eliminar</a></li>
          </ul>
        </div>
      </td>
    </tr>
  `
  );
};
init();

const addUser = function (event) {
  let inputAdd;
  const atribute = event.target.getAttribute('isImage') ? true : false;
  atribute ? (inputAdd = event.target.parentElement.previousElementSibling) : (inputAdd = event.target.previousElementSibling);

  const textInput = inputAdd.value;
  const textInputFilter = [...inputAdd.value];

  const filterResult = users.filter(user => user.email === textInput);

  if (filterResult.length !== 0) {
    console.log('El email ya existe');
    return;
  }

  const isValid = textInputFilter.filter(char => char === '@');

  if (isValid.length === 0) {
    console.log('Error email no valido');
    return;
  }

  const element = {
    id_user: idMax + 1,
    name: 'Anonimo',
    lastName: 'None',
    email: textInput,
    age: 'None',
    registration_date: 'None',
    gender: 'None',
    state: true,
    rut: 'xx.xxx.xxx-x',
  };

  //Falta la ruta

  $.ajax({
    url: '/agregar_usuario',
    type: 'POST',
    data: { response: JSON.stringify(element) },
    success: function (result) {
      console.log(result);
    },
  });

  users.push(element);

  insertRow(element);

  idMax++;
};

// ############################### Filtros

const removeChild = function () {
  while (containerUsers.lastElementChild) {
    containerUsers.removeChild(containerUsers.lastElementChild);
  }
};

const filterUser = function (event) {
  const dropdownParent = document.querySelector('.btnOrder');
  const filter = event.target.textContent;

  dropdownParent.textContent = dropdownParent.textContent.split(' ').join('');
  dropdownParent.textContent = dropdownParent.textContent.replace(/(\r\n|\n|\r)/gm, '');

  if (filter === 'Nombre' && dropdownParent.textContent !== 'Nombre') {
    users.sort(function (a, b) {
      return a.name > b.name;
    });
    removeChild();
    init();
  } else if (filter === 'Apellido' && dropdownParent.textContent !== 'Apellido') {
    users.sort(function (a, b) {
      return a.lastName > b.lastName;
    });
    removeChild();
    init();
  } else if (filter === 'Estado' && dropdownParent.textContent !== 'Estado') {
    users.sort(function (a, b) {
      return a.state < b.state;
    });
    removeChild();
    init();
  } else if (filter === 'Edad' && dropdownParent.textContent !== 'Edad') {
    users.sort(function (a, b) {
      return a.age > b.age;
    });
    removeChild();
    init();
  }

  dropdownParent.textContent = event.target.textContent + ' ';
};

const filterSearch = function () {
  let input, filter, tr, txtValue, trList;
  input = document.querySelector('.searchInputUser');
  filter = input.value.toUpperCase();
  trList = document.querySelectorAll('.users tr');
  tr = document.querySelectorAll('.users tr td[filtroTitle]');
  for (let i = 0; i < tr.length; i++) {
    txtValue = tr[i].textContent;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      trList[i].style.display = '';
    } else {
      trList[i].style.display = 'none';
    }
  }
};
