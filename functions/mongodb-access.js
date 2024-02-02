const { MongoClient } = require('mongodb');

exports.handler = async (event, context) => {
  const uri = process.env.MONGODB_URI;
  const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

  try {
    await client.connect();
    const database = client.db("yourDatabaseName");
    const collection = database.collection("yourCollectionName");
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
