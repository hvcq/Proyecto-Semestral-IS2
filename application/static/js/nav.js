'use strict'

const opcionNavA = document.querySelector(`a[name=${data.selected.toLowerCase()}]`);
const opcionNavDot = document.querySelector(`div[name=${data.selected}]`);

opcionNavA.style.color = '#000'
opcionNavDot.style.background = '#000'
opcionNavDot.style.borderColor = '#000'
opcionNavA.className +=' disabled'
