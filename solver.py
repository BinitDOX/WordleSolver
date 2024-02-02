class WordleSolverLogic:

    def __init__(self, word_list, n=5):
        self.N = n
        self.n_sets = [set(chr(ord('A') + i) for i in range(26)) for _ in range(n)]

        self.sorted_list = sorted(word_list, key=lambda k: word_list[k], reverse=True)

        self.must_use = []
        self.result = ""
        self.previous_attempt = ""
        self.sorted_list_index = 0

        print("SORTED+LIST = ")
        print(self.sorted_list)

    def greenify(self, index):
        self.n_sets[index] = {self.previous_attempt[index]}

    def blackify(self, index):
        for i in range(self.N):
            if self.previous_attempt[index] in self.n_sets[i]:
                self.n_sets[i].remove(self.previous_attempt[index])

    def yellowify(self, index):
        if self.previous_attempt[index] in self.n_sets[index]:
            self.n_sets[index].remove(self.previous_attempt[index])
        self.must_use.append(self.previous_attempt[index])

    def process_result(self, result_string):
        self.must_use = []
        self.result = result_string

        if self.result == "GGGGG":
            return self.previous_attempt

        for i, char in enumerate(self.result):
            if char == 'B':
                self.blackify(i)
            elif char == 'G':
                self.greenify(i)
            elif char == 'Y':
                self.yellowify(i)

    def is_guess_correct(self):
        return self.result == "GGGGG"

    def check_validity(self, word):
        for i, char in enumerate(word):
            if char not in self.n_sets[i]:
                return False

        # fixme: In all non green places, all mustUse letters must be used with at least as much frequency as in
        #  mustUse list
        for char in self.must_use:
            if char not in word:
                return False

        return True

    def get_next_guess(self):
        if self.previous_attempt == "":
            next_attempt = self.sorted_list[0]
            self.previous_attempt = next_attempt
            self.sorted_list_index = 1
            return next_attempt

        while self.sorted_list_index < len(self.sorted_list):
            word = self.sorted_list[self.sorted_list_index]
            self.sorted_list_index += 1

            if self.check_validity(word):
                self.previous_attempt = word
                return word

        raise RuntimeError("Dictionary ended")
