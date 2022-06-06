'use strict';

/*
  Hacer lo del opacity
  git commit --amend --no-edit NO TANTOS COMMITS.
*/

let dataSurvey = data.dataSurvey;

$.ajax({
  url: '/aumentar_visita',
  type: 'POST',
  data: { id_survey: dataSurvey.id },
  success: function (result) {
    delay();
  },
});

let numberCuestion = 0;
let totalQuestions = dataSurvey.questions.length;
let responses = {
  id: dataSurvey.id,
  correo: data.encuestado,
  respuestas: [],
};

const title = document.querySelector('.titleSurvey');
const leftRow = document.querySelector('.leftRow');
const rightRow = document.querySelector('.rightRow');
const questionContainer = document.querySelector('.accordion');
var myModal = new bootstrap.Modal(document.querySelector('.myModalId'), {
  keyboard: false,
});

// console.log(myModal);
title.classList.remove('invisible');

//Primera iteración

const init = function () {
  if (totalQuestions === 1) document.querySelector('.sendResponse').classList.remove('invisible');
  rightRow.classList.remove('invisible');
  responses.respuestas = dataSurvey.questions.map(element => {
    return {
      idPregunta: element.id,
      type: element.type,
      response: element.type === 'desarrollo' ? '' : { idOpcion: '', textAlt: '' },
    };
  });
  insertQuestion(0);
  document.querySelector('.survey').style.opacity = 1;
  document.querySelector('.question').style.opacity = 1;
};

const insertQuestion = function (pos) {
  const id = dataSurvey.questions[pos].id;
  const type = dataSurvey.questions[pos].type;
  const statement = dataSurvey.questions[pos].statement;
  let alternativeHtml = '';
  const [respuesta] = responses.respuestas.filter(element => element.idPregunta === id && element.type === type);

  console.log(id + type + statement);

  if (type === 'desarrollo') {
    questionContainer.insertAdjacentHTML(
      'afterend',
      `
        <div id="${'desarrollo' + id}" class="question__card d-flex flex-column ps-4 pe-4 pt-3 pb-3 shadow question">
            <div class="d-flex justify-content-between">
                <div class="d-flex align-items-center gap-2">
                    <p class="question__number question__number--rounded">${numberCuestion + 1}</p>
                    <p class="question__number">${type}</p>
                </div>
                <p class="question__number">${numberCuestion + 1}/${totalQuestions}</p>
            </div>
            <h1>${statement}</h1>
            <textarea tipo="desarrollo" id="${id}"name="title" class="form-control shadow-none p-0" rows="5"
            placeholder="Ingresa tu respuesta aquí" onchange="handleInput(event)">${respuesta.response}</textarea>
        </div>
    `
    );
  } else if (type === 'alternativa') {
    for (const alternative of dataSurvey.questions[pos].alternatives) {
      const check = respuesta.response.idOpcion === alternative.id ? 'checked' : '';
      alternativeHtml += `
      <div id="${id}" class="form-check d-flex align-items-center gap-3 p-0">
        <input tipo="alternativa" onclick="handleInput(event)" id="${alternative.id}" class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault2" ${check}>
        <h5 class="textOption">${alternative.textAlt}</h5>
      </div>
     `;
    }

    questionContainer.insertAdjacentHTML(
      'afterend',
      `
        <div id="${'alternativa' + id}" class="question__card d-flex flex-column ps-4 pe-4 pt-3 pb-3 shadow question">
            <div class="d-flex justify-content-between">
                <div class="d-flex align-items-center gap-2">
                    <p class="question__number question__number--rounded">${numberCuestion + 1}</p>
                    <p class="question__number">${type}</p>
                </div>
                <p class="question__number">${numberCuestion + 1}/${totalQuestions}</p>
            </div>
            <h1>${statement}</h1>
            <div class="survey__alternatives d-flex flex-column gap-2 pb-5">
              ${alternativeHtml}
            </div>
        </div>
    `
    );
  }
};

const handleInput = function (event) {
  const type = event.target.getAttribute('tipo');
  const id = type === 'alternativa' ? parseInt(event.target.parentNode.getAttribute('id')) : parseInt(event.target.getAttribute('id'));

  const [question] = responses.respuestas.filter(element => element.idPregunta === id && element.type === type);

  if (type === 'desarrollo') {
    question.response = event.target.value;
  } else {
    question.response.idOpcion = parseInt(event.target.id);
    question.response.textAlt = event.target.nextSibling.nextSibling.textContent;
  }

  console.log(question);
};

const changeCuestion = function (event, type) {
  //Arreglar el presionar rapido
  if (totalQuestions === 1) return;
  type === 'next' ? ++numberCuestion : --numberCuestion;

  if (numberCuestion === totalQuestions - 1) {
    document.querySelector('.sendResponse').style.opacity = 1;
  } else {
    document.querySelector('.sendResponse').style.opacity = 0;
  }

  numberCuestion === 0 ? leftRow.classList.add('invisible') : leftRow.classList.remove('invisible');
  numberCuestion === totalQuestions - 1 ? rightRow.classList.add('invisible') : rightRow.classList.remove('invisible');

  change();

  const elements = document.querySelectorAll('.question');
  elements[1]?.remove();
  delay();

  function change() {
    if (numberCuestion >= 0) {
      document.querySelector('.question').style.opacity = 0;
      insertQuestion(numberCuestion);
    }
  }

  async function delay() {
    await new Promise(done => setTimeout(() => done(), 5));
    document.querySelector('.question').style.opacity = 1;
  }
};

init();

const sendData = function (event) {
  const [estado] = responses.respuestas.map(element => {
    if (element.type === 'alternativa') {
      if (element.response.idOpcion === '') return element;
    } else if (element.type === 'desarrollo') {
      if (element.response === '') return element;
    }
  });

  console.log(estado);
  if (estado === undefined) {
    if (data.type === 'registrado') {
      console.log('ejecutado');
      document.querySelector('#registerLink').classList.add('invisible');
    }
    myModal.show();
    $.ajax({
      url: '/responder_encuesta',
      type: 'POST',
      data: { responses: JSON.stringify(responses) },
      success: function (result) {
        delay();
      },
    });

    // async function delay() {
    //   await new Promise(done => setTimeout(() => done(), 3000));
    //   window.location.href = '/';
    //   myModal.hide();
    // }
  } else {
    alert('TIENES QUE RESPONDER TODAS LAS PREGUNTAS');
  }
};
