import time

from kbot import KWordleSolverBot
from ksolver import KSolver
from solver import WordleSolverLogic
from data_loader import WordDataset
from solverhelper import WordleSolverHelper


def main(wait, slow):
    kbot = KWordleSolverBot()
    words = WordDataset().words
    n_final = 5
    k_final = 4

    # Main game loop
    try:
        while True:
            input("[*] Press Enter to start...")
            kbot.reset()
            ksolver = KSolver(word_list=words, n=n_final, k=k_final)
            time.sleep(1)

            while kbot.chance <= kbot.max_chances:
                word_to_guess = ksolver.get_next_guess()
                result_strings = kbot.input_guess_word(word_to_guess)
                ksolver.process_results(result_strings, word_to_guess)

                print(f"[+] Attempt=[{kbot.chance - 1}] Guessed=[{word_to_guess}] Result=[{result_strings}]")

                if ksolver.is_game_over():
                    print(f"[+] Successfully solved :)")
                    break

                if wait:
                    input("[*] Press Enter to continue...")
                if slow:
                    time.sleep(slow)

            if not ksolver.is_game_over():
                print("[-] Failed to solve, max chances reached :(")

    except KeyboardInterrupt:
        print("[+] Received Ctrl+C event, stopping")

    finally:
        kbot.driver.close()


if __name__ == "__main__":
    WAIT_FOR_USER_INPUT = False
    SLOW_DOWN = 0.25
    main(WAIT_FOR_USER_INPUT, SLOW_DOWN)
