'use strict';

console.log(data);
console.log(avatar);

if (data.selected !== 'answer' && data.selected !== '') {
  const opcionNavA = document.querySelector(`a[name=${data.selected.toLowerCase()}]`);
  const opcionNavDot = document.querySelector(`div[name=${data.selected}]`);
  opcionNavA.style.color = '#000';
  opcionNavDot.style.background = '#000';
  opcionNavDot.style.borderColor = '#000';
  opcionNavA.className += ' disabled';
}

const profileSection = document.querySelector('.profileList');
const profilePicture = document.querySelector('.profileImg');

if (avatar !== null) {
  profileSection.setAttribute('style', 'background-color: #1784d5');
  profilePicture.setAttribute('src', avatar);
  role === 'admin'
    ? profileSection.setAttribute('style', 'background-color: #1784d5')
    : profileSection.setAttribute('style', 'background-color: #ff3c69');
} else {
  if (role === 'admin') {
    profileSection.setAttribute('style', 'background-color: #1784d5');
    profilePicture.setAttribute('src', '/static/resources/user_blue.png');
  } else {
    profileSection.setAttribute('style', 'background-color: #ff3c69');
    profilePicture.setAttribute('src', '/static/resources/user_red.png');
  }
}
