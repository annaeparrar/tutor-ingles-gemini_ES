import streamlit as st
import google.generativeai as genai

# Configuración de la página web
st.set_page_config(page_title="Tutor de Inglés IA", page_icon="🇬🇧")

st.title("🇬🇧 Traductor y Tutor de Pronunciación")
st.markdown("Escribe una frase en español para recibir su traducción y guía fonética.")

# Configuración de la API Key desde los Secrets de Streamlit
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Error: La API Key no está configurada correctamente en los Secrets.")
    st.stop()

# Configuración del modelo
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Instrucción de sistema mejorada con tus nuevos requerimientos
system_prompt = (
    "Eres un tutor de inglés experto. Recibes frases en español y devuelves una respuesta estricta con este formato: "
    "\n\n1. Frase en Inglés: [Traducción natural al inglés] "
    "\n2. Pronunciación: [Usa una escritura fonética basada en la fonética del español para que un hispanohablante lo lea natural. Si es necesario para mayor claridad, añade entre paréntesis la versión en Alfabeto Fonético Internacional (IPA)]."
    "\n\nNo escribas saludos, explicaciones gramaticales ni nada adicional."
)

# Interfaz de usuario
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
        st.warning("Por favor, ingresa una frase antes de hacer clic en traducir.")
