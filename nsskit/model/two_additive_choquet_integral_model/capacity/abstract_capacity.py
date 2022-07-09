# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from abc import ABC
from itertools import combinations
from typing import Dict, Tuple, Union

from ....constant import CRITERIA
from ....tools import subsets


class AbstractCapacity(ABC):

    def __init__(self) -> None:
        self._weights: Dict[str, float] = {}

    def __getitem__(self, key: Union[str, Tuple[str, str]]) -> float:
        if isinstance(key, str):
            return self._weights[key]
        elif isinstance(key, tuple):
            return self._weights[tuple(sorted(key))]
        raise KeyError(key)

    def __repr__(self) -> str:
        representation = []

        for criterion in CRITERIA:
            representation.append(f"µ({criterion}) = {self[criterion]}")
        for combination in combinations(CRITERIA, 2):
            representation.append(f"µ({','.join(combination)}) = {self[combination]}")
        return "\n".join(representation)

    def _verify_monotonicity_constraints(self) -> None:
        for A in subsets(CRITERIA):
            if len(A) >= 2:
                for i in A:
                    assert sum([self[i, j] - self[j] for j in A if j != i]) >= ((len(A) - 2) * self[i]), f"A monotonicity constraint is not satisfied > ({'+'.join([f'({self[i, j]} - {self[j]})' for j in A if j != i])}) >= ({(len(A) - 2)} * {self[i]})"

    def _verify_nonnegativity_constraints(self) -> None:
        for criterion in CRITERIA:
            assert self[criterion] >= 0, f"A nonnegativity constraint is not satisfied > {self[criterion]} >= 0"

    def _verify_normality_constraint(self) -> None:
        assert (sum([self[i, j] for i, j in combinations(CRITERIA, 2)]) - (len(CRITERIA) - 2) * sum([self[i] for i in CRITERIA])) == 1.0, f"The normality constraint is not satisfied > (({'+'.join([f'{self[i, j]}' for i, j in combinations(CRITERIA, 2)])}) - {len(CRITERIA) - 2} * ({'+'.join([f'{self[i]}' for i in CRITERIA])})) == 1.0"
