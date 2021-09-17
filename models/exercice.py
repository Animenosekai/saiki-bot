from models.solution import Solution


class Exercice():
    def __init__(self, data: dict) -> None:
        try:
            self.number = int(data["number"])
            self.content = str(data.get("content", "N/A"))
            self.solutions = [Solution(number, solution)
                            for number, solution in data.get("solutions", {}).items()]
            self.solutions.sort(key=lambda solution: (solution.number, solution.letter))
            self.renderable = True
        except Exception:
            self.renderable = False
            self.number = -1

    def dump(self):
        if self.renderable:
            results = f"<h1>Solutions pour l'exercice {self.number}</h1>"
            for solution in self.solutions:
                results += solution.dump()
            return results
        else:
            return ""
