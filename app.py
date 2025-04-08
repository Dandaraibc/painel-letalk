import streamlit as st
import streamlit_authenticator as stauth
import requests

st.set_page_config(page_title="Painel Letalk", layout="centered", page_icon="💬")

# ============ AUTENTICAÇÃO ============
users = {
    "usernames": {
        "assinaturas@letalk.com.br": {
            "name": "Time Letalk",
            "password": "$2b$12$7GWaOYq1llG2lvAsRtuv0evK7hNPCEqxE.G6eNO/sXD0KRpQid4pG"
        }
    }
}

authenticator = stauth.Authenticate(
    users,
    "painel_letalk",
    "auth_token",
    cookie_expiry_days=1
)

# 👇 login no formato POSICIONAL compatível
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuário ou senha inválidos.")
elif authentication_status is None:
    st.warning("Digite suas credenciais para continuar.")
elif authentication_status:
    st.success(f"Bem-vinda, {name} 👋")

    # === TABS ===
    aba_bloqueio, aba_cancelados, aba_avisos = st.tabs([
        "🔒 Bloqueio de Instâncias",
        "🚫 Bloqueio de Cancelados",
        "📢 Avisos"
    ])

    # BLOQUEIO DE INSTÂNCIAS
    with aba_bloqueio:
        st.subheader("🔒 Bloquear instâncias por ID")
        ids_input = st.text_area("Cole os IDs separados por vírgula", placeholder="Ex: 7618, 7620, 8001")
        if st.button("🚀 Bloquear Instâncias"):
            if not ids_input.strip():
                st.warning("Informe pelo menos um ID.")
            else:
                ids = [i.strip() for i in ids_input.split(",") if i.strip()]
                with st.spinner("Processando..."):
                    try:
                        res = requests.post(
                            "https://api-bloqueio-production.up.railway.app/bloquear",
                            json={"instance_ids": ids}
                        )
                        if res.status_code == 200:
                            st.success("Bloqueio realizado com sucesso!")
                            for log in res.json().get("log", []):
                                st.markdown(f"- {log}")
                        else:
                            st.error(f"Erro: {res.status_code}")
                    except Exception as e:
                        st.error(f"Erro na conexão com a API: {e}")

    # BLOQUEIO DE CANCELADOS
    with aba_cancelados:
        st.subheader("🚫 Bloqueio de Cancelados (sem notificação)")
        ids_cancelados = st.text_area("Cole os IDs dos cancelados", placeholder="Ex: 7618, 7844")
        if st.button("🔒 Bloquear Cancelados"):
            if not ids_cancelados.strip():
                st.warning("Informe pelo menos um ID.")
            else:
                ids = [i.strip() for i in ids_cancelados.split(",") if i.strip()]
                with st.spinner("Bloqueando cancelados..."):
                    try:
                        res = requests.post(
                            "https://api-bloqueio-production.up.railway.app/bloquear_cancelados",
                            json={"instance_ids": ids}
                        )
                        if res.status_code == 200:
                            st.success("Cancelados bloqueados com sucesso!")
                            for log in res.json().get("log", []):
                                st.markdown(f"- {log}")
                        else:
                            st.error(f"Erro: {res.status_code}")
                    except Exception as e:
                        st.error(f"Erro na conexão com a API: {e}")

    # AVISOS
    with aba_avisos:
        st.subheader("📢 Enviar Avisos para Instâncias")
        ids_avisos = st.text_area("Cole os IDs para envio do aviso", placeholder="Ex: 7618, 7654")

        col1, col2, col3 = st.columns(3)

        if col1.button("📩 Aviso de Bloqueio"):
            ids = [i.strip() for i in ids_avisos.split(",") if i.strip()]
            if ids:
                with st.spinner("Enviando aviso de bloqueio..."):
                    try:
                        res = requests.post(
                            "https://api-bloqueio-production.up.railway.app/avisar_bloqueio",
                            json={"instance_ids": ids}
                        )
                        if res.status_code == 200:
                            st.success("Aviso de bloqueio enviado.")
                            for log in res.json().get("log", []):
                                st.markdown(f"- {log}")
                        else:
                            st.error(f"Erro: {res.status_code}")
                    except Exception as e:
                        st.error(f"Erro: {e}")

        if col2.button("📆 Aviso de Inadimplência (10 dias)"):
            ids = [i.strip() for i in ids_avisos.split(",") if i.strip()]
            if ids:
                with st.spinner("Enviando aviso de inadimplência..."):
                    try:
                        res = requests.post(
                            "https://api-bloqueio-production.up.railway.app/avisar_inadimplencia",
                            json={"instance_ids": ids}
                        )
                        if res.status_code == 200:
                            st.success("Aviso de inadimplência enviado.")
                            for log in res.json().get("log", []):
                                st.markdown(f"- {log}")
                        else:
                            st.error(f"Erro: {res.status_code}")
                    except Exception as e:
                        st.error(f"Erro: {e}")

        if col3.button("⛔ Aviso de Encerramento"):
            ids = [i.strip() for i in ids_avisos.split(",") if i.strip()]
            if ids:
                with st.spinner("Enviando aviso de encerramento..."):
                    try:
                        res = requests.post(
                            "https://api-bloqueio-production.up.railway.app/avisar_encerramento",
                            json={"instance_ids": ids}
                        )
                        if res.status_code == 200:
                            st.success("Aviso de encerramento enviado.")
                            for log in res.json().get("log", []):
                                st.markdown(f"- {log}")
                        else:
                            st.error(f"Erro: {res.status_code}")
                    except Exception as e:
                        st.error(f"Erro: {e}")
