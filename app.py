import streamlit as st
import google.generativeai as genai

# Configuración básica
st.set_page_config(page_title="Tutor Inglés", page_icon="🇬🇧")
st.title("🇬🇧 Traductor y Tutor")

# Configuración API con manejo de errores más estricto
try:
    key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=key)
    # USAMOS 'gemini-pro' (sin versiones flash o beta)
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

# Instrucción clara y concisa
prompt_base = "Traduce al inglés y dame fonética intuitiva en español. Formato: 1. Inglés: [Texto] 2. Fonética: [Texto]."

user_input = st.text_area("Frase en español:")

if st.button("Traducir"):
    if user_input:
        try:
            response = model.generate_content(f"{prompt_base} Frase: {user_input}")
            st.success(response.text)
        except Exception as e:
            st.error(f"Error técnico (posible falta de acceso al modelo): {e}")
    else:
        st.warning("Escribe una frase.")
