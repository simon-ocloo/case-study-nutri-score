# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from itertools import combinations
from typing import List

from .capacity import LearnedCapacity, LoadedCapacity
from ..abstract_model import AbstractModel
from ...component import Product
from ...constant import CRITERIA
from ...normalizer import AbstractNormalizer, NutriScoreNormalizer


class TwoAdditiveChoquetIntegralModel(AbstractModel):

    def __init__(self, capacity_path: str = None, normalizer: AbstractNormalizer = NutriScoreNormalizer) -> None:
        super().__init__(normalizer)

        if capacity_path is not None:
            self._capacity = LoadedCapacity(capacity_path)
        else:
            self._capacity = LearnedCapacity()
            self.train = lambda products: self._capacity.train(self.run, products)

    def _get_importance(self, i: str) -> float:
        return self._capacity[i] + 0.5 * sum([self._get_interaction(i, k) for k in CRITERIA if k != i])

    def _get_interaction(self, i: str, j: str) -> float:
        return self._capacity[i, j] - (self._capacity[i] + self._capacity[j])

    def run(self, product: Product) -> float:
        data = self._normalizer.run(product)
        importance_score = sum([self._get_importance(i) * data[i] for i in CRITERIA])
        interaction_score = sum([self._get_interaction(i, j) * abs(data[i] - data[j]) for i, j in combinations(CRITERIA, 2)])

        return importance_score - 0.5 * interaction_score
