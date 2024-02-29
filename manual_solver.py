from solver import WordleSolverLogic
from data_loader import WordDataset
from solverhelper import WordleSolverHelper

words = WordDataset().words
helper = WordleSolverHelper(word_list=words)
solver = WordleSolverLogic(helper)

print("---------SUGGESTION ----------> ")
print(solver.get_next_guess())

while True:
    guessed_word = input("Guessed word: ")
    result = input("Result: ")
    guessed_word = guessed_word.upper()
    result = result.upper()
    solver.process_result(result, guessed_word)
    if solver.is_guess_correct():
        print("Successfully solved :)")
        break
    print("---------SUGGESTION ----------> ")
    print(solver.get_next_guess())
