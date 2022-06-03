'use strict';

const containerAnswers = document.querySelector('.answers');

let answers = data.dataAnswers;

const initAns = function () {
  for (const answer of answers) insertRowAnswer(answer);
};

const insertRowAnswer = function (answer) {
  containerAnswers.insertAdjacentHTML(
    'beforeend',
    `
    <tr id="Answer${answer.id_registrado}">
      <td filtroUsuario="true">${answer.nombre}</td>
      <td>
        ${answer.email}
      </td>
      <td>
        ${answer.genero}
      </td>
      <td>
        ${answer.edad}
      </td>
    </tr>
  `
  );
};


initAns();
