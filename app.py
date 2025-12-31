import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import requests
import re

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# --- CSS: ESTILO POLACO 666 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #08090b; color: #00ffc3; }
    
    .logo-666 {
        font-family: 'Black Ops One', cursive; font-size: 35px;
        text-align: center; margin: 15px 0; color: #FF5F1F; 
        text-shadow: 2px 2px #000;
    }

    .tarjeta-juego {
        background: #111;
        padding: 0px; border-radius: 12px;
        border: 2px solid #FF5F1F; margin-bottom: 20px;
        overflow: hidden; height: 500px;
        display: flex; flex-direction: column;
        transition: 0.3s;
    }

    .contenedor-img {
        width: 100%; height: 280px;
        background: #000; display: flex;
        align-items: center; justify-content: center;
    }

    .img-neon { max-width: 100%; max-height: 100%; object-fit: contain; }

    .nombre-juego-gigante {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 11px !important; color: #ffffff !important;
        text-align: center; padding: 10px; height: 85px;
        text-transform: uppercase; background: #1a1a1a;
        display: flex; align-items: center; justify-content: center;
    }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE CABECERAS (Referer Impersonation) ---
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://myrient.erista.me/'
}

# --- LISTADO DE EMULADORES ---
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

mapeo_consola_real = {
    "🟣 Dolphin (GC)": "Nintendo GameCube", "🔴 Dolphin (Wii)": "Nintendo Wii", "🔴 Cemu": "Nintendo Wii U",
    "🔵 RPCS3": "Sony PlayStation 3", "🟢 Xenia": "Microsoft Xbox 360", "🟢 Xemu": "Microsoft Xbox Original",
    "🔵 PCSX2": "Sony PlayStation 2", "🔵 DuckStation": "Sony PlayStation 1", "🔵 PPSSPP": "Sony PSP",
    "🟠 Dreamcast": "Sega Dreamcast"
}

@st.cache_data(ttl=3600)
def obtener_lista(url):
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.7z', '.pkg', '.wux', '.rvz'))]
    except: return []

# --- FUNCIÓN DE DESCARGA INTERNA (TUNEL) ---
def descargar_a_app(url_file):
    # Streamlit descarga desde Myrient
    r = requests.get(url_file, headers=headers, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    
    barra = st.progress(0)
    texto = st.empty()
    
    buffer = b""
    descargado = 0
    
    for chunk in r.iter_content(chunk_size=1024*1024): # Bloques de 1MB
        if chunk:
            buffer += chunk
            descargado += len(chunk)
            # Calculamos el % real
            porcentaje = int((descargado / total_size) * 100)
            barra.progress(porcentaje)
            texto.write(f"📥 Capturando en la App: {porcentaje}%")
            
    return buffer

# --- INTERFAZ ---
letra_sel = st.select_slider('🎮 FILTRO:', options=["TODOS", "#"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
busq = st.text_input("🔍 BUSCAR:", "").lower()

tabs = st.tabs(tab_names)
for i, tab in enumerate(tabs):
    with tab:
        items = obtener_lista(urls_base[i])
        filtrados = [x for x in items if busq in x.lower()]
        if letra_sel != "TODOS":
            filtrados = [x for x in filtrados if x and (x[0].isalpha() == False if letra_sel == "#" else x.upper().startswith(letra_sel))]
        
        cols = st.columns(2)
        for idx, juego in enumerate(filtrados[:20]):
            with cols[idx % 2]:
                nombre_visual = re.sub(r'\.(zip|rvz|7z|iso|pkg|wux)$', '', juego, flags=re.I)
                nombre_img = nombre_visual.split('(')[0].strip()
                consola = mapeo_consola_real.get(tab_names[i], "")
                url_img = f"https://www.bing.com/th?q={urllib.parse.quote(nombre_img + ' ' + consola + ' box art')}&w=400&h=550&c=7"
                
                st.markdown(f'''
                    <div class="tarjeta-juego">
                        <div class="contenedor-img"><img src="{url_img}" class="img-neon"></div>
                        <span class="nombre-juego-gigante">{nombre_visual}</span>
                    </div>
                ''', unsafe_allow_html=True)
                
                # BOTÓN QUE ACTIVA EL TÚNEL
                if st.button(f"✨ POLVOS DE DIAMANTE ✨", key=f"btn_{i}_{idx}"):
                    # Fase 1: La App descarga de Myrient a alta velocidad
                    archivo_datos = descargar_a_app(urls_base[i] + juego)
                    
                    # Fase 2: La App te entrega el archivo a ti (Instantáneo)
                    st.download_button(
                        label="💾 GUARDAR EN DISPOSITIVO",
                        data=archivo_datos,
                        file_name=juego,
                        mime="application/octet-stream",
                        key=f"save_{i}_{idx}"
                    )
                    st.balloons()

st.markdown('<div style="text-align:center; color:#FF5F1F; padding:30px;">POLACO 666 | MODO TÚNEL ACTIVADO</div>', unsafe_allow_html=True)
