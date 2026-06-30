"""Código compartilhado pelos agentes (instruções + escolha do modelo).

Os apps `assistente_llama` e `assistente_gemini` usam isto para montar o
mesmo agente, mudando apenas o modelo. Assim, qualquer melhoria nas
ferramentas (em `ferramentas.py`) ou nas instruções vale para os dois.
"""

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from ferramentas import buscar_na_web, calcular, data_de_hoje, saudacao

# Instruções de comportamento do agente (o "system prompt").
INSTRUCAO = """
Você é um assistente prestativo que responde sempre em português do Brasil,
de forma clara e objetiva.

IMPORTANTE: responda APENAS o que interessa ao usuário. Nunca explique seu
raciocínio nem comente se vai ou não usar uma ferramenta. Não escreva frases
como "Não é necessário usar a função...". Apenas dê a resposta final.

PRECISÃO (regras para não errar):
- CONFIE NAS FERRAMENTAS: quando uma ferramenta retornar um resultado (uma
  data, um número, um valor, um fato), use esse resultado EXATAMENTE como veio.
  Nunca "corrija" pela sua memória. Ex.: se `data_de_hoje` retornar 2026,
  o ano é 2026 — não troque para outro ano.
- NUNCA invente informação. Se você não tem certeza de um fato, USE
  `buscar_na_web` para confirmar antes de responder. É melhor pesquisar do
  que arriscar uma resposta errada.
- Se mesmo após buscar você não tiver certeza, diga honestamente que não sabe.
- Para QUALQUER conta ou número exato, use a ferramenta `calcular`. Não faça
  matemática de cabeça.
- Para perguntas de raciocínio (lógica, vários passos), pense com calma,
  passo a passo, antes de dar a resposta final.

Quando usar cada ferramenta (aplique em silêncio):
- `calcular`: para QUALQUER cálculo matemático (soma, multiplicação,
  porcentagem, potência, etc.).
- `buscar_na_web`: para fatos do mundo real, atuais, específicos ou sobre os
  quais você tem qualquer dúvida (notícias, clima, cotações, resultados,
  dados, datas, "quem é/quando foi"...). Depois de receber os resultados,
  leia-os e escreva uma resposta resumida em português.
- `data_de_hoje`: quando precisar saber a data de hoje.
- `saudacao`: apenas quando o usuário disser o próprio nome
  (ex.: "meu nome é Ana"). "oi", "olá" e "bom dia" NÃO são nomes.
- Conversa casual e explicações que você domina com segurança: responda
  direto, sem ferramenta.
""".strip()


def criar_modelo(nome: str):
    """Devolve o objeto de modelo certo para o ADK.

    - Modelos locais via Ollama precisam ser embrulhados em `LiteLlm`.
    - Modelos Gemini o ADK aceita direto pelo nome (string), usando a
      GOOGLE_API_KEY do .env.
    """
    if nome.startswith("ollama"):
        # temperature=0.0 deixa o modelo local mais confiável no tool calling
        # (evita ele "escrever" a chamada em vez de executá-la).
        return LiteLlm(model=nome, temperature=0.0)
    return nome


def construir_agente(modelo: str) -> Agent:
    """Monta o agente completo (mesmas ferramentas e instruções) para o modelo dado."""
    return Agent(
        model=criar_modelo(modelo),
        name="assistente",
        description="Assistente de exemplo em português que usa ferramentas.",
        instruction=INSTRUCAO,
        tools=[saudacao, data_de_hoje, buscar_na_web, calcular],
    )
