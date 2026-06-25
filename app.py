import streamlit as st
import re
import os
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(
    page_title="Tutor de Inglés IA",
    page_icon="🇬🇧",
    layout="centered"
)

# 2. Estilos CSS personalizados
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #111111; margin-bottom: 5px; }
    .subtitle { font-size: 14px; color: #666666; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# 3. Función auxiliar para extraer secciones
def extract_section(text, header):
    pattern = rf"{header}:([\s\S]*?)(?=1\.|2\.||$)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""

# 4. Inicialización Segura de la API Key
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

if not api_key:
    st.error("❌ Faltando la configuración de 'GEMINI_API_KEY' en los Secrets.")
    st.stop()

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"❌ Error al inicializar Gemini: {e}")
    st.stop()

# 5. Interface del Usuario
st.markdown('<div class="main-title">🇬🇧 Tutor de Pronunciación IA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Obtén traducciones naturales y guías fonéticas precisas.</div>', unsafe_allow_html=True)

user_input = st.text_area("Escribe tu frase en español:", placeholder="Ej: Me gustaría reservar una mesa", height=100)

# 6. Lógica de Generación
if st.button("Traducir y Analizar", type="primary", use_container_width=True):
    if not user_input:
        st.warning("Por favor, ingresa una frase.")
    else:
        with st.spinner("Consultando al tutor..."):
            system_prompt = (
                "Eres un tutor de inglés experto. Recibes frases en español y devuelves una respuesta estricta con este formato: "
                "\n\n1. Inglés: [Traducción natural]"
                "\n2. Fonética: [Escritura fonética intuitiva en español. Añade IPA entre paréntesis si ayuda]."
            )
            
            try:
                response = model.generate_content(f"{system_prompt}\n\nFrase: {user_input}")
                generated_text = response.text
                
                # Extracción
                ingles = extract_section(generated_text, "1. Inglés")
                fonetica = extract_section(generated_text, "2. Fonética")
                
                # Mostrar resultados con el estilo del código que te gusta
                st.markdown("## ✨ Resultados")
                
                if ingles:
                    st.subheader("🇺🇸 Traducción")
                    st.success(ingles)
                
                if fonetica:
                    st.subheader("🗣️ Guía de Pronunciación")
                    st.code(fonetica, language=None)
                
                # Botón de descarga
                full_result = f"FRASE: {user_input}\n\nINGLÉS:\n{ingles}\n\nFONÉTICA:\n{fonetica}"
                st.download_button("📥 Exportar lección (.txt)", data=full_result, file_name="traduccion.txt")

            except Exception as e:
                st.error(f"Error al conectar con la IA: {e}")

# 7. Pie de página
st.markdown("---")
st.markdown("<p style='text-align: center; color: #aaa; font-size: 12px;'>Powered by Gemini AI • Tutor de Inglés PRO</p>", unsafe_allow_html=True)
