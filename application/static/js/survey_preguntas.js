'use strict';

/*
  Tareas 1: Colocar un id y elimar el padre del padre del padre.
*/

/*
 *LISTO: LECTURA DE DATOS Y VISUALIZACION.
 *LISTO: AL APRETAR BOTONES AGREGAR Y ELIMINAR SE MODIFICA EL ARREGLO.
 *LISTO: ELIMINAR Y AGREGAR ALTERNATIVAS.
 *LISTO: MANEJAR LOS INPUTS.

 *Por hacer
  *borrar el name de los botones.
  *Implementar un fade a las cards.
 */

console.log(data);

console.log(data.dataSurvey);

// if (data.dataSurvey.status !== 0) {
//   document.querySelector('#containerMayor').classList.add('disabledSupreme');
// }

function initTooltip() {
  const buttons = [...document.querySelectorAll("[data-toggle='tooltip']")];
  var tooltipList = buttons.map(element => {
    const toogle = new bootstrap.Tooltip(element);
    toogle._config.placement = 'bottom';
    return toogle;
  });
}

let poolId = {
  alternativa: [0],
  desarrollo: [0],
  opciones: [0],
};

data.dataSurvey.questions?.map(element => {
  element.type === 'alternativa' ? poolId.alternativa.push(element.id) : poolId.desarrollo.push(element.id);
  element.alternatives.map(idOption => {
    poolId.opciones.push(idOption.id);
  });
});

console.log(poolId.opciones);

const title = document.querySelector('#title');
const description = document.querySelector('#description');
const questionContainer = document.querySelector('.surveyQuestions');
// var myModal = new bootstrap.Modal(document.querySelector('.myModalId'), {
//   keyboard: false,
// });
const container = document.querySelector('.survey');
container.style.opacity = 1;
// console.log(myModal);

let num = data.dataSurvey.asigned;

const insertQuestion = function (statement, alternatives, type, id) {
  if (type === 'alternativa' && num == 0) {
    questionContainer.insertAdjacentHTML(
      'beforeend',
      `
      <div name="question" alternative="true" class="survey__card shadow pt-3 pb-3 mb-4 mt-4 mx-auto justify-content-center" id=${'alternativa' + id}>
        <textarea name="title" class="form-control shadow-none survey__elementTitle mb-3 textareaDisabled" rows="1"
          placeholder="Inserte enunciado" onchange="handleInputs(event)" maxlength="2000">${statement}</textarea>
        <div class="survey__alternatives">
          <div name=${id} class="list__alternatives ms-3">
            ${alternatives}
          </div>
          <div class="d-flex align-items-center">
            <button onclick="addAlternative(event)" type="button" class="suveryQuestions__button opacity-75" data-toggle="tooltip" title="Agregar alternativa"><img src="/static/resources/plus.png" class="img-fluid survey__image"></button>
            <span class="mb-1 opacity-75">Agregar alternativa</span>
          </div>
        </div>
        <div class="d-flex justify-content-end gap-2 mt-3 me-4">
          <button type="button" class="suveryQuestions__button" data-toggle="tooltip" title="Eliminar pregunta"><img name="alternativa"  id="imgDelet${id}" src="/static/resources/trash.png" class="img-fluid survey__image" onclick="deleteElement(event)"></button>
        </div>
    </div>
    `
    );
  } 
  else if (type === 'alternativa' && num != 0) {
    questionContainer.insertAdjacentHTML(
      'beforeend',
      `
      <div name="question" alternative="true" class="survey__card shadow pt-3 pb-3 mb-4 mt-4 mx-auto justify-content-center" id=${'alternativa' + id}>
        <textarea name="title" class="form-control shadow-none survey__elementTitle mb-3 textareaDisabled" rows="1"
          placeholder="Inserte enunciado" onchange="handleInputs(event)" maxlength="2000" disabled>${statement}</textarea>
        <div class="survey__alternatives">
          <div name=${id} class="list__alternatives ms-3">
            ${alternatives}
          </div>

        </div>

    </div>
    `
    );
  }
  else if (type === 'desarrollo') {
    questionContainer.insertAdjacentHTML(
      'beforeend',
      `
      <div name="question" alternative="false" class="survey__card shadow pt-3 pb-3 mb-4 mt-4 mx-auto justify-content-center" id=${'desarrollo' + id}>
        <textarea name="title" class="form-control shadow-none survey__elementTitle mb-3" rows="1"
          placeholder="Inserte enunciado" onchange="handleInputs(event)">${statement}</textarea>
        <div class="textReference">
          <textarea name="title"
            class="form-control shadow-none survey__elementDesc border-dotted textareaDisabled border__dotted" rows="3"
            placeholder="Cuadro de respuesta de referencia" disabled></textarea>
        </div>
        <div class="d-flex justify-content-end gap-2 mt-3 me-4">
          <button type="button" class="suveryQuestions__button" data-toggle="tooltip" title="Eliminar pregunta"><img name="desarrollo"  id="imgDelet${id}" src="/static/resources/trash.png" class="img-fluid survey__image" onclick="deleteElement(event)"></button>
        </div>
      </div>
    `
    );
  }
};

