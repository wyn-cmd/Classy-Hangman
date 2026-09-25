# Hangman game implementation using standard library tools

import csv
import random

# Core game logic for Hangman
class Hangman:
    def __init__(self, word_list, max_attempts):
        self.__word = random.choice(word_list).lower()
        self.__max_attempts = max_attempts
        self.__attempts_left = max_attempts
        self.__guessed_letters = set()
    
    def guess_letter(self, letter):
        letter = letter.lower()
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
        return self.__attempts_left <= 0 or all(letter in self.__guessed_letters for letter in self.__word)
    
    def get_masked_word(self):
        return "".join(
            char if char in self.__guessed_letters else "_" 
            for char in self.__word
        )
    
    def get_attempts_left(self):
        return self.__attempts_left
    
    def get_word(self):
        return self.__word


# Extracts a list of words from a specified column in a CSV file.
def get_words_from_csv(file_path, column_index):
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            words = []
            for row in csvreader:
                if len(row) > column_index:
                    for word in row[column_index].split():
                        words.append(word.strip())
            return [w for w in words if w]
    except FileNotFoundError:
        print(f"Warning: Could not find file {file_path}. Using fallback word list.")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}. Using fallback word list.")
        return []


if __name__ == "__main__":
    file_path = 'word_list.txt'
    column_index = 2
    word_list = get_words_from_csv(file_path, column_index) or ["python", "programming", "cyber"]

    game = Hangman(word_list, max_attempts=6)

    while not game.is_game_over():
        print(game.get_masked_word())
        print(f"Attempts left: {game.get_attempts_left()}")
        
        try:
            letter = input("Enter a letter: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGame interrupted. Exiting.")
            break
            
        if len(letter) != 1 or not letter.isalpha():
            print("Enter a single letter.")
            continue
            
        game.guess_letter(letter)

    if game.is_game_over():
        print(f"The word was: {game.get_word()}")
        if game.get_attempts_left() > 0:
            print("Congratulations! You guessed the word correctly.")
        else:
            print("Game over! You ran out of attempts.")