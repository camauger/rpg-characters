const { MongoClient } = require("mongodb");

// MongoDB connection details
const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri);

exports.handler = async (event, context) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  try {
    await client.connect();
    const collection = client.db("rpg").collection("characters");
    const data = JSON.parse(event.body);

    // Your character generation logic here
    // const characterManager = CharacterManager(); // You need to adapt this part
    // const newCharacter = characterManager.createCharacter({}, true); // Adapt this to work with MongoDB

    // Insert the modified data object into the database
    const newCharacter = await collection.insertOne(data);

    if (newCharacter) {
      return {
        statusCode: 200,
        body: JSON.stringify({ message: "Character created" }),
      };
    } else {
      return {
        statusCode: 500,
        body: JSON.stringify({ message: "Failed to create character" }),
      };
    }
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Internal Server Error" }),
    };
  } finally {
    await client.close();
  }
};