if (data.selected.toLowerCase() === 'preguntas' && Object.keys(data.dataSurvey).length !== 0) {
  //Se insertan los datos traidos en dataSurvey (Solo si viene con informacion)
  title.textContent = data.dataSurvey.title;
  description.textContent = data.dataSurvey.description;

  for (const element of data.dataSurvey.questions) {
    let alternativeHtml = '';
    //Si existen alternativas entra a este for, si no lo toma como respuesta .
    for (const alternative of element.alternatives) {
      
      if(num == 0){
      alternativeHtml += `
        <div id="opcion${alternative.id}" class="form-check d-flex align-items-center gap-2">
          <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
          <input placeholder="Inserte Texto" class="survey__inputAlt" value="${alternative.textAlt}" onchange="handleInputs(event)" maxlength="300">
          <button onclick="deleteAlternative(event)" type="button" class="suveryQuestions__button"><img src="/static/resources/remove.png" class="img-fluid survey__image"></button>
        </div>
     `;
      }

      else{
        alternativeHtml += `
        <div id="opcion${alternative.id}" class="form-check d-flex align-items-center gap-2 mt-4">
          <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
          <input placeholder="Inserte Texto" class="survey__inputAlt" value="${alternative.textAlt}" onchange="handleInputs(event)" maxlength="300" disabled>
          
        </div>
     `;
      }
    }
    insertQuestion(element.statement, alternativeHtml, element.type, element.id);
    // initTooltip();
  }
}

const moveScroll = function (id) {
  // console.log(id);
  function getOffset(el) {
    var _x = 0;
    var _y = 0;
    while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
      _x += el.offsetLeft - el.scrollLeft;
      _y += el.offsetTop - el.scrollTop;
      el = el.offsetParent;
    }
    return { top: _y, left: _x };
  }
  var x = getOffset(document.querySelector(`#alternativa${id}`)).left;
  var y = getOffset(document.querySelector(`#alternativa${id}`)).top;
  scroll(0, y);
};

// ADD AND DELETE INICIO--------------------------------------------------------

const addQuestion = function () {
  const idNew = newId('alternativa');
  const idOpcion1 = newId('opcion');
  poolId.opciones.push(idOpcion1);
  const idOpcion2 = newId('opcion');
  poolId.opciones.push(idOpcion2);
  // console.log(idNew);
  const textalt = `
    <div id="opcion${idOpcion1}" class="form-check d-flex align-items-center gap-2">
      <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
      <input class="survey__inputAlt" placeholder="Inserte Texto" onchange="handleInputs(event)" maxlength="300">
      <button type="button" class="suveryQuestions__button" data-toggle="tooltip" title="Eliminar alternativa"><img onclick="deleteAlternative(event)" src="/static/resources/remove.png" class="img-fluid survey__image"></button>
    </div>
    <div id="opcion${idOpcion2}" class="form-check d-flex align-items-center gap-2">
      <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
      <input class="survey__inputAlt" placeholder="Inserte Texto" onchange="handleInputs(event)" maxlength="300">
      <button type="button" class="suveryQuestions__button" data-toggle="tooltip" title="Eliminar alternativa"><img onclick="deleteAlternative(event)" src="/static/resources/remove.png" class="img-fluid survey__image"></button>
    </div>
`;
  insertQuestion('', textalt, 'alternativa', idNew);

  const questionAdd = {
    id: idNew,
    statement: '',
    type: 'alternativa',
    alternatives: [
      {
        id: idOpcion1,
        textAlt: '',
      },
      {
        id: idOpcion2,
        textAlt: '',
      },
    ],
  };
  data.dataSurvey.questions.push(questionAdd);
  poolId.alternativa.push(questionAdd.id);
  moveScroll(idNew);
  // console.log(data.dataSurvey.questions);
  // initTooltip();
  textAreaFunction();
};

