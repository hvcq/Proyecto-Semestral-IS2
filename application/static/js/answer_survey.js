"use strict";

const title = document.querySelector(".titleSurvey");
title.classList.remove("invisible");
console.log(title.classList);

const responses = {
  idEncuesta: "idEcuesta",
  usuario: {
    name: "nombre",
    correo: "example@udec.cl",
  },
  respuestas: [
    {
      idPregunta: "idPregunta",
      type: "desarrollo",
      response: "mi respuesta",
    },
    {
      idPregunta: "idPregunta",
      type: "alternativa",
      response: {
        idOpcion: "idOpcion",
        textAlt: "color azul",
      },
    },
  ],
};
