'use strict';

let currentStep = 0;

const containerStep = document.querySelector('#containerStep');

let userId;
let code = '';
let email = '';
let userResponse = ['', '', '', '', '', ''];

const insertStep = step => {
  containerStep.insertAdjacentHTML('afterbegin', step);
};

const step1 = `<div class="text-center">
<h3 class="text-dark">¿Olvidaste tu contraseña?</h3>
<p class="text-secondary ms-2">No te preocupes, puedes recuperarla!</p>
</div>

<form class="d-flex flex-column align-items-center gap-3 w-100 needs-validation" novalidate>
<div class="form-group w-100">
  <label for="exampleInputEmail1">Email</label>
  <input type="email" class="form-control" id="step1" aria-describedby="emailHelp" placeholder="Ingresa tu email" required/>
  <div class="valid-feedback">Excelente, luce bien!</div>
  <div class="invalid-feedback">Por favor, rellena con un email!</div>
</div>
<button class="btn btn-primary w-100" onclick="checkForm(event)">Enviar código</button>
</form>`;

let step2 = '';

const step3 = `<h3 class="text-dark ms-2 text-center">Ingresa tu código</h3>
<p class="text-secondary ms-2">Este código es único</p>
<form class="d-flex flex-column align-items-center gap-4 formCode">
  <div class="d-flex justify-content-center gap-3">
    <div class="form-group">
      <input type="text" class="form-control codeInput" id="code1" maxlength="1" oninput="nextInput(event)" required/>
    </div>
    <div class="form-group">
      <input type="text" class="form-control codeInput" id="code2" maxlength="1" oninput="nextInput(event)" required/>
    </div>
    <div class="form-group">
      <input type="text" class="form-control codeInput" id="code3" maxlength="1" oninput="nextInput(event)" required/>
    </div>
    <div class="form-group">
      <input type="text" class="form-control codeInput" id="code4" maxlength="1" oninput="nextInput(event)" required/>
    </div>
    <div class="form-group">
      <input type="text" class="form-control codeInput" id="code5" maxlength="1" oninput="nextInput(event)" required/>
    </div>
    <div class="form-group">
      <input type="text" class="form-control codeInput" id="code6" maxlength="1" oninput="nextInput(event)" required/>
    </div>
  </div>

  <div class="d-none incorrectCode">El código es incorrecto!</div>
  <div class="d-none correctCode">El código es correcto!</div>
  <button type="button" class="btn btn-primary" onclick="validateCode(event)">Validar código</button>
  <div class="d-flex justify-content-around gap-2">
    <p class="text-secondary ms-2">Necesito otro código</p>
    <a onclick="sendCode()">Click para reenviar</a>
  </div>
</form>`;

const step4 = `<div class="text-center">
<h3 class="text-dark">Ingresa tu nueva contraseña</h3>
<p class="text-secondary ms-2">Tu nueva contraseña debe ser diferente a las anteriores</p>
</div>

<form class="d-flex flex-column align-items-center gap-3 w-100">
<div class="form-group w-100">
  <label for="exampleInputEmail1">Nueva contraseña</label>
  <input type="password" class="form-control mb-2" id="Confirmacion1" />
  <label for="exampleInputEmail1">Confirmar Contraseña</label>
  <input type="password" class="form-control" id="Confirmacion2" />
</div>
<div class="d-none incorrectCode" id="coincidencia">Las contraseñas no coinciden!</div>
<div class="d-none incorrectCode" id="rellena">Rellena los campos necesarios!</div>
<button onclick="validatePassword(event)" class="btn btn-primary w-100">Guardar</button>
</form>`;

const step5 = ` <div class="text-center">
<img src="static/resources/success.gif">
</div>
<h3 class="text-dark ms-2 text-center">Contraseña cambiada con éxito</h3>
<h5 class="text-secondary ms-2 text-center">Tu contraseña ha sido restaurada con éxito!</h5>
<p class="text-secondary">Redireccionando al login...</p>
<form>
<h5></h5>
</form>`;

