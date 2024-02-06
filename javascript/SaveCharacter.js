const { MongoClient } = require("mongodb");
const CharacterClass = require("./CharacterClass"); // Assuming Character.js is in the same directory

const uri = process.env.MONGODB_URI;
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  try {
    await client.connect();
    const characterData = JSON.parse(event.body);
    const dbName = "yourDatabaseName"; // Replace with your actual database name
    const result = await CharacterClass.saveCharacter(client, dbName, characterData);

    return {
      statusCode: 200,
      body: JSON.stringify({ message: "Character created", id: result.insertedId }),
    };
  } catch (error) {
    console.error("Error saving character:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Failed to save character" }),
    };
  } finally {
    await client.close();
  }
};
