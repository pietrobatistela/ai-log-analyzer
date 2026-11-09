# AI Log & Ticket Analyzer

> **Pipeline Inteligente de Diagnóstico de Incidentes e Logs de TI containerizado com Docker, Podman e Kubernetes.**

---

## Sobre o Projeto

O **AI Log Analyzer** é uma solução *Cloud-Native* projetada para automatizar o diagnóstico de falhas em ambientes de infraestrutura e produção. A aplicação recebe logs brutos de erro ou tickets de suporte e utiliza modelos LLM via **Google Gemini** para gerar uma análise de causa raiz, nível de severidade e um plano de ação automatizado para os times de Operações.

---

## Tecnologias Utilizadas

* **Linguagem & Framework:** Python, FastAPI, Pydantic
* **AI & LLM:** Google GenAI SDK (Gemini 3.5 Flash)
* **Containerização:** Docker, Podman
* **Orquestração Cloud:** Kubernetes (Deployment & Service manifests)

---

## Arquitetura do Sistema

```mermaid
graph TD
    Client[Cliente / Dashboard TI] -->|POST /analyze| API[FastAPI Engine]
    API -->|Prompt Estruturado| Gemini[Google Gemini AI]
    Gemini -->|Análise & Plano de Ação| API
    API -->|Resposta JSON| Client