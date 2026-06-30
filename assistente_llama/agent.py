"""App do agente rodando no Llama local (via Ollama). Offline e ilimitado."""

from nucleo import construir_agente

root_agent = construir_agente("ollama_chat/llama3.1:8b")
