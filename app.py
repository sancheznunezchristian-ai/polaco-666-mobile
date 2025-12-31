import streamlit as st
from bs4 import BeautifulSoup
import urllib.parse
import os
import requests
from io import BytesIO

# --- CONFIGURACIÓN POLACO 666 ---
st.set_page_config(page_title="Polaco 666 Games", layout="wide")

# --- CSS: ESTILO POLACO 666 OPTIMIZADO PARA MÓVIL ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    
    .stApp { background: #08090b; color: #00ffc3; }
    
    .logo-666 {
        font-family: 'Black Ops One', cursive; font-size: 50px;
        text-align: center; margin-top: 10px; color: #FF5F1F; 
        animation: vibracion 0.3s linear infinite;
    }

    /* EFECTO ZOOM EN PESTAÑAS */
    button[data-baseweb="tab"] {
        transition: all 0.3s ease-in-out !important;
    }
    button[data-baseweb="tab"]:hover {
        transform: scale(1.15) !important;
        color: #FF5F1F !important;
        text-shadow: 0 0 10px #FF5F1F;
    }

    .tarjeta-juego {
        background: rgba(255, 255, 255, 0.02);
        padding: 15px; border-radius: 15px;
        border: 1px solid #222; margin-bottom: 25px;
        text-align: center;
    }

    .contenedor-caratula {
        width: 100%; aspect-ratio: 3/4;
        border: 2px solid #FF5F1F; border-radius: 10px;
        overflow: hidden; background: #000;
    }

    .img-neon { width: 100%; height: 100%; object-fit: cover; }

    .nombre-juego-gigante {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 18px !important; color: #ffffff !important;
        text-shadow: 0 0 8px #FF5F1F !important;
        margin: 10px 0 !important; display: block !important;
        min-height: 50px; line-height: 1.1; font-weight: 900 !important;
        text-transform: uppercase;
    }

    .stButton > button {
        border: 2px solid #FF5F1F !important; background: #111 !important;
        color: #ffae00 !important; font-weight: bold; width: 100%;
        font-size: 16px !important;
    }

    @keyframes vibracion {
        0% { transform: translate(0); }
        50% { transform: translate(-1px, 1px); }
        100% { transform: translate(0); }
    }
</style>
<div class="logo-666">POLACO 666 GAMES</div>
""", unsafe_allow_html=True)

# --- FUNCIÓN DESCARGA CON BARRA Y BOTÓN FINAL ---
def hacer_magia(url_descarga, nombre_archivo):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://myrient.erista.me/'
        }
        
        with requests.get(url_descarga, stream=True, timeout=None, headers=headers) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            progreso = st.progress(0)
            texto_status = st.empty()
            
            buffer = BytesIO()
            descargado = 0
            
            for chunk in r.iter_content(chunk_size=1048576): # 1MB chunks
                if chunk:
                    buffer.write(chunk)
                    descargado += len(chunk)
                    if total_size > 0:
                        porcentaje = min(descargado / total_size, 1.0)
                        progreso.progress(porcentaje)
                        # REGLA: "polvos de diamante" en lugar de "mg"
                        texto_status.markdown(f"<h3 style='color:#00ff00; text-align:center;'>⚡ {int(porcentaje*100)}% - {descargado//1048576} / {total_size//1048576} POLVOS DE DIAMANTE ⚡</h3>", unsafe_allow_html=True)
            
            st.balloons()
            st.success("¡PREPARACIÓN COMPLETADA!")
            st.download_button(
                label="💾 PULSA AQUÍ PARA GUARDAR JUEGO EN MÓVIL",
                data=buffer.getvalue(),
                file_name=nombre_archivo,
                mime="application/octet-stream"
            )
    except Exception as e:
        st.error(f"Fallo de conexión: {e}")

# --- LISTAS Y URLs ---
tab_names = ["🟣 GameCube", "🔴 Wii", "🔴 Wii U", "🔵 PS3", "🟢 Xbox 360", "🟢 Xbox", "🔵 PS2", "🔵 PS1", "🔵 PSP", "🟠 Dreamcast"]
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

# MAPEO PARA BÚSQUEDA DE IMÁGENES (EVITA MEZCLAS)
consola_map = {
    "GameCube": "Nintendo GameCube",
    "Wii": "Nintendo Wii",
    "Wii U": "Wii U",
    "PS3": "PlayStation 3",
    "Xbox 360": "Xbox 360",
    "Xbox": "Original Xbox",
    "PS2": "PlayStation 2",
    "PS1": "PlayStation 1",
    "PSP": "Sony PSP",
    "Dreamcast": "Sega Dreamcast"
}

@st.cache_data(ttl=3600)
def obtener_lista(url):
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [urllib.parse.unquote(a['href']) for a in soup.find_all('a') if a.get('href', '').lower().endswith(('.zip', '.iso', '.7z', '.pkg', '.wux', '.rvz'))]
    except: return []

# --- FILTROS ---
def reset_pagina():
    for i in range(10): st.session_state[f'pag_{i}'] = 1

abc = ["TODOS", "#"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
idx_abc = st.select_slider('🎮 LETRA:', options=range(len(abc)), format_func=lambda x: abc[x], on_change=reset_pagina)
letra_sel = abc[idx_abc]
busq = st.text_input("🔍 BUSCAR JUEGO (EUROPE, ASIA, USA...):", "", on_change=reset_pagina).lower()

# --- TABS CON NAVEGACIÓN ---
tabs = st.tabs(tab_names)
for i, tab in enumerate(tabs):
    with tab:
        key_pag = f"pag_{i}"
        if key_pag not in st.session_state: st.session_state[key_pag] = 1
        items = obtener_lista(urls_base[i])
        filtrados = [x for x in items if busq in x.lower()]
        
        if letra_sel != "TODOS":
            filtrados = [x for x in filtrados if x and (x[0].isalpha() == False if letra_sel == "#" else x.upper().startswith(letra_sel))]
        
        juegos_por_pagina = 12 
        total_pags = max((len(filtrados) - 1) // juegos_por_pagina + 1, 1)

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("⬅️", key=f"up_p_{i}"):
                if st.session_state[key_pag] > 1: st.session_state[key_pag] -= 1; st.rerun()
        with c2: st.write(f"Pág {st.session_state[key_pag]}/{total_pags}")
        with c3:
            if st.button("➡️", key=f"up_n_{i}"):
                if st.session_state[key_pag] < total_pags: st.session_state[key_pag] += 1; st.rerun()

        st.divider()
        inicio = (st.session_state[key_pag] - 1) * juegos_por_pagina
        fin = inicio + juegos_por_pagina
        
        cols = st.columns(2)
        for idx, juego in enumerate(filtrados[inicio:fin]):
            with cols[idx % 2]:
                nombre_visual = juego.replace('.zip','').replace('.rvz','').replace('.7z','').replace('.iso','').replace('.pkg','').replace('.wux','').strip()
                
                # CORRECCIÓN DE CARÁTULAS: Buscamos el nombre real de la consola
                nombre_pestaña = tab_names[i].split(" ")[-1]
                consola_real = consola_map.get(nombre_pestaña, nombre_pestaña)
                
                busqueda_bing = urllib.parse.quote(f"{nombre_visual} {consola_real} official box art cover")
                img_url = f"https://www.bing.com/th?q={busqueda_bing}&w=400&h=550&c=7&rs=1&p=0&pid=ImgDetMain"
                
                st.markdown(f'''<div class="tarjeta-juego">
                    <div class="contenedor-caratula"><img src="{img_url}" class="img-neon"></div>
                    <span class="nombre-juego-gigante">{nombre_visual}</span>
                </div>''', unsafe_allow_html=True)
                
                if st.button("✨ MAGIA ✨", key=f"dl_{i}_{juego}"):
                    hacer_magia(urls_base[i] + juego, juego)

        st.divider()
        b1, b2, b3 = st.columns([1, 1, 1])
        with b1:
            if st.button("⬅️ ", key=f"dw_p_{i}"):
                if st.session_state[key_pag] > 1: st.session_state[key_pag] -= 1; st.rerun()
        with b2: st.write(f"Pág {st.session_state[key_pag]}/{total_pags}")
        with b3:
            if st.button("➡️ ", key=f"dw_n_{i}"):
                if st.session_state[key_pag] < total_pags: st.session_state[key_pag] += 1; st.rerun()

st.markdown("""<div style='text-align:center; padding:20px; color:#FF5F1F;'>POLACO 666 | POLVOS DE DIAMANTE</div>""", unsafe_allow_html=True)
