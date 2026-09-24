# UseCases/FunctionGenerator.py
from typing import Callable

def SampleFunction(formula: str, samples: int, minimum: float, maximum: float, raiseError: Callable[[str], None] ) -> list[list[list[float]]]:
    if samples < 0:
        raiseError("Number of samples must be at least 1.")
        return[[[0.0]]]

    if samples == 0:
        return[[[0.0]]]

    output: list[list[list[float]]] = []
    x: list[float] = []
    coefficients: list[float] = []
    powers: list[int] = []

    formula = formula.lower().replace(' ','')

    terms: list[str] = formula.replace("-", "+-").split("+")

    for term in terms:
        if term == "":
            continue

        negative: bool = term.startswith("-")

        start: int = 1 if negative else 0
        if term.find("x") == start:
            term = term[:start] + "1" + term[start:]

        if "x" not in term:
            term += "x^0"
        elif "^" not in term:
            term += "^1"

        powerIndex: int = term.index("^")
        power: int = int(term[powerIndex + 1:])
        try:
            coefficientText: str = term[:powerIndex - 1]
            coefficient: float = float(coefficientText)
        except ValueError:
            raiseError(
                "Polynomial is in a wrong format.\n"
                "Expected format: [multiplicand]x^[power]\n"
                "Example: 4x^2-5x+7"
            )
            return[[[0.0]]]

        powers.append(power)
        coefficients.append(coefficient)

    maxPower: int = max(powers, default=0)
    coefficientsByPower: list[float] = [0.0] * (maxPower + 1)
    for power, coefficient in zip(powers, coefficients):
        coefficientsByPower[power] = coefficient
    
    if samples == 1:
        x.append(minimum + (maximum - minimum) / 2.0)
    else:
        step: float = (maximum - minimum) / (samples - 1)

        for i in range(samples):
            x.append(minimum + i * step)

    for xValue in x:
        value: float = 0.0
        for power, coefficient in enumerate(coefficientsByPower):
            value += coefficient * xValue ** power

        value = round(value, 3)
        output.append([[value]])

    print(f"{output = }")
    return output