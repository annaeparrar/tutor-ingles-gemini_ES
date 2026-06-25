import streamlit as st
import re
import os
import google.generativeai as genai

# 1. Configuración de la página (Debe ser lo primero)
st.set_page_config(
    page_title="Tutor de Inglés IA",
    page_icon="🇬🇧",
    layout="centered"
)

# 2. Estilos CSS
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #111111; margin-bottom: 5px; }
    .subtitle { font-size: 14px; color: #666666; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# 3. Función de extracción
def extract_section(text, header):
    pattern = rf"{header}:([\s\S]*?)(?=1\.|2\.||$)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""

# 4. Configuración de API (Forzamos modelo estable 'gemini-pro')
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

if not api_key:
    st.error("❌ API Key no configurada en los Secrets.")
    st.stop()

try:
    genai.configure(api_key=api_key)
    # Usamos 'gemini-pro' porque es el modelo más estable y menos propenso a errores 404
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"❌ Error al inicializar: {e}")
    st.stop()

# 5. Interface
st.markdown('<div class="main-title">🇬🇧 Tutor de Pronunciación IA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Obtén traducciones naturales y guías fonéticas.</div>', unsafe_allow_html=True)

user_input = st.text_area("Escribe tu frase en español:", placeholder="Ej: Me gustaría reservar una mesa", height=100)

if st.button("Traducir y Analizar", type="primary", use_container_width=True):
    if not user_input:
        st.warning("Por favor, ingresa una frase.")
    else:
        with st.spinner("Consultando al tutor..."):
            system_prompt = (
                "Eres un tutor de inglés. Responde estrictamente en este formato:\n"
                "1. Inglés: [Traducción natural]\n"
                "2. Fonética: [Fonética intuitiva en español. Añade IPA entre paréntesis si es necesario]."
            )
            
            try:
                # Llamada directa al modelo
                response = model.generate_content(f"{system_prompt}\n\nFrase: {user_input}")
                generated_text = response.text
                
                ingles = extract_section(generated_text, "1. Inglés")
                fonetica = extract_section(generated_text, "2. Fonética")
                
                st.markdown("## ✨ Resultados")
                st.subheader("🇺🇸 Traducción")
                st.success(ingles if ingles else generated_text)
                
                if fonetica:
                    st.subheader("🗣️ Guía de Pronunciación")
                    st.code(fonetica, language=None)
                
                # Botón de descarga
                full_result = f"FRASE: {user_input}\n\nINGLÉS: {ingles}\n\nFONÉTICA: {fonetica}"
                st.download_button("📥 Exportar lección (.txt)", data=full_result, file_name="traduccion.txt")

            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.info("Nota: Si el error persiste, asegúrate de que tu cuenta de Google Cloud tiene habilitado el servicio 'Generative Language API'.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #aaa; font-size: 12px;'>Powered by Gemini AI</p>", unsafe_allow_html=True)
