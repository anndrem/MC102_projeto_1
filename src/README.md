# 0. OBSERVAÇÃO
Este é um arquivo markdown (.md), então ele é melhor visto com visualização de markdown.

Você pode, por exemplo, acessar o site https://markdownlivepreview.com/ e colar todo o conteúdo desse arquivo para melhor visualizá-lo.

# 1. PRIMEIRO PROJETO DE MC102W: ADIVINHADOR DE REGRAS

Este projeto faz parte da disciplina **MC102** da turma **W** de **2026** e tem **peso 3**.

O projeto deve, obrigatoramente, ser feito em **dupla**. Caso você não consiga uma dupla, entre em contato com o professor ou um monitor.

Apenas um dos membros deve enviar o arquivo `player.py` (e apenas este arquivo), com nomes e RAs preenchidos no topo do arquivo, pelo **Google Classroom**. O outro membro deve fazer um **comentário particular** na atividade do Google Classroom avisando de qual dupla faz parte (para ficar registrada a concordância). Caso você entregue outros arquivos além do `player.py`, eles serão ignorados.

**Não é permitido alterar nenhum arquivo** além de `player.py`. Os demais (`game.py` e `tournament.py`) devem ser mantidos exatamente como fornecidos. Note que nós receberemos apenas o `player.py` e usaremos os outros arquivos originais para rodar o seu código, ou seja, se você alterar eles na sua máquina, isso não terá efeito na correção. 

Em qualquer momento, caso tenha alguma dúvida, fale com o professor ou um monitor!


# 2. O JOGO
Considere todos os números inteiros `n` de 1 a 100.000, inclusive.
Uma de três regras numéricas é escolhida aleatoriamente, com probabilidade igual para todas. Em seguida, seus parâmetros também são escolhidos aleatoriamente, de acordo com suas restrições. Uma regra numérica retorna `True` se `n` a satisfaz e `False` caso contrário. As regras são:

| Regra | Restrição 1 | Restrição 2 |
|-------|-------------|-------------|
| `n` mod `k` dá resto `r`, ou `n` dividido por `k` dá resto `r`  | `k` em [2, 100] | `r` em [0, `k` - 1] |
| `n` é uma potência perfeita de ordem `p`, ou raiz `p`-ésima de `n` é inteira | `p` em [1, 10] | - |
| `n` pertence ao intervalo fechado [`a`, `b`] | 1 <= `a` <= `b` <= 100.000 | `b` - `a` <= 100 |

Todos os parâmetros `k`, `r`, `p`, `a` e `b` são números inteiros.

Seja `N` o conjunto de todos os números `n` que satisfaçam a regra escolhida. Alguns exemplos:

| Regra | Conjunto N |
|-------|------------|
| `n` mod 5 dá resto 2 | {2, 7, 12, 17, ..., 999.992, 999.997} |
| `n` é uma potência perfeita de ordem 3 | {1, 8, 27, 64, ..., 91125, 97336} = {1³, 2³, 3³, 4³, ... 45³, 46³} |
| `n` pertence ao intervalo [68331, 68377] | {68331, 68332, 68333, 68334, ..., 68376, 68377} |


**O objetivo do jogo é descobrir qual regra gera um conjunto de números verdadeiros `N`.** Para isso, você pode chutar números ou regras.

- Com um chute de número, o jogo retorna se ele pertence a `N` e, se não pertence, também retorna se o número mais próximo ao seu chute que pertence a `N` é menor ou maior que seu chute. Se o chute estiver no meio de dois números que pertencem a `N`, o jogo retorna "menor".
- Com um chute de regra, o jogo retorna apenas se ela está correta. Se não estiver, o jogo continua, mas se estiver, o jogo é encerrado. 

## Exemplos de partidas

### Partida 1
| Chute | Resultado |
|-------|-----------|
| 50 | NÃO ESTÁ, mas um número mais próximo que pertence à regra é menor |
| 49 | OK |
| 48 | NÃO ESTÁ, mas um número mais próximo que pertence à regra é menor |
| 47 | OK |
| 46 | NÃO ESTÁ, mas um número mais próximo que pertence à regra é menor |
| "`n` mod 2 dá resto 1" | CORRETO, partida encerrada |

