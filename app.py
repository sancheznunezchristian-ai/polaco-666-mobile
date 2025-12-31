import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import requests
from io import BytesIO

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# --- CSS: ESTILO POLACO 666 (OPTIMIZADO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #08090b; color: #00ffc3; }
    
    .logo-666 {
        font-family: 'Black Ops One', cursive; font-size: 55px;
        text-align: center; margin-top: 10px; color: #FF5F1F; 
        text-shadow: 2px 2px #000;
    }

    /* Tarjeta más compacta y profesional */
    .tarjeta-juego {
        background: #111;
        padding: 5px; border-radius: 10px;
        border: 2px solid #FF5F1F; margin-bottom: 20px;
        transition: 0.3s;
    }
    .tarjeta-juego:hover { transform: scale(1.02); border-color: #00ffc3; }

    .img-neon { 
        width: 100%; 
        border-radius: 5px;
        display: block;
        margin: 0 auto;
    }

    .nombre-juego-gigante {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 13px !important; color: #ffffff !important;
        text-align: center; display: block;
        padding: 8px 2px; min-height: 40px;
        text-transform: uppercase; line-height: 1.2;
    }

    .pie-pagina {
        text-align: center; font-family: 'Orbitron', sans-serif;
        color: #FF5F1F; font-size: 14px; margin-top: 50px;
        padding: 30px; border-top: 3px solid #FF5F1F;
        background: #000;
    }

    /* Ajuste de botones para que no se vean gigantes */
    .stButton > button {
        width: 100%; font-size: 12px !important;
        background: #FF5F1F !important; color: white !important;
        border: none !important;
    }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- FUNCIÓN DESCARGA ---
def hacer_magia(url_descarga, nombre_archivo):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        with requests.get(url_descarga, stream=True, headers=headers) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            progreso = st.progress(0)
            status = st.empty()
            buffer = BytesIO()
            descargado = 0
            for chunk in r.iter_content(chunk_size=1048576):
                if chunk:
                    buffer.write(chunk)
                    descargado += len(chunk)
                    if total_size > 0:
                        p = min(descargado / total_size, 1.0)
                        progreso.progress(p)
                        status.markdown(f"<p style='text-align:center; color:#00ffc3;'>⚡ {int(p*100)}% - POLVOS DE DIAMANTE ⚡</p>", unsafe_allow_html=True)
            st.balloons()
            st.download_button("💾 GUARDAR", buffer.getvalue(), nombre_archivo)
    except Exception as e: st.error(f"Error: {e}")

# --- PESTAÑAS Y URLS ---
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

# MAPEO DE BÚSQUEDA CON LOGO OBLIGATORIO
consola_real_map = {
    "Dolphin (GC)": "Nintendo GameCube official front cover art logo",
    "Dolphin (Wii)": "Nintendo Wii official front cover logo NOT ps2",
    "Cemu": "Nintendo Wii U official front cover art blue logo",
    "RPCS3": "PS3 PlayStation 3 official front cover logo",
    "Xenia": "Xbox 360 official front cover logo",
    "Xemu": "Xbox Original official front cover logo",
    "PCSX2": "PS2 PlayStation 2 official front cover logo",
    "DuckStation": "PS1 PlayStation 1 official front cover logo",
    "PPSSPP": "PSP PlayStation Portable official front cover logo",
    "Dreamcast": "Sega Dreamcast official front cover logo"
}

@st.cache_data(ttl=3600)
def obtener_lista(url):
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.7z', '.pkg', '.wux', '.rvz'))]
    except: return []

abc = ["TODOS", "#"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
letra_sel = abc[st.select_slider('🎮 FILTRO:', options=range(len(abc)))]
busq = st.text_input("🔍 BUSCAR JUEGO:", "").lower()

tabs = st.tabs(tab_names)
for i, tab in enumerate(tabs):
    with tab:
        key_pag = f"pag_{i}"
        if key_pag not in st.session_state: st.session_state[key_pag] = 1
        
        items = obtener_lista(urls_base[i])
        filtrados = [x for x in items if busq in x.lower()]
        if letra_sel != "TODOS":
            filtrados = [x for x in filtrados if x and (x[0].isalpha() == False if letra_sel == "#" else x.upper().startswith(letra_sel))]
        
        # --- 16 juegos por página y 4 COLUMNAS ---
        juegos_por_pag = 16
        total_p = max((len(filtrados)-1)//juegos_por_pag + 1, 1)

        # FLECHAS ARRIBA
        c_nav = st.columns([1,2,1])
        with c_nav[0]: 
            if st.button("⬅️ ANTERIOR", key=f"ua_{i}"):
                if st.session_state[key_pag] > 1: st.session_state[key_pag] -= 1; st.rerun()
        with c_nav[1]: st.markdown(f"<h4 style='text-align:center;'>{st.session_state[key_pag]} / {total_p}</h4>", unsafe_allow_html=True)
        with c_nav[2]:
            if st.button("SIGUIENTE ➡️", key=f"us_{i}"):
                if st.session_state[key_pag] < total_p: st.session_state[key_pag] += 1; st.rerun()

        st.divider()
        inicio = (st.session_state[key_pag] - 1) * juegos_por_pag
        
        # MOSTRAR EN 4 COLUMNAS
        cols = st.columns(4)
        for idx, juego in enumerate(filtrados[inicio : inicio + juegos_por_pag]):
            with cols[idx % 4]:
                nombre_visual = juego.split('(')[0].replace('.zip','').replace('.rvz','').replace('.7z','').replace('.iso','').replace('.pkg','').replace('.wux','').strip()
                emulador_puro = tab_names[i].split(" ", 1)[-1]
                termino = consola_real_map.get(emulador_puro, emulador_puro)
                
                # Búsqueda ultra-específica para carátulas frontales con LOGO
                url_img = f"https://www.bing.com/th?q={urllib.parse.quote(nombre_visual + ' ' + termino)}&w=350&h=500&c=7&rs=1&p=0&pid=ImgDetMain"
                
                st.markdown(f'''<div class="tarjeta-juego">
                    <img src="{url_img}" class="img-neon">
                    <span class="nombre-juego-gigante">{nombre_visual}</span>
                </div>''', unsafe_allow_html=True)
                if st.button("✨ MAGIA ✨", key=f"btn_{i}_{juego}"):
                    hacer_magia(urls_base[i] + juego, juego)

        # FLECHAS ABAJO
        st.divider()
        c_nav_b = st.columns([1,2,1])
        with c_nav_b[0]:
            if st.button("⬅️ VOLVER", key=f"ba_{i}"):
                if st.session_state[key_pag] > 1: st.session_state[key_pag] -= 1; st.rerun()
        with c_nav_b[1]: st.markdown(f"<h3 style='text-align:center;'>PÁGINA {st.session_state[key_pag]}</h3>", unsafe_allow_html=True)
        with c_nav_b[2]:
            if st.button("AVANZAR ➡️", key=f"bs_{i}"):
                if st.session_state[key_pag] < total_p: st.session_state[key_pag] += 1; st.rerun()

# --- PIE DE PÁGINA: DERECHOS ---
st.markdown("""
<div class="pie-pagina">
    <p>POLACO 666 | MULTI-REGIÓN | POLVOS DE DIAMANTE</p>
    <p style="color: #00ffc3; font-size: 14px;">
        Esta aplicación es propiedad de <b>Polaco 666</b> y es totalmente <b>sin ánimos de lucro</b>.<br>
        Dedicada a la <b>retroemulación</b>, la comunidad y la <b>conservación</b> de los mismos.
    </p>
</div>
""", unsafe_allow_html=True)
