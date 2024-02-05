const { MongoClient } = require("mongodb");

exports.handler = async (event, context) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const data = JSON.parse(event.body);
  const uri = process.env.MONGO_CONNECTION_STRING;
  const client = new MongoClient(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });

  try {
    await client.connect();
    const collection = client.db("rpg").collection("rpgCharacters");
    const result = await collection.insertOne(data);

    return {
      statusCode: 200,
      body: JSON.stringify(result.ops[0]),
    };
  } catch (e) {
    console.error(e);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Failed to generate character" }),
    };
  } finally {
    await client.close();
  }
};
