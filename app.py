import streamlit as st
import os
from google import genai

# Configuración básica
st.set_page_config(page_title="Tutor de Inglés IA", page_icon="🇬🇧")
st.title("🇬🇧 Tutor de Pronunciación IA")

# Inicialización segura del cliente
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

if not api_key:
    st.error("❌ Faltando 'GEMINI_API_KEY' en los Secrets.")
    st.stop()

# Inicializamos el cliente sin especificar rutas beta
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Error al inicializar el cliente: {e}")
    st.stop()

user_input = st.text_area("Escribe tu frase en español:")

if st.button("Traducir y Analizar"):
    if user_input:
        with st.spinner("Consultando..."):
            try:
                # Usamos el cliente moderno para llamar a un modelo estable
                response = client.models.generate_content(
                    model='gemini-2.0-flash', 
                    contents=f"Traduce al inglés y dame fonética: {user_input}"
                )
                st.success(response.text)
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.info("Asegúrate de que 'google-genai' esté en tu requirements.txt.")
