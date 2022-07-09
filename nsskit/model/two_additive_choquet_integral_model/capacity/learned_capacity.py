# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from itertools import combinations
from typing import List

from docplex.mp.model import Model

from .abstract_capacity import AbstractCapacity
from ....component import Product
from ....constant import CRITERIA
from ....tools import subsets


class LearnedCapacity(AbstractCapacity):

    def __init__(self) -> None:
        super().__init__()

        self._model = Model("Capacity")

        self._initialize_weights()
        self._initialize_constraints()

    def _initialize_constraints(self):
        # Monotonicity.
        for A in subsets(CRITERIA):
            if len(A) >= 2:
                for i in A:
                    self._model.add_constraint(sum([self[i, j] - self[j] for j in A if j != i]) >= ((len(A) - 2) * self[i]))

        # Nonnegativity.
        for criterion in CRITERIA:
            self._model.add_constraint(self[criterion] >= 0)

        ## Normality.
        self._model.add_constraint((sum([self[i, j] for i, j in combinations(CRITERIA, 2)]) - (len(CRITERIA) - 2) * sum([self[i] for i in CRITERIA])) == 1.0)

    def _initialize_weights(self):
        for criterion in CRITERIA:
            self._weights[criterion] = self._model.continuous_var(lb=0.0, name=f"µ({criterion})")
        for combination in combinations(CRITERIA, 2):
            self._weights[combination] = self._model.continuous_var(lb=0.0, name=f"µ({','.join(combination)})")

    def train(self, get_score, products: List[Product]) -> None:
        data = [(product_a, product_b) for product_a, product_b in combinations(products, 2) if product_a.grade >= product_b.grade]
        gamma = len(data) / 2
        margin = self._model.continuous_var(lb=float('-inf'), ub=float('inf'))
        slacks = {product: self._model.continuous_var(lb=0.0) for product in products}

        for product_a, product_b in data:
            self._model.add_constraint((get_score(product_a) - get_score(product_b)) >= (margin - (slacks[product_a] + slacks[product_b])))
        self._model.maximize(margin - ((gamma / len(data)) * sum([slacks[a] + slacks[b] for a, b in data])))

        solution = self._model.solve()
        if solution:
            print(solution)
            for criterion in CRITERIA:
                self._weights[criterion] = self[criterion].solution_value
            for combination in combinations(CRITERIA, 2):
                self._weights[combination] = self[combination].solution_value
        else:
            assert False, "Aucune solution feasable."
