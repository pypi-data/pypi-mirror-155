from __future__ import annotations
from typing import Dict, List
import numpy as np


class Problem:
    """
    QUBO Problem
    """

    def __init__(
        self,
        linear: dict,
        quadratic: dict,
        problem_type: str = "QUBO",
    ):
        self.linear = linear
        self.quadratic = quadratic
        self.problem_type = problem_type


def load_problem(file_path: str = "") -> Problem:
    lin = {}
    quad = {}
    qubo = np.loadtxt(file_path)
    for ar in qubo:
        if ar[0] == ar[1]:
            lin[int(ar[0])] = ar[2]
        else:
            quad[(int(ar[0]), int(ar[1]))] = ar[2]
    return Problem(linear=lin, quadratic=quad)


def qubo_energy(
    linear: dict, quadratic: dict, unembed_result: List[dict]
) -> List[float]:

    # Check some stuff to make sure we can do this
    linear_indecies = list(linear.keys())
    all_quadratic_indecies = [x for y in list(quadratic.keys()) for x in y]
    unembed_indecies = list(unembed_result[0].keys())

    if len(unembed_result[0]) != len(linear):
        raise ValueError("Dimension mismatch between results and linear term")

    if not set(linear_indecies).issubset(set(unembed_indecies)):
        raise ValueError("Qubit labels mismatch between results and linear term")

    if not set(all_quadratic_indecies).issubset(set(unembed_indecies)):
        offender = all_quadratic_indecies - unembed_indecies
        raise ValueError(f"Quadratic index {offender} is not in results")

    # Calculate linear term
    E = []
    for s in unembed_result:
        E.append(np.sum([linear[i] * s[i] for i in s.keys()]))
    E_linear = [float(e) for e in E]

    # Calculate quadratic term
    E = []
    for k in quadratic.keys():
        E.append([s[k[0]] * s[k[1]] * quadratic[k] for s in unembed_result])

    E_quadratic = np.sum(E, axis=0)

    return [float(e) for e in E_linear + E_quadratic]
