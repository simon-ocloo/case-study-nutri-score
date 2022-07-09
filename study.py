#!/usr/bin/env python3
# Study on the Nutri-Score
# Brice MAYAG & Simon OCLOO - 2022
# University Paris Dauphine PSL

from itertools import combinations
from sys import argv
from typing import List

from nsskit.component import Product
from nsskit.model import AbstractModel, TwoAdditiveChoquetIntegralModel


def load_products(argv: List[str]) -> List[Product]:
    return [
        *Product.load_from_json(argv[1] if len(argv) == 2 else "./data/products.json"),
        *Product.load_from_database(50),
    ]


def visualize_rank(products: List[Product], model: AbstractModel) -> None:
    flags = {
        "A": [-15, False],
        "B": [0, False],
        "C": [3, False],
        "D": [11, False],
        "E": [19, False]
    }
    sorted_by_score = sorted(products, key=lambda x: (x.score, x.name))
    sorted_by_model = sorted(products, key=lambda x: (model.run(x), x.name))

    for rank, (a, b) in enumerate(zip(sorted_by_score, sorted_by_model), 1):
        for key, value in flags.items():
            if value[1] is True:
                continue
            if a.score >= value[0]:
                value[1] = True
                print(key.rjust(3), "=" * 84,)
                break

        a = f"{a.name} ({a.score})"
        b = f"{b.name} ({model.run(b)})"
        print(f"{str(rank).rjust(3)} | {a.rjust(80)} | {b.rjust(80)}")


def visualize_indice(products: List[Product], model: AbstractModel) -> None:
    data = list(combinations(products, 2))
    score = 0

    for product_a, product_b in data:
        if product_a.grade >= product_b.grade:
            score += int(model.run(product_a) >= model.run(product_b))
        else:
            score += int(model.run(product_a) < model.run(product_b))
    print(f"Indice : {score / len(data):.4f}")


if __name__ == "__main__":
    model = TwoAdditiveChoquetIntegralModel()
    products = load_products(argv)

    model.train(products)
    visualize_rank(products, model)
    visualize_indice(products, model)
