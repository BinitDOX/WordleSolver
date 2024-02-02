from bot import WordleSolverBot
from solver import WordleSolverLogic
from data_loader import WordDataset


def main(wait):
    bot = WordleSolverBot(clear_cookies=True)
    words = WordDataset().words

    # Main game loop
    try:
        while True:
            input("[*] Press Enter to start...")
            bot.reset()
            solver = WordleSolverLogic(word_list=words)

            while bot.chance <= bot.max_chances:
                word_to_guess = solver.get_next_guess()
                result = bot.input_guess_word(word_to_guess)
                solver.process_result(result)

                # Print or log the result
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
