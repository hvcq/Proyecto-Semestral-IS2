'use strict';

//FILTER

let containerUsers = document.querySelector('.users');
const totalUsers = document.querySelector('.totalUsers');
const theadUsers = document.querySelector('.theadUsers');
let current_id;
let ascUser = true;

totalUsers.textContent = data.dataUsers.length + ' Total';

var myModalSure = new bootstrap.Modal(document.querySelector('.myModalSure'), {
  keyboard: false,
});

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

      <th scope="row">${user.id_user + 1}</th>
      <td filtroTitle="true" idElement=${user.id_user}>${user.name}</td>
      <td filtroTitle="true" idElement=${user.id_user}>
        ${user.lastName}
      </td>
      <td filtroTitle="true" idElement=${user.id_user}>
        ${user.email}
      </td>
      <td filtroTitle="true" idElement=${user.id_user}>
        ${user.age}
      </td>
      <td filtroTitle="true" idElement=${user.id_user}>
        ${user.rut}
      </td>
      <td>
        <small id="State${user.id_user}" class="d-flex justify-content-center fw-semibold ${
      user.state ? ' text-success bg-success border-success' : ' text-danger bg-danger border-danger'
    } bg-opacity-10 border border-opacity-10 rounded-2 ps-2 pe-2 pt-1 pb-1" style="width: 40%">
        ${user.state ? 'Activo' : 'Inactivo'}</small>
      </td>
      <td class="text-center">
        <div class="btn-group dropstart">
          <button class="btn btn-secondary rounded-circle btn-circle p-1" type="button" id="dropdownCenterBtn" data-bs-toggle="dropdown" aria-expanded="false">
            <img class="imgDot" src="/static/resources/dots.png" alt="">
          </button>
          <ul class="dropdown-menu slideInAction animate" aria-labelledby="dropdownCenterBtn" idUser="${user.id_user}" style="z-index: 10000;">
          <li><a typeButton="ACTIVATE" class="dropdown-item" onclick="showModalSure(event)">Suscribir</a></li>
            <li><a typeButton="DEACTIVATE" class="dropdown-item" onclick="showModalSure(event)">Dar de baja</a></li>
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

  let textInput = inputAdd.value;
  textInput = textInput.toLowerCase();
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
    name: 'Invitado',
    lastName: 'None',
    email: textInput,
    age: 'None',
    registration_date: 'None',
    gender: 'None',
    state: false,
    rut: 'xx.xxx.xxx-x',
  };

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

  totalUsers.textContent = users.length + ' Total';

  idMax++;

  inputAdd.value = '';
};

const showModalSure = function (event) {
  const parent = event.target.parentNode.parentNode;
  console.log(parent);
  current_id = parent.attributes[2].textContent;
  console.log(current_id);
  const type = event.target.attributes[0].textContent;

  if (type === 'DEACTIVATE') {
    console.log('ENTRO DESACTIVAR');
    deactivate();
  } else if (type === 'ACTIVATE') {
    console.log('ENTRO ACTIVAR');
    activate();
  }
};

const deleteUser = function () {
  const response = {
    id_survey: Number(current_id),
  };

  const trElement = document.querySelector(`#User${current_id}`);
  trElement.remove();

  const usersArray = users.filter(user => `${user.id_user}` !== current_id);
  users = usersArray;
  console.log(users);

  $.ajax({
    url: '/delete_user',
    type: 'POST',
    data: { response: JSON.stringify(response) },
    success: function (result) {},
  });
  totalUsers.textContent = users.length + ' Total';
};

const activate = function () {
  const [userFilter] = users.filter(user => `${user.id_user}` === current_id);
  userFilter.state = true;

  const response = {
    email: userFilter.email,
    state: true,
  };

  console.log(response);

  const stateUser = document.querySelector(`#State${current_id}`);
  console.log();
  stateUser.className = '';
  stateUser.className =
    'd-flex justify-content-center fw-semibold text-success bg-success border-success bg-opacity-10 border border-opacity-10 rounded-2 ps-2 pe-2 pt-1 pb-1';
  stateUser.textContent = 'Activo';

  $.ajax({
    url: '/state_user',
    type: 'POST',
    data: { response: JSON.stringify(response) },
    success: function (result) {},
  });
};

