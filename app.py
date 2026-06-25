import streamlit as st
import os
import re
# Importante: Usamos la nueva librería de cliente
from google import genai
from google.genai.errors import APIError

# Configuración de página
st.set_page_config(page_title="Tutor de Inglés IA", page_icon="🇬🇧")

# Inicialización del cliente (igual que tu app que funciona)
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

if not api_key:
    st.error("❌ Faltando 'GEMINI_API_KEY' en los Secrets.")
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Error al inicializar el cliente: {e}")
    st.stop()

st.title("🇬🇧 Tutor de Pronunciación IA")
user_input = st.text_area("Escribe tu frase en español:")

if st.button("Traducir y Analizar"):
    if user_input:
        with st.spinner("Consultando..."):
            prompt = (
                "Eres un tutor de inglés. Responde en este formato:\n"
                "1. Inglés: [Traducción]\n"
                "2. Fonética: [Escritura intuitiva + IPA]"
            )
            try:
                # CAMBIO CLAVE: Usamos 'gemini-2.0-flash' o 'gemini-1.5-flash' 
                # con el cliente moderno
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=f"{prompt}\n{user_input}"
                )
                st.success(response.text)
            except APIError as e:
                st.error(f"Error de API: {e}")
            except Exception as e:
                st.error(f"Error inesperado: {e}")
