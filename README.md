# Primeiros passos com agente ADK

![alt text](image.png)

Agente de exemplo feito com o **Google ADK**. O mesmo agente roda em **dois
modelos** ao mesmo tempo, dá pra alternar no seletor da interface:

- **`assistente_llama`** → Llama local (via Ollama). Offline e ilimitado.
- **`assistente_gemini`** → Gemini (nuvem). Precisa de internet + chave grátis.

## Estrutura

```
meu_agente/
├── ferramentas.py          # as ferramentas (funções que o agente pode chamar)
├── nucleo.py               # instruções + montagem do agente (compartilhado)
├── assistente_llama/       # app que usa o Llama local
│   ├── __init__.py
│   └── agent.py
├── assistente_gemini/      # app que usa o Gemini
│   ├── __init__.py
│   ├── agent.py
│   └── .env                # GOOGLE_API_KEY (não versionar)
├── requirements.txt        # dependências travadas
├── .gitignore
├── GUIA.md                 # material de estudo e conceitos detalhados
└── README.md
```

> As ferramentas e instruções ficam em `ferramentas.py` e `nucleo.py`,
> compartilhadas pelos dois apps. Mudou ali, vale para os dois.

## Pré-requisitos

- [Ollama](https://ollama.com) instalado e rodando, com o modelo baixado:

  ```bash
  ollama pull llama3.1:8b
  ```

- (Opcional, para o Gemini) uma chave grátis do Google AI Studio em
  <https://aistudio.google.com/app/apikey>, colada em `assistente_gemini/.env`.

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Dica: se mover ou renomear a pasta, recrie o `.venv` (o ambiente virtual
> guarda caminhos absolutos e quebra ao ser movido).

## Como rodar

A partir desta pasta (`meu_agente/`):

```bash
adk web        # abre a interface em http://127.0.0.1:8000
```

No seletor (canto superior esquerdo) escolha **assistente_llama** ou
**assistente_gemini**. Se um parar (ex.: cota do Gemini), troque para o outro
sem reiniciar nada.

## Ferramentas disponíveis

- `calcular` — faz contas com precisão (o modelo não calcula "de cabeça").
- `buscar_na_web` — busca informação atual na internet (DuckDuckGo).
- `data_de_hoje` — informa a data de hoje.
- `saudacao` — cumprimenta pelo nome.

## Trocar o modelo de cada app

Edite a string em `assistente_llama/agent.py` ou `assistente_gemini/agent.py`.
Exemplos: `ollama_chat/llama3.1:8b`, `ollama_chat/qwen2.5:7b`,
`gemini-2.5-flash-lite`, `gemini-2.5-flash` (cota grátis menor).
