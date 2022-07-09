# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from .abstract_model import AbstractModel
from ..component import Product
from ..constant import  EN, FI, FR, PR, SA, SO, SU
from ..normalizer import AbstractNormalizer, NutriScoreNormalizer


class WeightedSumModel(AbstractModel):

    def __init__(self, normalizer: AbstractNormalizer = NutriScoreNormalizer) -> None:
        super().__init__(normalizer)

    def run(self, product: Product) -> float:
        data = self._normalizer.run(product)
        negative_points = (
              (10 - data[EN])
            + (10 - data[SA])
            + (10 - data[SO])
            + (10 - data[SU])
        )
        positive_points = (
              (2 * data[FI])
            + (2 * data[FR])
            + (2 * data[PR])
        )

        return 40 - (negative_points + (0.5 * positive_points))
