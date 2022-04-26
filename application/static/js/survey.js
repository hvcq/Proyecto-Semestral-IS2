"use strict";

/*
  Tareas 1: Colocar un id y elimar el padre del padre del padre.
*/

const title = document.querySelector("#title");
const description = document.querySelector("#description");
const questionContainer = document.querySelector(".surveyQuestions");
let numberQuestions = data.dataSurvey.questions?.length + 1 ?? 1;

const insertQuestion = function (statement, alternatives, type, id) {
  if (type === "alternativa") {
    questionContainer.insertAdjacentHTML(
      "beforeend",
      `
    <div name="question" alternative="true" class="survey__card shadow pt-3 pb-3 mb-4 mt-4 mx-auto justify-content-center" id=${
      "question" + id
    }>
      <textarea name="title" class="form-control shadow-none survey__elementTitle mb-3 textareaDisabled" rows="1"
        placeholder="Inserte enunciado" onchange="handleInputs(event)">${statement}</textarea>
      <div class="survey__alternatives">
        <div name=${id} class="list__alternatives ms-3">
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
      <div name="question" alternative="false" class="survey__card shadow pt-3 pb-3 mb-4 mt-4 mx-auto justify-content-center" id=${
        "question" + id
      }>
        <textarea name="title" class="form-control shadow-none survey__elementTitle mb-3" rows="1"
          placeholder="Inserte enunciado" onchange="handleInputs(event)">${statement}</textarea>
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
      <input class="survey__inputAlt" value=${textAlternative} onchange="handleInputs(event)">
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
  const questionExtra = {
    id: `${numberQuestions}`,
    statement: "",
    type: "desarrollo",
    alternatives: [],
  };
  data.dataSurvey.questions.push(questionExtra);
  moveScroll();
  console.log(data.dataSurvey);
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
  if (target.id === "title") data.dataSurvey.title = target.value;
  else if (target.id === "description")
    data.dataSurvey.description = target.value;
  else if (target.parentNode.getAttribute("name") === "question") {
    const idQuestion = target.parentNode.id.slice(8);
    const result = data.dataSurvey.questions.filter(
      (question) => question.id === idQuestion
    );
    if (result.length === 1) {
      result[0].statement = target.value;
    }
  } else {
    console.log(target.parentNode.parentNode);
    const position = parseInt(target.getAttribute("placeholder").slice(6));
    const idQuestion = target.parentNode.parentNode.getAttribute("name");
    const result = data.dataSurvey.questions.filter(
      (question) => question.id === idQuestion
    );
    if (result.length === 1) {
      console.log(result[0].alternatives);
      result[0].alternatives[position - 1] = target.value;
    }
  }
  // $.ajax({
  //   url: "/crear_nueva_encuesta",
  //   type: "POST",
  //   data: { ola: JSON.stringify(data.dataSurvey) },
  // });
  // console.log(data.dataSurvey);
  // console.log(target);
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
      <div name=${elementToAdd.parentNode
        .getAttribute("id")
        .slice(8)} class="list__alternatives ms-3">
        <div class="form-check d-flex align-items-center gap-2">
          <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
          <input class="survey__inputAlt" placeholder="Opcion1" onchange="handleInputs(event)">
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
    const elementId = element.id.slice(8);
    const question = data.dataSurvey.questions.filter(
      (question) => question.id === elementId
    );
    question[0].type = "alternativa";
    +question[0].alternatives.push("Opcion1");
    element.setAttribute("alternative", "true");
    changeResponse(element.id, ".textReference", ".survey__elementTitle");
  }
};

const setToParagraph = function (event) {
  let element = event.target.parentNode.parentNode.parentNode;
  if (element.getAttribute("alternative") === "true") {
    const elementId = element.id.slice(8);
    const question = data.dataSurvey.questions.filter(
      (question) => question.id === elementId
    );
    question[0].type = "desarrollo";
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
  let sibling = event.target.parentNode.previousElementSibling;
  if (parent.childElementCount > 1) {
    const position = parseInt(sibling.getAttribute("placeholder").slice(6));
    const idQuestion = parent.parentNode.parentNode.getAttribute("id").slice(8);
    const result = data.dataSurvey.questions.filter(
      (question) => question.id === idQuestion
    );
    const positionToDelete = result[0].alternatives.indexOf(
      sibling.getAttribute("placeholder")
    );

    result[0].alternatives.splice(positionToDelete, 1);
    console.log(result[0]);
    element.remove();
  }
};

const addAlternative = function (event) {
  let element = event.target.parentNode.parentNode.parentNode.firstElementChild;
  let parent = event.target.parentNode.parentNode.parentNode.parentNode;
  const idParent = parent.getAttribute("id").slice(8);
  const result = data.dataSurvey.questions.filter(
    (question) => question.id === idParent
  );
  result[0].alternatives.push(`Opcion${element.childElementCount + 1}`);
  console.log(result[0]);
  element.insertAdjacentHTML(
    "beforeend",
    `
    <div class="form-check d-flex align-items-center gap-2">
          <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
          <input class="survey__inputAlt" placeholder="Opcion${
            element.childElementCount + 1
          }" onchange="handleInputs(event)">
          <button type="button" class="suveryQuestions__button"><img onclick="deleteAlternative(event)" src="/static/resources/remove.png" class="img-fluid survey__image"></button>
    </div>
  `
  );
};
