import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import requests

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# --- CSS: ESTILO POLACO 666 (OPTIMIZADO MÓVIL) ---
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
        background: #111;
        padding: 0px; border-radius: 12px;
        border: 2px solid #FF5F1F; margin-bottom: 15px;
        overflow: hidden;
        height: 460px;
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
        text-align: center; display: flex;
        align-items: center; justify-content: center;
        padding: 8px; height: 60px;
        text-transform: uppercase; line-height: 1.1;
        background: #1a1a1a;
    }

    /* Botón tipo Polvos de Diamante */
    .stDownloadButton > button {
        width: 100% !important; height: 50px !important;
        background: #FF5F1F !important; color: white !important;
        border: none !important; font-weight: bold !important;
        font-family: 'Orbitron', sans-serif !important;
        border-radius: 0px !important;
    }
    .stDownloadButton > button:hover {
        background: #00ffc3 !important; color: black !important;
    }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- LÓGICA DE FLUJO CONTINUO (ANTI-CIERRE) ---
def obtener_stream(url):
    """Generador que descarga el archivo por trozos sin saturar la RAM"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://myrient.erista.me/'
    }
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192 * 4): # Trozos pequeños constantes
            yield chunk

# --- DATOS Y PESTAÑAS ---
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
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.7z', '.pkg', '.wux', '.rvz'))]
    except: return []

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
                nombre_visual = juego.split('(')[0].replace('.zip','').replace('.rvz','').replace('.7z','').replace('.iso','').replace('.pkg','').replace('.wux','').strip()
                consola_info = mapeo_consola_real.get(tab_names[i], "")
                
                # Imagen HD
                query_img = urllib.parse.quote(f"{nombre_visual} {consola_info} cover art -ebay")
                url_img = f"https://www.bing.com/th?q={query_img}&w=350&h=500&c=7&rs=1&p=0&pid=ImgDetMain"
                
                st.markdown(f'''
                    <div class="tarjeta-juego">
                        <div class="contenedor-img"><img src="{url_img}" class="img-neon"></div>
                        <span class="nombre-juego-gigante">{nombre_visual}</span>
                    </div>
                ''', unsafe_allow_html=True)
                
                # BOTÓN DIRECTO QUE PASA AL NAVEGADOR SIN CARGAR EN RAM
                st.download_button(
                    label="✨ POLVOS DE DIAMANTE ✨",
                    data=obtener_stream(urls_base[i] + juego),
                    file_name=juego,
                    mime="application/octet-stream",
                    key=f"dl_{i}_{idx}"
                )

st.markdown('<div style="text-align:center; color:#FF5F1F; padding:30px;">POLACO 666 | POLVOS DE DIAMANTE</div>', unsafe_allow_html=True)
