import csv
import random

# Hangman game logic.
class Hangman:
    def __init__(self, word_list, max_attempts):
        self._word = random.choice(word_list).lower()
        self._max_attempts = max_attempts
        self._attempts_left = max_attempts
        self._guessed_letters = set()
    
    def guess_letter(self, letter):
        letter = letter.lower()
        if letter in self._guessed_letters:
            print(f"You've already guessed '{letter}'. Guess another letter.")
            return
        
        self._guessed_letters.add(letter)
        
        if letter in self._word:
            print(f"Good guess: '{letter}' is in the word!")
        else:
            print(f"Bad luck: '{letter}' is not in the word.")
            self._attempts_left -= 1
    
    def is_game_over(self):
        return self._attempts_left <= 0 or all(char in self._guessed_letters for char in self._word)
    
    @property
    def masked_word(self):
        return "".join(char if char in self._guessed_letters else "_" for char in self._word)
    
    @property
    def attempts_left(self):
        return self._attempts_left
    
    @property
    def word(self):
        return self._word


# Load words from a specific CSV column.
def get_words_from_csv(file_path, column_index):
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            words = []
            for row in reader:
                if len(row) > column_index:
                    words.extend(row[column_index].split())
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
        print(game.masked_word)
        print(f"Attempts left: {game.attempts_left}")
        
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
        print(f"The word was: {game.word}")
        if game.attempts_left > 0:
            print("Congratulations! You guessed the word correctly.")
        else:
            print("Game over! You ran out of attempts.")