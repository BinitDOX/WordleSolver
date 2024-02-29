from solver import WordleSolverLogic
from solverhelper import WordleSolverHelper


class KSolver:

    def __init__(self, word_list, n=5, k=4):
        self.N = n
        self.K = k
        self.is_solved = [False] * k
        helper = WordleSolverHelper(word_list)
        self.solver_instances = [WordleSolverLogic(helper, n) for _ in range(k)]

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

    def get_next_guess(self, first_guess="STARE"):
        return self.get_next_unsolved_instance().get_next_guess(first_guess)

    def is_game_over(self):
        return all(self.is_solved)