### Partida 2
| Chute | Resultado |
|-------|-----------|
| 100 | NÃO ESTÁ, mas um número mais próximo que pertence à regra é maior |
| 150 | OK |
| 140 | OK |
| 130 | NÃO ESTÁ, mas um número mais próximo que pertence à regra é maior |
| "`n` pertence ao intervalo [140, 150]" | INCORRETO |
| 131 | OK |
| "`n` pertence ao intervalo [131, 150]" | INCORRETO |
| 151 | OK |
| 152 | NÃO ESTÁ, mas um número mais próximo que pertence à regra é menor |
| "`n` pertence ao intervalo [131, 151]" | CORRETO, partida encerrada | 

### Partida 3
| Chute | Resultado |
|-------|-----------|
| 500 | NÃO ESTÁ, mas um número mais próximo que pertence à regra é menor |
| 250 | NÃO ESTÁ, mas um número mais próximo que pertence à regra é maior |
| 256 | OK |
| "`n` é potência perfeita de 2" | INCORRETO |
| "`n` é potência perfeita de 4" | INCORRETO |
| "`n` é potência perfeita de 8" | CORRETO, partida encerrada | 


# 3. COMO RODAR O JOGO
## Glossário de comandos no terminal
| Comando | Significado |
|---------|-------------|
| `python game.py` | Modo manual |
| `python game.py --auto` | Modo automático com 800 ms entre chutes|
| `python game.py --auto [t]` | Modo automático com `t` ms entre chutes |
| `python tournament.py` | Modo torneio |

Em alguns sistemas operacionais, você pode/deve usar `python3` ao invés de `python`.

## Modo manual
No terminal, escreva:
```bash
python game.py
```

Esse comando abre a interface do jogo e permite que você insira comandos manualmente. Os comandos possíveis são:
| Comando | Significado |
|---------|-------------|
| `n` (ou `num n`) | Chute do número `n` |
| `mod k r` | Chute de "`n` mod `k` dá resto `r`" |
| `pot p` | Chute de "`n` é potência perfeita de `p`" |
| `int a b` | Chute de "`n` pertence ao intervalo [`a`, `b`]" |

Além dos comandos, você pode usar as seguintes teclas do teclado:
- Enter para rodar o comando escrito
- R para reiniciar a partida, isto é, criar outra regra e começar do zero
- Esc para fechar a janela do jogo

Após cada comando rodado, a interface exibe um feedback visual.

## Modo automático
No terminal, escreva:
```bash
python game.py --auto 
```

Esse comando também abre a interface do jogo, mas os chutes são dados pela sua função `player`. Se ocorrer algum erro, ele será exibido como feedback e a partida para.

No modo automático, você pode apertar a barra de espaço para pausar a partida e apertar novamente para retomá-la.

Por padrão, o intervalo entre cada chute é 800 ms, mas você pode customizar isso escrevendo um número inteiro positivo após `--auto` indicando qual intervalo você quer entre chutes. Por exemplo, para ter um chute a cada 100 ms, insira no terminal:

```bash
python game.py --auto 100
```

## Modo torneio
No terminal, escreva:
```bash
python tournament.py 
```

Esse comando inicia o modo torneio, que roda 1000 jogos com sua função `player`, extrai dados pertinentes sobre sua estratégia e os imprime no terminal. Se ocorrer algum erro, o torneio é interrompido e o feedback será exibido no terminal.

## Bibliotecas necessárias
Para executar o arquivo `game.py`, você precisa da biblioteca Pygame, instalável com:

```bash
python -m pip install pygame
```

No entanto, para as versões mais recentes de Python (3.14+), esse comando pode dar erro. Nesses casos, você pode instalar a versão comunitária do Pygame, Pygame-ce, e o arquivo vai rodar sem problemas:

```bash
python -m pip install pygame-ce
```

Para executar o arquivo `tournament.py`, você precisa da biblioteca tqdm, instalável com:

```bash
python -m pip install tqdm
```

# 4. SUA TAREFA

Sua principal tarefa será modificar o arquivo `player.py`. Especificamente, você deve implementar a lógica dentro da função `player`, que deve retornar sua ação na rodada (chute de número ou chute de regra) e seu chute.

1. Se for um chute de número, ele deve ser um inteiro entre 1 e 100.000.
2. Se for um chute de regra, ele deve ser uma lista do tipo `[TIPO, P1, P2]`, onde:
    - `TIPO` é uma string que pode ser `"mod"`, `"pot"` ou `"int"`, indicando o tipo da regra;
    - `P1` e `P2` são os parâmetros (números inteiros) da regra, que dependem do tipo.
        - Se `TIPO` for `"mod"`, `P1` é o valor de `k` e `P2` é o valor de `r`.
        - Se `TIPO` for `"pot"`, `P1` é o valor de `p`. `P2` é ignorado e pode ser qualquer valor.
        - Se `TIPO` for `"int"`, `P1` é o valor de `a` e `P2` é o valor de `b`.

