import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import requests
import re

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# --- CSS: ESTILO POLACO 666 (EFECTOS + BOTÓN RÁPIDO) ---
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
        transition: all 0.3s ease-in-out;
    }
    .tarjeta-juego:hover {
        transform: translateY(-10px);
        border-color: #00ffc3;
        box-shadow: 0px 10px 25px rgba(0, 255, 195, 0.4);
    }

    .contenedor-img {
        width: 100%; height: 280px;
        background: #000; display: flex;
        align-items: center; justify-content: center;
        overflow: hidden;
    }

    .img-neon { 
        max-width: 100%; max-height: 100%; 
        object-fit: contain; 
        transition: transform 0.5s ease;
    }
    .tarjeta-juego:hover .img-neon { transform: scale(1.15); }

    .nombre-juego-gigante {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 11px !important; color: #ffffff !important;
        text-align: center; padding: 10px; height: 85px;
        text-transform: uppercase; background: #1a1a1a;
        display: flex; align-items: center; justify-content: center;
        border-top: 1px solid #333;
    }

    .btn-polvos {
        display: block; width: 100%; padding: 20px 0;
        background: #FF5F1F; color: white !important;
        text-align: center; text-decoration: none !important;
        font-family: 'Orbitron', sans-serif; font-weight: 900;
        font-size: 16px; border-top: 2px solid #00ffc3;
    }
    .btn-polvos:hover { background: #00ffc3; color: black !important; }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE CONEXIÓN RÁPIDA (SESSION PERSISTENCE) ---
if 'session' not in st.session_state:
    st.session_state.session = requests.Session()
    # Cabeceras para saltar el límite de velocidad de los servidores
    st.session_state.session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Referer': 'https://myrient.erista.me/',
        'Accept-Encoding': 'identity'
    })

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
        r = st.session_state.session.get(url, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.7z', '.pkg', '.wux', '.rvz'))]
    except: return []

# --- FILTROS ---
letra_sel = st.select_slider('🎮 FILTRO LETRA:', options=["TODOS", "#"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
busq = st.text_input("🔍 BUSCAR TÍTULO:", "").lower()

tabs = st.tabs(tab_names)
for i, tab in enumerate(tabs):
    with tab:
        items = obtener_lista(urls_base[i])
        filtrados = [x for x in items if busq in x.lower()]
        if letra_sel != "TODOS":
            filtrados = [x for x in filtrados if x and (x[0].isalpha() == False if letra_sel == "#" else x.upper().startswith(letra_sel))]
        
        cols = st.columns(2)
        for idx, juego in enumerate(filtrados[:30]):
            with cols[idx % 2]:
                # Nombre con región para el usuario
                nombre_visual = re.sub(r'\.(zip|rvz|7z|iso|pkg|wux)$', '', juego, flags=re.I)
                
                # Nombre para buscar imagen
                nombre_img = nombre_visual.split('(')[0].strip()
                consola = mapeo_consola_real.get(tab_names[i], "")
                url_img = f"https://www.bing.com/th?q={urllib.parse.quote(nombre_img + ' ' + consola + ' box art')}&w=400&h=550&c=7"
                
                enlace_directo = urls_base[i] + juego
                
                st.markdown(f'''
                    <div class="tarjeta-juego">
                        <div class="contenedor-img"><img src="{url_img}" class="img-neon"></div>
                        <span class="nombre-juego-gigante">{nombre_visual}</span>
                        <a href="{enlace_directo}" target="_self" class="btn-polvos">✨ POLVOS DE DIAMANTE ✨</a>
                    </div>
                ''', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#FF5F1F; padding:30px;">POLACO 666 | DESCARGA MÁXIMA VELOCIDAD</div>', unsafe_allow_html=True)
