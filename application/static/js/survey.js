'use strict'

let title = document.querySelector("#title")
let description = document.querySelector("#description")
let questionContainer = document.querySelector(".surveyQuestions")

title.textContent = data.dataSurvey.title
description.textContent = data.dataSurvey.description


const insertQuestion = function (statement, alternatives, type) {

  if (type === "alternativa") {
    questionContainer.insertAdjacentHTML('beforeend',
      `
      <div class="survey__card shadow pt-3 pb-3 mb-4 mt-4 mx-auto justify-content-center">
        <textarea name="title" class="form-control shadow-none survey__elementTitle mb-3 textareaDisabled" rows="1"
          placeholder="Inserte enunciado">${statement}</textarea>
        <div class="survey__alternatives">
          <div class="list__alternatives ms-3">
            ${alternatives}
          </div>
          <div class="d-flex align-items-center">
            <button type="button" class="suveryQuestions__button opacity-75"><img src="/static/resources/plus.png" class="img-fluid survey__image" onclick="#"></button>
            <span class="mb-1 opacity-75">Agregar alternativa</span>
          </div>
        </div>
        <div class="d-flex justify-content-end gap-2 mt-3 me-4">
          <button type="button" class="suveryQuestions__button"><img src="/static/resources/justificar-parrafo.png" class="img-fluid survey__image" onclick="#"></button>
          <button type="button" class="suveryQuestions__button"><img src="/static/resources/radio.png" class="img-fluid survey__image" onclick="#"></button>
          <button type="button" class="suveryQuestions__button"><img src="/static/resources/trash.png" class="img-fluid survey__image" onclick="#"></button>
        </div>
      </div>
      `
    );

  } else if (type === "desarrollo") {
    questionContainer.insertAdjacentHTML('beforeend',
      `
      <div class="survey__card shadow pt-3 pb-3 mb-4 mt-4 mx-auto justify-content-center">
        <textarea name="title" class="form-control shadow-none survey__elementTitle mb-3 textareaDisabled" rows="1"
          placeholder="Inserte enunciado">${statement}</textarea>
        <textarea name="title"
          class="form-control shadow-none survey__elementDesc border-dotted textareaDisabled border__dotted" rows="3"
          placeholder="Cuadro de respuesta de referencia" disabled></textarea>
      <div class="d-flex justify-content-end gap-2 mt-3 me-4">
        <button type="button" class="suveryQuestions__button"><img src="/static/resources/justificar-parrafo.png" class="img-fluid survey__image" onclick="#"></button>
        <button type="button" class="suveryQuestions__button"><img src="/static/resources/radio.png" class="img-fluid survey__image" onclick="#"></button>
        <button type="button" class="suveryQuestions__button"><img src="/static/resources/trash.png" class="img-fluid survey__image" onclick="#"></button>
      </div>
      `)
    }
}

for (const element of data.dataSurvey.questions) {

  let alternativesSpread = ""
  for (const textAlternative of element.alternatives){
    alternativesSpread += `
    <div class="form-check d-flex align-items-center gap-2">
      <input class="form-check-input survey_alternative" type="radio" name="flexRadioDefault" id="flexRadioDefault1" disabled>
      <input class="survey__inputAlt" value=${textAlternative}>
      <button type="button" class="suveryQuestions__button"><img src="/static/resources/remove.png" class="img-fluid survey__image" onclick="#"></button>
    </div>
  `
  }
  insertQuestion(element.statement ,alternativesSpread, element.type)
}


const dataSurvey = {
  id: undefined,
  title: "",
  description: "",
  questions: [
    {
      statement: "",
      type: "",
      alternatives: []
    }
  ]
}

const handleInputs = function (event) {
  console.log(event)
  const target = event.target
  console.log(target.value)
}


