import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.firefox.options import Options


class KWordleSolverBot:
    def __init__(self, url="https://www.merriam-webster.com/games/quordle/#/practice", max_chances=9,
                 word_length=5, game_boards=4, profile_dir='./firefox_profile'):
        self.url = url
        self.game_boards = game_boards
        self.chance = 1
        self.max_chances = max_chances
        self.word_length = word_length
        self.profile_dir = profile_dir
        self.driver = self.setup_driver()
        self.initialize_driver()
        self.main_element = self.get_main_element()

    def setup_driver(self):
        options = Options()
        options.add_argument("-profile")
        options.add_argument(self.profile_dir)
        return webdriver.Firefox()

    def initialize_driver(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(30)

    def get_main_element(self):
        return self.driver.find_element("xpath", "//body")

    def get_result_string_for_board_row(self, game_board_number, row_number):
        cells = self.driver.find_elements("xpath", f"//div[@aria-label='Game Board {game_board_number}']/div[{row_number}]/div")
        result_string = ''.join([
            'B' if 'incorrect' in cell.get_attribute('aria-label')
            else 'Y' if 'different' in cell.get_attribute('aria-label')
            else 'G' if 'correct' in cell.get_attribute('aria-label')
            else 'I'
            for cell in cells
        ])
        return result_string

    def reset(self):
        self.chance = 1
        self.main_element = self.get_main_element()

    def input_guess_word(self, word):
        if self.chance > self.max_chances:
            raise RuntimeError("Max tries exceeded, please call reset")

        if len(word) != self.word_length or not word.isalpha():
            raise RuntimeError(f"Word must be of {self.word_length} letter alphabets")

        self.main_element.send_keys(word)
        self.main_element.send_keys(Keys.ENTER)

        time.sleep(0.2)
        result_strings = [self.get_result_string_for_board_row(board, self.chance) for board in range(1, self.game_boards+1)]

        if all([rs == 'I'*self.word_length for rs in result_strings]):
            self.main_element.send_keys(Keys.BACKSPACE * self.word_length)
        else:
            self.chance += 1

        return result_strings
