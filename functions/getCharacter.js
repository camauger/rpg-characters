const { MongoClient } = require("mongodb");

exports.handler = async (event) => {
  // Ensure we have a picture_id to look up
  const pictureId = event.queryStringParameters.picture_id;
  if (!pictureId) {
    return {
      statusCode: 400,
      body: JSON.stringify({ message: "Missing picture_id query parameter" }),
    };
  }

  const uri = process.env.MONGO_CONNECTION_STRING;
  const client = new MongoClient(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });

  try {
    await client.connect();
    const collection = client.db("rpg").collection("rpgCharacters");
    const character = await collection.findOne({ picture_id: pictureId });

    if (!character) {
      return {
        statusCode: 404,
        body: JSON.stringify({ message: "Character not found" }),
      };
    }

    return {
      statusCode: 200,
      body: JSON.stringify(character),
    };
  } catch (e) {
    console.error(e);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Internal server error" }),
    };
  } finally {
    await client.close();
  }
};
