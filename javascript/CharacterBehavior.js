const fs = require('fs');
const random = require('./random'); // assuming there's a 'random' module for generating random choices

class CharacterBehavior {
    constructor(character) {
        this.settings = this.loadSettings();
        this.character = character;
    }

    loadSettings() {
        let rawData = fs.readFileSync('data/character_behavior.json');
        let data = JSON.parse(rawData);
        return data;
    }

    selectRandomAttribute(attributeName) {
        const attributeList = this.settings[attributeName];
        const randomIndex = random(0, attributeList.length - 1); 
        return attributeList[randomIndex].toLowerCase();
    }

    createBehavior() {
        let pronoun = "their";
        if (this.character.gender === "Female") {
            pronoun = "her";
        } else if (this.character.gender === "Male") {
            pronoun = "his";
        }

        const behaviorDescription = `${this.character.full_name}'s ideal is ${this.selectRandomAttribute('ideals')}. ${pronoun} flaw is ${this.selectRandomAttribute('flaws')}, ${pronoun} bond is ${this.selectRandomAttribute('bonds')}, ${pronoun} behavior is ${this.selectRandomAttribute('behaviors')}, and ${pronoun} nature is ${this.selectRandomAttribute('natures')}.`;

        return behaviorDescription;
    }

    toString() {
        return `The character's ideal is ${this.selectRandomAttribute('ideals')}, their flaw is ${this.selectRandomAttribute('flaws')}, their bond is ${this.selectRandomAttribute('bonds')}, their behavior is ${this.selectRandomAttribute('behaviors')}, and their nature is ${this.selectRandomAttribute('natures')}.`;
    }
}
module.exports = { CharacterBehavior };