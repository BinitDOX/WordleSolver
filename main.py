from bot import WordleSolverBot
from solver import WordleSolverLogic
from data_loader import WordDataset


def main():
    bot = WordleSolverBot()
    words = WordDataset().words
    solver = WordleSolverLogic(words=words)

    # Main game loop
    try:
        while True:
            while bot.chance <= bot.max_chances:
                word_to_guess = solver.get_next_guess()
                result = bot.guess_word(word_to_guess)
                solver.process_result(result)

                # Print or log the result
                print(f"[+] Attempt=[{bot.chance - 1}] Guessed=[{word_to_guess}] Result=[{result}]")

                if solver.is_guess_correct(result):
                    print(f"[+] Successfully solved :)")
                    break

                input("[*] Press Enter to continue...")

            print("[-] Failed to solve, max chances reached :(")
            input("[*] Press Enter to reset...")

    except KeyboardInterrupt:
        print("[+] Received Ctrl+C event, stopping")
    finally:
        bot.driver.close()


if __name__ == "__main__":
    main()