const validatePassword = event => {
  event.preventDefault();
  const input1 = document.querySelector('#Confirmacion1');
  const input2 = document.querySelector('#Confirmacion2');

  if (input1.value === input2.value && input1.value !== '' && input2.value !== '') {
    let data = { user: email, password: input1.value };
    $.ajax({
      url: '/password_reset',
      type: 'POST',
      data: { response: JSON.stringify(data) },
      success: function (result) {
        if (result === 'password cambiada exitosamente') {
          nextStep();
          delay();
        }
      },
    });
    async function delay() {
      await new Promise(done => setTimeout(() => done(), 3000));
      window.location.href = '/login';
    }
  } else if (input1.value === '') {
    document.querySelector('#rellena').classList.remove('d-none');
    input1.style.borderColor = '#e74c3c';
    input2.style.borderColor = '#e74c3c';
  } else {
    document.querySelector('#rellena').classList.add('d-none');
    document.querySelector('#coincidencia').classList.remove('d-none');
    input1.style.borderColor = '#e74c3c';
    input2.style.borderColor = '#e74c3c';
  }
};

const validateCode = event => {
  event.preventDefault();
  if (userResponse.join('') === code) {
    document.querySelector('.incorrectCode').classList.add('d-none');
    document.querySelector('.correctCode').classList.remove('d-none');

    const inputs = document.querySelectorAll('.codeInput');
    inputs.forEach(element => {
      element.style.borderColor = '#58d68d';
    });
    nextStep();
  } else {
    document.querySelector('.incorrectCode').classList.remove('d-none');
    const inputs = document.querySelectorAll('.codeInput');
    inputs.forEach(element => {
      element.style.borderColor = '#e74c3c';
    });
  }
};

const nextInput = event => {
  const input = event.target;
  const id = input.attributes[2].value.slice(4);

  input.value = input.value.toUpperCase();
  userResponse[Number(id) - 1] = input.value;

  if (id === '1' && input.value !== '') {
    document.querySelector('#code2').focus();
  } else if (id === '2' && input.value !== '') {
    document.querySelector('#code3').focus();
  } else if (id === '3' && input.value !== '') {
    document.querySelector('#code4').focus();
  } else if (id === '4' && input.value !== '') {
    document.querySelector('#code5').focus();
  } else if (id === '5' && input.value !== '') {
    document.querySelector('#code6').focus();
  }
};

const nextStep = () => {
  currentStep++;
  changeStep();
  if (currentStep === 2) {
    document.querySelector('#code1').focus();
  }
};
const removeChild = () => {
  while (containerStep.firstChild) {
    containerStep.removeChild(containerStep.firstChild);
  }
};

const randomCode = () => {
  var letters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var code = '';
  for (let i = 0; i < 6; i++) code += letters[Math.floor(Math.random() * 36)];
  return code;
};

const addValidation = () => {
  var form = document.querySelectorAll('.needs-validation');
  if (form === undefined) return;
  Array.prototype.slice.call(form).forEach(function (elementForm) {
    elementForm.addEventListener(
      'submit',
      function (event) {
        if (!elementForm.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        elementForm.classList.add('was-validated');
      },
      false
    );
  });
};

const changeStep = () => {
  const card = document.querySelector('.card');
  if (currentStep === 0) {
    insertStep(step1);
    card.style.opacity = 1;
  } else if (currentStep === 1) {
    removeChild();
    insertStep(step2);
  } else if (currentStep === 2) {
    removeChild();
    insertStep(step3);
  } else if (currentStep === 3) {
    removeChild();
    insertStep(step4);
  } else if (currentStep === 4) {
    removeChild();
    insertStep(step5);
  }

  addValidation();
};

changeStep();

const setStep2 = () => {
  step2 = `<div class="text-center">
  <h3 class="text-dark">Revisa tu email</h3>
  <p class="text-secondary ms-2">Hemos enviado un codigo al correo</p>
  <p class="text-secondary ms-2">${email}</p>
  </div>
  
  <form class="d-flex flex-column align-items-center gap-3 w-100">
  <button class="btn btn-primary w-100" onclick="nextStep()">Tengo mi código!</button>
  <div class="d-flex justify-content-around gap-2">
    <p class="text-secondary ms-2">No he recibido mi codigo</p>
    <a onclick="sendCode()">Click para reenviar</a>
  </div>
  </form>`;
  nextStep();
};

const sendCode = () => {
  code = randomCode();
  const data = { user_mail: email, code: code };

  $.ajax({
    url: '/send_code',
    type: 'POST',
    data: { response: JSON.stringify(data) },
    success: function (result) {
      if (currentStep === 0) result !== 'Email no existe' ? setStep2() : '';
    },
  });
};

const checkForm = event => {
  event.preventDefault();
  let form = document.querySelector('.needs-validation');
  if (form.checkValidity()) {
    form.classList.remove('was-validated');
    const input = document.querySelector('#step1');
    email = input.value;
    sendCode();
  } else {
    form.classList.add('was-validated');
  }
};
