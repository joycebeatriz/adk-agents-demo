"""Ferramentas (tools) que o agente pode chamar.

Cada ferramenta é uma função Python comum. O que importa para o modelo é:
  - o NOME da função;
  - a DOCSTRING (descreve o que faz e QUANDO usar);
  - os ARGUMENTOS com type hints;
  - o RETORNO, sempre um dicionário com uma chave 'status'.
"""

import ast
import operator
from datetime import date

from ddgs import DDGS

# Operadores permitidos na calculadora (apenas matemática, nada de código).
_OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _avaliar(no):
    """Avalia com segurança um nó da árvore de uma expressão matemática."""
    if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
        return no.value
    if isinstance(no, ast.BinOp) and type(no.op) in _OPERADORES:
        return _OPERADORES[type(no.op)](_avaliar(no.left), _avaliar(no.right))
    if isinstance(no, ast.UnaryOp) and type(no.op) in _OPERADORES:
        return _OPERADORES[type(no.op)](_avaliar(no.operand))
    raise ValueError("expressão não permitida")


def calcular(expressao: str) -> dict:
    """Calcula uma expressão matemática com precisão.

    Use SEMPRE que precisar fazer qualquer conta (soma, subtração,
    multiplicação, divisão, potência, porcentagem). Nunca calcule "de cabeça".

    Args:
        expressao: A conta a calcular, ex.: "(12 + 7) * 3", "2 ** 10", "100 / 7".

    Returns:
        Dicionário com 'status' e o 'resultado'. Em caso de erro, 'status'
        = 'error' e uma 'mensagem'.
    """
    try:
        arvore = ast.parse(expressao, mode="eval")
        return {"status": "success", "resultado": _avaliar(arvore.body)}
    except Exception as e:  # noqa: BLE001 - devolvemos o erro ao modelo
        return {"status": "error", "mensagem": f"Não consegui calcular: {e}"}


def buscar_na_web(consulta: str) -> dict:
    """Busca informações ATUAIS na internet (DuckDuckGo).

    Use quando o usuário perguntar sobre fatos do mundo real ou recentes
    que você não tem como saber sozinho: notícias de hoje, clima, cotações,
    resultados, eventos atuais, etc.

    Args:
        consulta: O texto a pesquisar (ex.: "previsão do tempo São Paulo hoje").

    Returns:
        Dicionário com 'status' e uma lista 'resultados' (título, resumo e link).
        Em caso de falha, retorna 'status' = 'error' e uma 'mensagem'.
    """
    try:
        achados = DDGS().text(consulta, max_results=5, region="br-pt")
        resultados = [
            {"titulo": a.get("title"), "resumo": a.get("body"), "link": a.get("href")}
            for a in achados
        ]
        if not resultados:
            return {"status": "error", "mensagem": "Nenhum resultado encontrado."}
        return {"status": "success", "resultados": resultados}
    except Exception as e:  # noqa: BLE001 - queremos devolver o erro ao modelo
        return {"status": "error", "mensagem": f"Falha na busca: {e}"}


def saudacao(nome: str) -> dict:
    """Cumprimenta uma pessoa pelo nome.

    Use SOMENTE quando o usuário informar explicitamente o próprio nome,
    por exemplo "meu nome é Ana". Não use para cumprimentos genéricos
    como "oi", "olá" ou "bom dia".

    Args:
        nome: O nome da pessoa a ser cumprimentada.

    Returns:
        Dicionário com 'status' e a 'mensagem' de saudação.
    """
    return {"status": "success", "mensagem": f"Olá, {nome}! Como posso te ajudar?"}


def data_de_hoje() -> dict:
    """Informa a data de hoje no formato AAAA-MM-DD.

    Use quando o usuário perguntar que dia é hoje, a data atual,
    ou algo que dependa de saber a data de hoje.

    Returns:
        Dicionário com 'status' e a 'data' atual.
    """
    return {"status": "success", "data": date.today().isoformat()}
