import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Tutor de Inglés IA", page_icon="🇬🇧")

st.title("🇬🇧 Traductor y Tutor de Pronunciación")

# Configuración de la API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Error: Configura tu API Key en los 'Secrets' de Streamlit.")
    st.stop()

# CAMBIO CRÍTICO: Usaremos 'gemini-pro' para máxima compatibilidad
model = genai.GenerativeModel(model_name="gemini-pro")

system_prompt = (
    "Eres un tutor de inglés experto. Recibes frases en español y devuelves una respuesta estricta con este formato: "
    "\n\n1. Frase en Inglés: [Traducción natural al inglés] "
    "\n2. Pronunciación: [Usa una escritura fonética basada en el español para que sea intuitivo. Si es necesario, añade entre paréntesis la versión en Alfabeto Fonético Internacional (IPA)]."
    "\n\nNo escribas saludos ni explicaciones, solo entrega el resultado solicitado."
)

user_input = st.text_area("Escribe aquí tu frase en español:")

if st.button("Traducir"):
    if user_input:
        with st.spinner('Consultando a Gemini...'):
            try:
                full_prompt = f"{system_prompt}\n\nFrase a traducir: {user_input}"
                response = model.generate_content(full_prompt)
                st.markdown("---")
                st.markdown("### Resultado:")
                st.success(response.text)
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Por favor, ingresa una frase primero.")
