import streamlit as st

def bloquear_instancias(instance_ids):
    for instance_id in instance_ids:
        st.write(f"🔒 Bloqueando instância {instance_id}...")
        # Aqui você cola a lógica do Selenium adaptada
        # Por enquanto, vamos simular:
        st.success(f"Instância {instance_id} bloqueada com sucesso!")

st.title("Painel de Bloqueio - Letalk")

ids_input = st.text_area("Cole os IDs das instâncias (separados por vírgula):", "")
if st.button("Bloquear"):
    if ids_input.strip() == "":
        st.warning("Por favor, insira ao menos um ID.")
    else:
        ids = [id.strip() for id in ids_input.split(",")]
        bloquear_instancias(ids)
