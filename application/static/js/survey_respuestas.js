'use strict';

console.log(data);

console.log(document.querySelector('#carouselExampleDark'));

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

  console.log('Este es el config', config);

  console.log('id', question.id_pregunta);

  arrayCharts.push(new Chart(document.getElementById(`ChartQuestion${question.id_pregunta}`), config));
};

const init = function () {
  data.dataAnswers.map(question => insertQuestions(question));
  console.log(arrayCharts);
};

init();

// const containerUsers = document.querySelector('.users');
// const containerQuestions = document.querySelector('#ModalQuestions');

// let users = data.dataUsers;

// const initUsr = function () {
//   for (const user of users) insertRowUser(user);
// };

// const insertRowUser = function (user) {
//   containerUsers.insertAdjacentHTML(
//     'beforeend',
//     `
//     <tr id="User${user.id_registrado}">
//       <td filtroUsuario="true">${user.nombre}</td>
//       <td>
//         ${user.apellido}
//       </td>
//       <td>
//         ${user.email}
//       </td>
//       <td>
//         ${user.genero}
//       </td>
//       <td>
//         ${user.edad}
//       </td>
//     </tr>
//   `
//   );
// };

// initUsr();

// // ------ RESPUESTAS ------

// const showQuestions = function (event) {
//   myModal.show();
// };

// const containerTitle = document.querySelector('#surveyTitle');

// let surveyTitle = data.dataSurveyTitle;

// const insertTitle = function (title) {
//   containerTitle.insertAdjacentHTML(
//     'beforeend',
//     `
//     <h2>${title.titulo}</h2>
//   `
//   );
// };

// insertTitle(surveyTitle);

// const containerAnswers = document.querySelector('.questions');
// const containerAlternatives = document.querySelector('#containerAlternatives');

// console.log(containerAnswers);

// let answers = data.dataAnswers;

// const initAns = function () {
//   for (const ans of answers) insertRowAnswer(ans);
// };

// const insertRowAnswer = function (ans) {
// containerAnswers.insertAdjacentHTML(
//   'beforeend',
//   `
//   <div class="d-flex justify-content-between align-items-center">
//     <h1>${ans.numero}) ${ans.enunciado}</h1>
//   </div>
// `
// );

// ans.opciones.map(opcion => {
//   containerAlternatives.insertAdjacentHTML(
//     'beforeend',
//     `

//     <div class="d-flex align-items-center gap-3 mb-2">
//       <div class="form-check w-75">
//         <input class="form-check-input" type="radio" name="flexRadioDisabled" id="flexRadioDisabled" disabled>
//         <label class="form-check-label text-dark">
//           ${opcion.opcion}
//         </label>
//       </div>
//       <div class="d-flex gap-5">
//         <h6>${opcion.respuestas} respuestas</h6>
//         <h6>${opcion.porcentaje}%</h6>
//       </div>
//     </div>
//     `
//   );
//   });
// };

// // insertRowAnswer(answers);

// initAns();
// //Comentario para que se actualice
