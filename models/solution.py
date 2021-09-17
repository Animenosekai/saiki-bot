from re import compile

from utils.sanitize import sanitize_html

NUMBER_REGEX = compile("\d+")
LETTER_REGEX = compile("[a-zA-Z]+")


class Solution():
    def __init__(self, number: str, solution: str) -> None:
        self.number = int("".join(NUMBER_REGEX.findall(str(number))))
        self.letter = "".join(LETTER_REGEX.findall(str(number)))
        self.solution = str(solution)

    def dump(self):
        if len(self.solution) <= 0:
            return ""
        results = f"<h2>Question {self.number}{self.letter}</h2>"
        results += sanitize_html(self.solution)
        return results
