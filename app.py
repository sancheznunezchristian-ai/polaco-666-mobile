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
        font-family: 'Black Ops One', cursive; font-size: 60px;
        text-align: center; margin-top: 10px; color: #FF5F1F; 
        animation: vibracion 0.3s linear infinite;
    }
    .tarjeta-juego {
        background: rgba(0, 0, 0, 0.5);
        padding: 10px; border-radius: 15px;
        border: 1px solid #222; margin-bottom: 25px;
        text-align: center;
    }
    .contenedor-caratula {
        width: 100%; aspect-ratio: 3/4;
        border: 2px solid #FF5F1F; border-radius: 10px;
        overflow: hidden; background: #000;
        display: flex; align-items: center; justify-content: center;
    }
    .img-neon { width: 100%; height: 100%; object-fit: cover; }
    .nombre-juego-gigante {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 15px !important; color: #ffffff !important;
        text-shadow: 0 0 5px #FF5F1F !important;
        min-height: 45px; display: flex; align-items: center; justify-content: center;
        text-transform: uppercase; padding-top: 5px;
    }
    .pie-pagina {
        text-align: center; font-family: 'Orbitron', sans-serif;
        color: #FF5F1F; font-size: 14px; margin-top: 50px;
        padding: 40px; border-top: 2px solid #FF5F1F;
        background: rgba(0,0,0,0.9); line-height: 1.6;
    }
    @keyframes vibracion { 0% { transform: translate(0); } 50% { transform: translate(-1px, 1px); } 100% { transform: translate(0); } }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- FUNCIÓN DESCARGA (POLVOS DE DIAMANTE) ---
def hacer_magia(url_descarga, nombre_archivo):
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://myrient.erista.me/'}
        with requests.get(url_descarga, stream=True, timeout=None, headers=headers) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            progreso = st.progress(0)
            texto_status = st.empty()
            buffer = BytesIO()
            descargado = 0
            for chunk in r.iter_content(chunk_size=1048576):
                if chunk:
                    buffer.write(chunk)
                    descargado += len(chunk)
                    if total_size > 0:
                        porcentaje = min(descargado / total_size, 1.0)
                        progreso.progress(porcentaje)
                        texto_status.markdown(f"<h3 style='color:#00ff00; text-align:center;'>⚡ {int(porcentaje*100)}% - {descargado//1048576} / {total_size//1048576} POLVOS DE DIAMANTE ⚡</h3>", unsafe_allow_html=True)
            st.balloons()
            st.download_button(label="💾 GUARDAR JUEGO", data=buffer.getvalue(), file_name=nombre_archivo)
    except Exception as e:
        st.error(f"Error: {e}")

# --- PESTAÑAS Y MAPEO ---
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

# MAPEO DE BÚSQUEDA EN SITIOS RETRO (MobyGames, LaunchBox)
consola_real_map = {
    "Dolphin (GC)": "site:mobygames.com GameCube cover art",
    "Dolphin (Wii)": "site:mobygames.com Wii cover art scan",
    "Cemu": "site:launchbox-app.com Wii U front cover",
    "RPCS3": "site:steamgriddb.com PS3 cover",
    "Xenia": "site:mobygames.com Xbox 360 front cover",
    "Xemu": "site:launchbox-app.com Xbox Original front cover",
    "PCSX2": "site:mobygames.com PS2 front cover",
    "DuckStation": "site:mobygames.com PS1 front cover scan",
    "PPSSPP": "site:launchbox-app.com PSP cover",
    "Dreamcast": "site:mobygames.com Dreamcast front cover"
}

@st.cache_data(ttl=3600)
def obtener_lista(url):
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.7z', '.pkg', '.wux', '.rvz'))]
    except: return []

abc = ["TODOS", "#"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
letra_sel = abc[st.select_slider('🎮 LETRA:', options=range(len(abc)), format_func=lambda x: abc[x])]
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
        
        juegos_per_page = 12
        total_p = max((len(filtrados)-1)//juegos_per_page + 1, 1)

        # --- NAVEGACIÓN ARRIBA ---
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            if st.button("⬅️ ANTERIOR", key=f"up_{i}"):
                if st.session_state[key_pag] > 1: st.session_state[key_pag] -= 1; st.rerun()
        with c2: st.markdown(f"<h4 style='text-align:center;'>{st.session_state[key_pag]} / {total_p}</h4>", unsafe_allow_html=True)
        with c3:
            if st.button("SIGUIENTE ➡️", key=f"un_{i}"):
                if st.session_state[key_pag] < total_p: st.session_state[key_pag] += 1; st.rerun()

        st.divider()
        inicio = (st.session_state[key_pag] - 1) * juegos_per_page
        cols = st.columns(2)
        for idx, juego in enumerate(filtrados[inicio : inicio + juegos_per_page]):
            with cols[idx % 2]:
                nombre_visual = juego.replace('.zip','').replace('.rvz','').replace('.7z','').replace('.iso','').replace('.pkg','').replace('.wux','').strip()
                emulador_puro = tab_names[i].split(" ", 1)[-1]
                termino = consola_real_map.get(emulador_puro, emulador_puro)
                
                # Búsqueda PRO: Forzamos sitios de carátulas para evitar fotos de tiendas
                busqueda_final = f"{nombre_visual} {termino} clean scan"
                url_img = f"https://www.bing.com/th?q={urllib.parse.quote(busqueda_final)}&w=600&h=800&c=7&rs=1&p=0&pid=ImgDetMain"
                
                st.markdown(f'''<div class="tarjeta-juego">
                    <div class="contenedor-caratula"><img src="{url_img}" class="img-neon"></div>
                    <span class="nombre-juego-gigante">{nombre_visual}</span>
                </div>''', unsafe_allow_html=True)
                if st.button("✨ MAGIA ✨", key=f"btn_{i}_{juego}"): hacer_magia(urls_base[i] + juego, juego)

        # --- NAVEGACIÓN ABAJO ---
        st.divider()
        b1, b2, b3 = st.columns([1,1,1])
        with b1:
            if st.button("⬅️ PÁGINA ANTERIOR", key=f"dp_{i}"):
                if st.session_state[key_pag] > 1: st.session_state[key_pag] -= 1; st.rerun()
        with b2: st.markdown(f"<h3 style='text-align:center;'>PÁG {st.session_state[key_pag]}</h3>", unsafe_allow_html=True)
        with b3:
            if st.button("PÁGINA SIGUIENTE ➡️", key=f"dn_{i}"):
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
