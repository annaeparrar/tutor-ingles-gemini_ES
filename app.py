import streamlit as st
import google.generativeai as genai

# Configuración básica
st.set_page_config(page_title="Tutor Inglés", page_icon="🇬🇧")
st.title("🇬🇧 Traductor y Tutor")

# 1. Configuración simplificada de la API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 2. Usamos 'gemini-1.5-flash' sin intentar forzar versiones beta
    # Esto utiliza la configuración predeterminada de la librería
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error en configuración inicial: {e}")
    st.stop()

# Instrucción clara
prompt_base = "Eres un tutor de inglés. Traduce al inglés y dame fonética intuitiva en español. Formato: 1. Inglés: [Texto] 2. Fonética: [Texto]."

user_input = st.text_area("Frase en español:")

if st.button("Traducir"):
    if user_input:
        try:
            # 3. Llamada estándar
            response = model.generate_content(f"{prompt_base} Frase: {user_input}")
            st.success(response.text)
        except Exception as e:
            st.error(f"Error técnico al generar contenido: {e}")
    else:
        st.warning("Escribe una frase.")
