'use strict';

//FILTER

const filterSearch = function () {
  let input, filter, tr, txtValue, trList;
  input = document.querySelector('.searchInputUser');
  filter = input.value.toUpperCase();
  trList = document.querySelectorAll('.users tr');
  tr = document.querySelectorAll('.users tr td[filtroTitle]');
  for (let i = 0; i < tr.length; i++) {
    txtValue = tr[i].textContent;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      trList[i].style.display = '';
    } else {
      trList[i].style.display = 'none';
    }
  }
};
