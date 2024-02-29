class WordleSolverLogic:

    def __init__(self, helper, n=5):
        self.N = n
        self.n_sets = [set(chr(ord('A') + i) for i in range(26)) for _ in range(n)]
        self.must_use = []
        self.result = ""
        self.helper = helper
        self.sorted_list_index = 0
        self.is_guess_fixed = [False] * self.N

    def greenify(self, index):
        self.n_sets[index] = {self.helper.previous_attempt[index]}

    def blackify(self, index):
        def check_if_letter_all_black(letter):
            return all(self.result[_i] == 'B' for _i, char in enumerate(self.helper.previous_attempt) if char == letter)

        current_letter = self.helper.previous_attempt[index]
        if check_if_letter_all_black(current_letter):
            for i in range(self.N):
                if current_letter in self.n_sets[i]:
                    self.n_sets[i].remove(current_letter)
        else:
            # TODO: must not use this letter for more than number of yellows+green of that letter in complete word ever
            if current_letter in self.n_sets[index]:
                self.n_sets[index].remove(current_letter)

    def yellowify(self, index):
        current_letter = self.helper.previous_attempt[index]
        if current_letter in self.n_sets[index]:
            self.n_sets[index].remove(current_letter)

        def will_come_at_fixed_place(letter):
            return any((self.is_guess_fixed_at_index(i)) and (letter in self.n_sets[i]) and
                       (self.helper.previous_attempt[i] != letter) for i in range(self.N))
        if not will_come_at_fixed_place(current_letter):
            self.must_use.append(current_letter)

    def process_result(self, result_string, guessed_word):
        if result_string == "INVALID":
            return

        def is_letter_fixed_at_index(index):
            return len(self.n_sets[index]) == 1

        self.is_guess_fixed = list()
        for i in range(self.N):
            self.is_guess_fixed.append(is_letter_fixed_at_index(i))

        if guessed_word != self.helper.previous_attempt:
            self.helper.previous_attempt = guessed_word
            if self.sorted_list_index != 0:
                self.sorted_list_index -= 1

        self.result = result_string

        for i in range(self.N):
            if self.helper.previous_attempt[i] in self.must_use:
                self.must_use.remove(self.helper.previous_attempt[i])

        for i, char in enumerate(self.result):
            if char == 'B':
                self.blackify(i)
            elif char == 'G':
                self.greenify(i)
            elif char == 'Y':
                self.yellowify(i)

        print("--------------------------")
        print("-------------Must Use--------------")
        print(sorted(self.must_use))
        print("-------------N sets--------------")
        for i in range(self.N):
            print(sorted(self.n_sets[i]))

    def is_guess_correct(self):
        return self.result == "G" * self.N

    def is_guess_fixed_at_index(self, i):
        return self.is_guess_fixed[i]

    def get_next_guess(self, first_guess="STARE"):
        def check_validity(possible_word):
            for i, char in enumerate(possible_word):
                if char not in self.n_sets[i]:
                    return False

            temp_must_use = self.must_use.copy()
            for i in range(self.N):
                if (not self.is_guess_fixed_at_index(i)) and possible_word[i] in temp_must_use:
                    temp_must_use.remove(possible_word[i])
            if len(temp_must_use) != 0:
                return False

            return True

        # only first time
        if self.helper.previous_attempt == "":
            next_attempt = first_guess
            self.helper.previous_attempt = next_attempt
            return next_attempt

        while self.sorted_list_index < len(self.helper.sorted_list):
            word = self.helper.sorted_list[self.sorted_list_index]
            self.sorted_list_index += 1
            if check_validity(word):
                self.helper.previous_attempt = word
                return word

        print("!!!!!!!!!!!!--------------- DICTIONARY ENDED ----------------!!!!!!!!!!!!")
        return first_guess
