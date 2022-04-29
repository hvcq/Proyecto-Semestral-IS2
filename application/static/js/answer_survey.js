"use strict";

/*
  Hacer lo del opacity
  git commit --amend --no-edit NO TANTOS COMMITS.
*/

let numberCuestion = 0;
let totalQuestions = dataSurvey.questions.length;
let responses = {
  id: dataSurvey.id,
  usuario: {
    name: "anonimo",
    correo: "example@udec.cl",
  },
  respuestas: [],
};

const title = document.querySelector(".titleSurvey");
const leftRow = document.querySelector(".leftRow");
const rightRow = document.querySelector(".rightRow");
const questionContainer = document.querySelector(".accordion");
title.classList.remove("invisible");

//Primera iteración

const init = function () {
  rightRow.classList.remove("invisible");
  responses.respuestas = dataSurvey.questions.map((element) => {
    return {
      idPregunta: element.id,
      type: element.type,
      response:
        element.type === "desarrollo" ? "" : { idOpcion: "", textAlt: "" },
    };
  });
  insertQuestion(0);
  document.querySelector(".question").style.opacity = 1;
};

const insertQuestion = function (pos) {
  const id = dataSurvey.questions[pos].id;
  const type = dataSurvey.questions[pos].type;
  const statement = dataSurvey.questions[pos].statement;
  let alternativeHtml = "";
  const [respuesta] = responses.respuestas.filter(
    (element) => element.idPregunta === id && element.type === type
  );

  console.log(respuesta);

  if (type === "desarrollo") {
    questionContainer.insertAdjacentHTML(
      "afterend",
      `
        <div id="${
          "desarrollo" + id
        }" class="question__card d-flex flex-column ps-4 pe-4 pt-3 pb-3 shadow question">
            <div class="d-flex justify-content-between">
                <div class="d-flex align-items-center gap-2">
                    <p class="question__number question__number--rounded">${
                      numberCuestion + 1
                    }</p>
                    <p class="question__number">${type}</p>
                </div>
                <p class="question__number">${
                  numberCuestion + 1
                }/${totalQuestions}</p>
            </div>
            <h1>${statement}</h1>
            <textarea tipo="desarrollo" id="${id}"name="title" class="form-control shadow-none p-0" rows="5"
            placeholder="Ingresa tu respuesta aquí" onchange="handleInput(event)">${
              respuesta.response
            }</textarea>
        </div>
    `
    );
  } else if (type === "alternativa") {
    for (const alternative of dataSurvey.questions[pos].alternatives) {
      const check =
        respuesta.response.idOpcion === alternative.id ? "checked" : "";
      alternativeHtml += `
      <div id="${id}" class="form-check d-flex align-items-center gap-3 p-0">
        <input tipo="alternativa" onclick="handleInput(event)" id="${alternative.id}" class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault2" ${check}>
        <h5 class="textOption">${alternative.textAlt}</h5>
      </div>
     `;
    }

    questionContainer.insertAdjacentHTML(
      "afterend",
      `
        <div id="${
          "alternativa" + id
        }" class="question__card d-flex flex-column ps-4 pe-4 pt-3 pb-3 shadow question">
            <div class="d-flex justify-content-between">
                <div class="d-flex align-items-center gap-2">
                    <p class="question__number question__number--rounded">${
                      numberCuestion + 1
                    }</p>
                    <p class="question__number">${type}</p>
                </div>
                <p class="question__number">${
                  numberCuestion + 1
                }/${totalQuestions}</p>
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
  const type = event.target.getAttribute("tipo");
  const id =
    type === "alternativa"
      ? parseInt(event.target.parentNode.getAttribute("id"))
      : parseInt(event.target.getAttribute("id"));

  const [question] = responses.respuestas.filter(
    (element) => element.idPregunta === id && element.type === type
  );

  if (type === "desarrollo") {
    question.response = event.target.value;
  } else {
    question.response.idOpcion = parseInt(event.target.id);
    question.response.textAlt =
      event.target.nextSibling.nextSibling.textContent;
  }

  console.log(question);
};

const changeCuestion = function (event, type) {
  //Arreglar el presionar rapido
  type === "next" ? ++numberCuestion : --numberCuestion;

  if (numberCuestion === totalQuestions - 1) {
    document.querySelector(".sendResponse").classList.remove("invisible");
  } else {
    document.querySelector(".sendResponse").classList.add("invisible");
  }

  numberCuestion === 0
    ? leftRow.classList.add("invisible")
    : leftRow.classList.remove("invisible");
  numberCuestion === totalQuestions - 1
    ? rightRow.classList.add("invisible")
    : rightRow.classList.remove("invisible");

  change();

  const elements = document.querySelectorAll(".question");
  elements[1]?.remove();

  function change() {
    if (numberCuestion >= 0) insertQuestion(numberCuestion);
  }
  document.querySelector(".question").style.opacity = 1;
};

init();

// const responses = {
//   idEncuesta: "idEcuesta",
//   usuario: {
//     name: "nombre",
//     correo: "example@udec.cl",
//   },
//   respuestas: [
//     {
//       idPregunta: "idPregunta",
//       type: "desarrollo",
//       response: "mi respuesta",
//     },
//     {
//       idPregunta: "idPregunta",
//       type: "alternativa",
//       response: {
//         idOpcion: "idOpcion",
//         textAlt: "color azul",
//       },
//     },
//   ],
// };
