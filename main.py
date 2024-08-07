import csv
import random

class Hangman:
    def __init__(self, word_list, max_attempts):
        self.__word = random.choice(word_list).lower()  # Select a random word from word_list
        self.__max_attempts = max_attempts
        self.__attempts_left = max_attempts
        self.__guessed_letters = set()
    
    def guess_letter(self, letter):
        letter = letter.lower()  # Convert input to lowercase
        if letter in self.__guessed_letters:
            print(f"You've already guessed '{letter}'. Guess another letter.")
            return
        
        self.__guessed_letters.add(letter)
        
        if letter in self.__word:
            print(f"Good guess: '{letter}' is in the word!")
        else:
            print(f"Bad luck: '{letter}' is not in the word.")
            self.__attempts_left -= 1
    
    def is_game_over(self):
        if self.__attempts_left <= 0:
            return True
        if all(letter in self.__guessed_letters for letter in self.__word):
            return True
        return False
    
    def get_masked_word(self):
        masked_word = ""
        for char in self.__word:
            if char in self.__guessed_letters:
                masked_word += char
            else:
                masked_word += "_"
        return masked_word
    
    def get_attempts_left(self):
        return self.__attempts_left



def get_words_from_csv(file_path, column_index):
  """
  Extracts a list of words from a specified column in a CSV file.

  Args:
    file_path: The path to the CSV file.
    column_index: The index of the column containing the words (0-based).

  Returns:
    A list of words extracted from the specified column.
  """

  words = []
  with open(file_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
      words.extend(row[column_index].split())  # Assuming words are separated by spaces

  return words

# Example usage:
file_path = 'word_list.txt'
column_index = 2  # Adjust based on your column containing words
word_list = get_words_from_csv(file_path, column_index)
print(word_list)


# Create an instance of the Hangman class
word_list = ["python", "programming", "cyber"]
game = Hangman(word_list, max_attempts=6)

# Play the game
while not game.is_game_over():
    print(game.get_masked_word())
    print(f"Attempts left: {game.get_attempts_left()}")
    letter = input("Enter a letter: ")
    game.guess_letter(letter)

# Print the game result
if game.get_attempts_left() > 0:
    print("Congratulations! You guessed the word correctly.")
else:
    print("Game over! You ran out of attempts.")
