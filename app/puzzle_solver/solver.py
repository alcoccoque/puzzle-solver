"""Puzzle solver."""

import collections
from typing import Dict, List, Tuple, Union


class Field:
    """Puzzle board field information."""

    def __init__(self, size: int):
        """Initialize the Field with a given size."""
        self.check_size(size)
        self._size = size
        self._neighbor_cache = {}

    @staticmethod
    def check_size(size: int) -> None:
        """Check if the size is valid."""
        if not isinstance(size, int):
            raise TypeError("Field size should be an integer")

        if size < 2:
            raise ValueError("Minimum field size is 2")

    def size(self) -> int:
        """Return the size of the field."""
        return self._size

    def get_all_cells(self) -> List[Tuple[int, int]]:
        """Return all cells in the field."""
        for x in range(self._size):
            for y in range(self._size):
                yield x, y

    def get_neighbour_cells(self, cell: Tuple[int, int]) -> set:
        """Return neighbor cells for a given cell."""
        if cell not in self._neighbor_cache:
            x, y = cell
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            neighbour_cells = {(x + dx, y + dy) for dx, dy in directions}
            self._neighbor_cache[cell] = {
                (x, y)
                for x, y in neighbour_cells
                if 0 <= x < self._size and 0 <= y < self._size
            }
        return self._neighbor_cache[cell]


