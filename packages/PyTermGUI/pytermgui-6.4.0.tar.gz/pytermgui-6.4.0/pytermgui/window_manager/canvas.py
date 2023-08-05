from ..parser import StyledText
from ..terminal import get_terminal, Terminal

from functools import lru_cache


class Canvas:
    def __init__(self) -> None:
        self._matrix = []

        self.width, self.height = self.terminal.size
        for _ in range(self.height):
            self._matrix.append([" "] * self.width)

        self._ref_matrix = self._matrix.copy()

    @property
    def terminal(self) -> Terminal:
        return get_terminal()

    @lru_cache(maxsize=None)
    def to_styled_text(self, text: str) -> StyledText:
        return StyledText(text)

    def clear(self) -> None:
        for row in range(self.height):
            for col in range(self.width):
                self._matrix[row][col] = " "

    def set_at_offset(self, line: str, offset: tuple[int, int]) -> None:
        text = self.to_styled_text(line)
        start = len(text.value) - len(text)

        col, row = offset

        if row >= self.height:
            return

        try:
            line = self._matrix[row]
        except IndexError:
            raise IndexError(
                f"Invalid row {row} for matrix with length {len(self._matrix)}."
            )

        ref_line = self._ref_matrix[row]

        line[col] = text.value[:start]

        for char in repr(text.value)[start:]:
            if col >= self.width:
                return

            line[col] = char
            col += 1

    def gather(self) -> str:
        buff = ""
        for pos_y, row in enumerate(self._matrix):
            joined = "".join(row).replace("\\x1b", "\x1b")
            buff += f"\x1b[{pos_y}H{joined}"

        return buff
