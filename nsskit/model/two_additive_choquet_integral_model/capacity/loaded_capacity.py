# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from itertools import combinations
from json import load

from .abstract_capacity import AbstractCapacity
from ....constant import CRITERIA


class LoadedCapacity(AbstractCapacity):

    def __init__(self, capacity_path: str) -> None:
        super().__init__()
        self._load_capacity_from_json(capacity_path)

    def _load_weights_from_json(self, capacity_path: str) -> None:
        with open(capacity_path, "r") as file:
            data = load(file)

            for criterion in CRITERIA:
                self._weights[criterion] = data["1"][criterion]
            for combination in combinations(CRITERIA, 2):
                self._weights[combination] = data["2"][",".join(combination)]
        self._verify_monotonicity_constraints()
        self._verify_nonnegativity_constraints()
        self._verify_normality_constraint()
