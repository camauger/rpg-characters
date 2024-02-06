const fs = require('fs');

// Importing settings and utilities from their respective files
const { genderSettings, ageSettings, hairColorsSettings, physicalSettings } = require('./settings/characterSettings');
const { pickRandomDataFromFile } = require('./utils/dataUtils')

function pickRandomSetting(setting) {
    let randomIndex = Math.floor(Math.random() * setting.length);
    return setting[randomIndex];
}

function pickRandomSettingWithWeight(setting) {
  const totalWeight = setting.reduce((sum, curr) => sum + curr[1], 0); 
  const threshold = Math.floor(Math.random() * totalWeight);
    
  let runningSum = 0;
  
  for (let [item, weight] of setting) {
      runningSum += weight;
      if (runningSum >= threshold)
        return item;
  }
}

function pickRandomGender() {
  return pickRandomSettingWithWeight(genderSettings);
}

function pickRandomAge() {
  return pickRandomSettingWithWeight(ageSettings);
}

function pickRandomHairColor() {
  return pickRandomSettingWithWeight(hairColorsSettings);
}

function pickRandomPhysicalTrait() {
  return pickRandomSetting(physicalSettings);
}

function pickRandomBackground() {
  return pickRandomDataFromFile('data/background_data.json', 'backgrounds')
}

function pickRandomEthnicity() {
  return pickRandomDataFromFile('data/ethnicity_data.json', 'ethnicity')
}

function pickRandomEthnicityFantasy() {
  return pickRandomDataFromFile('data/ethnicity_fantasy_data.json', 'ethnicity')
}

function pickRandomCharacterClass() {
  return pickRandomDataFromFile('data/character_classes.json', 'classes')
}

function pickRandomSubclass(characterClass) {
  let randomIndex = Math.floor(Math.random() * characterClass.subclasses.length);
    return characterClass.subclasses[randomIndex];
}

function createPhysicalDescription() {
  let rawData = fs.readFileSync('data/physical_description.json');
  return JSON.parse(rawData);
}

function createPhysicalTrait() {
  return pickRandomPhysicalTrait();
}

function createPhysicalDescSynonym(key) {
  const data = createPhysicalDescription();
  const randomSynonymElement = pickRandomSetting(data[key]);
  const randomSynonym = pickRandomSetting(randomSynonymElement.synonyms);
  return randomSynonym.toLowerCase();
}

function createBodyType() {
  return createPhysicalDescSynonym('body_types');
}

function createHairStyle() {
  return createPhysicalDescSynonym('hair_styles')
}

function createHairColor() {
  return pickRandomHairColor();
}

function createEyeColor() {
  return createPhysicalDescSynonym('eye_colors')
}

function getEthnicityKeywords(ethnicity) {
  const totalKeywords = ethnicity.keywords;
    
  // Pick up to 5 keywords at random
  keywordCount = Math.min(5, totalKeywords.length);
  
  // Use Array.splice to remove and return random elements from totalKeywords
  let pickedKeywords = [];
  for (let i = 0; i < keywordCount; ++i) {
    const randomIndex = Math.floor(Math.random() * totalKeywords.length);
    pickedKeywords.push(totalKeywords.splice(randomIndex, 1)[0]);
  }

  // return the keywords in a string
  return pickedKeywords.join(', ');
}

module.exports = {
    pickRandomGender,
    pickRandomAge,
    pickRandomHairColor,
    pickRandomPhysicalTrait,
    pickRandomBackground,
    pickRandomEthnicity,
    pickRandomEthnicityFantasy,
    pickRandomCharacterClass,
    pickRandomSubclass,
    createPhysicalDescription,
    createPhysicalTrait,
    createBodyType,
    createHairStyle,
    createHairColor,
    createEyeColor,
    getEthnicityKeywords
    };