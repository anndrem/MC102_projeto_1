"""Torneio para avaliar estratégias de player no jogo de regras numéricas.

Este script simula várias partidas do jogo de adivinhar regras
e calcula métricas de desempenho do `player.py`.
"""

from importlib import reload
import player
from game import choose_rule, generate_numbers, direction, guess_rule, verify_player_guess

try:
    from tqdm import tqdm
except ImportError:
    print("Tqdm não foi instalado. Instale com: python -m pip install tqdm")
    raise SystemExit(1)


def play_one_game(max_attempts):
    """Simula uma partida e retorna estatísticas da partida."""
    rule, _, rule_info = choose_rule()
    numbers = generate_numbers(rule)

    reload(player)
    number_guesses = []
    rule_guesses = []
    attempts = 0

    while attempts < max_attempts:
        attempts += 1
        guess = verify_player_guess(player.player(number_guesses, rule_guesses))

        if guess[0] == "NUMBER":
            n = guess[1]
            d = direction(n, numbers)
            hit = n in numbers
            number_guesses.append([n, d, hit])
            continue

        rule_type, p1, p2 = guess[1]
        if rule_type == "mod":
            guessed_rule = {"type": "mod", "k": p1, "r": p2}
        elif rule_type == "pot":
            guessed_rule = {"type": "pot", "p": p1}
        else:
            guessed_rule = {"type": "int", "a": p1, "b": p2}

        rule_guesses.append([rule_type, p1, p2])
        if guess_rule(guessed_rule, rule_info):
            return {
                "win": True,
                "attempts": attempts,
                "number_guesses": len(number_guesses),
            }

    return {
        "win": False,
        "attempts": max_attempts,
        "number_guesses": len(number_guesses),
    }


def results_from_list(values):
    """Retorna média, mediana, desvio padrão, mínimo e máximo de uma lista."""
    ordered = sorted(values)
    n = len(ordered)
    mean = sum(ordered) / n
    median = ordered[n // 2] if n % 2 == 1 else (ordered[n // 2 - 1] + ordered[n // 2]) / 2
    std = (sum((x - mean) ** 2 for x in ordered) / n) ** 0.5
    return mean, median, std, ordered[0], ordered[-1]


def main():
    """Executa o torneio e imprime métricas agregadas."""
    max_games = 1000
    max_attempts = 1000 # Inclui chutes de números e de regras

    attempts = []
    number_guess_counts = []
    wins = 0

    for _ in tqdm(range(max_games)):
        result = play_one_game(max_attempts=max_attempts)
        attempts.append(result["attempts"])
        number_guess_counts.append(result["number_guesses"])
        if result["win"]:
            wins += 1

    fails = max_games - wins
    success_rate = (wins / max_games * 100) if max_games else 0

    attempts_stats = results_from_list(attempts)
    number_stats = results_from_list(number_guess_counts)

    print("\nTorneio finalizado!\n")
    print(f"Total de partidas simuladas: {max_games}")
    print(f"Máximo de tentativas por jogo: {max_attempts}")
    print(f"Partidas vencidas: {wins}")
    print(f"Partidas sem acerto: {fails}")
    print(f"Taxa de acerto: {success_rate:.2f}%")

    print("\nTentativas por partida:")
    print(f"Média: {attempts_stats[0]:.3f}")
    print(f"Mediana: {attempts_stats[1]:.3f}")
    print(f"Desvio padrão: {attempts_stats[2]:.3f}")
    print(f"Mínimo: {attempts_stats[3]}")
    print(f"Máximo: {attempts_stats[4]}")

    print("\nChutes de número por partida:")
    print(f"Média: {number_stats[0]:.3f}")
    print(f"Mediana: {number_stats[1]:.3f}")
    print(f"Desvio padrão: {number_stats[2]:.3f}")
    print(f"Mínimo: {number_stats[3]}")
    print(f"Máximo: {number_stats[4]}")


if __name__ == "__main__":
    main()  