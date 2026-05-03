import traceback
import math
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

NUMEROS_CORRETOS = []

MENOR = 1
MAIOR = 10
CHAMADAS = 0

def chute_numerico():
    global CHAMADAS
    anterior = CHUTES_ANTERIORES[CHUTE_DE_NUMERO][0][-1]


    def buscar(a=None, b=None):
        global MENOR, MAIOR
        meio = (MENOR + MAIOR)//2

        if a != None and b != None:
            meio = (MENOR + MAIOR)//2
            MAIOR = a
            MENOR = b
           
            if anterior[1] == 'maior':
                MENOR = meio + 1
            if anterior[1] == 'menor':
                MAIOR = meio - 1
        
            meio = (MENOR + MAIOR) // 2
            return meio 
     
        if MENOR > MAIOR:
            #o numero nao esta neste intervalo -- tratar erro
            if anterior[1] == 'maior':
                MENOR = MAIOR
                MAIOR = MAIOR + 100
            if anterior[1] == 'menor':
                MENOR = MENOR // 2               
                MAIOR = MAIOR
        
        if anterior[1] == 'maior':
            MENOR = meio + 1
        if anterior[1] == 'menor':
            MAIOR = meio - 1
        
        meio = (MENOR + MAIOR) // 2
        return meio 
    
    if CHAMADAS % 15 == 10 and anterior[1] == 'maior':
        return buscar(anterior[0], anterior[0] * 10)
    if anterior[2]:
        print('UM NUMERO FOI ACERTADO: ', anterior[0])
        return buscar(anterior[0] + 50, anterior[0] + 100)
    else:
        return buscar()
    

def chute_regra():
    TIPO = random.choice(["mod", "pot", "int"])
    print(NUMEROS_CORRETOS)
    n = NUMEROS_CORRETOS[0]
    if TIPO == "mod":
        k = random.randint(n, n + 100)
        r = random.randint(0, k - 1)
        chute = [TIPO, k, r]
    elif TIPO == "pot":
        # p = random.randint(2, 10)
        chute = [TIPO, math.sqrt(n), 0]
    else:
        a = random.randint(1, n) # Dica: o underline (_) pode ser usado para melhorar a legibilidade de números grandes em Python!
        b = random.randint(a, min(100_000, a + 100))
        chute = [TIPO, a, b]
    
    return chute


def player(number_guesses, rule_guesses):
    # comecando a partida: 
    try:
        global CHAMADAS
        CHAMADAS += 1
        CHUTES_ANTERIORES[CHUTE_DE_NUMERO].append(number_guesses)
        
        if len(CHUTES_ANTERIORES[CHUTE_DE_NUMERO][0]) == 0:
            return [CHUTE_DE_NUMERO, 5]

        if len(NUMEROS_CORRETOS) == 5:
            print('10 CHUTES NUMERICOS CORRETOS')
            return [CHUTE_DE_REGRA, chute_regra()]
        
        if number_guesses[-1][2] and number_guesses[-1][0] not in NUMEROS_CORRETOS:
            NUMEROS_CORRETOS.append(number_guesses[-1][0])        
        
        n = chute_numerico()
        return [CHUTE_DE_NUMERO, n]
        
    except Exception as e:
        print('Erro no código: ')
        traceback.print_exc()

