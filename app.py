import streamlit as st
import requests
import io
import gc
from bs4 import BeautifulSoup
import urllib.parse
import re

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# Estilo Neón para la APK
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
    .info-juego {
        background: #1a1a1a; padding: 10px; border-radius: 5px;
        border-left: 5px solid #FF5F1F; margin-bottom: 10px;
    }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- MOTOR DE DESCARGA POR PARTES DE 300MB (CORREGIDO) ---
def descargar_300mb(url_real):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://myrient.erista.me/'
    }
    TAMANO_BLOQUE = 300 * 1024 * 1024  # 300 MB
    
    try:
        # Aquí ya no habrá error porque url_real es la dirección completa
        with requests.get(url_real, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            buffer = io.BytesIO()
            descargado = 0
            barra = st.progress(0)
            status = st.empty()
            
            for chunk in r.iter_content(chunk_size=TAMANO_BLOQUE):
                if chunk:
                    buffer.write(chunk)
                    descargado += len(chunk)
                    porcentaje = min(int((descargado / total_size) * 100), 100)
                    barra.progress(porcentaje)
                    status.write(f"📥 Capturando bloque: {descargado // (1024*1024)}MB / {total_size // (1024*1024)}MB")
                    del chunk
                    gc.collect() 
            
            return buffer.getvalue()
    except Exception as e:
        st.error(f"Error al conectar con el servidor: {e}")
        return None

# --- DATOS DE CATÁLOGOS ---
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
        # Extrae los nombres de los juegos que terminen en extensiones válidas
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.rvz', '.7z', '.pkg', '.wux'))]
    except: return []

# --- INTERFAZ DE USUARIO ---
letra = st.select_slider('🎮 FILTRAR POR LETRA:', options=["TODOS", "#"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
busqueda = st.text_input("🔍 BUSCAR JUEGO ESPECÍFICO:", "").lower()

tabs = st.tabs(tab_names)
for i, tab in enumerate(tabs):
    with tab:
        juegos = obtener_lista(urls_base[i])
        # Filtrar por búsqueda de texto
        filtrados = [j for j in juegos if busqueda in j.lower()]
        # Filtrar por letra inicial
        if letra != "TODOS":
            filtrados = [j for j in filtrados if j and (j[0].isalpha() == False if letra == "#" else j.upper().startswith(letra))]
        
        # Mostrar los primeros 30 juegos para evitar lentitud
        for j in filtrados[:30]:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f'<div class="info-juego"><b>{j}</b></div>', unsafe_allow_html=True)
                with col2:
                    # Al pulsar el botón, enviamos la URL COMPLETA al motor de descarga
                    if st.button("✨ POLVOS DE DIAMANTE ✨", key=f"btn_{i}_{j}"):
                        url_final = urls_base[i] + j
                        data = descargar_300mb(url_final)
                        if data:
                            st.download_button(
                                label="💾 GUARDAR EN DISPOSITIVO", 
                                data=data, 
                                file_name=j, 
                                mime="application/octet-stream"
                            )
                            st.balloons()

st.markdown('<div style="text-align:center; padding:30px; color:#FF5F1F;">POLACO 666 | SISTEMA DE BLOQUES OK</div>', unsafe_allow_html=True)
