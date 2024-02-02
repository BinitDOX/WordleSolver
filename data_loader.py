import json


class WordDataset:
    def __init__(self, filename='word_frequency.json'):
        self.filename = filename
        self.words = self.extract_words_from_dataset()

    def extract_words_from_dataset(self):
        with open(self.filename, 'r') as file:
            word_frequency_data = json.load(file)

        return {
            word: frequency
            for word, frequency in word_frequency_data.items()
            if len(word) == 5 and word.isalpha()
        }
