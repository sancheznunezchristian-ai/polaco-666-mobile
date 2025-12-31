    import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import requests

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# --- CSS: ESTILO POLACO 666 OPTIMIZADO PARA ESCRITURA EN DISCO MÓVIL ---
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
        overflow: hidden; height: 460px;
        display: flex; flex-direction: column;
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
        text-align: center; padding: 10px; height: 60px;
        text-transform: uppercase; background: #1a1a1a;
        display: flex; align-items: center; justify-content: center;
    }

    /* BOTÓN DE DESCARGA DIRECTA AL DISCO DEL DISPOSITIVO */
    .btn-disco-directo {
        display: block;
        width: 100%;
        padding: 18px 0;
        background: #FF5F1F;
        color: white !important;
        text-align: center;
        text-decoration: none !important;
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 15px;
        border-top: 2px solid #00ffc3;
        transition: 0.3s ease;
    }
    .btn-disco-directo:active {
        background: #00ffc3;
        color: black !important;
        transform: scale(0.98);
    }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- LISTADO DE EMULADORES (NOMBRES SEGÚN CATÁLOGO) ---
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

# --- FILTROS Y BÚSQUEDA ---
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
                nombre_visual = juego.split('(')[0].replace('.zip','').replace('.rvz','').replace('.7z','').replace('.iso','').replace('.pkg','').replace('.wux','').strip()
                consola_info = mapeo_consola_real.get(tab_names[i], "")
                
                # Imagen HD
                busqueda_img = urllib.parse.quote(f"{nombre_visual} {consola_info} official game cover art -ebay")
                url_img = f"https://www.bing.com/th?q={busqueda_img}&w=400&h=550&c=7&rs=1&p=0&pid=ImgDetMain"
                
                # EL BOTÓN DE DISCO DIRECTO
                # Usamos el atributo 'download' para que el navegador del móvil lo guarde en disco directamente
                enlace_directo = urls_base[i] + juego
                
                st.markdown(f'''
                    <div class="tarjeta-juego">
                        <div class="contenedor-img"><img src="{url_img}" class="img-neon"></div>
                        <span class="nombre-juego-gigante">{nombre_visual}</span>
                        <a href="{enlace_directo}" download="{juego}" target="_self" class="btn-disco-directo">✨ POLVOS DE DIAMANTE ✨</a>
                    </div>
                ''', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:#FF5F1F; padding:30px;">POLACO 666 | POLVOS DE DIAMANTE</div>', unsafe_allow_html=True)
