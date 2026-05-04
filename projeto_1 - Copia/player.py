import traceback
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

import random

CHUTE_DE_NUMERO = "NUMBER"
CHUTE_DE_REGRA = "RULE"

CHUTES_ANTERIORES = {}
CHUTES_ANTERIORES[CHUTE_DE_NUMERO] = []
CHUTES_ANTERIORES[CHUTE_DE_REGRA] = []
TEM_INTERVALO = []
NUMEROS_CORRETOS = []

MENOR = 1
MAIOR = 10
CHAMADAS = 0

def buscar_intervalo(proximidade, a=None, b=None):
    global MENOR, MAIOR
    if a is not None and b is not None:
        MENOR = a
        MAIOR = b
    
    meio = (MENOR + MAIOR)//2
    
    if MENOR > MAIOR:
        # raise Exception('intervalo invalido')
        MAIOR*=2
    
    if proximidade == 'maior':
        MENOR = meio + 1
    if proximidade == 'menor':
        MAIOR = meio - 1
    
    meio = (MENOR + MAIOR) // 2
    return meio 

def chute_numerico(intervalo, acertou):
    global CHAMADAS, MENOR, MAIOR
    anterior = CHUTES_ANTERIORES[CHUTE_DE_NUMERO][0][-1]
    
    ultimo_numero = anterior[0]
    proximidade = anterior[1]
    if acertou:
        print(f'ULTIMO NUMERO ESTÁ CORRETO: {ultimo_numero}\nSAINDO DO INTERVALO: [{MAIOR},{MENOR}]')
        return ultimo_numero + 1000
    
    if intervalo:
        MAIOR = ultimo_numero
        return buscar_intervalo(proximidade)
    elif not intervalo:    
        MENOR = ultimo_numero
        return ultimo_numero * 2
    
def chute_regra(chutes_certos):
    
    def pot(chutes_certos):
        """verifica valores de p que satisfazem a regra para todos os chutes e os retornam, caso existam"""
        valores = []
        for n in chutes_certos:
            #verifica valores de p que satisfazem a regra para cada n na lista
            for p in range(2,11):
                k = round(n**(1/p))
                if k**p == n:
                    valores.append(p)
        comuns = []   #valores de p comuns para todo n na lista
        for p in valores:
            for n in chutes_certos:
                k = round(n**(1/p))
                if k**p != n:    #quando é encontrado um valor de n que não se aplica para a regra, o loop é quebrado
                    break
            else: # quando é encontrado um valor de p que vale para todo n na lista,ou seja, quando o loop nao quebra
                if p not in comuns:
                    comuns.append(p)
        if len(comuns) == 1: #quando é encontrada uma unica regra possivel para n,ou seja, a regra do jogo
                comuns.append(0)
                chute = ["pot"] + comuns  
                return chute
        elif len(comuns) > 1:  #para o caso de existirem mais de uma regra possivel para n
            chute = []
            for p in comuns:
                lista = ["pot",p,0]
                chute.append(lista)
            return chute
        return None    
    
    def mod(chutes_certos):
        """verifica valores de k e r que satisfazem a regra para todos os chutes e os retornam, caso exitam """
        valores = [] #valores de [k,r] válidos para cada n em chutes_certos
        for n in chutes_certos:
            for k in range(2,101):
                for r in range(0,k):
                    if n%k == r:
                        valores.append([k,r])
        comuns = [] # [k,r] comuns para todo n em chutees_certos
        for [k,r] in valores:
            for n in chutes_certos:
                if n%k != r:
                    break
            else: #quando o loop não quebrar, ou seja, houver [k,r] valido para todo n
                if [k,r] not in comuns:
                    comuns.append([k,r])       
        #verificando quando se há uma ou múltiplas regras válidas para todo n em chutes_certos
        if len(comuns) == 1:
            chute = ["mod"] + (comuns[0])
            return chute    
        elif len(comuns) > 1:
            chutes = []
            for i in comuns:
                chute = ["mod"] + i
                chutes.append(chute)
                return chutes
        return None
    if pot(chutes_certos):
        return pot(chutes_certos)
    elif mod(chutes_certos):
        return mod(chutes_certos)
    else:
        a = random.randint(1, 100_000) # Dica: o underline (_) pode ser usado para melhorar a legibilidade de números grandes em Python!
        b = random.randint(a, min(100_000, a + 100))
        chute = ["int", a, b]
    
    return chute
        # chute = ["int", a, b]
        # return chute
    
    


def player(number_guesses, rule_guesses):

    """Função principal do jogador.     
    """
    try:
        global CHAMADAS, MENOR, MAIOR
        CHAMADAS += 1


        if len(NUMEROS_CORRETOS) == 3:
            print(f'{len(NUMEROS_CORRETOS)} CHUTES NUMERICOS CORRETOS')
            regra = chute_regra(NUMEROS_CORRETOS)
            return [CHUTE_DE_REGRA, regra]

        CHUTES_ANTERIORES[CHUTE_DE_NUMERO].append(number_guesses)
        CHUTES_ANTERIORES[CHUTE_DE_REGRA].append(rule_guesses)
       

        """ CHUTE INICIAL
        """
        if len(CHUTES_ANTERIORES[CHUTE_DE_NUMERO][0]) == 0:
            return [CHUTE_DE_NUMERO, 10]
        
        numero_correto = number_guesses[-1][0]

        if number_guesses[-1][2] and numero_correto not in NUMEROS_CORRETOS:
            NUMEROS_CORRETOS.append(numero_correto)        

        anterior = CHUTES_ANTERIORES[CHUTE_DE_NUMERO][0][-1]
        intervalo = True

        if anterior[2]:
            TEM_INTERVALO.append(not intervalo)

        if len(TEM_INTERVALO) > 0 and TEM_INTERVALO[-1]:
            n = buscar_intervalo(anterior[1])

        elif anterior[1] == 'menor':
            TEM_INTERVALO.append(intervalo)
            n = buscar_intervalo(anterior[1])
        else:
            TEM_INTERVALO.append(not intervalo)
            n = chute_numerico(not intervalo, anterior[2])
        
        # verificando n
        if n <= 0 or n > 100_000:
            print(f'CUIDADO: {n} fora do intervalo!\nRecalculando...')
            n = buscar_intervalo(anterior[1])

        return [CHUTE_DE_NUMERO, n]
        
    except Exception as e:
        print('Erro no código: ')
        traceback.print_exc()

