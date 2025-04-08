import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def bloquear_instancias(instance_ids):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = './chrome-linux64/chrome'
    service = Service(executable_path='./chrome-linux64/chromedriver')

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://a.letalk.com.br/signin")
    st.write("🔐 Acessando página de login...")

    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-email"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-password"))
        )

        email_field.send_keys("dandara.letalk@gmail.com")
        password_field.send_keys("K7#*H*%ftIhLIeTJ")
        password_field.send_keys(Keys.RETURN)

        WebDriverWait(driver, 20).until(EC.url_changes("https://a.letalk.com.br/signin"))
        st.success("Login realizado com sucesso.")

    except Exception as e:
        st.error(f"Erro ao fazer login: {e}")
        driver.quit()
        return

    for instance_id in instance_ids:
        if instance_id != "7618":
            st.warning(f"⚠️ O ID {instance_id} não é permitido nesta versão de teste.")
            continue

        try:
            driver.get(f"https://a.letalk.com.br/inbox/instance/{instance_id}")
            st.write(f"▶️ Acessando instância {instance_id}...")

            access_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Acessar account do dono da Instância')]"))
            )
            time.sleep(2)
            access_link.click()

            WebDriverWait(driver, 10).until(EC.url_contains("/account/"))

            instance_row = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[text()='{instance_id}']/.."))
            )
            expand_icon = instance_row.find_element(By.XPATH, ".//button[@aria-label='expand row']")
            driver.execute_script("arguments[0].click();", expand_icon)

            block_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-contained') and span[text()='Bloquear assinatura']]"))
            )
            block_button.click()

            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton-contained') and span[text()='Bloquear']]"))
            )
            confirm_button.click()

            st.success(f"✅ Instância {instance_id} bloqueada com sucesso.")
            time.sleep(3)

        except TimeoutException:
            st.error(f"⏳ Tempo esgotado ao bloquear a instância {instance_id}.")
        except NoSuchElementException:
            st.error(f"❌ Elemento não encontrado para a instância {instance_id}.")
        except Exception as e:
            st.error(f"🚨 Erro inesperado na instância {instance_id}: {e}")

    driver.quit()
    st.write("✅ Processo finalizado.")

# ==== STREAMLIT UI ====

st.title("Painel de Bloqueio em Massa (Teste)")

ids_input = st.text_area("Cole os IDs separados por vírgula (ex: 7618):")
if st.button("Bloquear"):
    if ids_input.strip() == "":
        st.warning("⚠️ Por favor, insira ao menos um ID.")
    else:
        ids = [i.strip() for i in ids_input.split(",")]
        bloquear_instancias(ids)

