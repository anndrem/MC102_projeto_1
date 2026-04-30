### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    André de Almeida Maximiano 
# RA #01 (quem entregou o código):      306387
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]

"""Implemente aqui o seu código para adivinhar a regra.

Seu principal objetivo é implementar a função `player`, que deve retornar sua ação na rodada (chute de número ou chute de regra) e seu chute.
1. Se for um chute de número, ele deve ser um inteiro entre 1 e 100.000.
2. Se for um chute de regra, ele deve ser uma lista do tipo [TIPO, P1, P2], onde:
    - TIPO é uma string que pode ser "mod", "pot" ou "int", indicando o tipo da regra;
    - P1 e P2 são os parâmetros (números inteiros) da regra, que dependem do tipo.
        - Se TIPO for "mod", P1 é o valor de k e P2 é o valor de r.
        - Se TIPO for "pot", P1 é o valor de p. P2 é ignorado e pode ser qualquer valor.
        - Se TIPO for "int", P1 é o valor de a e P2 é o valor de b.

Exemplos de retornos válidos da função `player`:
- ["NUMBER", 42]             Chutando o número 42
- ["NUMBER", 100000]         Chutando o número 100.000
- ["RULE", ["mod", 3, 1]]    Chutando a regra "n mod 3 dá resto 1"
- ["RULE", ["pot", 2, 999]]  Chutando a regra "n é potência perfeita de ordem 2"
- ["RULE", ["int", 10, 20]]  Chutando a regra "n pertence ao intervalo [10, 20]"

Caso sua função não tenha um retorno adequado, a automatização não irá ocorrer tanto em game.py quanto em tournament.py.

---

A função `player` recebe duas listas como argumentos:
- number_guesses: lista de respostas aos chutes de número anteriores, onde cada elemento é uma lista do tipo [chute, direção, acerto], sendo:
    - chute:            o número inteiro chutado
    - direção:          a direção que indica se um número mais próximo que satisfaz a regra é maior ou menor do que o chute,
        sendo "igual" se o chute satisfizer a regra e menor se o chute estiver exatamente entre dois números que satisfazem a regra
    - acerto:           booleano indicando se o chute satisfaz a regra ou não

- rule_guesses: lista de respostas aos chutes de regras anteriores, onde cada elemento é uma lista do tipo [TIPO, P1, P2], 
    que significam a mesma coisa que os elementos do chute de regra descritos mais acima

Você pode implementar outras funções para auxiliar a função `player` e salvar informações entre os chutes usando variáveis globais (fora de qualquer função).

Para mais informações, verifique o README.md ou consulte um monitor.
"""

import random

CHUTE_DE_NUMERO = "NUMBER"
CHUTE_DE_REGRA = "RULE"
CHUTES_ANTERIORES = {}

CHUTES_ANTERIORES[CHUTE_DE_NUMERO] = []
CHUTES_ANTERIORES[CHUTE_DE_REGRA] = []


def chute_numerio():
    if len(CHUTES_ANTERIORES[CHUTE_DE_NUMERO]) == 0:
        return random.randint(0, 100)
    item = CHUTES_ANTERIORES[CHUTE_DE_NUMERO][-1][-1]
    if item[1] == 'maior':
        return random.randint(item[0], item[0] + 100)
    
    return random.randint(0, item[0])

def chute_regra(n):
    TIPO = random.choice(["mod", "pot", "int"])
    
    if TIPO == "mod":
        k = random.randint(n, 100)
        r = random.randint(0, k - 1)
        chute = [TIPO, k, r]
    elif TIPO == "pot":
        # p = random.randint(2, 10)
        chute = [TIPO, n, 0]
    else:
        a = random.randint(1, n) # Dica: o underline (_) pode ser usado para melhorar a legibilidade de números grandes em Python!
        b = random.randint(a, min(100_000, a + 100))
        chute = [TIPO, a, b]

    chute_atual = [CHUTE_DE_REGRA, chute]
    
    CHUTES_ANTERIORES[CHUTE_DE_REGRA].append(chute_atual[1])
    
    return chute_atual


def player(number_guesses, rule_guesses):
    """Função principal do jogador. 
    
    Exemplo de estratégia: chutar regras aleatórias.
    """
    # comecando a partida: 
    try:
        n = chute_numerio()
        if(len(number_guesses) == 0):
                return [CHUTE_DE_NUMERO, n]
        
        CHUTES_ANTERIORES[CHUTE_DE_NUMERO].append(number_guesses)
        while(not number_guesses[-1][-1]): 
            return [CHUTE_DE_NUMERO,n]
    
        CHUTES_ANTERIORES[CHUTE_DE_NUMERO].append(number_guesses)
        if number_guesses[-1]:
            return chute_regra(n)
    
        CHUTES_ANTERIORES[CHUTE_DE_REGRA].append(rule_guesses)

        return [CHUTE_DE_NUMERO,chute_numerio()]
    except Exception as e:
        print('Erro no código: ', e)

