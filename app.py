import streamlit as st
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

st.set_page_config(page_title="Painel Letalk – Bloqueios e Avisos")

st.title("🔧 Painel Letalk – Bloqueios e Avisos")
st.subheader("📢 Enviar Avisos para Instâncias")

ids_aviso = st.text_area("Cole os IDs para envio do aviso", placeholder="Ex: 7618, 7654")

col1, col2, col3, col4 = st.columns(4)

# Função para capturar o telefone
def pegar_telefone(instance_id):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # roda em segundo plano
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        url = f"https://cp.letalk.com.br/attendance/chat?phone={instance_id}"
        driver.get(url)
        time.sleep(5)  # dá tempo da página carregar

        telefone_element = driver.find_element(By.XPATH, '//span[contains(text(), "+55")]')
        telefone = telefone_element.text.strip()
        driver.quit()
        return telefone
    except Exception as e:
        driver.quit()
        return f"Erro: {e}"

# Botão para recuperar cancelamento
if col4.button("♻️ Recuperar Cancelamento"):
    ids = [i.strip() for i in ids_aviso.split(",") if i.strip()]
    if ids:
        with st.spinner("Enviando solicitação de recuperação..."):
            instancias = []
            for i in ids:
                telefone = pegar_telefone(i)
                instancias.append({
                    "id": i,
                    "telefone": telefone
                })
            try:
                res = requests.post(
                    "https://webhook.letalk.com.br/b092b8a0-9433-4e3d-b14b-e7894b7cc8b3",
                    json={"instances": instancias}
                )
                if res.status_code == 200:
                    st.success("✅ Recuperação enviada com sucesso!")
                    for log in res.json().get("log", []):
                        st.markdown(f"- {log}")
                else:
                    st.error(f"❌ Erro: {res.status_code}")
            except Exception as e:
                st.error(f"❌ Erro: {e}")
    else:
        st.warning("⚠️ Informe ao menos um ID.")
