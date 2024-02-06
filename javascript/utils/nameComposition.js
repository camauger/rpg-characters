const fs = require('fs');

// Generate a random first name
function generateRandomFirstName(gender = "Female") {
    let data = '';

    if (gender === 'Male') {
        data = 'data/names-mal.txt';
    } else if (gender === 'Female') {
        data = 'data/names-fem.txt';
    } else {
        data = 'data/names.txt';
    }

    const names = fs.readFileSync(data, 'utf8').split('\n');
    const firstName = names[Math.floor(Math.random() * names.length)];
    
    return firstName.charAt(0).toUpperCase() + firstName.slice(1);
}

// Generate a random character last name
function generateRandomLastName() {
    const dataFile = ['data/syllables_fem.json', 'data/syllables_mal.json', 'data/syllables_gen.json'][Math.floor(Math.random() * 3)];
    
    const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
    const prefixes = data.syllables.prefixes;
    const middle = data.syllables.middle;
    const suffixes = data.syllables.suffixes;

    const lastNameLength = Math.floor(Math.random() * 4) + 1;
    let lastName = '';

    for(let i = 0; i < lastNameLength; i++) {
        lastName += prefixes.concat(middle, suffixes)[Math.floor(Math.random() * (prefixes.length + middle.length + suffixes.length))];
    }
    
    return lastName.charAt(0).toUpperCase() + lastName.slice(1);
}

module.exports = { generateRandomFirstName, generateRandomLastName };