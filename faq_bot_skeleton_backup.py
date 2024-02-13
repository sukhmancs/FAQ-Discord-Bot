""" This is a very simple skeleton for a FAQ bot, based on the handout given in
class. Your job is to create your own FAQ bot that can answer 20 questions
using basic string matching. See the handout for more details.

When you create your bot you can adapt this code or start from scratch and
write your own code.

If you adapt this code, add yourself below as author and rewrite this header
comment from scratch. Make sure you properly comment all classes, methods
and functions as well. See the Resources folder on Canvas for documentation
standards.

YOUR NAME AND DATE
Sukhmanjeet Singh, Jan 2024
"""
# Import the necessary modules
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from file_input import *

def load_FAQ_data():
    """This method returns a list of questions and answers. The
    lists are parallel, meaning that intent n pairs with response n."""

    questions = file_input("questions.txt")
    answers = file_input("answers.txt")

    return questions, answers

def understand_with_cosine_similarity(utterance):
    """This method processes an utterance to determine which intent it
    matches. The index of the intent is returned, or -1 if no intent
    is found."""

    global intents # declare that we will use a global variable

    try:
        # Create a TF-IDF vectorizer and fit it on the intents
        vectorizer = TfidfVectorizer().fit(intents)

        # Transform the utterance and intents into TF-IDF vectors
        utterance_vector = vectorizer.transform([utterance])
        intents_vectors = vectorizer.transform(intents)

        # Compute the cosine similarity between the utterance vector and each intent vector
        similarities = cosine_similarity(utterance_vector, intents_vectors)

        # Find the index of the intent with the highest similarity to the utterance
        best_match_index = similarities.argmax()

        # If the highest similarity is 0, then no intent was found
        if similarities[0, best_match_index] == 0:
            return -1

        return best_match_index
    except ValueError:
        return -1

def understand(utterance):
    """This method processes an utterance to determine which intent it
    matches. The index of the intent is returned, or -1 if no intent
    is found."""

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
    """This function returns an appropriate response given a user's
    intent."""

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
    while True:
        utterance = input(">>> ")
        if utterance == "goodbye":
            break;
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