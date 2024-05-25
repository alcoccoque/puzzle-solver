"""Puzzle generator."""

import random
from typing import List

from .solver import FieldState, PuzzleSolver


class PuzzleGenerator:
    """Generates puzzles."""

    def __init__(self, size: int):
        """Initialize the PuzzleGenerator with a given size."""
        self.size = size

    def generate_puzzle(self, filled_percentage: float) -> List[List[int]]:
        """Generate a puzzle."""
        solved_puzzle = self.solve_puzzle()
        total_cells = self.size * self.size
        filled_cells_count = int(total_cells * filled_percentage)
        filled_cells = [
            (x, y)
            for x in range(self.size)
            for y in range(self.size)
            if solved_puzzle[x][y] != 0
        ]
        cells_to_reset = random.sample(
            filled_cells, len(filled_cells) - filled_cells_count
        )
        for x, y in cells_to_reset:
            solved_puzzle[x][y] = 0

        return solved_puzzle

    def solve_puzzle(self) -> List[List[int]]:
        """Solve the puzzle."""
        field = [[0] * self.size for _ in range(self.size)]
        x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        value = random.randint(1, self.size)
        field[x][y] = value
        field_state = FieldState.from_list_to_state(field)["state"]
        solver = PuzzleSolver(field_state)
        solved_puzzle = solver.solve()["solved_puzzle"]

        return solved_puzzle
