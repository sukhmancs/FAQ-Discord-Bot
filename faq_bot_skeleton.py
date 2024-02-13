import re
import spacy
from fuzzywuzzy import fuzz

# Load English language model for spaCy
nlp = spacy.load("en_core_web_sm")

# Import the necessary modules
from file_input import *

def load_FAQ_data():
    """This method returns a list of questions and answers. The
    lists are parallel, meaning that intent n pairs with response n."""

    # Sources:
    # https://en.wikipedia.org/wiki/International_Space_Station
    # https://science.nasa.gov/mission/hubble/
    # https://www.nasa.gov/specials/artemis/
    # https://webbtelescope.org/home
    # questions = file_input("questions.txt")

    # Load regex patterns from file
    regex_list = file_input("regular_expressions.txt")
    answers = file_input("answers.txt")

    return regex_list, answers

# Function to match intent using fuzzy regular expressions
def generate(utterance):
    """
    This function matches the user's utterance with the best response
    using fuzzy regular expressions. It returns the best response
    if the score is above the threshold, else it returns None.

    Args:
        utterance (str): The user's input.
    
    Returns:
        str: The best response if the score is above the threshold, else None.    
    """

    best_match = None
    best_score = float('-inf')

    # Global variables to access the regex patterns and responses
    global responses
    global regex_list

    for regex, answer in zip(regex_list, responses):
        #regex = r"(purpose|goals).*(International Space Station|ISS)"
        score = fuzz.ratio(regex.lower(), utterance.lower())  # Use the ratio function for approximate pattern matching
        if score > best_score:
            best_match = answer
            best_score = score

    # If the best score is below the threshold, return None
    if best_score < 50:
        return None

    return best_match # Else, return the best match

# Function to classify speech act
def classify_speech_act(utterance):
    """
    This function classifies the user's utterance into one of three
    categories: question, command, or statement. It returns the
    classified speech act.

    Args:
        utterance (str): The user's input.
    
    Returns:
        str: The classified speech act.    
    """

    utterance = utterance.lower()
    doc = nlp(utterance)
    speech_act = None
    question_text = ["is", "are", "who", "what", "where", "when", "why", "how", "?"]
    command_text = ["please", "could", "would"]

    # Check if the user input is a question
    if any((token.pos_ == "AUX" and token.dep_ == "aux") or
           (token.text in question_text) for token in doc):
        speech_act = "question"
    # Check if the user input is a command
    elif any((token.pos_ == "VERB" and token.dep_ == "ROOT") or
             (token.text in command_text) for token in doc):
        speech_act = "command"
    # Default to statement
    else:
        speech_act = "statement"

    return speech_act

# Function to perform named entity recognition (NER) and provide appropriate response
def perform_ner(utterance):
    """
    This function performs Named Entity Recognition (NER) on the user's
    utterance and provides an appropriate response based on the named
    entities found. It returns the response to the user's input.

    Args:
        utterance (str): The user's input.
    
    Returns:
        str: The response to the user's input.
    """

    utterance = utterance.lower()
    doc = nlp(utterance)
    named_entities = [ent.text for ent in doc.ents] # Extract named entities from user input
    response = None # Initialize response

    # If no named entities are found, use nouns and proper nouns
    if not named_entities:
        named_entities = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]

    if named_entities:
        for entity in named_entities:
            # Check entity label and provide response accordingly
            if "ORG" in [ent.label_ for ent in doc.ents]:
                response = "Sorry, I don't know. I don't work for " + entity
                print(response)
            elif "GPE" in [ent.label_ for ent in doc.ents]:
                response = "Sorry, I don't know. I've never been to " + entity
                print(response)
            elif "PERSON" in [ent.label_ for ent in doc.ents]:
                response = "Sorry, I don't know who " + entity + " is."
                print(response)
            elif "DATE" in [ent.label_ for ent in doc.ents]:
                response = "Sorry, I don't know what happened on " + entity
                print(response)
            elif "MONEY" in [ent.label_ for ent in doc.ents]:
                response = "Sorry, I don't know anything about " + entity + " money."
                print(response)
            elif "TIME" in [ent.label_ for ent in doc.ents]:
                response = "Sorry, I don't know what happened at " + entity
                print(response)
            elif "PRODUCT" in [ent.label_ for ent in doc.ents]:
                response = "Sorry, I don't know anything about " + entity
                print(response)
            else:
                response = "Sorry, I don't know anything about " + entity
                print(response)
            return response # Return after the first named entity is processed
    else:
        response = handle_assistant_functions(utterance) # If no named entities are found, handle automated assistant functions

    return response # Return the response

