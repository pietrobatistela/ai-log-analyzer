import time
import pandas as pd
import plotly.express as px
import streamlit as st

from log_generator import generate_log_entry
from ai_engine import analyze_incident_with_ai

st.set_page_config(page_title="Live Incident & Log Monitor", page_icon="🛡️", layout="wide")

# Estado da sessão para armazenar logs recebidos em tempo real
if "logs" not in st.session_state:
    st.session_state.logs = []
if "selected_incident" not in st.session_state:
    st.session_state.selected_incident = None

st.title("🛡️ Live Incident & Log Monitor")
st.caption("Plataforma de Monitoramento Inteligente e Detecção de Anomalias de Infraestrutura")

# Sidebar de Controles
st.sidebar.header("Painel de Controle")
env_choice = st.sidebar.selectbox("Ambiente Target", ["PRD-Cluster-01", "QAS-Environment", "DEV-Local"])
auto_generate = st.sidebar.toggle("Simular Ingestão Contínua", value=False)

# Métricas do Topo
col1, col2, col3, col4 = st.columns(4)

df_logs = pd.DataFrame(st.session_state.logs)
total_logs = len(df_logs)
total_errors = len(df_logs[df_logs["level"] == "ERROR"]) if total_logs > 0 else 0
error_rate = f"{(total_errors / total_logs * 100):.1f}%" if total_logs > 0 else "0.0%"

col1.metric("Total de Logs Ingeridos", total_logs)
col2.metric("Incidentes/Erros", total_errors, delta_color="inverse")
col3.metric("Taxa de Erro", error_rate)
col4.metric("Status do Sistema", "CRÍTICO" if total_errors > 3 else "OPERACIONAL", 
            delta="Alertas Ativos" if total_errors > 3 else "Normal")

st.divider()

# Layout Principal: Graficos e Feed de Logs
left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.subheader("Feed de Logs & Ingestão ao Vivo")
    
    # Botão para simular 1 log manualmente
    if st.button("➕ Simular Evento de Sistema"):
        new_log = generate_log_entry()
        st.session_state.logs.append(new_log)
        st.rerun()

    if total_logs > 0:
        # Exibe os logs mais recentes primeiro
        recent_df = pd.DataFrame(st.session_state.logs[::-1])
        st.dataframe(
            recent_df[["timestamp", "level", "service", "message"]],
            width='stretch',
            height=300
        )
    else:
        st.info("Nenhum log ingerido ainda. Clique em 'Simular Evento' ou ative o modo contínuo no menu lateral.")

with right_col:
    st.subheader("Distribuição de Tráfego por Serviço")
    if total_logs > 0:
        fig = px.bar(
            df_logs, 
            x="service", 
            color="level", 
            color_discrete_map={"INFO": "#1f77b4", "WARN": "#ff7f0e", "ERROR": "#d62728"},
            title="Volume de Logs por Serviço e Nível"
        )
        st.plotly_chart(fig, width='stretch')

st.divider()
st.subheader("Diagnóstico Inteligente de Incidentes")

error_logs = [l for l in st.session_state.logs if l["level"] == "ERROR"]

if error_logs:
    selected_log_idx = st.selectbox(
        "Selecione um erro detectado para gerar o diagnóstico:",
        options=range(len(error_logs)),
        format_func=lambda i: f"[{error_logs[i]['timestamp']}] {error_logs[i]['service']} - {error_logs[i]['message'][:60]}..."
    )
    
    if st.button("Gerar Diagnóstico", type="primary"):
        target_log = error_logs[selected_log_idx]
        with st.spinner("Analisando telemetria e consultando o modelo de IA..."):
            diagnosis = analyze_incident_with_ai(target_log, environment=env_choice)
            st.markdown("### Relatório Técnico do Incidente")
            st.info(diagnosis)
else:
    st.success("Nenhum erro crítico pendente de análise no momento.")

if auto_generate:
    time.sleep(2)
    st.session_state.logs.append(generate_log_entry())
    st.rerun()