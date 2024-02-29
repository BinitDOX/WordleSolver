from solver import WordleSolverLogic
from solverhelper import WordleSolverHelper


class KSolver:

    def __init__(self, word_list, n=5, k=4):
        self.N = n
        self.K = k
        self.is_solved = [False] * k
        self.helper = WordleSolverHelper(word_list)
        self.solver_instances = [WordleSolverLogic(self.helper, n) for _ in range(k)]

    def process_results(self, result_strings, guessed_word):
        for index, solver_instance in enumerate(self.solver_instances):
            if not self.is_solved[index]:
                if result_strings[index] == "G" * self.N:
                    self.is_solved[index] = True
                solver_instance.process_result(result_strings[index], guessed_word)

    def get_next_unsolved_instance(self):
        for index, value in enumerate(self.is_solved):
            if not value:
                return self.solver_instances[index]
        return self.solver_instances[0]

    def get_most_likely_to_solve_instance(self):
        max_total_possibilities = 0
        instance_index = 0
        for index, val in enumerate(self.is_solved):
            if not val:
                current_total_possibilities = self.solver_instances[index].get_total_qualifying_words()
                if current_total_possibilities > max_total_possibilities:
                    max_total_possibilities = current_total_possibilities
                    instance_index = index
        print("GOING FOR THE INSTANCE: ")
        print(instance_index + 1)
        return self.solver_instances[instance_index]

    def get_next_guess(self, first_guess="STARE"):
        return self.get_most_likely_to_solve_instance().get_next_guess(first_guess)

    def is_game_over(self):
        return all(self.is_solved)
