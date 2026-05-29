##### Pergunta 01 #####
"""
O primeiro passo foi validar a entrada da função para que tenha pelo menos dois caracteres.
Tendo esse mínimo de tamanho podemos validar se o começo e fim começa e termina com 'A' e
'B'.
"""


def verifica_string(texto: str) -> bool:
    if len(texto) < 2 or (texto[0] != "A" or texto[-1] != "B"):
        return False

    return True


assert verifica_string("") == False
assert verifica_string("a") == False
assert verifica_string("b") == False
assert verifica_string("ab") == False
assert verifica_string("aaaaabbbbB") == False
assert verifica_string("Aaaaabbbbb") == False

assert verifica_string("AB") == True
assert verifica_string("AaaaabbbbB") == True


##### Pergunta 02 #####
"""
A sequência numérica se trata de uma PA crescente com primeiro termo 11 e razão 7.
Caso o usuário passse um valor menor do que 1, a função devolve o valor -1 indicando
erro.
"""


def print_valor(x: int) -> float:
    if x <= 0:
        return -1

    return 11 + (x - 1) * 7


assert print_valor(x=1) == 11
assert print_valor(x=2) == 18
assert print_valor(x=200) == 1404
assert print_valor(x=254) == 1782
assert print_valor(x=3542158) == 24795110


##### Pergunta 03 #####

"""
Antes de iniciar o desenvolvimento, vamos entender a partir de exemplos dos tabuleiros de
tamanho 3, 4 e 5 como se comportam:

Tabuleiro de tamanho 3 - [][][]
1 1 1 *
1 2   *
2 1   *
3     *
4 combinações de caminho
1 caminho ótimo

Tabuleiro de tamanho 4 - [][][][]
1 1 1 1 *
2 1 1   *
1 2 1   *
1 1 2   *
2 2     *
3 1     *
1 3     *
7 combinações de caminho
3 caminhos ótimos

Tabuleiro de tamanho 5 - [][][][][]
1 1 1 1 1 *
2 1 1 1   *
1 2 1 1   *
1 1 2 1   *
1 1 1 2   *
1 2 2     *
2 1 2     *
2 2 1     *
3 1 1     *
1 3 1     *
1 1 3     *
2 3       *
3 2       *
13 combinações de caminho
2 caminhos ótimos


Com essas informações em mãos agora é possível saber qual o caminho esperado. A tarefa de procurar 
quantas combinações de movimentos diferentes e quantos caminhos ótimos existem me remeteu a 
programação dinâmica. Essa técnica consiste em encontrar o resultado se baseando em subproblemas 
menores que ficam reaparecendo e tem uma subestrutura ótima, ou seja, a solução ótima pode ser 
obtida a partir da solução ótima dos seus subproblemas. Com isso, tanto  o item 2 e 3 podem ser 
solucionados através dessa técnica de programação. No item 2 através da função 'contar_caminhos_otimos'
eu utilizo o processo de memoização via programação funcional e no 3 através da função 
'movimentos_totais' é escolhida a tabulação como método de solução e utilização de matrizes e loops, 
ambos dentro do conceito de programação dinâmica.

É importante ressaltar que a escolha do uso de memoização foi feita para mostrar outro processo
de resolução de uma questão de programação dinâmica. O uso do decorator '@cache' evita recalcular
várias vezes a mesma coisa mas não impede o problema de explodir a pilha de recursão do python por conta
do python não ter Tail Call Optimization nativa e ter um limite estipulado para as chamadas.
Essa solução deve ser utilizada caso se conheça o problema e saiba que não será necessário tantas
chamadas recursivas, sendo dada preferência para subir em produção a resolução via tabulação para 
problemas de maior escala como é dito no problema que não tem tamanho limite. 
"""

from functools import cache
from math import ceil
from typing import NamedTuple


class ResultadoTabuleiro(NamedTuple):
    quantidade_minima_de_turnos: int
    probabilidade_do_caminho_otimo: float
    numero_de_combinacoes: int


def informacoes_do_tabuleiro(tamanho_tabuleiro: int) -> ResultadoTabuleiro:
    if tamanho_tabuleiro < 3:
        return ResultadoTabuleiro(0, 0, 0)

    qtd_minima_de_turnos = quantidade_minima_de_turnos(tamanho_tabuleiro)
    qtd_caminhos_otimos = contar_caminhos_otimos(tamanho_tabuleiro)
    qtd_movimentos_totais = movimentos_totais(tamanho_tabuleiro)

    return ResultadoTabuleiro(
        qtd_minima_de_turnos,
        qtd_caminhos_otimos / (3**qtd_caminhos_otimos),
        qtd_movimentos_totais,
    )


def quantidade_minima_de_turnos(tamanho_tabuleiro: int):
    return ceil(tamanho_tabuleiro / 3)


