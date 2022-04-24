"use strict";

/*
  Tareas 1: Colocar un id y elimar el padre del padre del padre.
*/

console.log(data.selected.toLowerCase());

const title = document.querySelector("#title");
const description = document.querySelector("#description");
const questionContainer = document.querySelector(".surveyQuestions");
let numberQuestions = data.dataSurvey.questions?.length ?? 1;

const insertQuestion = function (statement, alternatives, type, id) {
  if (type === "alternativa") {
    questionContainer.insertAdjacentHTML(
      "beforeend",
      `
    <div alternative="true" class="survey__card shadow pt-3 pb-3 mb-4 mt-4 mx-auto justify-content-center" id=${
      "question" + id
    }>
      <textarea name="title" class="form-control shadow-none survey__elementTitle mb-3 textareaDisabled" rows="1"
        placeholder="Inserte enunciado">${statement}</textarea>
      <div class="survey__alternatives">
        <div class="list__alternatives ms-3">
          ${alternatives}
        </div>
        <div class="d-flex align-items-center">
          <button onclick="addAlternative(event)" type="button" class="suveryQuestions__button opacity-75"><img src="/static/resources/plus.png" class="img-fluid survey__image"></button>
          <span class="mb-1 opacity-75">Agregar alternativa</span>
        </div>
      </div>
      <div class="d-flex justify-content-end gap-2 mt-3 me-4">
        <button onclick="setToParagraph(event)" type="button" class="suveryQuestions__button"><img src="/static/resources/justificar-parrafo.png" class="img-fluid survey__image"></button>
        <button onclick="setToAlternative(event)" type="button" class="suveryQuestions__button"><img src="/static/resources/radio.png" class="img-fluid survey__image"></button>
        <button onclick="deleteElement(event)" type="button" class="suveryQuestions__button"><img src="/static/resources/trash.png" class="img-fluid survey__image"></button>
      </div>
    </div>
    `
    );
  } else if (type === "desarrollo") {
    questionContainer.insertAdjacentHTML(
      "beforeend",
      `
      <div alternative="false" class="survey__card shadow pt-3 pb-3 mb-4 mt-4 mx-auto justify-content-center" id=${
        "question" + id
      }>
        <textarea name="title" class="form-control shadow-none survey__elementTitle mb-3" rows="1"
          placeholder="Inserte enunciado">${statement}</textarea>
        <div class="textReference">
          <textarea name="title"
            class="form-control shadow-none survey__elementDesc border-dotted textareaDisabled border__dotted" rows="3"
            placeholder="Cuadro de respuesta de referencia" disabled></textarea>
        </div>
        <div class="d-flex justify-content-end gap-2 mt-3 me-4">
          <button onclick="setToParagraph(event)" type="button" class="suveryQuestions__button"><img src="/static/resources/justificar-parrafo.png" class="img-fluid survey__image"></button>
          <button onclick="setToAlternative(event)" type="button" class="suveryQuestions__button"><img src="/static/resources/radio.png" class="img-fluid survey__image"></button>
          <button onclick="deleteElement(event)" type="button" class="suveryQuestions__button"><img src="/static/resources/trash.png" class="img-fluid survey__image"></button>
        </div>
      </div>
    `
    );
  }
};

if (data.selected.toLowerCase() === "preguntas") {
  title.textContent = data.dataSurvey.title;
  description.textContent = data.dataSurvey.description;

  if (Object.keys(data.dataSurvey).length !== 0) {
    for (const element of data.dataSurvey.questions) {
      let alternativesSpread = "";
      for (const textAlternative of element.alternatives) {
        alternativesSpread += `
    <div class="form-check d-flex align-items-center gap-2">
      <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
      <input class="survey__inputAlt" value=${textAlternative}>
      <button onclick="deleteAlternative(event)" type="button" class="suveryQuestions__button"><img src="/static/resources/remove.png" class="img-fluid survey__image"></button>
    </div>
  `;
      }
      insertQuestion(
        element.statement,
        alternativesSpread,
        element.type,
        element.id
      );
    }
  }
}

const addQuestion = function (event) {
  let questionContainer = document.querySelector(".surveyQuestions");
  insertQuestion("", "", "desarrollo", numberQuestions);
  moveScroll();
  numberQuestions++;
};

const moveScroll = function () {
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
  var x = getOffset(document.querySelector(`#question${numberQuestions}`)).left;
  var y = getOffset(document.querySelector(`#question${numberQuestions}`)).top;
  scroll(0, y);
};

const handleInputs = function (event) {
  const target = event.target;
};

const deleteElement = function (event) {
  event.target.parentNode.parentNode.parentNode.remove();
};

const changeResponse = function (id, deleteText, addText) {
  let elementToDelete = document.querySelector(`#${id} > ${deleteText}`);
  let elementToAdd = document.querySelector(`#${id} > ${addText}`);
  elementToDelete?.remove();
  if (deleteText === ".textReference") {
    elementToAdd.insertAdjacentHTML(
      "afterend",
      `
    <div class="survey__alternatives">
      <div class="list__alternatives ms-3">
        <div class="form-check d-flex align-items-center gap-2">
          <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
          <input class="survey__inputAlt" placeholder="Opcion1">
          <button type="button" class="suveryQuestions__button"><img onclick="deleteAlternative(event)" src="/static/resources/remove.png" class="img-fluid survey__image"></button>
        </div>
      </div>
      <div class="d-flex align-items-center">
        <button onclick="addAlternative(event)" type="button" class="suveryQuestions__button opacity-75"><img src="/static/resources/plus.png" class="img-fluid survey__image"></button>
        <span class="mb-1 opacity-75">Agregar alternativa</span>
      </div>
    </div>
    `
    );
  } else {
    elementToAdd.insertAdjacentHTML(
      "afterend",
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

const setToAlternative = function (event) {
  let element = event.target.parentNode.parentNode.parentNode;
  if (element.getAttribute("alternative") === "false") {
    element.setAttribute("alternative", "true");
    changeResponse(element.id, ".textReference", ".survey__elementTitle");
  }
};

const setToParagraph = function (event) {
  let element = event.target.parentNode.parentNode.parentNode;
  if (element.getAttribute("alternative") === "true") {
    element.setAttribute("alternative", "false");
    changeResponse(
      element.id,
      ".survey__alternatives",
      ".survey__elementTitle"
    );
  }
};

const deleteAlternative = function (event) {
  let element = event.target.parentNode.parentNode;
  let parent = event.target.parentNode.parentNode.parentNode;
  if (parent.childElementCount > 1) element.remove();
};

const addAlternative = function (event) {
  let element = event.target.parentNode.parentNode.parentNode.firstElementChild;
  element.insertAdjacentHTML(
    "beforeend",
    `
    <div class="form-check d-flex align-items-center gap-2">
          <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
          <input class="survey__inputAlt" placeholder="Opcion${
            element.childElementCount + 1
          }">
          <button type="button" class="suveryQuestions__button"><img onclick="deleteAlternative(event)" src="/static/resources/remove.png" class="img-fluid survey__image"></button>
    </div>
  `
  );
};