const deleteElement = function (event) {
  const parent = event.target.parentNode.parentNode.parentNode;
  let idElement = 0;
  let typeElement = '';

  if (parent.getAttribute('alternative') === 'true') {
    idElement = parseInt(parent.getAttribute('id').slice(11));
    typeElement = 'alternativa';
  } else if (parent.getAttribute('alternative') === 'false') {
    idElement = parseInt(parent.getAttribute('id').slice(10));
    typeElement = 'desarrollo';
  }

  console.log(idElement + typeElement);

  console.log(parent);
  const arrayElement = data.dataSurvey.questions.filter(element => element.id !== idElement || element.type !== typeElement);

  data.dataSurvey.questions = arrayElement;
  console.log(data.dataSurvey.questions);
  parent.remove();
};

// ADD AND DELETE FIN--------------------------------------------------------

// CHANGE TYPE INICIO--------------------------------------------------------

const changeResponse = function (id, deleteText, addText, type, idOption1, idOption2) {
  let elementToDelete = document.querySelector(`#${type + id} > ${deleteText}`);
  let elementToAdd = document.querySelector(`#${type + id} > ${addText}`);
  console.log(elementToAdd);
  elementToDelete?.remove();
  if (deleteText === '.textReference') {
    elementToAdd.insertAdjacentHTML(
      'afterend',
      `
    <div class="survey__alternatives">
      <div name=${elementToAdd.parentNode.getAttribute('id').slice(8)} class="list__alternatives ms-3">
        <div id="${'opcion' + idOption1}" class="form-check d-flex align-items-center gap-2">
          <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
          <input class="survey__inputAlt" placeholder="Inserte Texto" onchange="handleInputs(event)" maxlength="300">
          <button type="button" class="suveryQuestions__button" data-toggle="tooltip" title="Eliminar alternativa"><img onclick="deleteAlternative(event)" src="/static/resources/remove.png" class="img-fluid survey__image"></button>
        </div>
        <div id="${'opcion' + idOption2}" class="form-check d-flex align-items-center gap-2">
          <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
          <input class="survey__inputAlt" placeholder="Inserte Texto" onchange="handleInputs(event)" maxlength="300">
          <button type="button" class="suveryQuestions__button" data-toggle="tooltip" title="Eliminar alternativa"><img onclick="deleteAlternative(event)" src="/static/resources/remove.png" class="img-fluid survey__image"></button>
        </div>
      </div>
      <div class="d-flex align-items-center">
        <button onclick="addAlternative(event)" type="button" class="suveryQuestions__button opacity-75"><img src="/static/resources/plus.png" class="img-fluid survey__image"></button>
        <span class="mb-1 opacity-75">Agregar alternativa</span>
      </div>
    </div>
    `
    );
    textAreaFunction();
  } else {
    elementToAdd.insertAdjacentHTML(
      'afterend',
      `
      <div class="textReference">
        <textarea name="title"
          class="form-control shadow-none survey__elementDesc border-dotted textareaDisabled border__dotted" rows="3"
          placeholder="Cuadro de respuesta de referencia" disabled></textarea>
      </div>
    `
    );
  }
};

function newId(type) {
  return type === 'alternativa' ? Math.max(...poolId.alternativa) + 1 : Math.max(...poolId.opciones) + 1;
}

