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

const containerAnswers = document.querySelector('.firstQuestion');
const containerAlternatives = document.querySelector('#containerAlternatives');

console.log(containerAnswers);

let answers = data.dataAnswers;

const initAns = function () {
  for (const ans of answers) insertRowAnswer(ans);
};

const insertRowAnswer = function (ans) {
  containerAnswers.insertAdjacentHTML(
    'afterbegin',
    `
    <div class="d-flex justify-content-between align-items-center">
      <h1>${ans.enunciado}</h1> <!--Mutable-->
      <button class="btn btn-secondary bg-transparent border-0 btnOrder h-50 text-secondary" type="button" id="dropdownMenuButton1"
            data-bs-toggle="dropdown" aria-expanded="false" onclick="showQuestions(event)">
            Ver las preguntas
      </button>
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
        <h6>${opcion.respuestas} respuestas</h6>
      </div>  
      `
    );
  });
};

insertRowAnswer(answers[0]);

// initAns();
