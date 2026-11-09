import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("A variável GEMINI_API_KEY não foi configurada no .env")

client = genai.Client(api_key=api_key)

app = FastAPI(
    title="Log & Ticket AI Analyzer",
    description="API para análise automatizada de logs e incidentes com IA",
    version="1.0.0"
)

class LogRequest(BaseModel):
    log_content: str
    environment: str = "Production"

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API de Análise de Logs online!"}

@app.post("/analyze")
def analyze_log(payload: LogRequest):
    try:
        prompt = f"""
        Você é um engenheiro especialista em infraestrutura e operações de TI.
        Analise o seguinte log/incidente vindo do ambiente '{payload.environment}':
        
        ---
        {payload.log_content}
        ---
        
        Responda em formato estruturado:
        1. **Resumo do Problema**: Qual é a causa raiz provável.
        2. **Severidade**: (Baixa, Média, Alta, Crítica).
        3. **Plano de Ação Recomendado**: Passos práticos para solução.
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        return {
            "environment": payload.environment,
            "analysis": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))