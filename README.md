<div id="header" align="center">
  <h1>
     🤖 FAQ-Discord-Bot 
  </h1>
</div>

This Discord bot is designed to handle frequently asked questions (FAQs) within your Discord server efficiently. It utilizes Pyzo and Python for implementation, along with Spacy for natural language processing, and advanced regex pattern matching to provide relevant responses.

# Features

   - __FAQ Management:__ The bot is equipped with a database of predefined questions and answers, primarily focusing on space-related topics such as space exploration, telescopes, astronauts, space missions, and NASA.
   - __Dynamic Response:__ Utilizes Spacy pattern matching to differentiate between commands and questions. If a user's input constitutes a question not covered in the FAQ database, the bot adopts a chattier demeanor and generates a suitable response.
   - __Versatile Handling:__ Beyond space-related queries, the bot intelligently redirects users to appropriate resources for other types of inquiries, such as directions or Python tutorials.

# Installation

1. Clone the repository:
   ```bash
    git clone https://github.com/sukhmancs/FAQ-Discord-Bot.git
   ```

2. Set up a Discord bot account and obtain the token.
3. Add the token to the environment variables or directly in the code.

# Usage

1. Run the bot:
    ```bash
    python faq_bot_skeleton.py
    ```

2. Invite the bot to your Discord server.
3. Interact with the bot by asking questions or using predefined commands.

# Configuration

  Modify the `faq_bot_skeleton.py` file to customize bot behavior, such as command prefixes, FAQ database, etc.

# Contributing
Contributions are welcome! If you have suggestions, bug reports, or feature requests, feel free to open an issue or submit a pull request.
