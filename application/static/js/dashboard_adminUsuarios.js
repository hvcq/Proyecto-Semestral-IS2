'use strict';

//FILTER

const containerUsers = document.querySelector('.users');

let users = data.dataUsers;

const init = function () {
  for (const user of users) insertRow(user);
};

const insertRow = function (user) {
  containerUsers.insertAdjacentHTML(
    'beforeend',
    `
    <tr id="Encuesta${user.id_survey}">
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
        ${user.registration_date}
      </td>
      <td class="text-center">
        <div class="btn-group dropstart">
          <button class="btn btn-secondary rounded-circle btn-circle p-1" type="button" id="dropdownCenterBtn" data-bs-toggle="dropdown" aria-expanded="false">
            <img class="imgDot" src="/static/resources/dots.png" alt="">
          </button>
          <ul class="dropdown-menu slideInAction animate" aria-labelledby="dropdownCenterBtn" idEncuesta="${users.}" style="z-index: 10000;">
            <li><a typeButton="POST" class="dropdown-item" onclick="showModalSure(event)">Dar de baja</a></li>
            <li><a typeButton="DELETE" class="dropdown-item" onclick="showModalSure(event)">Eliminar</a></li>
          </ul>
        </div>
      </td>
    </tr>
  `
  );
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
