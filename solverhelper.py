class WordleSolverHelper:

    def __init__(self, word_list):
        self.sorted_list = sorted(word_list, key=lambda k: word_list[k], reverse=True)
        self.previous_attempt = ""

        print("----------------SORTED LIST-------------")
        print(self.sorted_list)
