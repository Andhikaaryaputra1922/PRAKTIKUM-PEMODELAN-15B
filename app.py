# ============================================================
# PRAKTIKUM 15B — Simulator Kebijakan Keuntungan Toko
# Theme    : Blue Brutalism + Lucide SVG Icons
# ============================================================

import streamlit as st
import numpy as np
import pandas as pd
import joblib

st.set_page_config(
    page_title="SIMULATOR KEBIJAKAN // PRAKTIKUM 15B",
    page_icon="https://api.iconify.design/lucide/store.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── BLUE BRUTALISM CSS ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Space+Grotesk:wght@700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Mono', monospace !important;
    background-color: #F8F9FC !important;
    color: #1A2F50 !important;
}
.stApp { background-color: #F8F9FC !important; }
.block-container {
    padding: 2rem 1rem 2rem !important;
    max-width: 100% !important;
}
@media (max-width: 768px) {
    .block-container {
        padding: 1.5rem 0.5rem !important;
    }
    [data-testid="stMetric"] {
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
}
section[data-testid="stSidebar"] {
    background-color: #1A2F50 !important;
    border-right: 4px solid #1A2F50 !important;
}
section[data-testid="stSidebar"] .stMarkdown, 
section[data-testid="stSidebar"] label { 
    color: #F8F9FC !important; 
}
section[data-testid="stSidebar"] .stSlider * {
    color: #F8F9FC !important;
}
section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #3A6EA5 !important;
    border: 3px solid #F8F9FC !important;
    box-shadow: 2px 2px 0 #D6E0EE !important;
    border-radius: 50% !important;
    width: 20px !important; height: 20px !important;
}
.stSlider > div > div > div { background: #3A6EA5 !important; }
[data-testid="stFileUploader"] {
    background: #EEF3FA !important;
    border: 3px dashed #3A6EA5 !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"] * {
    color: #1A2F50 !important;
}
[data-testid="stExpander"] {
    border: 2px solid #1A2F50 !important;
    border-radius: 8px !important;
    box-shadow: 4px 4px 0 #3A6EA5 !important;
    background: #ffffff !important;
    margin-bottom: 1rem !important;
    overflow: hidden !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="stExpander"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 6px 6px 0 #3A6EA5 !important;
}
[data-testid="stExpander"] details summary, .streamlit-expanderHeader {
    background: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 900 !important;
    font-size: 0.75rem !important;
    color: #1A2F50 !important;
    padding: 0.6rem 1rem !important;
    border-bottom: 2px dashed #D6E0EE !important;
}
[data-testid="stExpander"] details div {
    padding: 0.6rem 1rem !important;
    background: #ffffff !important;
}
    background: #F8F9FC !important;
    border: 3px solid #1A2F50 !important;
    color: #1A2F50 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    border-radius: 6px !important;
    box-shadow: 4px 4px 0 #3A6EA5 !important;
    transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    width: 100% !important;
    padding: 0.5rem !important;
}
.stButton > button:hover {
    background: #3A6EA5 !important;
    color: #F8F9FC !important;
    box-shadow: 2px 2px 0 #1A2F50 !important;
    transform: translate(2px, 2px) !important;
}
.stButton > button:active {
    box-shadow: 0px 0px 0 #1A2F50 !important;
    transform: translate(4px, 4px) !important;
}
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 3px solid #1A2F50 !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: 6px 6px 0 #3A6EA5 !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-4px) !important;
    box-shadow: 10px 10px 0 #3A6EA5 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.65rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #3A6EA5 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.8rem !important;
    font-weight: 900 !important;
    color: #1A2F50 !important;
}
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stMetricDelta"] {
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    border: 2px solid currentColor !important;
    border-radius: 4px !important;
    padding: 0.15rem 0.5rem !important;
    display: inline-block !important;
}
.custom-alert {
    padding: 1rem 1.5rem;
    border-radius: 8px;
    border: 3px solid #1A2F50;
    margin-bottom: 1rem;
    font-weight: 700;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    box-shadow: 4px 4px 0 #1A2F50;
}
.custom-alert.success, .custom-alert.success * { background: #e0f2e9 !important; color: #1e5631 !important; }
.custom-alert.warning, .custom-alert.warning * { background: #fff3cd !important; color: #856404 !important; }
.custom-alert.error, .custom-alert.error * { background: #f8d7da !important; color: #721c24 !important; }
.custom-alert.info, .custom-alert.info * { background: #d1ecf1 !important; color: #0c5460 !important; }
.custom-alert svg { flex-shrink: 0; margin-top: 2px; background: transparent !important; }

.section-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 900;
    font-size: 1.5rem;
    color: #1A2F50;
    margin: 2rem 0 1rem 0;
    text-transform: uppercase;
    letter-spacing: -0.02em;
}
.section-header svg { color: #3A6EA5; }
[data-testid="stDataFrame"] { border: 3px solid #1A2F50 !important; border-radius: 8px !important; overflow: hidden !important; }
hr {
    border: none !important;
    border-top: 3px dashed #D6E0EE !important;
    margin: 1.5rem 0 !important;
}
</style>
""", unsafe_allow_html=True)



# ════════════════════════════════════════════════════════════
# LUCIDE SVG ICONS
# ════════════════════════════════════════════════════════════
def icon(name, size=16, color="currentColor", style=""):
    icons = {
        "chevron-right": '<polyline points="9 18 15 12 9 6"/>',
        "store": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
        "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/>',
        "sliders": '<line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="6" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="6" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="10" y2="3"/><line x1="1" x2="7" y1="14" y2="14"/><line x1="9" x2="15" y1="12" y2="12"/><line x1="17" x2="23" y1="16" y2="16"/>',
        "bar-chart": '<line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/>',
        "table": '<path d="M12 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/>',
        "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
        "rotate-ccw": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>',
        "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
        "minus-circle": '<circle cx="12" cy="12" r="10"/><line x1="8" x2="16" y1="12" y2="12"/>',
        "trending-up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
        "trending-down": '<polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/>',
        "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
        "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
        "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2M9 2v2M2 15h2M2 9h2M22 15h-2M22 9h-2M15 22v-2M9 22v-2"/>',
        "check-circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
        "alert-triangle": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
        "megaphone": '<polygon points="11 19 2 12 11 5 11 19"/><path d="M22 12c0-4.6-3.4-8.3-8-8.9V21c4.6-.6 8-4.3 8-8.9z"/>',
        "pie-chart": '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
        "info": '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
        "refresh-cw": '<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>'
    }
    path = icons.get(name, '<circle cx="12" cy="12" r="5"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;{style}">{path}</svg>'


# ════════════════════════════════════════════════════════════
# BAGIAN 1: MODEL LOADING (TIPS #1 - GUNAKAN CACHING & TIPS #2 - ORGANISASI KODE)
# ════════════════════════════════════════════════════════════

@st.cache_resource
def load_model_from_pkl(file_buffer):
    """
    TIPS #1 & INTEGRASI MODEL (.pkl): 
    Menggunakan joblib.load() sesuai instruksi dosen untuk memuat file model_bisnis.pkl.
    """
    m = joblib.load(file_buffer)
    return m, 10, 10  # Return Model, Baseline Iklan default, Baseline Diskon default

@st.cache_resource
def load_demo_model():
    from sklearn.linear_model import LinearRegression
    X = np.array([[5,10],[10,20],[15,5],[20,25],[25,15]])
    y = np.array([50, 80, 110, 90, 150])
    m = LinearRegression().fit(X, y)
    return m, 10, 10


# ════════════════════════════════════════════════════════════
# BAGIAN 2: LOGIKA MATEMATIKA / SIMULATION ENGINE (TIPS #2 - PISAHKAN LOGIKA)
# ════════════════════════════════════════════════════════════

def calculate_what_if(model, baseline_input, intervention_input):
    """
    Menghitung prediksi dan membandingkannya (TIPS #4: Validasi Baseline)
    """
    baseline_pred = float(model.predict(baseline_input)[0])
    intervention_pred = float(model.predict(intervention_input)[0])
    delta = intervention_pred - baseline_pred
    efisiensi = (delta / baseline_pred * 100) if baseline_pred != 0 else 0
    return baseline_pred, intervention_pred, delta, efisiensi


# ════════════════════════════════════════════════════════════
# BAGIAN 3: ANTARMUKA PENGGUNA / UI (STREAMLIT)
# ════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(f"""
    <div style="background:#F8F9FC;border:4px solid #D6E0EE;
                box-shadow:6px 6px 0 #3A6EA5;padding:1rem 1.25rem;
                margin-bottom:1.25rem;">
        <div style="font-family:'Space Grotesk',sans-serif;font-weight:900;
                    font-size:1.05rem;text-transform:uppercase;
                    letter-spacing:-0.01em;color:#1A2F50;">
            {icon('database', 18, '#3A6EA5')} PRAKTIKUM 15B
        </div>
        <div style="font-family:'Space Mono',monospace;font-size:0.6rem;
                    color:#3A6EA5;letter-spacing:0.12em;margin-top:0.2rem;">
            SIMULATOR KEBIJAKAN TOKO
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. LOAD MODEL
    # Secara default, gunakan model demo (5 baris data sesuai alur modul dosen)
    # agar nilai baseline konsisten = Rp 80.62 Juta (Iklan=10, Diskon=10).
    # Pengguna dapat meng-upload file .pkl milik sendiri untuk mengganti model.

    def alert_ui(msg, type, icn):
        st.markdown(f"<div class='custom-alert {type}'>{icon(icn, 20)} <div>{msg}</div></div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload model_bisnis.pkl (Opsional)", type=["pkl"], label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            model, bl_iklan, bl_diskon = load_model_from_pkl(uploaded_file)
            src = "Upload (.pkl)"
            alert_ui("Model Berhasil Dimuat dari File Upload!", "success", "check-circle")
        except Exception as e:
            alert_ui(f"Gagal memuat PKL: {e}", "error", "alert-triangle")
            model, bl_iklan, bl_diskon = load_demo_model()
            src = "Demo (5 baris)"
    else:
        # Default: gunakan model demo sesuai data di modul dosen
        model, bl_iklan, bl_diskon = load_demo_model()
        src = "Demo (5 baris)"

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # --- TIPS #4: VALIDASI BASELINE (SIMPAN NILAI BASELINE) ---
    st.markdown(f"<div style='color:#D6E0EE;font-weight:bold;margin-bottom:10px;font-size:0.8rem;'>{icon('database', 14, '#D6E0EE')} 1. KONDISI SAAT INI (BASELINE)</div>", unsafe_allow_html=True)
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        base_iklan = st.number_input("Iklan (Jt)", min_value=0, max_value=50, value=bl_iklan, step=1)
    with col_b2:
        base_diskon = st.number_input("Diskon (%)", min_value=0, max_value=50, value=bl_diskon, step=1)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. CAPTURE INPUT (Sliding widget intervensi)
    st.markdown(f"<div style='color:#D6E0EE;font-weight:bold;margin-bottom:10px;font-size:0.8rem;'>{icon('sliders', 14, '#D6E0EE')} 2. TUAS KEBIJAKAN (INTERVENSI)</div>", unsafe_allow_html=True)
    
    iklan_slider  = st.slider("ANGGARAN IKLAN BARU (JUTA)", 0, 50, base_iklan, 1)
    diskon_slider = st.slider("BESARAN DISKON BARU (%)",    0, 50, base_diskon, 1)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("SAMAKAN DGN BASELINE"):
        st.rerun()


# --- HEADER
st.markdown(f"""
<div style="background:#3A6EA5;border:4px solid #1A2F50;
            box-shadow:6px 6px 0 #D6E0EE;padding:1rem;
            margin-bottom:1.5rem;display:flex;align-items:center;gap:0.8rem;flex-wrap:wrap;justify-content:center;text-align:center;">
    <div>{icon('store', 32, '#F8F9FC')}</div>
    <div>
        <div style="font-family:'Space Grotesk',sans-serif;font-weight:900;
                    font-size:clamp(1.2rem,5vw,2.2rem);line-height:1.2;color:#F8F9FC;">SIMULATOR KEBIJAKAN TOKO</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. PREDICT (Eksekusi fungsi prediksi real-time)
baseline_input = np.array([[base_iklan, base_diskon]])
intervention_input = np.array([[iklan_slider, diskon_slider]])

b_pred, i_pred, delta, eff = calculate_what_if(model, baseline_input, intervention_input)
sign = "+" if delta >= 0 else ""


# 4. DISPLAY (Tampilkan hasil prediksi ke UI Metrics)
c1, c2, c3 = st.columns(3)

def render_metric(label, value, sub_text, icon_n, positive_delta=None):
    if positive_delta is True:   dc, di = "#2e8b57", "trending-up"
    elif positive_delta is False: dc, di = "#c0392b", "trending-down"
    else:                         dc, di = "#3A6EA5", "minus-circle"
    
    st.markdown(f"""
    <div style="background:#ffffff;border:3px solid #1A2F50;border-radius:12px;box-shadow:6px 6px 0 #3A6EA5;padding:1.2rem;margin-bottom:1rem;transition: transform 0.2s;">
        <div style="font-size:0.65rem;font-weight:bold;color:#3A6EA5;margin-bottom:0.5rem;text-transform:uppercase;">
            {icon(icon_n, 14, '#3A6EA5')} &nbsp;{label}
        </div>
        <div style="font-size:1.8rem;font-weight:900;color:#1A2F50;line-height:1;">{value}</div>
        <div style="font-size:0.8rem;font-weight:700;color:{dc};border:2px solid {dc};border-radius:4px;padding:0.15rem 0.6rem;display:inline-flex;align-items:center;margin-top:0.8rem;">
            {icon(di, 12, dc)} &nbsp;{sub_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

with c1:
    render_metric("HASIL INTERVENSI", f"Rp {i_pred:.2f} Jt", f"{sign}{delta:.2f} Jt", "target", delta > 0 if delta != 0 else None)
with c2:
    # TIPS #4: VALIDASI BASELINE - Selalu tampilkan kondisi saat ini sebagai pembanding absolut
    render_metric("KONDISI SAAT INI (BASELINE)", f"Rp {b_pred:.2f} Jt", f"Iklan: {base_iklan} | Diskon: {base_diskon}%", "database")
with c3:
    render_metric("EFEKTIVITAS (EFISIENSI)", f"{sign}{eff:.2f}%", "Delta / Baseline", "activity", delta > 0 if delta != 0 else None)


# --- TIPS #3: STORYTELLING (PENJELASAN NARATIF) ---
# Menggunakan st.info() dan st.warning() sesuai arahan modul untuk penjelasan naratif
st.markdown(f"<div class='section-header'>{icon('megaphone', 28)} Analisis Kebijakan</div>", unsafe_allow_html=True)
if delta > 0:
    st.success(f"**Rekomendasi Positif:** Keputusan Anda menaikkan/mengubah tuas kebijakan terbukti efektif. Toko diprediksi akan mengalami **peningkatan keuntungan sebesar Rp {abs(delta):.2f} Juta** (naik {abs(eff):.2f}% dari kondisi baseline).")
elif delta < 0:
    st.warning(f"**Peringatan Risiko:** Berhati-hatilah dengan skenario ini! Kebijakan yang Anda pilih diprediksi akan menimbulkan **kerugian sebesar Rp {abs(delta):.2f} Juta** (turun {abs(eff):.2f}% dibandingkan kondisi saat ini).")
else:
    st.info("**Kondisi Stabil:** Skenario yang Anda terapkan sama dengan baseline. Tidak ada proyeksi perubahan pada keuntungan toko.")

st.markdown("<br>", unsafe_allow_html=True)


# --- VISUALISASI GRAFIK ---
st.markdown(f"<div class='section-header'>{icon('pie-chart', 28)} Perbandingan Hasil</div>", unsafe_allow_html=True)

import plotly.graph_objects as go

# Warna bar intervensi: hijau jika untung, merah jika rugi, abu jika sama
intervensi_color = "#2e8b57" if delta > 0 else ("#c0392b" if delta < 0 else "#7f8c8d")

fig = go.Figure(data=[
    go.Bar(
        name="Baseline",
        x=["Baseline (Kondisi Awal)"],
        y=[b_pred],
        marker=dict(
            color="#3A6EA5",
            line=dict(width=0)
        ),
        text=[f"Rp {b_pred:.2f} Jt"],
        textposition="outside",
        textfont=dict(family="Space Mono", size=13, color="#1A2F50"),
        width=0.4
    ),
    go.Bar(
        name="Intervensi",
        x=["Intervensi (Skenario Baru)"],
        y=[i_pred],
        marker=dict(
            color=intervensi_color,
            line=dict(width=0)
        ),
        text=[f"Rp {i_pred:.2f} Jt"],
        textposition="outside",
        textfont=dict(family="Space Mono", size=13, color="#1A2F50"),
        width=0.4
    )
])

fig.update_layout(
    plot_bgcolor="#F8F9FC",
    paper_bgcolor="#F8F9FC",
    font=dict(family="Space Mono", color="#1A2F50"),
    height=320,
    margin=dict(l=20, r=20, t=20, b=20),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right", x=1,
        font=dict(size=11)
    ),
    yaxis=dict(
        gridcolor="#D6E0EE",
        gridwidth=1,
        title="Keuntungan (Juta Rp)",
        title_font=dict(size=11)
    ),
    xaxis=dict(showgrid=False),
    bargap=0.3,
    showlegend=True
)
fig.update_yaxes(rangemode="tozero")

st.plotly_chart(fig, use_container_width=True)


# --- DETAIL MODEL ---
with st.expander("LIHAT PARAMETER MODEL REGRESI & RINCIAN PERHITUNGAN"):
    # Pre-compute parts for display
    b0   = model.intercept_
    b1   = model.coef_[0]
    b2   = model.coef_[1]
    b1_x_iklan_base = b1 * base_iklan
    b2_x_diskon_base = b2 * base_diskon
    b1_x_iklan_int  = b1 * iklan_slider
    b2_x_diskon_int  = b2 * diskon_slider

    st.markdown(f"""
    <div style="font-size: 0.88rem; line-height: 1.8;">

    <strong>① PARAMETER MODEL (Bobot Regresi Linear)</strong>
    <ul style="margin: 0.3rem 0 0.8rem 1rem;">
        <li>Intercept &nbsp;&nbsp;&nbsp;(B0) : <code>{b0:.6f}</code></li>
        <li>Koef. Iklan &nbsp;(B1) : <code>{b1:.6f}</code></li>
        <li>Koef. Diskon (B2) : <code>{b2:.6f}</code></li>
    </ul>

    <strong>② PERSAMAAN UMUM</strong><br>
    <code>Y = B0 + (B1 × Iklan) + (B2 × Diskon)</code>
    <br><br>

    <strong>③ PERHITUNGAN BASELINE</strong>
    <span style="color:#3A6EA5;">(Iklan = {base_iklan} Jt, Diskon = {base_diskon}%)</span><br>
    <code>Y_baseline = {b0:.4f} + ({b1:.4f} × {base_iklan}) + ({b2:.4f} × {base_diskon})</code><br>
    <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = {b0:.4f} + ({b1_x_iklan_base:.4f}) + ({b2_x_diskon_base:.4f})</code><br>
    <code style="color:#1A2F50;font-weight:bold;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = {b_pred:.4f} Juta</code>
    <br><br>

    <strong>④ PERHITUNGAN INTERVENSI</strong>
    <span style="color:#3A6EA5;">(Iklan = {iklan_slider} Jt, Diskon = {diskon_slider}%)</span><br>
    <code>Y_intervensi = {b0:.4f} + ({b1:.4f} × {iklan_slider}) + ({b2:.4f} × {diskon_slider})</code><br>
    <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= {b0:.4f} + ({b1_x_iklan_int:.4f}) + ({b2_x_diskon_int:.4f})</code><br>
    <code style="color:#1A2F50;font-weight:bold;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= {i_pred:.4f} Juta</code>
    <br><br>

    <strong>⑤ DELTA Y (Efektivitas Kebijakan)</strong><br>
    <code>ΔY = Y_intervensi − Y_baseline</code><br>
    <code>&nbsp;&nbsp;&nbsp;&nbsp;= {i_pred:.4f} − {b_pred:.4f}</code><br>
    <code style="color:{'#2e8b57' if delta >= 0 else '#c0392b'};font-weight:bold;">&nbsp;&nbsp;&nbsp;&nbsp;= {delta:+.4f} Juta ({eff:+.2f}%)</code>

    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div style="margin-top: 3rem; border-top: 3px dashed #D6E0EE; padding-top: 1.2rem;
            text-align: center; font-family: 'Space Mono', monospace;">
    <div style="font-size: 0.7rem; color: #3A6EA5; letter-spacing: 0.12em; text-transform: uppercase;">
        © 2025 &nbsp;·&nbsp; Andhika Arya Putra &nbsp;·&nbsp; Praktikum 15B
    </div>
    <div style="font-size: 0.62rem; color: #9aafc7; margin-top: 0.3rem; letter-spacing: 0.08em;">
        Simulator Kebijakan Toko &nbsp;·&nbsp; Powered by Streamlit & Scikit-learn
    </div>
</div>
""", unsafe_allow_html=True)
