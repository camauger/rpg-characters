const { writeFile } = require('fs').promises;

exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const { email } = JSON.parse(event.body);
  const data = { subscribers: [email] }; // Simplified for example

  try {
    await writeFile('subscribers.json', JSON.stringify(data, null, 2), 'utf8');
    return {
      statusCode: 200,
      body: JSON.stringify({ message: "Subscription successful" }),
    };
  } catch (e) {
    console.error(e);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Failed to subscribe" }),
    };
  }
};
