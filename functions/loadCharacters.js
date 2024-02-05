const { MongoClient } = require('mongodb');

exports.handler = async (event, context) => {
  const uri = process.env.MONGO_CONNECTION_STRING;
  const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

  try {
    await client.connect();
    const collection = client.db("rpg").collection("characters");
    const characters = await collection.find({}).toArray();
    
    return {
      statusCode: 200,
      body: JSON.stringify(characters),
    };
  } catch (e) {
    console.error(e);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Failed to load characters" }),
    };
  } finally {
    await client.close();
  }
};
