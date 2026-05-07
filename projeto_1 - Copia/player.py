### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    André de Almeida Maximiano 
# RA #01 (quem entregou o código):      306387
# Nome #02:                             Vinicius Brasil Turibio da Silva
# RA #02:                               306565

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

import traceback

CHUTE_DE_NUMERO = "NUMBER"
CHUTE_DE_REGRA = "RULE"

CHUTES_ANTERIORES = {}
CHUTES_ANTERIORES[CHUTE_DE_NUMERO] = []
CHUTES_ANTERIORES[CHUTE_DE_REGRA] = []

NUMEROS_CORRETOS = []
N_CORRETOS_COPY = []

CHAMADAS_REGRA = 0
CHAMADAS = 0

PRESO_NO_INTERVALO = 1
MENOR = 1
MAIOR = 100_000

TRY_INTERVAL_END = 0
TRY_INTERVAL_START = 0
INTERVAL_SUBINDO = True
def buscar_intervalo():
    global MENOR, MAIOR
    if MENOR >= MAIOR:
        MENOR=MAIOR
        MAIOR+=1000

    meio = (MENOR + MAIOR) // 2
    return meio 

def chute_numerico(is_first):
    global MENOR, MAIOR, PRESO_NO_INTERVALO

    if is_first: return 50_000
    
    anterior = CHUTES_ANTERIORES[CHUTE_DE_NUMERO][0][-1]
    ultimo_numero = anterior[0]
    proximidade = anterior[1]
    acertou = anterior[2]

    """
    FORCANDO A SAIDA DO INTERVALO
    """           
    if PRESO_NO_INTERVALO > 2 and acertou:
        PRESO_NO_INTERVALO*=1.5
        MAIOR += int(PRESO_NO_INTERVALO)

    if acertou and ultimo_numero not in NUMEROS_CORRETOS:
        print(f'NUMERO CORRETO: {ultimo_numero}')
        PRESO_NO_INTERVALO = 1
        NUMEROS_CORRETOS.append(ultimo_numero)
        return ultimo_numero+1000

    if ultimo_numero in NUMEROS_CORRETOS:
        PRESO_NO_INTERVALO*=1.5

    if proximidade == 'menor':
        MAIOR = ultimo_numero
    else:    
        MENOR = ultimo_numero

    return buscar_intervalo()
    
def interval(subindo):
    global TRY_INTERVAL_END, TRY_INTERVAL_START, N_CORRETOS_COPY

    if subindo:
        TRY_INTERVAL_END+=1
        extremo = N_CORRETOS_COPY[-1] + TRY_INTERVAL_END
    else:
        TRY_INTERVAL_START-=1
        extremo = N_CORRETOS_COPY[0] + TRY_INTERVAL_START
    return extremo

def pot(chutes_certos):
        """retorna uma lista com as regras de potência comuns aos chutes numericos, caso existam"""
        valores = [] 
        for n in chutes_certos:
            for p in range(2,11):
                k = round(n**(1/p))
                if k**p == n:
                    valores.append(p)
        comuns = []   
        for p in valores:
            for n in chutes_certos:
                k = round(n**(1/p))
                if k**p != n:   
                    break
            else: 
                if p not in comuns:
                    comuns.append(p)
        if len(comuns) != 0:
                chute = []
                for p in comuns:
                    lista = ["pot",p,0]
                    chute.append(lista)       
                return chute
        return None

def mod(chutes_certos):
        """retorna uma lista com as regras de resto comuns aos chutes numericos, caso existam """
        valores = [] 
        for n in chutes_certos:
            for k in range(2,101):
                for r in range(0,k):
                    if n%k == r:
                        valores.append([k,r])
        comuns = [] 
        for k,r in valores:
            for n in chutes_certos:
                if n%k != r:
                    break
            else: 
                if [k,r] not in comuns:
                    comuns.append([k,r])       
        if len(comuns) != 0:
            chute = []
            for k,r in comuns:
                lista = ["mod",k,r]
                chute.append(lista)
            return chute   
        return None

def chute_regra(chutes_certos):
    """retorna um chute de regra com base na lista de chutes de numeros corretos"""    
    #evitar repetições de chute
    if pot(chutes_certos):
        for chute in pot(chutes_certos):
            if chute not in CHUTES_ANTERIORES[CHUTE_DE_REGRA][0]:
                return chute
        
    if mod(chutes_certos):   
        for chute in mod(chutes_certos):
            if chute not in CHUTES_ANTERIORES[CHUTE_DE_REGRA][0]:
                return chute
    
    NUMEROS_CORRETOS.sort()
    a = chutes_certos[0]
    b = chutes_certos[-1]

    chute = ["int", a, b]
    return chute  
  
def player(number_guesses, rule_guesses):

    """Função principal do jogador.     
    """
    try:
        global CHAMADAS, CHAMADAS_REGRA, MENOR, MAIOR, NUMEROS_CORRETOS, TRY_INTERVAL_START, N_CORRETOS_COPY, TRY_INTERVAL_END, INTERVAL_SUBINDO
        CHAMADAS+=1
        CHUTES_ANTERIORES[CHUTE_DE_REGRA].append(rule_guesses)
        CHUTES_ANTERIORES[CHUTE_DE_NUMERO].append(number_guesses)

        """
        CHUTE DE REGRA
        """
        if CHAMADAS_REGRA == 1:
            NUMEROS_CORRETOS.sort()
            N_CORRETOS_COPY = NUMEROS_CORRETOS.copy()
        
        regra = CHUTES_ANTERIORES[CHUTE_DE_REGRA][0]

        if CHAMADAS_REGRA > 1 and regra[-1][0] == 'int':
            CHAMADAS+=1
            ultimo_numero = number_guesses[-1][0]
            proximidade = number_guesses[-1][1]
            acertou = number_guesses[-1][2]

            if CHAMADAS == 56: return [CHUTE_DE_NUMERO, interval(False)]

            if acertou and ultimo_numero not in NUMEROS_CORRETOS: NUMEROS_CORRETOS.append(ultimo_numero)

            if proximidade == 'maior' and CHAMADAS > 58:
                extremo = interval(True)
                return [CHUTE_DE_NUMERO, extremo]
            if proximidade == 'menor' and CHAMADAS > 57:
                regra = chute_regra(NUMEROS_CORRETOS)
                return [CHUTE_DE_REGRA, regra]
            
            extremo = interval(False)
            return [CHUTE_DE_NUMERO, extremo]

        if len(NUMEROS_CORRETOS) == 3 or CHAMADAS > 55:
            print(f'CHUTANDO REGRA...')
            CHAMADAS_REGRA+=1
            CHAMADAS = 55
            regra = chute_regra(NUMEROS_CORRETOS)
            return [CHUTE_DE_REGRA, regra]
        
        """ 
        CHUTE INICIAL
        """
        is_first = True if CHAMADAS == 1 else False
        ultimo_numero = 1 if CHAMADAS == 1 else number_guesses
        n = chute_numerico(is_first)

        if n <= 0:
            print(f'CUIDADO: {n} <= 0\nRecalculando...')
            MAIOR = ultimo_numero[-1][0]            
            n = buscar_intervalo()
        elif n > 100_000:
            print(f'CUIDADO: {n} > 100_000\nRecalculando...')
            MAIOR = 100_000
            MENOR = 0
            n = buscar_intervalo()

        return [CHUTE_DE_NUMERO, n]
        
    except Exception:
        print('Erro no código: ')
        traceback.print_exc()
