import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import requests
from io import BytesIO

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# --- CSS: ESTILO POLACO 666 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #08090b; color: #00ffc3; }
    
    .logo-666 {
        font-family: 'Black Ops One', cursive; font-size: 35px;
        text-align: center; margin: 10px 0; color: #FF5F1F; 
        text-shadow: 2px 2px #000;
    }

    .tarjeta-juego {
        background: #111;
        padding: 0px; border-radius: 12px;
        border: 2px solid #FF5F1F; margin-bottom: 15px;
        overflow: hidden; height: 460px;
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

    .stButton > button {
        width: 100% !important; height: 50px !important;
        background: #FF5F1F !important; color: white !important;
        border: none !important; font-weight: bold !important;
        font-family: 'Orbitron', sans-serif !important;
    }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- FUNCIÓN DE DESCARGA SEGURA PARA ARCHIVOS GRANDES ---
def descargar_a_la_app(url, nombre_archivo):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://myrient.erista.me/'
        }
        
        with st.status(f"⚡ Procesando: {nombre_archivo}", expanded=True) as status:
            r = requests.get(url, headers=headers, stream=True, timeout=300)
            r.raise_for_status()
            
            total_size = int(r.headers.get('content-length', 0))
            buffer = BytesIO()
            descargado = 0
            
            progreso = st.progress(0)
            # Chunks más grandes (2MB) para mayor velocidad en archivos pesados
            for chunk in r.iter_content(chunk_size=2097152): 
                if chunk:
                    buffer.write(chunk)
                    descargado += len(chunk)
                    if total_size > 0:
                        progreso.progress(min(descargado / total_size, 1.0))
            
            status.update(label="✅ POLVOS DE DIAMANTE LISTOS", state="complete")
            
            # Al terminar, mostramos el botón real de descarga del navegador
            st.download_button(
                label="💾 GUARDAR EN MI MÓVIL",
                data=buffer.getvalue(),
                file_name=nombre_archivo,
                mime="application/octet-stream",
                key=f"final_{nombre_archivo}"
            )
            st.balloons()
    except Exception as e:
        st.error(f"Error al procesar: {e}")

# --- CONFIGURACIÓN DE PESTAÑAS Y MAPEO ---
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
busq = st.text_input("🔍 BUSCAR JUEGO:", "").lower()

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
                
                # Al pulsar el botón, se ejecuta la descarga pesada
                if st.button("✨ POLVOS DE DIAMANTE ✨", key=f"btn_{i}_{idx}"):
                    descargar_a_la_app(urls_base[i] + juego, juego)

st.markdown('<div style="text-align:center; color:#FF5F1F; padding:30px;">POLACO 666 | POLVOS DE DIAMANTE</div>', unsafe_allow_html=True)