class FieldState:
    """Represents the state of the field."""

    def __init__(self, field: Field):
        """Initialize the FieldState with a given field."""
        self.field = field
        self._state = collections.defaultdict(lambda: 0)

    @staticmethod
    def from_list_to_state(
        matrix: List[List[int]],
    ) -> Dict[str, Union["FieldState", str]]:
        """Create a FieldState object from a given matrix."""
        try:
            size = len(matrix)
            field = Field(size)
            state = FieldState(field)

            for x in range(size):
                for y in range(size):
                    state.set_state((x, y), matrix[x][y])

            return {"state": state}
        except (TypeError, ValueError) as excp:
            return {"error": str(excp)}

    def to_list(self) -> List[List[int]]:
        """Convert FieldState to a list of lists."""
        size = self.field.size()
        result = []
        for x in range(size):
            row = []
            for y in range(size):
                row.append(self._state[x, y])
            result.append(row)
        return result

    def set_state(self, coords: Tuple[int, int], value: int) -> None:
        """Set the state of a cell."""
        if value < 0:
            raise ValueError("Value should be non-negative")

        if not isinstance(value, int):
            raise TypeError("Value should be an integer")
        self._state[coords] = value

    def get_state(self, coords: Tuple[int, int]) -> int:
        """Get the state of a cell."""
        return self._state[coords]

    def get_involved(self, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get involved cells for a given cell."""
        involved = [cell]
        value = self._state[cell]
        not_checked = [cell]

        while not_checked:
            cell = not_checked.pop()

            for neighbour in self.field.get_neighbour_cells(cell):
                if neighbour not in involved and self._state[neighbour] == value:
                    involved.append(neighbour)
                    not_checked.append(neighbour)

        return involved


class CellsGroup:
    """Represents a group of cells with the same value."""

    def __init__(self, value: int, initial_cells: List[Tuple[int, int]]):
        """Initialize the CellsGroup with a value and initial cells."""
        self.value = value
        self.initial_cells = initial_cells
        self.possible_cells = []
        self.possible_connection_cells = []

    def get_value(self) -> int:
        """Get the value of the group."""
        return self.value

    def get_possible_length(self) -> int:
        """Get the possible length of the group."""
        return (
            len(self.initial_cells)
            + len(self.possible_cells)
            + len(self.possible_connection_cells)
        )

    def add_possible_cell(self, cell: Tuple[int, int]) -> None:
        """Add a possible cell to the group."""
        if cell not in self.possible_cells:
            self.possible_cells.append(cell)

    def add_connection(self, cell: Tuple[int, int]) -> None:
        """Add a connection to the group."""
        if cell not in self.possible_connection_cells:
            self.possible_connection_cells.append(cell)


class PuzzleSolver:
    """Solves the puzzle."""

    possible_values: collections.defaultdict
    involved: list = []
    unfilled_groups: dict = {}

    def __init__(self, field_state: FieldState):
        """Initialize the PuzzleSolver with a field state."""
        self.field_state = field_state
        self.state_changed = True

    def solve(self) -> Dict[str, Union[List[List[int]], str]]:
        """Solve the puzzle."""
        try:
            self._refresh_state()
            self._try_fill_empty_cells()
            if self.check_for_zeros():
                return {"error": "Puzzle is unsolvable"}
            return {"solved_puzzle": self.field_state.to_list()}
        except (ValueError, TypeError) as excp:
            return {"error": str(excp)}

    def _refresh_state(self) -> None:
        """Refresh the state of the puzzle."""
        self._find_unfilled_groups()
        for cell in filter(
            lambda c: self.field_state.get_state(c) != 0 and c in self.unfilled_groups,
            self.field_state.field.get_all_cells(),
        ):
            self._find_possible_values(cell)

        empty_cells = list(
            filter(
                lambda c: self.field_state.get_state(c) == 0,
                self.field_state.field.get_all_cells(),
            )
        )

        involved = set()
        for cell in empty_cells:
            if all(
                self.field_state.get_state(n) != 1
                for n in self.field_state.field.get_neighbour_cells(cell)
            ):
                self._add_possible_value(cell, 1)

            if cell not in involved:
                empty_group = self.field_state.get_involved(cell)
                involved = involved.union(empty_group)
                self._find_additional_values(empty_group)

        self.state_changed = True

    def _find_additional_values(self, empty_group: List[Tuple[int, int]]) -> None:
        """Find additional values for an empty group."""
        for value in range(2, min(len(empty_group) + 1, 10)):
            involved_for_value = set(empty_group)
            not_possible_cells = set()

            for involved in involved_for_value:
                if any(
                    self.field_state.get_state(n) == value
                    for n in self.field_state.field.get_neighbour_cells(involved)
                ):
                    not_possible_cells.add(involved)
            involved_for_value -= not_possible_cells

            if value <= len(involved_for_value):
                for cell in involved_for_value:
                    self._add_possible_value(cell, value)

    def _find_unfilled_groups(self) -> None:
        """Find unfilled groups in the puzzle."""
        self.unfilled_groups = {}
        self.involved = []
        self.possible_values = collections.defaultdict(lambda: [])

        for cell in filter(
            lambda x: self.field_state.get_state(x) != 0,
            self.field_state.field.get_all_cells(),
        ):
            if cell not in self.involved:
                initial_cells = self.field_state.get_involved(cell)
                self.involved += initial_cells
                value = self.field_state.get_state(cell)

                if len(initial_cells) < value:
                    new_group = CellsGroup(value, initial_cells)
                    for c in initial_cells:
                        self.unfilled_groups[c] = new_group

                if len(initial_cells) > value:
                    raise ValueError("Wrong group size")

    def _find_possible_values(self, cell: Tuple[int, int]) -> None:
        """Find possible values for a cell."""
        next_cells = [(cell, 0)]
        value = self.field_state.get_state(cell)
        previous_cells = []
        group = self.unfilled_groups[cell]

        while next_cells:
            current_cell, current_length = next_cells.pop()
            previous_cells.append(current_cell)

            way_length = current_length + len(group.initial_cells)

            if way_length < value and current_cell != cell:
                self._add_possible_value(current_cell, value)
                group.add_possible_cell(current_cell)

            elif way_length == value:
                self._add_possible_value(current_cell, value)
                group.add_possible_cell(current_cell)
                continue

            free_neighbours = filter(
                lambda n: self.field_state.get_state(n) == 0
                and n not in previous_cells,
                self.field_state.field.get_neighbour_cells(current_cell),
            )

            for neighbour in free_neighbours:
                if any(
                    self._connection_cells_found(n, neighbour, group)
                    for n in self.field_state.field.get_neighbour_cells(neighbour)
                ):
                    continue

                next_cells.append((neighbour, current_length + 1))

    def _connection_cells_found(
        self, neighbour: Tuple[int, int], cell: Tuple[int, int], group: CellsGroup
    ) -> bool:
        """Check if connection cells are found."""
        value = group.get_value()

        if (
            self.field_state.get_state(neighbour) == value
            and neighbour not in group.initial_cells
            and neighbour not in group.possible_cells
        ):
            self.field_state.set_state(cell, value)
            intersection_length = len(self.field_state.get_involved(cell))
            self.field_state.set_state(cell, 0)

            if intersection_length <= value:
                group.add_connection(cell)
                self._add_possible_value(cell, value)
            return True

        return False

    def _add_possible_value(self, cell: Tuple[int, int], value: int) -> None:
        """Add a possible value to a cell."""
        if value not in self.possible_values[cell]:
            # self.possible_values[cell].add(value)
            for n in self.field_state.field.get_neighbour_cells(cell):
                n_value = self.field_state.get_state(n)
                if n_value != 0 and abs(n_value - value) == 1:
                    break  # Value conflicts with adjacent cell
            else:
                self.possible_values[cell].append(value)

    def _try_fill_empty_cells(self) -> None:
        """Try to fill empty cells."""

        def backtrack():
            if not free_cells:
                return True
            cell = free_cells.pop()
            possible_values[cell] = self.possible_values[cell]
            for value in possible_values[cell]:
                self.field_state.set_state(cell, value)
                try:
                    self.check_group_size()
                    if backtrack():
                        return True
                except ValueError:
                    pass
                self.field_state.set_state(cell, 0)
            free_cells.append(cell)

            return False

        free_cells = list(
            filter(
                lambda c: self.field_state.get_state(c) == 0,
                self.field_state.field.get_all_cells(),
            )
        )
        possible_values = self.possible_values
        backtrack()

    def check_group_size(self) -> None:
        """Check if group size is correct."""
        self._refresh_state()
        if any(
            group.get_possible_length() < group.get_value()
            and not group.possible_connection_cells
            for group in self.unfilled_groups.values()
        ):
            raise ValueError("Wrong group size")

    def check_for_zeros(self) -> bool:
        """Check if there is any zero in field state"""
        return any(0 in sublist for sublist in self.field_state.to_list())
