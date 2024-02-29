from data_loader import WordDataset
from ksolver import KSolver

n_final = 5
k_final = 4

words = WordDataset().words
ksolver = KSolver(word_list=words, n=n_final, k=k_final)

print("---------SUGGESTION ----------> ")
print(ksolver.get_next_guess())

while True:
    guessed_word = input("Guessed word: ")
    result_strings = list()
    for index in range(k_final):
        if not ksolver.is_solved[index]:
            result = input(f"Result string {index + 1}: ")
            result_strings.append(result.upper())
        else:
            result_strings.append("G" * n_final)
    guessed_word = guessed_word.upper()
    ksolver.process_results(result_strings, guessed_word)
    if ksolver.is_game_over():
        print("Game Over :)")
        break
    print("---------SUGGESTION ----------> ")
    print(ksolver.get_next_guess())