const setToAlternative = function (event) {
  let parent = event.target.parentNode.parentNode.parentNode;
  const idParent = parent?.getAttribute('id').slice(10);

  if (parent.getAttribute('alternative') === 'false') {
    const [question] = data.dataSurvey.questions.filter(question => question.id === parseInt(idParent) && question.type === 'desarrollo');

    const idNew = newId('alternativa');
    poolId.alternativa.push(idNew);
    question.type = 'alternativa';

    const idOpcion1 = newId('opcion');
    poolId.opciones.push(idOpcion1);
    const idOpcion2 = newId('opcion');
    poolId.opciones.push(idOpcion2);

    question.alternatives.push(
      {
        id: idOpcion1,
        textAlt: '',
      },
      {
        id: idOpcion2,
        textAlt: '',
      }
    );
    question.id = idNew;

    parent.setAttribute('alternative', 'true');
    changeResponse(idParent, '.textReference', '.survey__elementTitle', 'desarrollo', 1, 2);
    parent.setAttribute('id', `alternativa${idNew}`);
    console.log(parent);
    // console.log(data.dataSurvey.questions);
  }
};

const setToParagraph = function (event) {
  let parent = event.target.parentNode.parentNode.parentNode;
  const idParent = parent?.getAttribute('id').slice(11);
  console.log(idParent);

  if (parent.getAttribute('alternative') === 'true') {
    const [question] = data.dataSurvey.questions.filter(question => question.id === parseInt(idParent) && question.type === 'alternativa');

    const idNew = newId('desarrollo');
    poolId.desarrollo.push(idNew);
    question.type = 'desarrollo';
    question.alternatives = [];
    question.id = idNew;
    parent.setAttribute('alternative', 'false');
    changeResponse(idParent, '.survey__alternatives', '.survey__elementTitle', 'alternativa');
    parent.setAttribute('id', `desarrollo${idNew}`);
    console.log(data.dataSurvey.questions);
  }
};

// CHANGE TYPE FIN--------------------------------------------------------

// ADD AND DELETE ALTERNATIVES INICIO--------------------------------------------------------

const deleteAlternative = function (event) {
  let element = event.target.parentNode.parentNode;
  let parent = event.target.parentNode.parentNode.parentNode;
  let idOpcion = element.getAttribute('id').slice(6);
  let idParent = parent.parentNode.parentNode.getAttribute('id').slice(11);

  if (parent.childElementCount > 2) {
    const [result] = data.dataSurvey.questions.filter(question => question.id === parseInt(idParent) && question.type === 'alternativa');
    const [option] = result.alternatives.filter(val => val.id === parseInt(idOpcion));
    const index = result.alternatives.indexOf(option);
    console.log(index);
    result.alternatives.splice(index, 1);
    console.log(result);
    element.remove();
  }
};

const addAlternative = function (event) {
  let element = event.target.parentNode.parentNode.parentNode.firstElementChild;
  let parent = event.target.parentNode.parentNode.parentNode.parentNode;
  const idParent = parent.getAttribute('id').slice(11);

  const [result] = data.dataSurvey.questions.filter(question => question.id === parseInt(idParent) && question.type === 'alternativa');
  const idOption = Math.max(...result.alternatives.map(val => val.id)) + 1;

  const idOpcion1 = newId('opcion');
  poolId.opciones.push(idOpcion1);

  result.alternatives.push({
    id: idOpcion1,
    textAlt: '',
  });
  console.log(result);
  console.log(element);
  element.insertAdjacentHTML(
    'beforeend',
    `
    <div id="opcion${idOpcion1}" class="form-check d-flex align-items-center gap-2">
          <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
          <input class="survey__inputAlt" placeholder="Inserte Texto" onchange="handleInputs(event)" maxlength="300">
          <button type="button" class="suveryQuestions__button" data-toggle="tooltip" title="Eliminar alternativa"><img onclick="deleteAlternative(event)" src="/static/resources/remove.png" class="img-fluid survey__image"></button>
    </div>
  `
  );
};

// ADD AND DELETE ALTERNATIVES FIN--------------------------------------------------------

