import streamlit as st
import requests
import gc
from bs4 import BeautifulSoup
import urllib.parse
import re

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 APK Stable", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #08090b; color: #00ffc3; }
    .logo-666 {
        font-family: 'Black Ops One', cursive; font-size: 35px;
        text-align: center; color: #FF5F1F; text-shadow: 2px 2px #000;
        margin: 20px 0;
    }
    .stButton>button {
        width: 100%; background: #FF5F1F !important;
        color: white !important; font-family: 'Orbitron', sans-serif;
        font-weight: 900; border: 2px solid #00ffc3 !important;
        padding: 15px !important; border-radius: 5px !important;
    }
    .nombre-juego {
        background: #1a1a1a; padding: 10px; border-radius: 5px;
        border-left: 5px solid #FF5F1F; margin-bottom: 5px;
        font-family: 'Orbitron', sans-serif; font-size: 12px;
    }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- MOTOR DE FLUJO (STREAMING) PARA EVITAR CRASHEO EN DISCO ---
# Esta es la "tubería" que envía trozos al móvil sin llenar la RAM
def generar_descarga_por_partes(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://myrient.erista.me/'
    }
    try:
        def flujo():
            with requests.get(url, headers=headers, stream=True, timeout=60) as r:
                r.raise_for_status()
                # Enviamos trozos de 5MB constantes al móvil
                for chunk in r.iter_content(chunk_size=5 * 1024 * 1024):
                    if chunk:
                        yield chunk
                        gc.collect() # Limpieza automática de RAM
        return flujo
    except:
        return None

# --- CATÁLOGOS (NOMBRES DE EMULADORES) ---
tab_names = ["Dolphin (GC)", "Dolphin (Wii)", "Cemu", "RPCS3", "Xenia", "Xemu", "PCSX2", "DuckStation", "PPSSPP", "Dreamcast"]
urls_base = [
    "https://myrient.erista.me/files/Redump/Nintendo%20-%20GameCube%20-%20NKit%20RVZ%20%5Bzstd-19-128k%5D/",
    "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20-%20NKit%20RVZ%20%5Bzstd-19-128k%5D/",
    "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20U%20-%20WUX/",
    "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%203/",
    "https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox%20360/",
    "https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox/",
    "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/",
    "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/",
    "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%20Portable/",
    "https://myrient.erista.me/files/Redump/Sega%20-%20Dreamcast/"
]

@st.cache_data(ttl=3600)
def obtener_lista(url):
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.rvz', '.7z', '.pkg', '.wux'))]
    except: return []

# --- INTERFAZ ---
letra = st.select_slider('🎮 FILTRO:', options=["TODOS", "#"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
busqueda = st.text_input("🔍 BUSCAR JUEGO:", "").lower()

tabs = st.tabs(tab_names)
for i, tab in enumerate(tabs):
    with tab:
        juegos = obtener_lista(urls_base[i])
        filtrados = [j for j in juegos if busqueda in j.lower()]
        if letra != "TODOS":
            filtrados = [j for j in filtrados if j and (j[0].isalpha() == False if letra == "#" else j.upper().startswith(letra))]
        
        for j in filtrados[:25]:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f'<div class="nombre-juego">{j}</div>', unsafe_allow_html=True)
                with col2:
                    # CLAVE: Pasamos la función generadora al botón
                    # Esto hace que el archivo fluya de 5MB en 5MB al disco
                    st.download_button(
                        label="✨ POLVOS DE DIAMANTE ✨",
                        data=generar_descarga_por_partes(urls_base[i] + j)(), 
                        file_name=j,
                        mime="application/octet-stream",
                        key=f"dl_{i}_{j}"
                    )

st.markdown('<div style="text-align:center; padding:30px; color:#FF5F1F;">POLACO 666 | RESET COMPLETADO</div>', unsafe_allow_html=True)       

