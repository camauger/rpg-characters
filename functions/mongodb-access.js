
const { MongoClient } = require('mongodb');

exports.handler = async (event, context) => {
  const uri = process.env.MONGO_CONNECTION_STRING;
  const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

  try {
    await client.connect();
    const database = client.db("rpg");
    const collection = database.collection("rpgCharacters");
    const documents = await collection.find({}).toArray();

    return {
      statusCode: 200,
      body: JSON.stringify(documents),
    };
  } catch (e) {
    return {
      statusCode: 500,
      body: 'Internal Server Error: ' + e.message,
    };
  } finally {
    await client.close();
  }
};