// HANDLE INPUTS INICIO--------------------------------------------------------

const handleInputs = function (event) {
  const target = event.target;
  const parent = target.parentNode;
  if (target.id === 'title') data.dataSurvey.title = target.value;
  else if (target.id === 'description') data.dataSurvey.description = target.value;
  else if (parent.getAttribute('name') === 'question') {
    let idQuestion = 0;
    let type = '';
    if (parent.getAttribute('alternative') === 'true') {
      idQuestion = parseInt(parent.getAttribute('id').slice(11));
      type = 'alternativa';
    } else if (parent.getAttribute('alternative') === 'false') {
      idQuestion = parseInt(parent.getAttribute('id').slice(10));
      type = 'desarrollo';
    }
    const [result] = data.dataSurvey.questions.filter(question => question.id === idQuestion && question.type === type);
    result.statement = target.value;
    console.log(result);
  } else {
    const parentOption = target.parentNode.parentNode.parentNode.parentNode;
    const idOption = parseInt(target.parentNode.getAttribute('id').slice(6));
    const idParent = parseInt(parentOption.getAttribute('id').slice(11));

    const [result] = data.dataSurvey.questions.filter(question => question.id === idParent && question.type === 'alternativa');

    const [resultOption] = result.alternatives.filter(option => option.id === idOption);

    resultOption.textAlt = target.value;
  }
  console.log(data.dataSurvey);
};

// HANDLE INPUTS FIN--------------------------------------------------------

const sendData = function () {
  // myModal.show();

  if (data.textButton === 'Guardar') {
    Swal.fire({
      title: 'Guardando encuesta',
      icon: 'info',
      showCloseButton: false,
      showCancelButton: false,
      didOpen: () => {
        Swal.showLoading();
        return fetch(`/create_survey`, {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
          },
          body: JSON.stringify(data.dataSurvey),
        })
          .then(responseServer => {
            if (!responseServer.ok) {
              throw responseServer.statusText;
            }
            return responseServer.json();
          })
          .then(data => {
            console.log(data);
            if (data !== 'Encuesta Guardada') {
              throw data;
            } else {
              Swal.fire('Excelente!', 'Encuesta guardada con exito.', 'success');
            }
          })
          .catch(error => {
            Swal.fire('Error!', 'Error inesperado: ' + error, 'error');
          });
      },
    });
  } else if (data.textButton === 'Modificar') {
    Swal.fire({
      title: 'Modificando encuesta',
      icon: 'info',
      showCloseButton: false,
      showCancelButton: false,
      didOpen: () => {
        Swal.showLoading();
        return fetch(`/modify_survey`, {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
          },
          body: JSON.stringify(data.dataSurvey),
        })
          .then(responseServer => {
            if (!responseServer.ok) {
              throw responseServer.statusText;
            }
            return responseServer.json();
          })
          .then(data => {
            console.log(data);
            if (data !== 'Modificacion Exitosa') {
              throw data;
            } else {
              Swal.fire('Excelente!', 'Encuesta modificada con exito.', 'success');
            }
          })
          .catch(error => {
            Swal.fire('Error!', 'Error inesperado: ' + error, 'error');
          });
      },
    });
  }

  async function delay() {
    await new Promise(done => setTimeout(() => done(), 3000));
    window.location.href = '/dashboard_admin';
    // myModal.hide();
  }
};

// Effects and others.

const textAreaFunction = function () {
  const tx = document.querySelectorAll('textarea');
  for (let i = 0; i < tx.length; i++) {
    tx[i].setAttribute('style', 'height:' + tx[i].scrollHeight + 'px;overflow-y:hidden;');
    tx[i].addEventListener('input', OnInput, false);
  }

  function OnInput() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
  }
};

textAreaFunction();

// Contador de caracteres.

const characters = document.querySelector('.charactersRemaining');
const descriptionSurvey = document.querySelector('#description');
characters.textContent = 3000 - descriptionSurvey.value.length;

console.log(descriptionSurvey.value.length);

const couterCharacters = function (event) {
  characters.textContent = 3000 - descriptionSurvey.value.length;
};