Exemplos de retornos válidos da função `player`:
| Retorno | Chute |
|--------------|------------|
|`["NUMBER", 42]` | Chutando o número 42 |
|`["NUMBER", 100000]` | Chutando o número 100.000 |
|`["RULE", ["mod", 3, 1]]` | Chutando a regra "`n` mod 3 dá resto 1" |
|`["RULE", ["pot", 2, 999]]` | Chutando a regra "`n` é potência perfeita de ordem 2"
|`["RULE", ["int", 10, 20]]` | Chutando a regra "`n` pertence ao intervalo [10, 20]"

Caso sua função não tenha um retorno adequado, a automatização não irá ocorrer tanto em game.py quanto em tournament.py.

A função `player` recebe duas listas como argumentos:

- `number_guesses`: É uma lista de respostas para enigmas numéricos anteriores, onde cada elemento é uma lista do tipo `[[chute, direção, acerto], [chute, direção, acerto],...]`, sendo:
    - `chute`:  o número inteiro chutado
    - `direção`:  a direção que indica se um número mais próximo que satisfaz a regra é maior ou menor do que o chute, sendo "igual" se o chute satisfizer a regra e menor se o chute estiver exatamente entre dois números que satisfazem a regra
    - `acerto`:  booleano indicando se o chute satisfaz a regra ou não

Exemplo:  
```python
[[50, NÃO ESTÁ, mas um número mais próximo que pertence à regra é menor, False], [48, NÃO ESTÁ, mas um número mais próximo que pertence à regra é menor, False], [49, OK, True]]
```

- `rule_guesses`: lista de respostas aos chutes de regras anteriores, onde cada elemento é uma lista do tipo `[[TIPO, P1, P2], [TIPO, P1, P2], ...]`, que significam a mesma coisa que os elementos do chute de regra descritos mais acima, sendo:
    - `Tipo`: O tipo de regra matemática (`mod`, `pot`, `int`)
    - `P1`: o primeiro parâmetro da regra (o divisor $k$, a potência $p$, o início do intervalo $a$)
    - `P2`: o segundo parâmetro da regra (o resto $r$, o fim do intervalo $h$, a potência é ignorada (Por padrão, está definido como $0$))

Exemplo: 
```python
[[mod, 2, 0], [pot, 3, 0], [int, 10, 50]]
```

Você pode implementar outras funções para auxiliar a função `player` e salvar informações entre os chutes usando variáveis globais (fora de qualquer função).

## Avaliação

Para a avaliação de sua função `player`, cinco torneios serão rodados em sequência usando `python tournament.py`. A avaliação será dividida em três partes de peso igual:

1. **Implementação do algoritmo**, que trata da qualidade e clareza do que foi implementado `player.py` com revisão manual do código. A nota pode ser:
    - **100% (Satisfatória)**: O código contém documentação clara, sua implementação é clara e segue boas práticas, e a execução é livre de erros durante os cinco torneios; a função `player` faz uso inteligente de variáveis de histórico (`number_guesses` e `rule_guesses`) ou variáveis globais para reduzir o espaço de busca; o formato de saídas da função `player` segue o formato de saída exigido.
    - **50% (Parcial)**: O código é funcional, mas apresenta pequenas falhas lógicas (por exemplo, repete tentativas falhas, não aproveita o rastreamento de endereços, etc.) ou contém código redundante, e a documentação está incompleta.
    - **0% (Insuficiente)**: O código gera exceções em tempo de execução que interrompem o torneio ou faz previsões aleatórias sem aplicar qualquer lógica, e o código não está documentado.

2. **Taxa de sucesso**, dada em função da média `m` das taxas de acerto dos cinco torneios. A nota pode ser:
    - **100% (Ótima)**: `m` >= 95%.
    - **70% (Satisfatória)**: 95% >`m` >= 80%.
    - **30% (Média)**: 80% > `m` >= 50%.
    - **0% (Insuficiente)**: 50% > `m`.

3. **Média de tentativas**, dada em função da média `t` das médias de tentativas por partida dos cinco torneios. A nota pode ser:
    - **100% (Ótima)**: 25 >= `t`.
    - **70% (Satisfatória)**: 50 >= `t` > 25.
    - **30% (Média)**: 150 >= `t` > 50.
    - **0% (Insuficiente)**: `t` > 150.