# Function to handle automated assistant functions
def handle_assistant_functions(utterance):
    """
    This function handles automated assistant functions based on the
    user's input and provides an appropriate response. It returns the
    response to the user's input.

    Args:
        utterance (str): The user's input.
    
    Returns:
        str: The response to the user's input.
    """

    utterance = utterance.lower()
    response = None # Initialize response

    if re.search(r'(search|find|give me|google)\s+(.*)', utterance):
        # Extract search query from user input
        query = re.search(r'(search|find|give me|google)\s+(.*)', utterance).group(1)
        # Perform a web search using the default browser
        search_result = "https://www.google.com/search?q=" + query.replace(" ", "+")
        response = "You can find the search results for " + query + " on this link: " + search_result
        print(response)
    elif re.search(r'(wikipedia|info about)\s+(.*)', utterance):
        # Extract search query from user input
        query = re.search(r'(wikipedia|info about)\s+(.*)', utterance).group(1)
        # Search for the query on Wikipedia
        wiki_result = "https://en.wikipedia.org/wiki/" + query.replace(" ", "_")
        response = "You can find the Wikipedia page for " + query + " on this link: " + wiki_result
        print(response)
    elif re.search(r'(youtube|video)\s+(.*)', utterance):
        # Extract search query from user input
        query = re.search(r'(youtube|video)\s+(.*)', utterance).group(1)
        # Search for the query on YouTube
        youtube_result = "https://www.youtube.com/results?search_query=" + query.replace(" ", "+")
        response = "You can find the YouTube search results for " + query + " on this link: " + youtube_result
        print(response)
    elif re.search(r'(news|latest|update)\s+(.*)', utterance):
        # Extract search query from user input
        query = re.search(r'(news|latest|update)\s+(.*)', utterance).group(1)
        # Search for the query on Google News
        news_result = "https://news.google.com/search?q=" + query.replace(" ", "+")
        response = "You can find the latest news articles for " + query + " on this link: " + news_result
        print(response)
    elif re.search(r'(weather|forecast)\s+(.*)', utterance):
        # Extract location from user input
        query = re.search(r'(weather|forecast)\s+(.*)', utterance).group(1)
        # Search for the weather forecast for the location
        weather_result = "https://www.google.com/search?q=weather+forecast+" + query.replace(" ", "+")
        response = "You can find the weather forecast for " + query + " on this link: " + weather_result
        print(response)
    elif re.search(r'(map|directions|drive me)\s+(.*)', utterance):
        # Extract location from user input
        query = re.search(r'(map|directions|drive me)\s+(.*)', utterance).group(1)
        # Search for the map and directions to the location
        location_result = "https://www.google.com/maps/search/" + query.replace(" ", "+")
        response = "You can find the map and directions to " + query + " on this link: " + location_result
        print(response)
    elif re.search(r'(calculate|math|solve)\s+(.*)', utterance):
        # Extract math expression from user input
        query = re.search(r'(calculate|math|solve)\s+(.*)', utterance).group(1)
        # give bot the ability to do website that point to a calculator
        calculator_result = "https://www.google.com/search?q=" + query.replace(" ", "+")
        response = "You can find the calculator for " + query + " on this link: " + calculator_result
        print(response)
    elif re.search(r'(tell me|get me).*(something|useful).*(information|interesting|fun|worth|important).*', utterance):
        response = "Did you know that the first computer was invented in the 1940s?"
        print(response)
    elif re.search(r'do(n’t|not) say.*(i|you) don’t know.*', utterance):
        response = "Understood. I'll do my best to provide useful information."
        print(response)
    else:
        response = "Sorry, I don't know how to help with that."
        print(response)

    return response # Return the response

## Load the questions and responses
regex_list, responses = load_FAQ_data()

# Main function to handle user interaction
def main():
    """Implements a chat session in the shell."""
    print("Welcome to the FAQ Bot Plus!")
    while True:
        utterance = input("You: ")

        # Handle greetings
        if utterance.lower() in ["hello", "hi", "hey"]:
            print("Bot: Hello! How can I help you?")
            continue
        # Handle goodbyes
        elif utterance.lower() in ["goodbye", "bye", "quit"]:
            print("Bot: Goodbye!")
            break

        # Match intent using fuzzy regular expressions
        response = generate(utterance)

        # Set default response
        default_response = "Sorry, I was unable to find the answer to that."

        # Provide response if it is not the default response
        if response is not default_response:
            print("Bot:", response)
        else: # If the response is the default response
            # Classify speech act
            speech_act = classify_speech_act(utterance)
            if speech_act == "question":
                # Perform Named Entity Recognition (NER) and provide appropriate response
                perform_ner(utterance)
            elif speech_act == "command":
                # Handle automated assistant functions
                handle_assistant_functions(utterance)
            else:
                print("Bot: Sorry, I didn't understand that.")

if __name__ == "__main__":
    main()
