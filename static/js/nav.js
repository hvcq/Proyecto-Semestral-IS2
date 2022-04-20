'use strict'
console.log(navOptions.selected.toLowerCase())

const opcionNavA = document.querySelector(`a[name=${navOptions.selected.toLowerCase()}]`);
const opcionNavDot = document.querySelector(`div[name=${navOptions.selected}]`);

opcionNavA.style.color = '#000'
opcionNavDot.style.background = '#000'
opcionNavDot.style.borderColor = '#000'
opcionNavA.className +=' disabled'



// password.addEventListener('blur', (event) => {
//   event.target.style.background = '';
// });
