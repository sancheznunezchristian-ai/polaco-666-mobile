import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import requests
import re

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# --- CSS: ESTILO POLACO 666 CON EFECTOS RECUPERADOS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #08090b; color: #00ffc3; }
    
    .logo-666 {
        font-family: 'Black Ops One', cursive; font-size: 35px;
        text-align: center; margin: 15px 0; color: #FF5F1F; 
        text-shadow: 2px 2px #000;
    }

    /* TARJETA CON EFECTO ZOOM Y LUZ NEÓN */
    .tarjeta-juego {
        background: #111;
        padding: 0px; border-radius: 12px;
        border: 2px solid #FF5F1F; margin-bottom: 20px;
        overflow: hidden; height: 490px;
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
    .tarjeta-juego:hover .img-neon {
        transform: scale(1.15);
    }

    .nombre-juego-gigante {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 11px !important; color: #ffffff !important;
        text-align: center; padding: 10px; height: 80px;
        text-transform: uppercase; background: #1a1a1a;
        display: flex; align-items: center; justify-content: center;
    }

    .btn-disco-directo {
        display: block; width: 100%; padding: 18px 0;
        background: #FF5F1F; color: white !important;
        text-align: center; text-decoration: none !important;
        font-family: 'Orbitron', sans-serif; font-weight: 900;
        font-size: 15px; border-top: 2px solid #00ffc3;
        transition: 0.3s ease;
    }
    .btn-disco-directo:hover { background: #00ffc3; color: black !important; }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

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
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.7z', '.pkg', '.wux', '.rvz'))]
    except: return []

# --- LÓGICA DE DESCARGA CON BARRA SINCRONIZADA ---
def descargar_con_progreso(url, nombre):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    barra = st.progress(0)
    estado = st.empty()
    buffer = b""
    descargado = 0
    
    for chunk in response.iter_content(chunk_size=1024*1024):
        if chunk:
            buffer += chunk
            descargado += len(chunk)
            porcentaje = int((descargado / total_size) * 100)
            barra.progress(porcentaje)
            estado.write(f"📥 Cargando: {porcentaje}%")
    return buffer

# --- INTERFAZ ---
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
        for idx, juego in enumerate(filtrados[:20]):
            with cols[idx % 2]:
                # MANTENEMOS LA REGIÓN EN EL NOMBRE (Captura todo hasta el final antes de la extensión)
                nombre_limpio = re.sub(r'\.(zip|rvz|7z|iso|pkg|wux)$', '', juego, flags=re.I)
                
                # Para la búsqueda de imagen usamos el nombre sin paréntesis para que sea más exacta
                nombre_para_img = nombre_limpio.split('(')[0].strip()
                consola_info = mapeo_consola_real.get(tab_names[i], "")
                
                busqueda_img = urllib.parse.quote(f"{nombre_para_img} {consola_info} box art")
                url_img = f"https://www.bing.com/th?q={busqueda_img}&w=400&h=550&c=7&rs=1&p=0&pid=ImgDetMain"
                
                st.markdown(f'''
                    <div class="tarjeta-juego">
                        <div class="contenedor-img"><img src="{url_img}" class="img-neon"></div>
                        <span class="nombre-juego-gigante">{nombre_limpio}</span>
                    </div>
                ''', unsafe_allow_html=True)
                
                # PROCESO DE "POLVOS DE DIAMANTE" SINCRONIZADO
                if st.button(f"✨ POLVOS DE DIAMANTE ✨", key=f"btn_{i}_{idx}"):
                    archivo_bytes = descargar_con_progreso(urls_base[i] + juego, juego)
                    st.download_button(
                        label="💾 GUARDAR EN DISPOSITIVO",
                        data=archivo_bytes,
                        file_name=juego,
                        mime="application/octet-stream",
                        key=f"dl_{i}_{idx}"
                    )
                    st.balloons()

st.markdown('<div style="text-align:center; color:#FF5F1F; padding:30px;">POLACO 666 | REGIÓN & DISCO</div>', unsafe_allow_html=True)
