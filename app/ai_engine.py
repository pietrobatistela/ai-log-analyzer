import os
import time
import streamlit as st 
from google import genai
from dotenv import load_dotenv

load_dotenv()

def analyze_incident_with_ai(log_entry: dict, environment: str = "Production") -> str:
    """Envia o log de erro para a IA com tratamento de erros de indisponibilidade (503)."""
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "Chave de API não configurada no arquivo .env."

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
        Você é um Engenheiro de AIOps/SRE sênior responsável pelo monitoramento de infraestrutura.
        Analise a falha de sistema detectada abaixo:

        - **Horário:** {log_entry['timestamp']}
        - **Serviço Afetado:** {log_entry['service']}
        - **Ambiente:** {environment}
        - **Mensagem de Erro:** {log_entry['message']}

        REGRAS DE FORMATAÇÃO OBRIGATÓRIAS:
        - NUNCA inclua saudações, intros como "Como Engenheiro...", nem notas de rodapé.
        - Comece a resposta DIRETAMENTE no primeiro item numerado ("1. Causa Raiz Provável:").

        Estrutura exata da resposta:
        1. **Causa Raiz Provável:** [explicação técnica]
        2. **Nível de Severidade:** [Baixa, Média, Alta ou Crítica]
        3. **Comando ou Ação de Mitigação Recomendada:** [passo a passo técnico e comandos]
    """

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            return response.text
        except Exception as e:
            if "503" in str(e) and attempt < 2:
                time.sleep(2) 
                continue
            elif attempt == 2:
                try:
                    response = client.models.generate_content(
                        model="gemini-3.1-flash-lite",
                        contents=prompt
                    )
                    return response.text
                except Exception as fallback_err:
                    return f"Serviço temporariamente indisponível. Por favor, tente novamente em alguns segundos. (Erro: {str(fallback_err)})"