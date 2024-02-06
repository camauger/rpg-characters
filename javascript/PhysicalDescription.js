const { createEyeColor, createHairColor, createHairStyle, createPhysicalTrait } 
    = require('settings/randomSettings'); // assuming these methods are exported from the randomSettings module

class PhysicalDescription {
    constructor() {
        this.physicalTrait = createPhysicalTrait();
        this.hairColor = createHairColor();
        this.hairStyle = createHairStyle();
        this.eyeColor = createEyeColor();
    }

    getDescription() {
        return `The character has ${this.hairColor} ${this.hairStyle} hair and ${this.eyeColor} eyes.`;
    }
}
module.exports = { PhysicalDescription };