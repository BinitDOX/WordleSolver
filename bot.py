import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.firefox.options import Options


class WordleSolverBot:
    def __init__(self, url="https://wordleunlimited.org/", clear_cookies=True,
                 word_length=5, max_chances=6, profile_dir="/Users/bits/Desktop/Wordle/firefox_profile"):
        self.url = url
        self.profile_dir = profile_dir
        self.clear_cookies = clear_cookies
        self.chance = 1
        self.driver = self.setup_driver()
        self.main_element = self.get_main_element()
        self.wordle_rows = self.get_game_board_rows()
        self.word_length = word_length
        self.max_chances = max_chances

    def setup_driver(self):
        options = Options()
        options.add_argument("-profile")
        options.add_argument(self.profile_dir)
        return webdriver.Firefox(options=options)

    def get_main_element(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(30)

        if self.clear_cookies:
            self.driver.delete_all_cookies()

        return self.driver.find_element("xpath", "//body[@class='nightmode']")

    def get_game_board_rows(self):
        host_element = self.driver.find_element("xpath", "//game-app")
        shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", host_element)

        board_element = shadow_root.find_element("css selector", "div#board")
        board_rows = board_element.find_elements("xpath", "./*")

        return board_rows

    def reset(self):
        self.chance = 1

        self.main_element = self.get_main_element()
        self.wordle_rows = self.get_game_board_rows()

    def input_guess_word(self, word):
        if self.chance > self.max_chances:
            raise RuntimeError("Max tries exceeded, please call reset")

        if len(word) != self.word_length or not word.isalpha():
            raise RuntimeError(f"Word must be of {self.word_length} letter alphabets")

        current_row = self.wordle_rows[self.chance - 1]
        self.main_element.send_keys(word)

        row_letters = current_row.get_attribute('letters')
        if row_letters.upper() != word.upper():
            self.main_element.send_keys(Keys.BACKSPACE * self.word_length)
            raise RuntimeError(f"Input out of sync: Input=[{row_letters.upper()}] Guess=[{word.upper()}]")

        self.main_element.send_keys(Keys.ENTER)

        if current_row.get_attribute('invalid') == '':
            self.main_element.send_keys(Keys.BACKSPACE * self.word_length)
            return "INVALID"

        result = ""
        row_shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', current_row)
        tile_elements = row_shadow_root.find_elements("css selector", "game-tile")

        for tile, g_letter in zip(tile_elements, word):
            letter = tile.get_attribute('letter')
            evaluation = tile.get_attribute('evaluation')
            reveal = tile.get_attribute('reveal')

            if letter.upper() != g_letter.upper():
                raise RuntimeError(f"Input out of sync: Input=[{letter.upper()}] Guess=[{g_letter.upper()}]")

            result += 'G' if evaluation == 'correct' else 'Y' if evaluation == 'present' else 'B'

        self.chance += 1

        time.sleep(4.5)
        return result
