"""App do agente rodando no Gemini (nuvem). Precisa de internet + GOOGLE_API_KEY.

Usa o gemini-2.5-flash-lite, que tem cota grátis bem maior que o
gemini-2.5-flash (menos risco de estourar o limite numa apresentação).
"""

from nucleo import construir_agente

root_agent = construir_agente("gemini-2.5-flash-lite")
