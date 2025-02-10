import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def load(path: Path) -> dict:
    with path.open("r") as file:
        return json.load(file)


def find_equilibrium(payoff_matrix: np.ndarray) -> np.ndarray:
    num_decks = payoff_matrix.shape[0]
    c = np.concatenate([np.zeros(num_decks), np.array([-1])])
    a_ub = np.zeros((num_decks, num_decks + 1))
    for j in range(num_decks):
        a_ub[j, :num_decks] = -payoff_matrix[:, j]
        a_ub[j, -1] = 1.0
    b_ub = np.zeros(num_decks)
    a_eq = np.zeros((1, num_decks + 1))
    a_eq[0, :num_decks] = 1.0
    b_eq = np.array([1.0])
    bounds = [(0, None)] * num_decks + [(None, None)]
    result = linprog(
        c,
        A_ub=a_ub,
        b_ub=b_ub,
        A_eq=a_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="highs",
    )
    if not result.success:
        error_message = f"LP solver failure: {result.message}"
        raise RuntimeError(error_message)

    return result.x


def save_equilibrium(
    path: Path,
    probabilities: np.ndarray,
    deck_names: list[str],
    epsilon: float = 1e-16,
) -> dict:
    prob_name_pairs = [
        (prob, name) for prob, name in zip(probabilities, deck_names) if prob > epsilon
    ]
    prob_name_pairs.sort(key=lambda pair: pair[0], reverse=True)

    with path.open("w") as file:
        json.dump(
            {
                "deck_names": [name for _, name in prob_name_pairs],
                "probabilities": [prob for prob, _ in prob_name_pairs],
            },
            file,
            indent=4,
        )


def main() -> None:
    input_path = Path("record.json")
    output_path = Path("equilibrium.json")

    record = load(input_path)

    deck_names = record["deck_names"]
    payoff_matrix = np.array(record["payoff_matrix"])

    equilibrium = find_equilibrium(payoff_matrix)

    save_equilibrium(output_path, equilibrium, deck_names)


if __name__ == "__main__":
    main()
