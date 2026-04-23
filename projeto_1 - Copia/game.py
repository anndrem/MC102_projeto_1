"""Arquivo responsável pela interface gráfica e inicialização do jogo.

Este script é a implementação principal da interface gráfica do jogo, utilizando a biblioteca Pygame. 
O jogo é um adivinhador de regra matemática, no qual o jogador deve adivinhar uma regra que um conjunto de números de 1 a 100.000 satisfaz. 
A interface permite ao jogador interagir com o jogo por meio de entradas de teclado.
O feedback das tentativas é exibido de forma sequencial.

A estrutura do código está dividida entre a inicialização do jogo, o controle dos eventos de entrada do jogador, 
a lógica de verificação dos chutes tentados, a atualização da interface e 
a automatização de jogadas de um jogador automático.

O código também inclui a definição de algumas constantes, como a largura e altura da janela, 
o tamanho da grade de jogo, a fonte a ser utilizada e a regra secreta a ser adivinhada.

Além disso, o código permite que o jogo seja pausado ao pressionar a tecla espaço quando o modo automático está ativado. 
"""


import argparse
import importlib
import random
from bisect import bisect_left
import player as player_module

try:
    import pygame
except ImportError:
    print("Pygame não foi instalado. Instale com: python -m pip install pygame")
    raise SystemExit(1)


# Configurações da interface do jogo em pygame
WIDTH, HEIGHT = 1200, 720
FPS = 60
AUTO_EVENT = pygame.USEREVENT + 1

# Cores da interface em RGB. Sinta-se livre para alterá-las, afinal, essa parte do código não muda a lógica do jogo, apenas a aparência :)
# Lembre-se que game.py e tournament.py serão usados exatamente como estavam originalmente para testar seu código.
BG = (18, 18, 22)
PANEL = (30, 30, 36)
BORDER = (72, 72, 86)
TEXT = (235, 235, 245)
MUTED = (180, 180, 195)
OK = (74, 222, 128)
ERR = (239, 82, 82)
ACCENT = (103, 159, 255)
PAUSED = (255, 218, 3)

graphic_design_is_my_passion = False