const deactivate = function () {
  const [userFilter] = users.filter(user => `${user.id_user}` === current_id);
  userFilter.state = false;

  const response = {
    email: userFilter.email,
    state: false,
  };

  console.log(response);

  const stateUser = document.querySelector(`#State${current_id}`);
  console.log();
  stateUser.className = '';
  stateUser.className =
    'd-flex justify-content-center fw-semibold text-danger bg-danger border-danger bg-opacity-10 border border-opacity-10 rounded-2 ps-2 pe-2 pt-1 pb-1';
  stateUser.textContent = 'Inactivo';

  $.ajax({
    url: '/state_user',
    type: 'POST',
    data: { response: JSON.stringify(response) },
    success: function (result) {},
  });

  myModalSure.hide();
};

// ############################### Filtros

const removeChild = function () {
  while (containerUsers.lastElementChild) {
    containerUsers.removeChild(containerUsers.lastElementChild);
  }
};

const filterUser = function (event, isChange) {
  const dropdownParent = document.querySelector('.btnOrder');

  dropdownParent.textContent = dropdownParent.textContent.split(' ').join('');
  dropdownParent.textContent = dropdownParent.textContent.replace(/(\r\n|\n|\r)/gm, '');

  const filter = !isChange ? event.target.textContent : dropdownParent.textContent;

  console.log(dropdownParent.textContent !== 'Nombre');

  if (filter === 'Nombre') {
    console.log('Entro');
    users.sort(function (a, b) {
      return ascUser ? a.name > b.name : a.name < b.name;
    });
    removeChild();
    init();
  } else if (filter === 'Apellido') {
    users.sort(function (a, b) {
      return ascUser ? a.lastName > b.lastName : a.lastName < b.lastName;
    });
    removeChild();
    init();
  } else if (filter === 'Estado') {
    users.sort(function (a, b) {
      return ascUser ? a.state < b.state : a.state > b.state;
    });
    removeChild();
    init();
  } else if (filter === 'Edad') {
    users.sort(function (a, b) {
      return ascUser ? a.age > b.age : a.age < b.age;
    });
    removeChild();
    init();
  }

  dropdownParent.textContent = filter + ' ';
};

const changeOrder = event => {
  const dropdownParent = document.querySelector('.btnAsc');
  const filter = event.target.textContent;

  ascUser = filter === 'Ascendente';

  filterUser(null, true);

  dropdownParent.textContent = dropdownParent.textContent.split(' ').join('');
  dropdownParent.textContent = dropdownParent.textContent.replace(/(\r\n|\n|\r)/gm, '');
  dropdownParent.textContent = filter + ' ';
};

const filterSearch = function () {
  let input, filter, tr, txtValue, trList;
  input = document.querySelector('.searchInputUser');
  filter = input.value.toUpperCase();
  trList = document.querySelectorAll('.users tr');
  tr = document.querySelectorAll('.users tr td[filtroTitle]');
  let counter = 0;

  trList = Array.from(trList);

  trList.sort(function (a, b) {
    return a.attributes[0].value.slice(4) > b.attributes[0].value.slice(4);
  });

  for (let i = 0; i < tr.length; i++) {
    console.log('ESTE ES EL VALOR DE COUNTER', counter);
    console.log('valaor de i al principio;:', i);
    txtValue = tr[i].textContent;
    txtValue = txtValue.split(' ').join('');
    txtValue = txtValue.replace(/(\r\n|\n|\r)/gm, '');
    txtValue = txtValue.toUpperCase();
    let idElement = Number(tr[i].attributes[1].value);

    console.log(idElement);

    console.log('LA COMPARATIVA:', txtValue, '/', filter);

    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      console.log('Entro al true');
      trList[idElement].style.display = '';
      console.log(trList[idElement]);
      i += 4 - counter;
      console.log('Este es el valor de i', i);
      counter = 4;
    } else {
      console.log('Entro al false');
      console.log(trList[idElement]);
      trList[idElement].style.display = 'none';
    }
    counter++;

    if (counter >= 4) counter = 0;
  }
};
