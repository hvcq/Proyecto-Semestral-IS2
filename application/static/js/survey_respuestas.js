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
    <tr id="Answer${answer.id_user}">
      <td filtroUsuario="true">${answer.name}</td>
      <td>
        ${answer.status}
      </td>
      <td>
        ${answer.date}
      </td>
      <td>
        ${answer.hour}
      </td>
    </tr>
  `
  );
};

initAns();