if graphic_design_is_my_passion:
    BG = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    PANEL = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    BORDER = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    TEXT = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    MUTED = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    OK = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    ERR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    ACCENT = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    PAUSED = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def parse_arguments():
    """Parser para receber o modo do jogo."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--auto",
        nargs="?",
        const=800,
        type=int,
        default=None,
        help="Ativa jogadas automáticas usando player.py (intervalo opcional em ms, padrão: 800)",
    )
    return parser.parse_args()


args = parse_arguments()

number_guesses = []
rule_guesses = []


def choose_rule():
    """Escolhe e retorna uma das regras disponíveis aleatoriamente.
    
    Retorna função que representa a regra, uma descrição e um dicionário com nome da regra e seus números.
    """
    rule_type = random.choice(["mod", "pot", "int"])
    if rule_type == "mod":
        k = random.randint(2, 100)
        r = random.randint(0, k - 1)
        return lambda n: n % k == r, f"n % {k} == {r}", {"type": rule_type, "k": k, "r": r}
    elif rule_type == "pot":
        p = random.randint(2, 10)
        return lambda n: round(n ** (1 / p)) ** p == n, f"n é potência perfeita de ordem {p}", {"type": rule_type, "p": p}
    else:
        a = random.randint(1, 100_000)
        b = random.randint(a, min(100_000, a + 100))
        return lambda n: a <= n <= b, f"n está entre {a} e {b}, inclusive", {"type": rule_type, "a": a, "b": b}


def generate_numbers(rule):
    """Gera e retorna a lista de números que satisfazem a regra."""
    return [n for n in range(1, 100_001) if rule(n)]


def direction(guess, numbers):
    """Retorna a direção do número mais próximo na lista de números que satisfazem a regra em relação ao número chutado."""
    i = bisect_left(numbers, guess)
    if i == 0:
        return "maior"
    elif i == len(numbers):
        return "menor"
    else:
        return "maior" if (numbers[i] - guess) < (guess - numbers[i - 1]) else "menor"


def rule_is_possible(guess):
    """Verifica se o chute de regra do jogador é possível considerando os limites para os parâmetros."""
    if guess["type"] == "mod":
        return 2 <= guess["k"] <= 100 and 0 <= guess["r"] < guess["k"]
    elif guess["type"] == "pot":
        return 2 <= guess["p"] <= 10
    elif guess["type"] == "int":
        return 1 <= guess["a"] <= guess["b"] <= 100_000
    else:
        return False


def guess_rule(guess, rule_info):
    """Verifica se o chute de regra do jogador está correto e retorna booleano indicando acerto ou erro."""
    if guess["type"] != rule_info["type"]:
        return False
    elif rule_info["type"] == "mod":
        return guess["k"] == rule_info["k"] and guess["r"] == rule_info["r"]
    elif rule_info["type"] == "pot":
        return guess["p"] == rule_info["p"]
    else:
        return guess["a"] == rule_info["a"] and guess["b"] == rule_info["b"]


def verify_player_guess(player_guess):
    """Verifica o retorno da função player, gerando erros caso não esteja no formato esperado."""
    if not isinstance(player_guess, list) or len(player_guess) != 2:
        raise ValueError("Retorno da função player não é lista e/ou não é do tipo [ação, chute]")

    action = str(player_guess[0]).upper()
    if action == "NUMBER":
        n = int(player_guess[1])
        if not (1 <= n <= 100_000):
            raise ValueError(f"Chute de número {n} fora do intervalo [1, 100.000].")
        return ["NUMBER", n]

    elif action == "RULE":
        guess = player_guess[1]
        if not isinstance(guess, list):
            raise ValueError("Chute de regra não é uma lista.")
        tipo = str(guess[0]).lower()
        if tipo == "mod":
            if len(guess) != 3:
                raise ValueError(f"mod admite 2 parâmetros (k e r), foram dados {len(guess) - 1}: {guess[1:]}.")
            return ["RULE", ["mod", int(guess[1]), int(guess[2])]]
        elif tipo == "pot":
            if len(guess) != 3:
                raise ValueError(f"pot admite 2 parâmetros (o primeiro sendo p), foram dados {len(guess) - 1}: {guess[1:]}.")
            return ["RULE", ["pot", int(guess[1]), 0]]
        elif tipo == "int":
            if len(guess) != 3:
                raise ValueError(f"int admite 2 parâmetros (a e b), foram dados {len(guess) - 1}: {guess[1:]}.")
            return ["RULE", ["int", int(guess[1]), int(guess[2])]]
        else:
            raise ValueError(f"Tipo de regra \"{tipo}\" inválido, deve ser \"mod\", \"pot\" ou \"int\".")
    else:
        raise ValueError(f"Ação deve ser NUMBER ou RULE, mas foi dado \"{action}\".")


def parse_manual_input(text):
    """Verifica e normaliza o comando digitado pelo usuário no modo manual, retornando o chute no formato esperado."""
    tokens = text.strip().lower().split()
    if not tokens:
        raise ValueError("Digite um comando.")

    # Comando "<número>"
    elif len(tokens) == 1:
        n = tokens[0]
        if not n.isdigit():
            raise ValueError(f"'{n}' não é um número válido.")
        n = int(n)
        if not 1 <= n <= 100_000:
            raise ValueError(f"Chute de número {n} fora do intervalo [1, 100.000].")
        return ["NUMBER", n]

    # Comando "num <número>"
    elif tokens[0] == "num" and len(tokens) == 2:
        n = tokens[1]
        if not n.isdigit():
            raise ValueError(f"'{n}' não é um número válido.")
        n = int(n)
        if not 1 <= n <= 100_000:
            raise ValueError(f"Chute de número {n} fora do intervalo [1, 100.000].")
        return ["NUMBER", n]

    # Comandos de chute de regra
    elif tokens[0] == "mod" and len(tokens) == 3:
        k, r = tokens[1], tokens[2]
        if not k.isdigit() or not r.isdigit():
            raise ValueError(f"Parâmetros k e r devem ser números inteiros, foram dados '{k}' e '{r}'.")
        return ["RULE", ["mod", int(k), int(r)]]
    elif tokens[0] == "pot" and 2 <= len(tokens) <= 3: # Permitir terceiro parâmetro para alinhar com função player, mas ignorá-lo
        p = tokens[1]
        if not p.isdigit():
            raise ValueError(f"Parâmetro p deve ser um número inteiro, foi dado '{p}'.")
        return ["RULE", ["pot", int(p), 0]]
    elif tokens[0] == "int" and len(tokens) == 3:
        a, b = tokens[1], tokens[2]
        if not a.isdigit() or not b.isdigit():
            raise ValueError(f"Parâmetros a e b devem ser números inteiros, foram dados '{a}' e '{b}'.")
        return ["RULE", ["int", int(a), int(b)]]

    else:
        raise ValueError("Comando inválido. Use n, num n, mod k r, pot p ou int a b.")


def apply_guess(player_guess, numbers, rule_info):
    """Analisa o chute do jogador e atualiza o jogo de forma adequada."""
    action = player_guess[0]

    if action == "NUMBER":
        guess = player_guess[1]
        d = direction(guess, numbers)
        hit = guess in numbers
        number_guesses.append([guess, "igual" if hit else d, hit])
        if hit:
            return False, f"Número {guess} satisfaz a regra."
        return False, f"Número {guess} não satisfaz a regra, mas um número mais próximo que satisfaz a regra é {d}."

    if action == "RULE":
        rule_type, p1, p2 = player_guess[1]
        if rule_type == "mod":
            guess = {"type": "mod", "k": p1, "r": p2}
        elif rule_type == "pot":
            guess = {"type": "pot", "p": p1}
        elif rule_type == "int":
            guess = {"type": "int", "a": p1, "b": p2}
        else:
            return False, "Tipo de regra inválido."

        if not rule_is_possible(guess):
            if guess["type"] == "mod":
                return False, f"Regra impossível: no 'mod', k ({guess['k']}) deveria estar em [2, 100], e r ({guess['r']}) deveria estar em [0, {guess['k'] - 1}]."
            elif guess["type"] == "pot":
                return False, f"Regra impossível: no 'pot', p ({guess['p']}) deveria estar em [2, 10]."
            elif guess["type"] == "int":
                return False, f"Regra impossível: no 'int', a ({guess['a']}) e b ({guess['b']}) deveriam satisfazer 1 <= a <= b <= 100.000."
        rule_guesses.append([rule_type, p1, p2])
        if guess_rule(guess, rule_info):
            return True, f"Parabéns, você acertou a regra secreta!"
        return False, "Chute de regra incorreto, continue tentando."

    return False, "Ação inválida."


def new_match():
    """Reinicia as variáveis do jogo, escolhe uma nova regra e gera a lista de números que satisfazem a regra."""
    number_guesses.clear()
    rule_guesses.clear()
    importlib.reload(player_module)
    rule, desc, info = choose_rule()
    numbers = generate_numbers(rule)
    return desc, info, numbers


def write_text(surface, text, font, color, x, y):
    """Escreve texto na interface do jogo."""
    rendered = font.render(text, True, color)
    surface.blit(rendered, (x, y))


def game():
    """Função central do jogo."""
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Adivinhador de Regras")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("consolas", 22)
    small = pygame.font.SysFont("consolas", 18)

    rule_desc, rule_info, numbers = new_match()
    game_over = False
    paused = False
    input_text = ""
    messages = ["Digite um comando e pressione Enter."]

    if args.auto:
        pygame.time.set_timer(AUTO_EVENT, args.auto)
        messages.append(f"Modo automático ativado (--auto). Intervalo: {args.auto}ms.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                
                if event.key == pygame.K_SPACE and args.auto:
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(AUTO_EVENT, 0)
                        messages.append("Jogo pausado. Pressione Espaço para continuar.")
                    else:
                        pygame.time.set_timer(AUTO_EVENT, args.auto)
                        messages.append("Jogo continuado.")
                    continue

                if event.key == pygame.K_r:
                    rule_desc, rule_info, numbers = new_match()
                    game_over = False
                    paused = False
                    if args.auto:
                        pygame.time.set_timer(AUTO_EVENT, args.auto)
                    input_text = ""
                    messages = ["Nova partida iniciada."]
                    continue

                if args.auto is not None:
                    continue

                if event.key == pygame.K_RETURN and not game_over:
                    try:
                        guess = parse_manual_input(input_text)
                        game_over, msg = apply_guess(guess, numbers, rule_info)
                    except ValueError as exc:
                        msg = f"Entrada inválida: {exc}"
                    messages.append(msg)
                    input_text = ""
                    continue

                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    ch = event.unicode
                    if ch.isprintable():
                        input_text += ch

            if event.type == AUTO_EVENT and args.auto is not None and not game_over:
                try:
                    auto_guess = verify_player_guess(player_module.player(number_guesses, rule_guesses))
                    game_over, msg = apply_guess(auto_guess, numbers, rule_info)
                except Exception as exc:
                    msg = f"Erro no player automático: {exc}"
                    game_over = True
                messages.append(msg)

        screen.fill(BG)

        pygame.draw.rect(screen, PANEL, (20, 20, WIDTH - 40, HEIGHT - 40), border_radius=8)
        pygame.draw.rect(screen, BORDER, (20, 20, WIDTH - 40, HEIGHT - 40), 2, border_radius=8)

        write_text(screen, "Adivinhador de Regras", font, TEXT, 40, 36)
        write_text(screen, "Comandos: n | num n | mod k r | pot p | int a b", small, MUTED, 40, 70)
        write_text(screen, "Teclas: Enter=chutar, R=reiniciar, Esc=fechar, Espaço=pausar (apenas em modo --auto)", small, MUTED, 40, 94)

        status = "FINALIZADO" if game_over else ("PAUSADO" if paused else "EM ANDAMENTO")
        status_color = OK if game_over else (PAUSED if paused else ACCENT)
        write_text(screen, f"Status: {status}", font, status_color, 40, 128)

        write_text(screen, "Entrada:", font, TEXT, 40, 168)
        pygame.draw.rect(screen, (12, 12, 15), (140, 164, WIDTH - 190, 40), border_radius=6)
        pygame.draw.rect(screen, ACCENT, (140, 164, WIDTH - 190, 40), 2, border_radius=6)
        shown_input = "(desabilitada no modo --auto)" if args.auto is not None else input_text
        write_text(screen, shown_input, small, TEXT, 150, 174)

        write_text(screen, f"Chutes de número: {len(number_guesses)}", small, TEXT, 40, 224)
        write_text(screen, f"Chutes de regra: {len(rule_guesses)}", small, TEXT, 500, 224)

        y = 256
        write_text(screen, "Últimos chutes de número:", small, MUTED, 40, y)
        y += 24
        for guess, d, hit in number_guesses[-8:]:
            color = OK if hit else TEXT
            tag = "OK" if hit else "NÃO ESTÁ"
            write_text(screen, f"n={guess:<6} dist={d:<6} {tag}", small, color, 40, y)
            y += 22

        y = 256
        write_text(screen, "Últimos chutes de regra:", small, MUTED, 500, y)
        y += 24
        for tipo, p1, p2 in rule_guesses[-8:]:
            if tipo == "pot":
                label = f"pot {p1}"
            else:
                label = f"{tipo} {p1} {p2}"
            write_text(screen, label, small, TEXT, 500, y)
            y += 22

        y = 470
        write_text(screen, "Mensagens:", small, MUTED, 40, y)
        y += 26
        for msg in messages[-7:]:
            color = OK if "Parabéns" in msg else (ERR if "inválido" in msg.lower() or "erro" in msg.lower() else (PAUSED if "pausado" in msg.lower() else TEXT))
            write_text(screen, msg[:100], small, color, 40, y)
            y += 22

        if game_over:
            write_text(screen, f"Regra secreta: {rule_desc}", font, OK, 40, HEIGHT - 52)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


# Inicialização do Jogo
# Esse bloco garante que o jogo só será executado se este arquivo for rodado diretamente,
# evitando sua execução caso seja importado como módulo em outro script.
if __name__ == "__main__":
    game()
