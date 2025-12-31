import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import requests

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# --- CSS: ESTILO NEÓN Y EFECTOS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #08090b; color: #00ffc3; }
    
    .logo-666 {
        font-family: 'Black Ops One', cursive; font-size: 38px;
        text-align: center; margin: 15px 0; color: #FF5F1F; 
        text-shadow: 2px 2px #000;
    }

    .tarjeta-juego {
        background: #111; padding: 0px; border-radius: 12px;
        border: 2px solid #FF5F1F; margin-bottom: 20px;
        overflow: hidden; height: 460px; transition: 0.3s;
    }
    .tarjeta-juego:hover {
        transform: translateY(-5px); border-color: #00ffc3;
        box-shadow: 0px 5px 15px rgba(0, 255, 195, 0.3);
    }

    .contenedor-img {
        width: 100%; height: 280px; background: #000;
        display: flex; align-items: center; justify-content: center;
    }

    .img-neon { 
        max-width: 100%; max-height: 100%; object-fit: contain;
        transition: 0.5s;
    }
    .tarjeta-juego:hover .img-neon { transform: scale(1.1); }

    .nombre-juego-gigante {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 11px !important; color: #ffffff !important;
        text-align: center; padding: 10px; height: 60px;
        text-transform: uppercase; background: #1a1a1a;
    }

    .stProgress > div > div > div > div { background-color: #FF5F1F; }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- LISTADO ---
tab_names = ["🟣 Dolphin (GC)", "🔴 Dolphin (Wii)", "🔴 Cemu", "🔵 RPCS3", "🟢 Xenia", "🟢 Xemu", "🔵 PCSX2", "🔵 DuckStation", "🔵 PPSSPP", "🟠 Dreamcast"]
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
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.7z', '.rvz', '.pkg'))]
    except: return []

# --- LÓGICA DE DESCARGA SINCRONIZADA ---
def descargar_a_disco(url_file, file_name):
    # Usamos stream=True para no cargar el archivo en RAM de golpe
    response = requests.get(url_file, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    barra_progreso = st.progress(0)
    texto_estado = st.empty()
    
    bytes_descargados = 0
    # Creamos un contenedor de bytes para ir guardando
    buffer = b""
    
    for chunk in response.iter_content(chunk_size=1024 * 1024): # Bloques de 1MB
        if chunk:
            buffer += chunk
            bytes_descargados += len(chunk)
            porcentaje = int((bytes_descargados / total_size) * 100)
            barra_progreso.progress(porcentaje)
            texto_estado.text(f"📥 Descargando: {porcentaje}% ({bytes_descargados // (1024*1024)}MB / {total_size // (1024*1024)}MB)")
    
    return buffer

# --- INTERFAZ ---
busq = st.text_input("🔍 BUSCAR JUEGO:", "").lower()
tabs = st.tabs(tab_names)

for i, tab in enumerate(tabs):
    with tab:
        items = obtener_lista(urls_base[i])
        filtrados = [x for x in items if busq in x.lower()][:10]
        
        cols = st.columns(2)
        for idx, juego in enumerate(filtrados):
            with cols[idx % 2]:
                nombre_visual = juego.split('(')[0].strip()
                # URL de imagen
                url_img = f"https://www.bing.com/th?q={urllib.parse.quote(nombre_visual + ' box art')}&w=300&h=400&c=7"
                
                st.markdown(f'''
                    <div class="tarjeta-juego">
                        <div class="contenedor-img"><img src="{url_img}" class="img-neon"></div>
                        <span class="nombre-juego-gigante">{nombre_visual}</span>
                    </div>
                ''', unsafe_allow_html=True)
                
                # BOTÓN QUE ACTIVA LA DESCARGA Y LA BARRA
                if st.button(f"✨ POLVOS DE DIAMANTE ✨", key=f"btn_{i}_{idx}"):
                    datos = descargar_a_disco(urls_base[i] + juego, juego)
                    st.download_button(
                        label="✅ GUARDAR EN DISPOSITIVO",
                        data=datos,
                        file_name=juego,
                        mime="application/octet-stream",
                        key=f"dl_{i}_{idx}"
                    )
                    st.balloons()

st.markdown('<div style="text-align:center; color:#FF5F1F; padding:30px;">POLACO 666 | SINCRONIZADO</div>', unsafe_allow_html=True)
