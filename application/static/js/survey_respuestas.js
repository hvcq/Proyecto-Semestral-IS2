'use strict';

console.log(data)

const containerUsers = document.querySelector('.users');

let users = data.dataUsers;

const initUsr = function () {
  for (const user of users) insertRowUser(user);
};

const insertRowUser = function (user) {
  containerUsers.insertAdjacentHTML(
    'beforeend',
    `
    <tr id="User${user.id_registrado}">
      <td filtroUsuario="true">${user.nombre}</td>
      <td>
        ${user.email}
      </td>
      <td>
        ${user.genero}
      </td>
      <td>
        ${user.edad}
      </td>
    </tr>
  `
  );
};

initUsr();

// ------ RESPUESTAS ------

const containerAnswers = document.querySelector('.answers');

let answers = data.dataAnswers;

const initAns = function () {
  for (const ans of answers) insertRowAnswer(ans);
};

const insertRowAnswer = function (ans) {
  containerAnswers.insertAdjacentHTML(
    'beforeend',
    `
    <tr id="Answer${ans.id_pregunta}">
      <td>${ans.numero}</td>
      
    </tr>
  `
  );
};

initAns();

