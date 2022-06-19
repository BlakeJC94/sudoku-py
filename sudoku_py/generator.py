"""Class for generating new puzzles"""
import logging
from random import randint, shuffle, seed
from typing import Optional

from .puzzle import Puzzle
from .solver import Solver
from .exceptions import InvalidPuzzleError, EmptyCheckpointer

logger = logging.getLogger(__name__)


class Generator:
    """"""

    def __init__(
        self,
        order: int = 3,
        difficulty: int = 5,
        max_attempts: int = 10000,
        max_solver_loops: int = 10000,
    ):
        """Constructor.

        Args:
            order: Order of puzzles to generate (2 or 3 supported).
            difficulty: An integer between 1 (very easy) and 5 (very hard) controlling the number
                of empty cells in generated puzzles.
            max_attempts: Number of random seeds to attempt.
            max_solver_loops: Maximum number of solver loops top use for a random seed.
        """
        assert order in [2, 3], "Can only generate order 2 or order 3 puzzles."
        self.order = int(order)
        self.total_elements = int(order) ** 4

        # random_fraction = 0.05
        random_fraction = 1 / (4 * (1 + 5 ** (0.5)))
        self.initial_elements = random_fraction * self.total_elements

        assert (
            1 <= difficulty <= 5
        ), "A value between 1 and 5 expected for `difficulty`."
        self.generated_elements = int(6 - (difficulty)) / 6 * self.total_elements

        assert max_attempts > 0, "Max attempts should be larger than 0."
        self.max_attempts = max_attempts

        assert max_solver_loops > 0, "Max iterations should be larger than 0."
        self.solver = Solver(max_loops=max_solver_loops)

    def spawn(self, rng_seed: Optional[int] = None) -> Puzzle:
        """Generate a random puzzle.

        Args:
            rng_seed: Sets the random number generator state if provided.

        Returns:
            A random sudoku puzzle with a proportion of the cells emptied according to selected
            difficulty.
        """
        if rng_seed is not None:
            seed(rng_seed)

        random_puzzle = []  # TODO handle possibly unbound more elegantly
        for attempt in range(self.max_attempts):
            logger.info("attempt %d", attempt)

            try:
                random_puzzle = self._generate_random_puzzle()
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
            raise InvalidPuzzleError(
                "Unable to generate puzzle. Try increaing `max_attempts`."
            )

        mask = [
            1 if i <= int(self.generated_elements) else 0
            for i in range(self.total_elements)
        ]
        shuffle(mask)
        random_puzzle.data = [e * m for e, m in zip(random_puzzle.data, mask)]
        return random_puzzle

    def _generate_random_puzzle(self) -> Puzzle:
        random_input = [
            randint(1, self.order**2) if i <= self.initial_elements else 0
            for i in range(self.total_elements)
        ]
        shuffle(random_input)
        return Puzzle(random_input)
