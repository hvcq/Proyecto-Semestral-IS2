'use strict';

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
