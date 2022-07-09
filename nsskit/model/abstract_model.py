# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from abc import ABC, abstractmethod

from ..normalizer import AbstractNormalizer
from ..component import Product


class AbstractModel(ABC):

    def __init__(self, normalizer: AbstractNormalizer) -> None:
        self._normalizer: AbstractNormalizer = normalizer

    @abstractmethod
    def run(self, product: Product) -> float:
        pass
