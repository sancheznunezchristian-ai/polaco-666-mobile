import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import requests
from io import BytesIO

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# --- CSS: ESTILO POLACO 666 (CALIDAD HD Y DISEÑO LIMPIO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #08090b; color: #00ffc3; }
    
    .logo-666 {
        font-family: 'Black Ops One', cursive; font-size: 55px;
        text-align: center; margin-top: 10px; color: #FF5F1F; 
        text-shadow: 2px 2px #000;
    }

    .tarjeta-juego {
        background: #111;
        padding: 0px; border-radius: 12px;
        border: 2px solid #FF5F1F; margin-bottom: 25px;
        transition: 0.3s;
        overflow: hidden;
        height: 520px; /* Altura fija para alineación perfecta */
    }
    .tarjeta-juego:hover { transform: scale(1.03); border-color: #00ffc3; box-shadow: 0px 0px 15px #00ffc3; }

    .contenedor-img {
        width: 100%;
        height: 400px;
        background: #000;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .img-neon { 
        max-width: 100%;
        max-height: 100%;
        object-fit: contain; /* Mantiene la proporción original sin deformar */
    }

    .nombre-juego-gigante {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 13px !important; color: #ffffff !important;
        text-align: center; display: flex;
        align-items: center; justify-content: center;
        padding: 10px; height: 70px;
        text-transform: uppercase; line-height: 1.2;
        background: #1a1a1a;
    }

    .pie-pagina {
        text-align: center; font-family: 'Orbitron', sans-serif;
        color: #FF5F1F; font-size: 14px; margin-top: 50px;
        padding: 30px; border-top: 3px solid #FF5F1F;
        background: #000;
    }

    .stButton > button {
        width: 100%; font-size: 14px !important;
        background: #FF5F1F !important; color: white !important;
        border: none !important; font-weight: bold !important;
    }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- FUNCIÓN DESCARGA (PERSISTENTE) ---
def hacer_magia(url_descarga, nombre_archivo):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        with requests.get(url_descarga, stream=True, headers=headers) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            progreso = st.progress(0)
            status = st.empty()
            buffer = BytesIO()
            descargado = 0
            for chunk in r.iter_content(chunk_size=1048576): # 1MB chunks
                if chunk:
                    buffer.write(chunk)
                    descargado += len(chunk)
                    if total_size > 0:
                        p = min(descargado / total_size, 1.0)
                        progreso.progress(p)
                        status.markdown(f"<p style='text-align:center; color:#00ffc3;'>⚡ {int(p*100)}% - POLVOS DE DIAMANTE ⚡</p>", unsafe_allow_html=True)
            st.balloons()
            st.download_button("💾 GUARDAR JUEGO", buffer.getvalue(), nombre_archivo)
    except Exception as e: st.error(f"Error en la descarga: {e}")

# --- PESTAÑAS (NOMBRES DE EMULADORES) ---
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

# --- MAPEO PARA BÚSQUEDA HD (CONSOLA REAL) ---
# Esto evita que busque "RPCS3" y busque "PlayStation 3"
mapeo_consola_real = {
    "🟣 Dolphin (GC)": "Nintendo GameCube",
    "🔴 Dolphin (Wii)": "Nintendo Wii",
    "🔴 Cemu": "Nintendo Wii U",
    "🔵 RPCS3": "Sony PlayStation 3",
    "🟢 Xenia": "Microsoft Xbox 360",
    "🟢 Xemu": "Microsoft Xbox Original",
    "🔵 PCSX2": "Sony PlayStation 2",
    "🔵 DuckStation": "Sony PlayStation 1",
    "🔵 PPSSPP": "Sony PSP",
    "🟠 Dreamcast": "Sega Dreamcast"
}

@st.cache_data(ttl=3600)
def obtener_lista(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=15, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.7z', '.pkg', '.wux', '.rvz'))]
    except: return []

# --- INTERFAZ DE FILTROS ---
abc = ["TODOS", "#"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
letra_sel = abc[st.select_slider('🎮 SELECCIONA LETRA:', options=range(len(abc)))]
busq = st.text_input("🔍 BUSCAR TÍTULO ESPECÍFICO:", "").lower()

tabs = st.tabs(tab_names)
for i, tab in enumerate(tabs):
    with tab:
        nombre_tab = tab_names[i]
        key_pag = f"pag_{i}"
        if key_pag not in st.session_state: st.session_state[key_pag] = 1
        
        items = obtener_lista(urls_base[i])
        filtrados = [x for x in items if busq in x.lower()]
        if letra_sel != "TODOS":
            filtrados = [x for x in filtrados if x and (x[0].isalpha() == False if letra_sel == "#" else x.upper().startswith(letra_sel))]
        
        juegos_por_pag = 16
        total_p = max((len(filtrados)-1)//juegos_por_pag + 1, 1)

        # Navegación Superior
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
        
        cols = st.columns(4)
        for idx, juego in enumerate(filtrados[inicio : inicio + juegos_por_pag]):
            with cols[idx % 4]:
                # Limpieza de nombre para visualización y búsqueda
                nombre_visual = juego.split('(')[0].replace('.zip','').replace('.rvz','').replace('.7z','').replace('.iso','').replace('.pkg','').replace('.wux','').strip()
                
                # Lógica de búsqueda HD: Consola Real + Filtros negativos (no ventas)
                consola_query = mapeo_consola_real.get(nombre_tab, "")
                busqueda_hd = f"{nombre_visual} {consola_query} official cover art -ebay -wallapop -mercadolibre -amazon -vinted"
                query_encoded = urllib.parse.quote(busqueda_hd)
                
                # URL de Bing con parámetros de tamaño HD (600x800)
                url_img = f"https://www.bing.com/th?q={query_encoded}&w=600&h=800&c=7&rs=1&p=0&pid=ImgDetMain"
                
                # Renderizado de Tarjeta
                st.markdown(f'''
                    <div class="tarjeta-juego">
                        <div class="contenedor-img">
                            <img src="{url_img}" class="img-neon">
                        </div>
                        <span class="nombre-juego-gigante">{nombre_visual}</span>
                    </div>
                ''', unsafe_allow_html=True)
                
                if st.button("✨ MAGIA ✨", key=f"btn_{i}_{juego}"):
                    hacer_magia(urls_base[i] + juego, juego)

        st.divider()
        # Navegación Inferior
        c_nav_b = st.columns([1,2,1])
        with c_nav_b[0]:
            if st.button("⬅️ VOLVER", key=f"ba_{i}"):
                if st.session_state[key_pag] > 1: st.session_state[key_pag] -= 1; st.rerun()
        with c_nav_b[1]: st.markdown(f"<h3 style='text-align:center;'>PÁGINA {st.session_state[key_pag]}</h3>", unsafe_allow_html=True)
        with c_nav_b[2]:
            if st.button("AVANZAR ➡️", key=f"bs_{i}"):
                if st.session_state[key_pag] < total_p: st.session_state[key_pag] += 1; st.rerun()

# --- PIE DE PÁGINA: POLACO 666 ---
st.markdown("""
<div class="pie-pagina">
    <p>POLACO 666 | MULTI-REGIÓN | POLVOS DE DIAMANTE</p>
    <p style="color: #00ffc3; font-size: 14px;">
        Esta aplicación es propiedad de <b>Polaco 666</b> y es totalmente <b>sin ánimos de lucro</b>.<br>
        Dedicada a la <b>retroemulación</b>, la comunidad y la <b>conservación</b> de los mismos.
    </p>
</div>
""", unsafe_allow_html=True)