def contar_caminhos_otimos(tamanho_tabuleiro: int) -> float:
    @cache
    def contar_caminhos_otimos_aux(
        tamanho_tabuleiro_restante: int, quantidade_de_turnos_restantes: int
    ) -> int:
        if tamanho_tabuleiro_restante == 0 and quantidade_de_turnos_restantes == 0:
            return 1

        if tamanho_tabuleiro_restante <= 0 or quantidade_de_turnos_restantes <= 0:
            return 0

        return (
            contar_caminhos_otimos_aux(
                tamanho_tabuleiro_restante - 1, quantidade_de_turnos_restantes - 1
            )
            + contar_caminhos_otimos_aux(
                tamanho_tabuleiro_restante - 2, quantidade_de_turnos_restantes - 1
            )
            + contar_caminhos_otimos_aux(
                tamanho_tabuleiro_restante - 3, quantidade_de_turnos_restantes - 1
            )
        )

    qtd_minima_turnos = quantidade_minima_de_turnos(tamanho_tabuleiro)
    return contar_caminhos_otimos_aux(tamanho_tabuleiro, qtd_minima_turnos)


def movimentos_totais(tamanho_tabuleiro) -> int:
    soma_de_possibilidades = [0 for _ in range(tamanho_tabuleiro)]
    soma_de_possibilidades[0] = 1
    soma_de_possibilidades[1] = 2
    soma_de_possibilidades[2] = 4

    for i in range(3, len(soma_de_possibilidades)):
        soma_de_possibilidades[i] += (
            soma_de_possibilidades[i - 1]
            + soma_de_possibilidades[i - 2]
            + soma_de_possibilidades[i - 3]
        )

    return soma_de_possibilidades[-1]


assert quantidade_minima_de_turnos(3) == 1
assert quantidade_minima_de_turnos(4) == 2
assert quantidade_minima_de_turnos(5) == 2
assert quantidade_minima_de_turnos(7) == 3
assert quantidade_minima_de_turnos(10) == 4

assert contar_caminhos_otimos(3) == 1
assert contar_caminhos_otimos(4) == 3
assert contar_caminhos_otimos(5) == 2

assert movimentos_totais(3) == 4
assert movimentos_totais(4) == 7
assert movimentos_totais(5) == 13

##### Pergunta 04 #####
"""
O cálculo de datas foi feito lembrando de anos bissextos. Não foi necessário checar se
o determinado ano é bissexto pois a conta com os dias para verificar os benefícios já
observa caso fevereiro tenha 29 dias.

Os valores monetários em ambiente de produção não devem utilizar o float como tipo de 
dado para armazenar por ter problemas de arrendondamento e imprecisão. Independente da
linguagem ou banco de dados utilizado é necessário utilizar uma estrutura própria para
realizar as operações bancárias sem perda nenhuma. No Python temos o Decimal e um ecossistema
ao redor para realizar esse trabalho.

O valor resultante é baseado no salário bruto sem descontar os devidos impostos.
"""

from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import TypedDict


class Beneficios(TypedDict):
    decimo_terceiro: Decimal
    ferias: Decimal


DATA_ATUAL = date.today()


def valor_a_receber_beneficios(
    data_contratacao: date, salario_bruto: Decimal, data_demissao: date
) -> Beneficios:
    if salario_bruto < 0 or data_demissao < data_contratacao:
        raise Exception("Dados incorretos para cálculo de benefícios.")

    return {
        "decimo_terceiro": decimo_terceiro_valor_total(salario_bruto, data_demissao),
        "ferias": ferias_valor_total(data_contratacao, data_demissao, salario_bruto),
    }


def decimo_terceiro_valor_total(salario_bruto: Decimal, data_demissao: date) -> Decimal:
    meses_trabalhados: int
    if data_demissao.day < 15:
        meses_trabalhados = data_demissao.month - 1
    else:
        meses_trabalhados = data_demissao.month

    valor_decimo_terceiro = (salario_bruto / 12) * meses_trabalhados
    return valor_decimo_terceiro.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)


def ferias_valor_total(
    data_contratacao: date, data_demissao: date, salario_bruto: Decimal
):
    data_inicial = data_contratacao
    if data_contratacao.year != data_demissao.year:
        data_inicial = date(
            data_demissao.year - 1, data_contratacao.month, data_contratacao.day
        )

    diferenca_ultimas_ferias = relativedelta(data_demissao, data_inicial)
    meses_para_contagem = diferenca_ultimas_ferias.months
    if diferenca_ultimas_ferias.days >= 15:
        meses_para_contagem += 1

    valor_ferias = (salario_bruto / 12) * meses_para_contagem
    terco_salario = valor_ferias / 3

    return (valor_ferias + terco_salario).quantize(
        Decimal("0.00"), rounding=ROUND_HALF_UP
    )


beneficios = valor_a_receber_beneficios(
    date(2023, 10, 10), Decimal("3000.00"), date(2024, 4, 20)
)
assert beneficios["decimo_terceiro"] == 1000
assert beneficios["ferias"] == 2000
