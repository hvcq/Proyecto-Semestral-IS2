'use strict';

console.log(data);

const containerUsers = document.querySelector('.users');
const containerQuestions = document.querySelector('#ModalQuestions');

var myModal = new bootstrap.Modal(document.querySelector('.myModalQuestions'), {
  keyboard: false,
});

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
        ${user.apellido}
      </td>
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

const showQuestions = function (event) {
  myModal.show();
};

const containerTitle = document.querySelector('#surveyTitle');

let surveyTitle = data.dataSurveyTitle;

const insertTitle = function (title) {
  containerTitle.insertAdjacentHTML(
    'beforeend',
    `
    <h2>${title.titulo}</h2>
    <h6 class="text-secondary">${title.descripcion}</h6>
  `
  );
};

insertTitle(surveyTitle);

const containerAnswers = document.querySelector('.questions');
const containerAlternatives = document.querySelector('#containerAlternatives');

console.log(containerAnswers);

let answers = data.dataAnswers;

const initAns = function () {
  for (const ans of answers) insertRowAnswer(ans);
};

const insertRowAnswer = function (ans) {
  containerAnswers.insertAdjacentHTML(
    'beforeend',
    `
    <div class="d-flex justify-content-between align-items-center">
      <h1>${ans.numero}) ${ans.enunciado}</h1>
    </div>
  `
  );

  ans.opciones.map(opcion => {
    containerAlternatives.insertAdjacentHTML(
      'beforeend',
      `
      
      <div class="d-flex align-items-center gap-3 mb-2">
        <div class="form-check w-75">
          <input class="form-check-input" type="radio" name="flexRadioDisabled" id="flexRadioDisabled" disabled>
          <label class="form-check-label text-dark">
            ${opcion.opcion}
          </label>
        </div>
        <div class="d-flex gap-5">
          <h6>${opcion.respuestas} respuestas</h6>
          <h6>${opcion.porcentaje}%</h6>
        </div>
      </div>  
      `
    );
  });
};

// insertRowAnswer(answers);

initAns();
//Comentario para que se actualice
