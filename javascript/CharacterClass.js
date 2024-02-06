const { MongoClient } = require("mongodb");
const {
  pickRandomAge,
  pickRandomBackground,
  pickRandomCharacterClass,
  pickRandomEthnicity,
  pickRandomGender,
  pickRandomSubclass,
} = require("./settings/randomSettings");
const { CharacterBehavior } = require("./CharacterBehavior");
const { PhysicalDescription } = require("./PhysicalDescription");
const { createImage } = require("./utils/createImage");
const { getEthnicityKeywords } = require("./utils/ethnicityUtils");
const {
  createPhysicalTrait,
  createHairColor,
  createHairStyle,
  createEyeColor,
} = require("./settings/randomSettings");
const { fetchCharacterData, optimizePrompt } = require("./utils/openaiUtils");

const fs = require("fs");
const path = require("path");

// Load environment variables
require("dotenv").config();
const apiKey = process.env.OPENAI_API_KEY;

// Set OpenAI API key
const openai = require("openai");
openai.apiKey = apiKey;

// Load data from JSON files
const dataFiles = [
  "artists",
  "illustrators",
  "accessories",
  "angles",
  "clothing",
  "facial_expressions",
  "portraits",
  "genres",
  "styles",
  "lighting",
  "cameras",
  "posing",
];

let data = {};

dataFiles.forEach((file) => {
  let rawData = fs.readFileSync(`data/${file}.json`);
  data[file] = JSON.parse(rawData);
});

function fileExists(folderPath, filename) {
  const filePath = path.join(folderPath, filename);
  fs.access(filePath, fs.constants.F_OK, (err) => {
    if (err) {
      console.error("File doesn't exist");
      return false;
    } else {
      console.log("File exists");
      return true;
    }
  });
}

// toDict() {
//   let data = this.toObject();
//   return data;
// }


class CharacterClass {
  constructor(data) {
    // Basic character information
    this.first_name = data.first_name;
    this.last_name = data.last_name;
    this.full_name = `${data.first_name} ${data.last_name}`;
    this.gender = data.gender;

    // Character class and subclass information
    this.character_class_name = data.character_class_name;
    this.character_subclass_name = data.character_subclass_name;

    // Background information
    this.background_name = data.background_name;
    this.background_setting = data.background_setting;

    // Ethnicity information
    this.ethnicity_name = data.ethnicity_name;

    // Other character attributes
    this.age = data.age;
    this.background_story = data.background_story;
    this.eye_color = data.eye_color;
    this.hair_color = data.hair_color;
    this.hair_style = data.hair_style;
    this.has_image = data.has_image || false;
    this.picture_id = data.picture_id || this.generatePictureId();

    // Image prompt attributes
    this.clothing = data.clothing;
    this.physical_trait = data.physical_trait;
  }

  toString() {
    return `${this.fullName} is a ${this.gender} ${this.ethnicityName} ${this.characterClassName} 
           (${this.characterSubclassName}) and a ${this.backgroundName} | ${this.ethnicityKeywords}`;
  }

  generatePictureId() {
    // Simplified version of generating a picture ID
    return `${this.full_name.replace(" ", "_").toLowerCase()}`;
    // For adding randomness as in the Python version, uncomment the next line:
    // return `${this.full_name.replace(' ', '_').toLowerCase()}_${Math.floor(Math.random() * (9999 - 1000 + 1)) + 1000}`;
  }

  createPhysicalDescriptionText() {
    let physicalDescription = `${this.indefiniteArticle(
      this.physicalTrait
    )} ${this.gender.toLowerCase()} ${this.ethnicityName}. ${
      this.fullName
    } has ${this.hairColor.toLowerCase()} ${this.hairStyle} hair and ${
      this.eyeColor
    } eyes`;
    return `${this.fullName} is ${physicalDescription}.`;
  }

  indefiniteArticle(word) {
    if (!word) return "";
    let vowelTest = "aeiouAEIOU";
    if (vowelTest.indexOf(word[0]) !== -1) return "an";
    else return "a";
  }

  async createBackgroundStory() {
    console.log("Creating background story");
    let prompt = `Write a background story for an RPG character named ${this.fullName}, a ${this.characterClass} in the world of Forgotten Realms. The character is a ${this.backgroundName} with ${this.ethnicity} heritage. Describe their upbringing, key events in their life, and their motivations. Please write three paragraphs with a total word count of around 300 words. Conclude the background story by including a potential adventure hook or a mystery that the character seeks to unravel.`;
    let backgroundStory = await fetchCharacterData(prompt);
    return backgroundStory;
  }

  async createPersonalityDescription() {
    console.log("Creating personality description");
    let prompt = `Write a personality description for an RPG character named ${this.fullName}. The character is a ${this.characterClass} with a ${this.backgroundName} background and has ${this.ethnicity} heritage. Describe their personality traits, motivations, and how they interact with others. Please write a paragraph with a total word count of around 100 words. Use this ${this.behavior} to inform their personality.`;
    let personality = await fetchCharacterData(prompt);
    return personality;
  }
  static async saveCharacter(client, dbName, characterData) {
    try {
      const db = client.db(dbName);
      const collection = db.collection("characters");
      const character = new Character(characterData);
      const result = await collection.insertOne(character);
      return result;
    } catch (error) {
      console.error("Failed to save character:", error);
      throw error; // Re-throw the error for further handling
    }
  }

