async function optimizePrompt(prompt) {
  // Optimize the prompt for the GPT-4 model
  console.log("Optimizing prompt");
  try {
    response = await openai.ChatCompletion.create({
      model: "gpt-4-turbo-preview",
      messages: [
        {
          role: "system",
          content: "You are a prompt engineer specialized in dall-e.",
        },
        {
          role: "user",
          content: `Optimize this prompt for dall-e: ${prompt}. Give only the text prompt to use with dall-e, nothing else.`,
        },
      ],
    });
    return response.choices[0].message.content;
  } catch (error) {
    console.log(`An error occurred: ${error}`);
    return null;
  }
}

async function fetchCharacterData(prompt) {
  console.log("Fetching character data");
  try {
    let response = await openai.ChatCompletion.create({
      model: "gpt-4-turbo-preview",
      messages: [
        {
          role: "system",
          content: `You are a RPG character in the world of Forgotten Realms. Write a background story for your character. 
                                Include their upbringing, key events in their life, and their motivations. Conclude the background story 
                                by including a potential adventure hook or a mystery that the character seeks to unravel. 
                                Please write three paragraphs with a total word count of around 300 words. Write output in JSON format.`,
        },
        {
          role: "user",
          content: `${prompt}`,
        },
      ],
    });

    return response.choices[0].message.content;
  } catch (error) {
    console.log(`An error occurred: ${error}`);
    return null;
  }
}

module.exports = { optimizePrompt, fetchCharacterData };
