"""
This is a very simple script to put the FAQ bot skeleton code on line
as a discord bot.

Author:
    Sukhmanjeet Singh
Date:
    February 2024
"""

import discord
from faq_bot_skeleton import *

## MYClient Class Definition

class MyClient(discord.Client):
    """This is the client class for the bot. It inherits from the
    discord.Client class."""

    def __init__(self):
        """This is the constructor. Sets the default 'intents' for the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)

    async def on_message(self, message):
        """
        This is the main function that processes the incoming message and
        generates a response. It uses the 'understand' and 'generate' functions
        from the faq_bot_skeleton.py file to process the incoming message and
        generate a response.

        Args:
            message (discord.Message): The incoming message.
        """

        # don't respond to ourselves
        if message.author == self.user:
            return

        # get the utterance and generate the response
        utterance = message.content

        # Handle greetings
        if utterance.lower() in ["hello", "hi", "hey"]:
            # send the response
            await message.channel.send("Hello! How can I help you?")
            return # wait for the next user message
        # Handle goodbyes
        elif utterance.lower() in ["goodbye", "bye", "quit"]:
            # send the response
            await message.channel.send("Goodbye!")
            return # wait for the next user message

        # Handle intent using fuzzy regular expressions
        response = generate(utterance)

        # Provide response if it is not the default response
        if response:
            # send the response
            await message.channel.send(response)
        else: # If the response is the default response
            # Classify speech act
            speech_act = classify_speech_act(utterance)
            if speech_act == "question":
                # Perform Named Entity Recognition (NER) and provide appropriate response
                response = perform_ner(utterance)
                # send the response
                await message.channel.send(response)
            elif speech_act == "command":
                # Handle automated assistant functions
                response = handle_assistant_functions(utterance)
                # send the response
                await message.channel.send(response)
            else:
                response = "Sorry, I didn't understand that."
                # send the response
                await message.channel.send(response)

## Set up and log in
client = MyClient()
with open("bot_token.txt") as file:
    token = file.read()
client.run(token)