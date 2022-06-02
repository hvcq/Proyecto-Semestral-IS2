'use strict';

console.log(data);
let current_id;
const containerSurveys = document.querySelector('.surveys');
let surveys = data.dataSurveys;

var myModalSure = new bootstrap.Modal(document.querySelector('.myModalSure'), {
  keyboard: false,
});

const init = function () {
  for (const survey of surveys) insertRow(survey);
};

const insertRow = function (survey) {
  let percentage = survey.answers.total === 0 ? 0 : Number.parseFloat((survey.answers.current_answers * 100) / survey.answers.total).toFixed(0);

  containerSurveys.insertAdjacentHTML(
    'beforeend',
    `
    <tr id="Encuesta${survey.id_survey}">
      <td scope="row">
        <div class="form-check form-switch">
          <input idEncuesta="${survey.id_survey}" class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" ${
      survey.active ? 'checked' : ''
    } onclick="statusSurvey(event)"> 
        </div>
      </td>
      <td filtroTitle="true"><a href="/survey/${survey.id_survey}/preguntas">${survey.title}</a></td>
      <td>
        ${survey.visits}
      </td>
      <td>
        <div class="progress w-75">
          <div class="progress-bar" role="progressbar" style="width: ${percentage}%;" aria-valuenow="${percentage}" aria-valuemin="0"
            aria-valuemax="100">${percentage}%</div>
        </div>
      </td>
      <td>
        ${survey.start_date}
      </td>
      <td>
        None
      </td>
      <td class="text-center">
        <div class="btn-group dropstart">
          <button class="btn btn-secondary rounded-circle btn-circle p-1" type="button" id="dropdownCenterBtn" data-bs-toggle="dropdown" aria-expanded="false">
            <img class="imgDot" src="/static/resources/dots.png" alt="">
          </button>
          <ul class="dropdown-menu slideInAction animate" aria-labelledby="dropdownCenterBtn" idEncuesta="${survey.id_survey}">
            <li><a typeButton="POST" class="dropdown-item" onclick="showModalSure(event)">Publicar</a></li>
            <li><a typeButton="DELETE" class="dropdown-item" onclick="showModalSure(event)">Eliminar</a></li>
          </ul>
        </div>
      </td>
    </tr>
  `
  );
};

init();

const statusSurvey = function (event) {
  const input = event.target;
  const id = input.attributes[0].textContent;
  const [survey] = surveys.filter(element => `${element.id_survey}` === id);

  survey.active ? (survey.active = false) : (survey.active = true);

  const response = {
    id_survey: survey.id_survey,
    status: survey.active,
  };

  $.ajax({
    url: '/cambiar_estado',
    type: 'POST',
    data: { response: JSON.stringify(response) },
    success: function (result) {},
  });
};

const showModalSure = function (event) {
  myModalSure.show();
  const parent = event.target.parentNode.parentNode;
  current_id = parent.attributes[2].textContent;
  const type = event.target.attributes[0].textContent;
  const button = document.querySelector('.buttonModal');
  const title = document.querySelector('.titleModal');

  if (type === 'POST') {
    button.removeEventListener('click', deleteSurvey);
    console.log('ENTRO POST');
    title.textContent = '¿Estas seguro de publicar la encuesta?';
    button.addEventListener('click', postSurvey);
  } else if (type === 'DELETE') {
    button.removeEventListener('click', postSurvey);
    console.log('ENTRO DELETE');
    title.textContent = '¿Estas seguro de eliminar la encuesta?';
    button.addEventListener('click', deleteSurvey);
  }
};

const deleteSurvey = function () {
  const response = {
    id_survey: Number(current_id),
  };

  const trElement = document.querySelector(`#Encuesta${current_id}`);
  trElement.remove();

  const surveyArray = surveys.filter(element => `${element.id_survey}` !== current_id);
  surveys = surveyArray;
  console.log(surveys);

  $.ajax({
    url: '/delete_survey',
    type: 'POST',
    data: { response: JSON.stringify(response) },
    success: function (result) {},
  });
  myModalSure.hide();
};

const postSurvey = function () {
  const response = {
    id_survey: Number(current_id),
  };

  console.log(response);
  $.ajax({
    url: '/mail_sent',
    type: 'POST',
    data: { response: JSON.stringify(response) },
    success: function (result) {},
  });

  myModalSure.hide();
};

//CHARTS ------------------------------------------------------------------------------------

const dataChart = {
  labels: ['Registrados', 'Anonimos'],
  datasets: [
    {
      data: [300, 50],
      backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)'],
      hoverOffset: 4,
    },
  ],
};

const config = {
  type: 'doughnut',
  data: dataChart,
  options: {
    reponsive: true,
    maintainAspectRatio: true,
    aspectRatio: 2,
    onResize: null,
    resizeDelay: 0,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  },
};

const myChart = new Chart(document.getElementById('myChart'), config);

//Filter

const filterSearch = function () {
  let input, filter, tr, txtValue, trList;
  input = document.querySelector('.searchInput');
  filter = input.value.toUpperCase();
  trList = document.querySelectorAll('.surveys tr');
  tr = document.querySelectorAll('.surveys tr td[filtroTitle]');
  for (let i = 0; i < tr.length; i++) {
    txtValue = tr[i].textContent;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      trList[i].style.display = '';
    } else {
      trList[i].style.display = 'none';
    }
  }
};
