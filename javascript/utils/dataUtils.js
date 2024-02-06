const fs = require('fs');

function pickRandomDataFromFile(filename, key) {
  const rawData = fs.readFileSync(filename);
  const data = JSON.parse(rawData);
  
  let randomIndex = Math.floor(Math.random() * data[key].length);
  return data[key][randomIndex];
}

function pickRandomItem(data, attributePath, key=null) {
  let items = data;
  
  // remove id from attributePath
  if (attributePath[0] === '_id') {
    attributePath.shift();
  }

  for (let attr of attributePath) {
    items = items[attr];
  }
  
  if (key !== null) {
    items = items.map(item => item[key]);
  }

  let randomIndex = Math.floor(Math.random() * items.length);
  return items[randomIndex];
}

function chooseTwoAndJoin(elements) {
  let indices = new Set();

  while(indices.size < 2) {
    indices.add(Math.floor(Math.random() * elements.length));
  }

  let choices = [...indices].map(i => elements[i]);
  return choices.join(" and ");
}

module.exports = { pickRandomDataFromFile, pickRandomItem, chooseTwoAndJoin };