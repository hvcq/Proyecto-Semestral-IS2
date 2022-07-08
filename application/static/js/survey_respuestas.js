'use strict';


document.querySelector('#carouselExampleDark').style.opacity = 1;

let isFirst = false;

const colors = [
  '#cd6155',
  '#af7ac5',
  '#5499c7',
  '#48c9b0',
  '#52be80',
  '#f4d03f',
  '#eb984e',
  '#566573',
  '#a04000',
  '#a569bd',
  '#5dade2',
  '#45b39d',
  '#58d68d',
  '#f5b041',
  '#dc7633',
];

const containerQuestions = document.querySelector('.carousel-inner');
let arrayCharts = [];

const insertQuestions = function (question) {
  let text = '';

  for (const option of question.opciones) {
    text += `
    <div class="row align-items-center gap-2">
      <input class="radioButton col-2" type="radio" disabled>
      <h4 class="text-dark col-8">${option.opcion}</h4>
      <h6 class="col-2">${option.porcentaje}%</h6>
    </div>
  `;
  }

  containerQuestions.insertAdjacentHTML(
    'beforeend',
    `
    <div class="carousel-item cardResponse shadow h-100 overflow-auto ${!isFirst ? 'active' : ''}">

        <div class="d-flex align-items-center h-100 gap-5">          
          <div class="d-flex flex-column align-self-start w-100 gap-5">
            <div>
              <h1 class="fw-bolder">${question.enunciado}</h1>
              <h6 class="text-secondary">${question.total_respuestas} respuestas</h6>
            </div>

            <div class="container d-flex flex-column gap-3">
              ${text}
            </div>
          </div>
          
          <div style="width: 40%;">
            <canvas id="ChartQuestion${question.id_pregunta}"></canvas>
          </div>

        </div>

    </div>
  `
  );
  isFirst = true;

  let dataQuestions = {
    data: [],
    labels: [],
  };

  for (const opcion of question.opciones) {
    dataQuestions.data.push(opcion.respuestas);
    dataQuestions.labels.push(opcion.opcion);
  }

  const dataChart = {
    labels: [...dataQuestions.labels],
    datasets: [
      {
        data: [...dataQuestions.data],
        backgroundColor: colors.map(color => color),
        hoverOffset: 4,
      },
    ],
  };

  const config = {
    type: 'pie',
    data: [],
    options: {
      animation: {
        duration: 0,
        delay: 100,
      },
      reponsive: true,
      maintainAspectRatio: true,
      aspectRatio: 1.3,
      onResize: null,
      resizeDelay: 0,
      normalized: true,
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  };

  config.data = dataChart;


  arrayCharts.push(new Chart(document.getElementById(`ChartQuestion${question.id_pregunta}`), config));
};

const init = function () {
  data.dataAnswers.map(question => insertQuestions(question));
};

init();