"""Class for generating new puzzles"""
import logging
from random import randint, shuffle, seed

from .puzzle import Puzzle
from .solver import Solver
from .exceptions import InvalidPuzzleError, EmptyCheckpointer

logger = logging.getLogger(__name__)

# TODO docs
# TODO add to readme
class Generator:
    """"""

    # TODO docs
    def __init__(
        self,
        order: int = 3,
        max_attempts: int = 10000,
        max_solver_loops: int = 10000,
        difficulty: float = 0.6,
    ):
        """"""
        assert order in [2, 3], "Can only generate order 2 or order 3 puzzles."
        self.order = order
        self.total_elements = order**4

        assert max_attempts > 0, "Max attempts should be larger than 0."
        assert max_solver_loops > 0, "Max iterations should be larger than 0."
        self.max_attempts = max_attempts
        self.solver = Solver(max_loops=max_solver_loops)

        assert 0 < difficulty < 1, ""  # TODO
        self.difficulty = difficulty

        # random_fraction = 1 / (1 + 5 ** (0.5))
        random_fraction = 0.05
        self.n_randoms = random_fraction * self.total_elements

    # TODO docs
    def spawn(self, rng_seed: int = 12345) -> Puzzle:
        """"""
        random_puzzle = []  # TODO handle possibly unbound more elegantly
        for attempt in range(self.max_attempts):
            logger.error("attempt %d", attempt)

            try:
                random_puzzle = self._generate_random_puzzle(rng_seed)
            except InvalidPuzzleError:
                continue

            try:
                random_puzzle = self.solver(random_puzzle)
            except EmptyCheckpointer:
                continue

            if not random_puzzle.is_solved():
                continue
            break

        if len(random_puzzle) == 0:
            raise InvalidPuzzleError  # TODO replace with warning?

        mask = [
            0 if i <= int(self.total_elements * self.difficulty) else 1
            for i in range(self.total_elements)
        ]
        shuffle(mask)
        random_puzzle.data = [e * m for e, m in zip(random_puzzle.data, mask)]
        return random_puzzle

    def _generate_random_puzzle(self, rng_seed: int) -> Puzzle:
        seed(rng_seed)
        random_input = [
            randint(1, self.order**2) if i <= self.n_randoms else 0
            for i in range(self.total_elements)
        ]
        shuffle(random_input)
        return Puzzle(random_input)