  async createImagePrompt() {
    // Now form the prompt string using literals
    let prompt = `${this.portrait} in the style of ${this.artist} mixed with ${this.style} | ${this.genre} | ${this.description} | 
                  ${this.behavior} | ${this.fullName} is wearing ${this.clothing} clothing | ${this.tones} tones | ${this.camera} | 
                  ${this.posing} | ${this.accessories} | ${this.lighting} | ${this.backgroundSetting}`;
    prompt += ` | ${this.ethnicityKeywords}`;

    // This is the prompt for midjourney
    let promptMidjourney = `${prompt}, RPG, D&D. --s 750 --ar 90:160`;

    const fs = require("fs");
    // Append prompt to image_prompts.txt
    fs.appendFileSync("data/image_prompts.txt", promptMidjourney + "\n");
    console.log(
      `Midjourney Image prompt for the chracter: ${promptMidjourney}`
    );

    // Create the image using the prompt with dall-e
    let promptDallE = prompt;
    promptDallE = await optimizePrompt(promptDallE);

    // Append prompt to image_prompts_dalle.txt
    fs.appendFileSync("data/image_prompts_dalle.txt", promptDallE + "\n");
    console.log(promptDallE);

    // use full name as name for image
    let pictureName = this.fullName.replace(" ", "_").toLowerCase();

    // Assuming createImage is an asynchronous function that returns a Promise.
    await createImage(promptDallE, pictureName);
    console.log("Image created successfully.");

    return prompt;
  }

  static toDict() {
    // Converts the character instance to a plain object suitable for JSON serialization
    return {
      first_name: this.first_name,
      last_name: this.last_name,
      full_name: this.full_name,
      gender: this.gender,
      character_class_name: this.character_class_name,
      character_subclass_name: this.character_subclass_name,
      background_name: this.background_name,
      background_setting: this.background_setting,
      ethnicity_name: this.ethnicity_name,
      age: this.age,
      background_story: this.background_story,
      eye_color: this.eye_color,
      hair_color: this.hair_color,
      hair_style: this.hair_style,
      has_image: this.has_image,
      picture_id: this.picture_id,
      clothing: this.clothing,
      physical_trait: this.physical_trait,
    };
  }

  updateHasImage() {
    const fs = require("fs");
    const path = require("path");

    this.hasImage = fs.existsSync(
      path.join("static", "images", `${this.pictureId}.png`)
    );
  }

  createPictureId() {
    this.pictureId = this.fullName.replace(" ", "_").toLowerCase();
  }

  createPhysicalDescription() {
    return new PhysicalDescription(); // Assuming `PhysicalDescription` is another class
  }

  createBehavior() {
    let behavior = new CharacterBehavior(this); // Assuming `CharacterBehavior` is another class
    let behaviorText = behavior.createBehavior();
    return behaviorText;
  }

  async createCharacter(params, isRandom = false) {
    if (isRandom) {
      this.gender = await pickRandomGender();
      this.firstName = await generateRandomFirstName(this.gender);
      this.lastName = await generateRandomLastName();
    } else {
      this.firstName = params.firstName || "";
      this.lastName = params.lastName || "";
    }

    this.fullName = `${this.firstName} ${this.lastName}`;

    // Additional fields could be set here similarly, example:
    // this.id = int(random.randint(1, 9999)),
    this.characterClass = await pickRandomCharacterClass();
    this.characterClassID = this.characterClass.id;
    this.characterClassName = this.characterClass.name;
    this.characterSubclass = await pickRandomSubclass(this.characterClass);
    this.characterSubclassID = this.characterSubclass.id;
    this.characterSubclassName = this.characterSubclass.name;

    // Background
    this.background = await pickRandomBackground();
    this.backgroundID = this.background.id;
    this.backgroundName = this.background.name;
    this.backgroundSetting = this.background.setting;
    this.backgroundStory = this.createBackgroundStory();

    // Traits
    this.age = await pickRandomAge();
    this.physicalTrait = createPhysicalTrait();
    this.hairColor = createHairColor();
    this.hairStyle = createHairStyle();
    this.eyeColor = createEyeColor();
    this.behavior = this.createBehavior();
    this.personalityDescription = this.createPersonalityDescription();

    // Race
    this.ethnicity = await pickRandomEthnicity();
    this.ethnicityID = this.ethnicity.id;
    this.ethnicityName = this.ethnicity.name;
    this.ethnicityKeywords = getEthnicityKeywords(this.ethnicity);

    // Image
    this.pictureID = this.createPictureID();
    this.updateHasImage();

    // Description
    this.description = `${this.fullName} is a ${this.gender} ${
      this.ethnicityName
    } ${this.characterClassName} and ${indefiniteArticle(this.backgroundName)}`;

    // Prompt
    // Assuming data is available in some form
    this.camera = pickRandomItem(data, ["cameras", "cameras"], "name");
    this.angle = pickRandomItem(data, ["angles", "angles"], "name");
    this.posing = pickRandomItem(data, ["posing", "posing"]);
    this.accessories = pickRandomItem(data, ["accessories", "accessories"]);
    this.facialExpression = pickRandomItem(
      data,
      ["facialExpressions", "facialExpressions"],
      "expression"
    );
    this.genre = pickRandomItem(data, ["genres", "genres"], "name");
    this.tones = " and ".join(random.sample(colors, 2));
    // Get the description of the artistic style rather than the name
    this.artist = pickRandomItem(
      data,
      ["illustrators", "illustrators"],
      "description"
    );

    this.style = pickRandomItem(data, ["styles", "styles"], "name");
    this.lighting = pickRandomItem(data, ["lighting", "lighting"], "name");
    this.assignRandomClothing();

    this.portrait = pickRandomItem(data, ["portraits", "portraits"], "name");

    // Final prompt
    this.imagePrompt = this.createImagePrompt();

    return this;
  }
}

module.exports = { CharacterClass };
