from bot import WordleSolverBot
from solver import WordleSolverLogic
from data_loader import WordDataset
from solverhelper import WordleSolverHelper


def main(wait):
    bot = WordleSolverBot(clear_cookies=True)
    words = WordDataset().words

    # Main game loop
    try:
        while True:
            input("[*] Press Enter to start...")
            bot.reset()
            helper = WordleSolverHelper(word_list=words)
            solver = WordleSolverLogic(helper)

            while bot.chance <= bot.max_chances:
                word_to_guess = solver.get_next_guess()
                result = bot.input_guess_word(word_to_guess)
                solver.process_result(result, word_to_guess)

                print(f"[+] Attempt=[{bot.chance - 1}] Guessed=[{word_to_guess}] Result=[{result}]")

                if solver.is_guess_correct():
                    print(f"[+] Successfully solved :)")
                    break

                if wait:
                    input("[*] Press Enter to continue...")

            if not solver.is_guess_correct:
                print("[-] Failed to solve, max chances reached :(")

    except KeyboardInterrupt:
        print("[+] Received Ctrl+C event, stopping")

    finally:
        bot.driver.close()


if __name__ == "__main__":
    WAIT_FOR_USER_INPUT = False
    main(WAIT_FOR_USER_INPUT)
