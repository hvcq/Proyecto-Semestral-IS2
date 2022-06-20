'use strict';

console.log(document.querySelector('.users'));

console.log(data.dataUsers);

document.querySelector('.users').style.opacity = 1;

const containerUsers = document.querySelector('.usersBody');

let users = data.dataUsers;

const initUsr = function () {
  for (const user of users) insertRowUser(user);
};

const insertRowUser = function (user) {
  containerUsers.insertAdjacentHTML(
    'beforeend',
    `
    <tr id="User${user.id_registrado}">
      <td>${user.nombre}</td>
      <td>
        ${'none'}
      </td>
      <td>
        ${user.email !== '-' ? user.email : 'none'}
      </td>
      <td>
        ${user.genero !== '-' ? user.genero : 'none'}
      </td>
      <td>
        ${user.edad !== '-' ? user.edad : 'none'}
      </td>
    </tr>
  `
  );
};

initUsr();
