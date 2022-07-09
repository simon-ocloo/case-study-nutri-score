# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from typing import Any, Dict, List

from .abstract_normalizer import AbstractNormalizer
from ..component import Product
from ..constant import EN, FI, FR, PR, SA, SO, SU


class NutriScoreNormalizer(AbstractNormalizer):

    ENERGY_THRESHOLD = (335.0, 670.0, 1005.0, 1340.0, 1675.0, 2010.0, 2345.0, 2680.0, 3015.0, 3350.0)
    FIBERS_THRESHOLD = {"AOAC": (0.9, 1.9, 2.8, 3.7, 4.7), "NSP": (0.7, 1.4, 2.1, 2.8, 3.5)}
    FRUITS_VEGETABLES_THRESHOLD = (40.0, 60.0, 80.0, 80.0, 80.0)
    PROTEINS_THRESHOLD = (1.6, 3.2, 4.8, 6.4, 8.0)
    SATURATED_FAT_THRESHOLD = (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0)
    SODIUM_THRESHOLD = (90.0, 180.0, 270.0, 360.0, 450.0, 540.0, 630.0, 720.0, 810.0, 900.0)
    SUGAR_THRESHOLD = (4.5, 9.0, 13.5, 18.0, 22.5, 27.0, 31.0, 36.0, 40.0, 45.0)

    @staticmethod
    def run(product: Product, **kwargs: Dict[str, Any]) -> Dict[str, int]:
        def compute_points(value: float, thresholds: List[float]) -> int:
            points = 0

            for threshold in thresholds:
                if value <= threshold:
                    break
                points += 1
            return points

        fibers_obtention_method = kwargs.get("fibers_obtention_method", "AOAC")

        return {
            EN: compute_points(product[EN], NutriScoreNormalizer.ENERGY_THRESHOLD),
            FI: compute_points(product[FI], NutriScoreNormalizer.FIBERS_THRESHOLD[fibers_obtention_method]),
            FR: compute_points(product[FR], NutriScoreNormalizer.FRUITS_VEGETABLES_THRESHOLD),
            PR: compute_points(product[PR], NutriScoreNormalizer.PROTEINS_THRESHOLD),
            SA: compute_points(product[SA], NutriScoreNormalizer.SATURATED_FAT_THRESHOLD),
            SO: compute_points(product[SO], NutriScoreNormalizer.SODIUM_THRESHOLD),
            SU: compute_points(product[SU], NutriScoreNormalizer.SUGAR_THRESHOLD)
        }
