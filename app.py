import streamlit as st
import requests
import io
import gc
from bs4 import BeautifulSoup
import urllib.parse

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #08090b; color: #00ffc3; }
    .logo-666 { font-family: 'Black Ops One', cursive; font-size: 35px; text-align: center; color: #FF5F1F; text-shadow: 2px 2px #000; margin: 20px 0; }
    .stButton>button { width: 100%; background: #FF5F1F !important; color: white !important; font-family: 'Orbitron', sans-serif; font-weight: 900; border: 2px solid #00ffc3 !important; padding: 15px !important; }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- MOTOR DE DESCARGA COMPATIBLE (ANTI-CRASH) ---
def motor_descarga_estable(url):
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://myrient.erista.me/'}
    try:
        with requests.get(url, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            
            # Usamos BytesIO para recibir los bloques
            b_io = io.BytesIO()
            progreso = st.progress(0)
            status_text = st.empty()
            
            descargado = 0
            # Bloques de 300MB para eficiencia
            for chunk in r.iter_content(chunk_size=300 * 1024 * 1024):
                if chunk:
                    b_io.write(chunk)
                    descargado += len(chunk)
                    # Actualizar barra
                    porcentaje = min(int((descargado / total_size) * 100), 100)
                    progreso.progress(porcentaje)
                    status_text.write(f"📥 Capturando bloque: {descargado // (1024*1024)}MB / {total_size // (1024*1024)}MB")
                    del chunk
                    gc.collect() # Limpiar RAM
            
            # IMPORTANTE: Convertimos a bytes al final para Streamlit 3.13
            final_data = b_io.getvalue()
            b_io.close()
            return final_data
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- CONFIGURACIÓN DE CATÁLOGOS ---
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
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.rvz', '.7z', '.pkg', '.wux'))]
    except: return []

busqueda = st.text_input("🔍 BUSCAR JUEGO:", "").lower()
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs):
    with tab:
        juegos = obtener_lista(urls_base[i])
        filtrados = [j for j in juegos if busqueda in j.lower()]
        for j in filtrados[:10]: # Muestra 10 para que cargue rápido en móvil
            col1, col2 = st.columns([3, 1])
            with col1: st.write(f"🎮 {j}")
            with col2:
                # El botón ahora ejecuta la descarga primero y luego habilita el guardado
                if st.button("✨ POLVOS DE DIAMANTE ✨", key=f"btn_{i}_{j}"):
                    with st.spinner("Preparando archivo..."):
                        data_juego = motor_descarga_estable(urls_base[i] + j)
                        if data_juego:
                            st.download_button(
                                label="💾 GUARDAR AHORA",
                                data=data_juego,
                                file_name=j,
                                mime="application/octet-stream",
                                key=f"dl_{i}_{j}"
                            )
                            st.balloons()

st.markdown('<div style="text-align:center; padding:20px; color:#FF5F1F;">POLACO 666 | VERSIÓN 3.13 OK</div>', unsafe_allow_html=True)
