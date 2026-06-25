import streamlit as st
import google.generativeai as genai

# Configuración de página
st.set_page_config(page_title="Tutor Inglés IA", page_icon="🇬🇧")

# Configuración de Gemini desde Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("Error: API Key no configurada en los Secrets de Streamlit.")
    st.stop()

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Eres un tutor de inglés. Recibes frases en español y devuelves "
        "exactamente este formato: "
        "1. Frase en Inglés: [Traducción natural] "
        "2. Pronunciación: [Fonética para hispanohablantes]. "
        "No incluyas explicaciones adicionales."
    )
)

st.title("🇬🇧 Traductor y Tutor de Pronunciación")
user_input = st.text_area("Escribe aquí tu frase en español:")

if st.button("Traducir"):
    if user_input:
        with st.spinner('Procesando...'):
            response = model.generate_content(user_input)
            st.markdown("### Resultado:")
            st.success(response.text)
    else:
        st.warning("Escribe una frase primero.")