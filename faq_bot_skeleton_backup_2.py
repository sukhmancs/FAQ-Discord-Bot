"""
This is a very simple skeleton for a FAQ bot. This bot answer 20 questions using basic string matching.

Author:
    Sukhmanjeet Singh
Date:
    Jan 2024
"""
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
    questions = file_input("questions.txt")
    answers = file_input("answers.txt")

    return questions, answers

def understand(utterance):
    """
    This method processes an utterance to determine which intent it
    matches. The index of the intent is returned, or -1 if no intent
    is found.

    Args:
        utterance (str): The user's input.

    Returns:
        int: The index of the intent that best matches the user's input.
    """

    global intents # declare that we will use a global variable

    limit = 1 # the minimum number of matching words needed to be considered a match

    try:
        # Convert the utterance to lowercase and split it into words
        utterance_words = utterance.lower().split()

        # Initialize a list to keep track of the number of matching words for each intent
        matching_words_counts = []

        # For each intent in the list of intents
        for intent in intents:
            # Convert the intent to lowercase and split it into words
            intent_words = intent.lower().split()

            # Count the number of words from the utterance that are in the intent words
            matching_words_count = sum(word in intent_words for word in utterance_words)

            # Add the count to the list
            matching_words_counts.append(matching_words_count)

        # Find the maximum number of matching words
        max_matching_words = max(matching_words_counts)

        # If the maximum number of matching words is less than the limit, return -1
        if max_matching_words < limit:
            return -1

        # Otherwise, return the index of the first intent with the maximum number of matching words
        return matching_words_counts.index(max_matching_words)
    except ValueError:
        return -1

def generate(intent):
    """
    This function returns an appropriate response given a user's
    intent.

    Args:
        intent (int): The index of the intent that best matches the user's input.

    Returns:
        str: The response to the user's input.
    """

    global responses # declare that we will use a global variable

    if intent == -1:
        return "Sorry, I don't know the answer to that!"

    return responses[intent]

## Load the questions and responses
intents, responses = load_FAQ_data()

## Main Function

def main():
    """Implements a chat session in the shell."""
    print("Hello! I know stuff about chat bots. When you're done talking, just say 'goodbye'.")
    print()
    utterance = ""
    while True:  # Loop forever until the user says "goodbye"
        utterance = input(">>> ")
        if utterance == "hello":
            print("Hi! Nice to meet you!")
            continue;  # Skip the rest of the loop and start over

        if utterance == "goodbye":
            break;     # Exit the loop
        intent = understand(utterance)
        response = generate(intent)
        print(response)
        print()

    print("Nice talking to you!")

## Run the chat code
# the if statement checks whether or not this module is being run
# as a standalone module. If it is beign imported, the if condition
# will be false and it will not run the chat method.
if __name__ == "__main__":
    main()