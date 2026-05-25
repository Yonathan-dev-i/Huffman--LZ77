"""
Aplicación Web Interactiva - Compresión Sin Pérdida
Algoritmos: Huffman Coding y LZ77
Desarrollado para exposición académica universitaria
"""

import streamlit as st
import json
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import huffman
import lz77

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CompresorLab · Compresión Sin Pérdida",
    page_icon="🗜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Sora:wght@300;400;600;700;800&display=swap');

    :root {
        --bg-primary: #0a0e1a;
        --bg-secondary: #111827;
        --bg-card: #1a2035;
        --accent-cyan: #00d4ff;
        --accent-purple: #7c3aed;
        --accent-green: #10b981;
        --accent-orange: #f59e0b;
        --accent-red: #ef4444;
        --text-primary: #f0f4ff;
        --text-secondary: #8892b0;
        --border: rgba(0, 212, 255, 0.15);
    }

    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0f172a 50%, #0a0e1a 100%);
        font-family: 'Sora', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        border-right: 1px solid var(--border);
    }

    /* Header hero */
    .hero-header {
        background: linear-gradient(135deg, rgba(124,58,237,0.15) 0%, rgba(0,212,255,0.08) 100%);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(0,212,255,0.06) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin-top: 0.4rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    /* Section titles */
    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--accent-cyan);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, var(--border), transparent);
    }

    /* Cards */
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        border-color: rgba(0,212,255,0.35);
        transform: translateY(-2px);
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent-cyan);
    }
    .stat-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.3rem;
    }

    /* Validation box */
    .validation-success {
        background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(16,185,129,0.05));
        border: 1px solid rgba(16,185,129,0.4);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .validation-success h2 {
        color: #10b981;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 0.3rem 0;
    }
    .validation-success p {
        color: #6ee7b7;
        margin: 0;
        font-size: 0.9rem;
    }

    .validation-error {
        background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(239,68,68,0.05));
        border: 1px solid rgba(239,68,68,0.4);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin: 1rem 0;
    }

    /* Algorithm badge */
    .algo-badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .badge-huffman {
        background: rgba(124,58,237,0.2);
        border: 1px solid rgba(124,58,237,0.5);
        color: #a78bfa;
    }
    .badge-lz77 {
        background: rgba(0,212,255,0.12);
        border: 1px solid rgba(0,212,255,0.4);
        color: #00d4ff;
    }

    /* Info panels */
    .info-panel {
        background: rgba(26,32,53,0.7);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        font-size: 0.88rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    .info-panel strong {
        color: var(--text-primary);
    }

    /* Metrics override */
    [data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem;
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 0.75rem !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--accent-cyan) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #5b21b6);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Sora', sans-serif;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        padding: 0.6rem 1.5rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #8b5cf6, #7c3aed);
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(124,58,237,0.4);
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: rgba(26,32,53,0.5);
        border: 2px dashed rgba(0,212,255,0.2);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(0,212,255,0.5);
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        color: var(--text-primary);
    }

    /* Code block */
    .code-preview {
        background: #0d1117;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #79c0ff;
        white-space: pre-wrap;
        word-break: break-all;
        max-height: 120px;
        overflow-y: auto;
        line-height: 1.5;
    }

    /* Tabs */
    [data-testid="stTabs"] [data-baseweb="tab"] {
        font-family: 'Sora', sans-serif;
        color: var(--text-secondary);
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        color: var(--accent-cyan) !important;
    }

    /* Divider */
    hr {
        border-color: var(--border);
        margin: 1.5rem 0;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--accent-purple); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ─── SESSION STATE ───────────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "compressed_data": None,
        "compression_stats": None,
        "original_text": None,
        "decompressed_text": None,
        "decompression_stats": None,
        "huffman_metadata": None,
        "lz77_tokens": None,
        "lz77_serialized": None,
        "algorithm": None,
        "filename": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()


# ─── HELPERS ─────────────────────────────────────────────────────────────────────
def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024**2):.2f} MB"


def make_comparison_chart(original: int, compressed: int, algo: str) -> go.Figure:
    labels = ["Original", "Comprimido"]
    values = [original, compressed]
    colors = ["#7c3aed", "#00d4ff"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels, y=values,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.1)', width=1)
        ),
        text=[format_size(v) for v in values],
        textposition='outside',
        textfont=dict(color='#f0f4ff', family='JetBrains Mono', size=12),
        width=0.5
    ))

    saving = (1 - compressed / original) * 100 if original > 0 else 0
    fig.update_layout(
        title=dict(
            text=f"Comparación de Tamaños — {algo} <br><sup>Reducción: {saving:.1f}%</sup>",
            font=dict(color='#f0f4ff', family='Sora', size=14),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            title="Bytes",
            gridcolor='rgba(255,255,255,0.06)',
            color='#8892b0',
            tickfont=dict(family='JetBrains Mono', size=11)
        ),
        xaxis=dict(color='#8892b0'),
        font=dict(color='#f0f4ff'),
        height=320,
        margin=dict(l=30, r=30, t=70, b=30)
    )
    return fig


def make_huffman_code_chart(code_table: dict, freq_table: dict, top_n: int = 15) -> go.Figure:
    items = sorted(code_table.items(), key=lambda x: freq_table.get(x[0], 0), reverse=True)[:top_n]
    chars = [repr(c) for c, _ in items]
    lengths = [len(code) for _, code in items]
    freqs = [freq_table.get(c, 0) for c, _ in items]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=chars, y=lengths,
        marker=dict(
            color=freqs,
            colorscale=[[0, '#1a2035'], [0.5, '#7c3aed'], [1, '#00d4ff']],
            showscale=True,
            colorbar=dict(title="Frecuencia", tickfont=dict(color='#8892b0'))
        ),
        text=lengths, textposition='outside',
        textfont=dict(color='#f0f4ff', size=11),
        width=0.7
    ))

    fig.update_layout(
        title=dict(
            text="Longitud de Código Huffman por Carácter",
            font=dict(color='#f0f4ff', family='Sora', size=13),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(color='#8892b0', tickfont=dict(family='JetBrains Mono', size=11)),
        yaxis=dict(
            title="Bits por símbolo",
            gridcolor='rgba(255,255,255,0.06)',
            color='#8892b0'
        ),
        height=320,
        margin=dict(l=30, r=30, t=50, b=30)
    )
    return fig


def make_lz77_token_chart(stats: dict) -> go.Figure:
    labels = ["Literales (sin referencia)", "Referencias (offset, length)"]
    values = [stats.get("literal_tokens", 0), stats.get("reference_tokens", 0)]
    colors = ["#7c3aed", "#00d4ff"]

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        marker=dict(colors=colors, line=dict(color='#0a0e1a', width=2)),
        hole=0.55,
        textfont=dict(color='#f0f4ff', family='Sora', size=12),
        hovertemplate="<b>%{label}</b><br>%{value} tokens (%{percent})<extra></extra>"
    ))
    fig.update_layout(
        title=dict(
            text="Distribución de Tokens LZ77",
            font=dict(color='#f0f4ff', family='Sora', size=13),
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(font=dict(color='#8892b0')),
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:2.5rem;'>🗜️</div>
        <div style='font-size:1.1rem; font-weight:800; color:#00d4ff; letter-spacing:1px;'>CompresorLab</div>
        <div style='font-size:0.75rem; color:#8892b0; margin-top:0.2rem;'>Compresión Sin Pérdida</div>
    </div>
    <hr style='border-color:rgba(0,212,255,0.15);'>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>⚙ Configuración</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📂 Cargar archivo",
        type=["txt", "csv", "json", "bin", "py", "bmp", "log", "xml", "html", "gz"],
        help="Soporta archivos .txt, .csv y .json (texto plano)"
    )

    algorithm = st.selectbox(
        "🧮 Algoritmo de compresión",
        ["Huffman Coding", "LZ77"],
        help="Selecciona el algoritmo a demostrar"
    )

    st.markdown("<hr style='border-color:rgba(0,212,255,0.1);'>", unsafe_allow_html=True)

    if algorithm == "Huffman Coding":
        st.markdown("""
        <span class='algo-badge badge-huffman'>Huffman</span>
        <div class='info-panel' style='margin-top:0.8rem;'>
        <strong>Huffman Coding</strong> asigna códigos binarios más cortos a los símbolos más frecuentes y más largos a los menos frecuentes, construyendo un árbol óptimo de prefijos.<br><br>
        <strong>Tipo:</strong> Basado en estadísticas<br>
        <strong>Complejidad:</strong> O(n log n)<br>
        <strong>Ideal para:</strong> Texto con caracteres repetidos
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <span class='algo-badge badge-lz77'>LZ77</span>
        <div class='info-panel' style='margin-top:0.8rem;'>
        <strong>LZ77</strong> reemplaza secuencias repetidas por referencias (offset, length, next_char) a apariciones previas dentro de una ventana deslizante.<br><br>
        <strong>Tipo:</strong> Basado en diccionario<br>
        <strong>Complejidad:</strong> O(n·w)<br>
        <strong>Ideal para:</strong> Texto con patrones repetitivos
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(0,212,255,0.1);'>", unsafe_allow_html=True)

    if algorithm == "LZ77":
        st.markdown("<div style='font-size:0.8rem; color:#8892b0; margin-bottom:0.5rem;'>⚙ Parámetros LZ77</div>", unsafe_allow_html=True)
        window_size = st.slider("Tamaño de ventana", 32, 512, 255, 32)
        lookahead_size = st.slider("Tamaño lookahead", 4, 32, 15, 1)
    else:
        window_size, lookahead_size = 255, 15

    st.markdown("<hr style='border-color:rgba(0,212,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#4a5568; text-align:center; line-height:1.6;'>
        Proyecto Académico<br>
        Teoría de la Información<br>
        <span style='color:#6366f1;'>Compresión Sin Pérdida</span>
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
    <p class='hero-title'>🗜️ CompresorLab</p>
    <p class='hero-subtitle'>Demostración interactiva de algoritmos de compresión sin pérdida · Huffman Coding & LZ77</p>
</div>
""", unsafe_allow_html=True)

# ─── FILE PREVIEW ─────────────────────────────────────────────────────────────────
if uploaded_file is not None:
    try:
        raw_bytes = uploaded_file.read()
        text_content = raw_bytes.decode('utf-8', errors='replace')

        st.session_state.original_text = text_content
        st.session_state.filename = uploaded_file.name

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"<div class='section-title'>📄 Archivo Cargado</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='info-panel'>
            <strong>Nombre:</strong> {uploaded_file.name}<br>
            <strong>Tamaño:</strong> {format_size(len(raw_bytes))}<br>
            <strong>Caracteres:</strong> {len(text_content):,}<br>
            <strong>Caracteres únicos:</strong> {len(set(text_content))}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.metric("📦 Tamaño Original", format_size(len(raw_bytes)))

        with col3:
            st.metric("🔤 Caracteres", f"{len(text_content):,}")

        with st.expander("👁 Vista previa del contenido", expanded=False):
            preview = text_content[:500] + ("..." if len(text_content) > 500 else "")
            st.markdown(f"<div class='code-preview'>{preview}</div>", unsafe_allow_html=True)

        st.markdown("---")

        # ─── ACTIONS ─────────────────────────────────────────────────────────────
        col_compress, col_decompress, col_reset = st.columns([1, 1, 1])

        with col_compress:
            compress_btn = st.button("🚀 Comprimir", use_container_width=True, type="primary")

        with col_decompress:
            decompress_btn = st.button(
                "🔓 Descomprimir",
                use_container_width=True,
                disabled=st.session_state.compressed_data is None
            )

        with col_reset:
            reset_btn = st.button("🔄 Reiniciar", use_container_width=True)

        if reset_btn:
            for key in ["compressed_data", "compression_stats", "decompressed_text",
                        "decompression_stats", "huffman_metadata", "lz77_tokens", "lz77_serialized", "algorithm"]:
                st.session_state[key] = None
            st.rerun()

        # ─── COMPRESSION ─────────────────────────────────────────────────────────
        if compress_btn:
            with st.spinner(f"Comprimiendo con {algorithm}..."):
                try:
                    if algorithm == "Huffman Coding":
                        comp_bytes, metadata, stats = huffman.compress(text_content)
                        st.session_state.compressed_data = comp_bytes
                        st.session_state.huffman_metadata = metadata
                        st.session_state.compression_stats = stats
                        st.session_state.algorithm = "Huffman Coding"
                    else:
                        tokens, serialized, stats = lz77.compress(
                            text_content, window_size, lookahead_size
                        )
                        st.session_state.compressed_data = serialized
                        st.session_state.lz77_tokens = tokens
                        st.session_state.lz77_serialized = serialized
                        st.session_state.compression_stats = stats
                        st.session_state.algorithm = "LZ77"

                    st.session_state.decompressed_text = None
                    st.session_state.decompression_stats = None
                    st.success("✅ Compresión completada exitosamente")
                except Exception as e:
                    st.error(f"❌ Error durante la compresión: {str(e)}")

        # ─── DECOMPRESSION ────────────────────────────────────────────────────────
        if decompress_btn and st.session_state.compressed_data is not None:
            with st.spinner(f"Descomprimiendo con {st.session_state.algorithm}..."):
                try:
                    if st.session_state.algorithm == "Huffman Coding":
                        text_recovered, d_stats = huffman.decompress(
                            st.session_state.compressed_data,
                            st.session_state.huffman_metadata
                        )
                    else:
                        text_recovered, d_stats = lz77.decompress_from_bytes(
                            st.session_state.lz77_serialized,
                            len(st.session_state.original_text)
                        )
                    st.session_state.decompressed_text = text_recovered
                    st.session_state.decompression_stats = d_stats
                    st.success("✅ Descompresión completada exitosamente")
                except Exception as e:
                    st.error(f"❌ Error durante la descompresión: {str(e)}")

        # ─── RESULTS ─────────────────────────────────────────────────────────────
        if st.session_state.compression_stats is not None:
            stats = st.session_state.compression_stats
            algo = st.session_state.algorithm

            st.markdown(f"<div class='section-title'>📊 Resultados de Compresión — {algo}</div>", unsafe_allow_html=True)

            # Metrics row
            m1, m2, m3, m4, m5 = st.columns(5)
            with m1:
                st.metric("📦 Tamaño Original", format_size(stats["original_size"]))
            with m2:
                st.metric("🗜️ Tamaño Comprimido", format_size(stats["compressed_size"]))
            with m3:
                saving = stats.get("space_saving", 0)
                delta_color = "normal" if saving > 0 else "inverse"
                st.metric("📉 Reducción", f"{saving:.1f}%", delta=f"{saving:.1f}% menos")
            with m4:
                ratio = stats.get("compression_ratio", 0)
                st.metric("⚖️ Ratio", f"{ratio:.2f}x")
            with m5:
                elapsed = stats.get("time_elapsed", 0)
                st.metric("⏱️ Tiempo", f"{elapsed*1000:.1f} ms")

            # Charts tabs
            tab1, tab2 = st.tabs(["📊 Comparación de Tamaños", "🔍 Análisis del Algoritmo"])

            with tab1:
                col_chart, col_table = st.columns([3, 2])
                with col_chart:
                    fig = make_comparison_chart(stats["original_size"], stats["compressed_size"], algo)
                    st.plotly_chart(fig, use_container_width=True)

                with col_table:
                    st.markdown("<br>", unsafe_allow_html=True)
                    table_data = {
                        "Métrica": ["Tamaño original", "Tamaño comprimido", "Bytes ahorrados",
                                    "Porcentaje reducción", "Ratio compresión", "Tiempo ejecución"],
                        "Valor": [
                            format_size(stats["original_size"]),
                            format_size(stats["compressed_size"]),
                            format_size(max(0, stats["original_size"] - stats["compressed_size"])),
                            f"{stats.get('space_saving', 0):.2f}%",
                            f"{stats.get('compression_ratio', 0):.3f}x",
                            f"{stats.get('time_elapsed', 0)*1000:.2f} ms"
                        ]
                    }
                    df = pd.DataFrame(table_data)
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Métrica": st.column_config.TextColumn("Métrica", width="medium"),
                            "Valor": st.column_config.TextColumn("Valor", width="medium")
                        }
                    )

            with tab2:
                if algo == "Huffman Coding" and "code_table" in stats:
                    col_alg1, col_alg2 = st.columns(2)
                    with col_alg1:
                        fig2 = make_huffman_code_chart(stats["code_table"], stats["freq_table"])
                        st.plotly_chart(fig2, use_container_width=True)

                    with col_alg2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class='info-panel'>
                        <strong>📐 Estadísticas Huffman</strong><br><br>
                        <strong>Símbolos únicos:</strong> {stats.get('unique_chars', 0)}<br>
                        <strong>Bits totales codificados:</strong> {stats.get('bit_length', 0):,}<br>
                        <strong>Bits por símbolo (prom.):</strong> {stats.get('bit_length', 0)/max(1,len(st.session_state.original_text)):.2f}<br><br>
                        <strong>Top 5 Códigos generados:</strong><br>
                        </div>
                        """, unsafe_allow_html=True)

                        code_table = stats["code_table"]
                        freq_table = stats["freq_table"]
                        top5 = sorted(code_table.items(), key=lambda x: freq_table.get(x[0], 0), reverse=True)[:5]
                        for char, code in top5:
                            freq = freq_table.get(char, 0)
                            st.markdown(
                                f"`{repr(char)}` → `{code}` ({len(code)} bits, freq={freq})"
                            )

                elif algo == "LZ77":
                    col_alg1, col_alg2 = st.columns(2)
                    with col_alg1:
                        fig2 = make_lz77_token_chart(stats)
                        st.plotly_chart(fig2, use_container_width=True)

                    with col_alg2:
                        st.markdown(f"""
                        <div class='info-panel'>
                        <strong>📐 Estadísticas LZ77</strong><br><br>
                        <strong>Total tokens:</strong> {stats.get('token_count', 0):,}<br>
                        <strong>Tokens literales:</strong> {stats.get('literal_tokens', 0):,}<br>
                        <strong>Tokens referencia:</strong> {stats.get('reference_tokens', 0):,}<br>
                        <strong>Ventana usada:</strong> {stats.get('window_size', 0)} bytes<br>
                        <strong>Lookahead:</strong> {stats.get('lookahead_size', 0)} bytes<br><br>
                        <strong>Eficiencia:</strong> {stats.get('reference_tokens',0)/max(1,stats.get('token_count',1))*100:.1f}% referencias
                        </div>
                        """, unsafe_allow_html=True)

                        if st.session_state.lz77_tokens:
                            sample = st.session_state.lz77_tokens[:8]
                            st.markdown("**Primeros tokens generados:**")
                            df_tokens = pd.DataFrame(
                                [(f"{t[0]}", f"{t[1]}", repr(t[2])) for t in sample],
                                columns=["Offset", "Length", "Next char"]
                            )
                            st.dataframe(df_tokens, hide_index=True, use_container_width=True)

            # ─── DECOMPRESSION RESULTS ────────────────────────────────────────────
            if st.session_state.decompressed_text is not None:
                st.markdown("---")
                st.markdown("<div class='section-title'>🔓 Resultado de Descompresión</div>", unsafe_allow_html=True)

                d_stats = st.session_state.decompression_stats
                d1, d2 = st.columns(2)
                with d1:
                    st.metric("⏱️ Tiempo descompresión", f"{d_stats.get('time_elapsed', 0)*1000:.1f} ms")
                with d2:
                    st.metric("🔤 Longitud recuperada", f"{d_stats.get('recovered_length', 0):,} chars")

                # VALIDATION
                original = st.session_state.original_text
                recovered = st.session_state.decompressed_text
                is_valid = original == recovered

                if is_valid:
                    st.markdown("""
                    <div class='validation-success'>
                        <div style='font-size:2rem;'>✅</div>
                        <h2>✔ VALIDACIÓN EXITOSA</h2>
                        <p>El archivo recuperado es <strong>idéntico</strong> al original.<br>
                        Compresión sin pérdida verificada — cada byte coincide perfectamente.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    diff_chars = sum(1 for a, b in zip(original, recovered) if a != b)
                    st.markdown(f"""
                    <div class='validation-error'>
                        <div style='font-size:2rem;'>❌</div>
                        <h2 style='color:#ef4444;'>✘ VALIDACIÓN FALLIDA</h2>
                        <p style='color:#fca5a5;'>El archivo recuperado difiere del original.<br>
                        Diferencias detectadas: {diff_chars} caracteres distintos.</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Show recovered preview
                with st.expander("👁 Vista previa del texto recuperado", expanded=False):
                    preview = recovered[:500] + ("..." if len(recovered) > 500 else "")
                    st.markdown(f"<div class='code-preview'>{preview}</div>", unsafe_allow_html=True)

                # Download button
                st.download_button(
                    "⬇️ Descargar texto recuperado",
                    data=recovered.encode('utf-8'),
                    file_name=f"recuperado_{st.session_state.filename}",
                    mime="text/plain"
                )

    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {str(e)}")
        st.info("💡 Asegúrate de que el archivo sea de texto plano (UTF-8).")

else:
    # Welcome state
    st.markdown("""
    <div style='text-align:center; padding: 3rem 1rem;'>
        <div style='font-size:4rem; margin-bottom:1rem;'>📂</div>
        <h3 style='color:#8892b0; font-weight:400;'>Carga un archivo para comenzar</h3>
        <p style='color:#4a5568; font-size:0.9rem;'>Soporta archivos .txt, .csv y .json · Usa el panel lateral izquierdo</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>🎓 Acerca de los Algoritmos</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class='info-panel' style='border-color:rgba(124,58,237,0.3);'>
        <span class='algo-badge badge-huffman'>Huffman Coding — 1952</span><br><br>
        Desarrollado por David Huffman, construye un árbol binario óptimo donde cada carácter recibe un código de longitud variable inversamente proporcional a su frecuencia de aparición.<br><br>
        <strong>Proceso:</strong><br>
        1. Calcular frecuencia de cada símbolo<br>
        2. Construir árbol de mínima prioridad<br>
        3. Asignar códigos binarios<br>
        4. Codificar el texto<br><br>
        <strong>Garantía:</strong> Código prefijo óptimo para distribución conocida.
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class='info-panel' style='border-color:rgba(0,212,255,0.2);'>
        <span class='algo-badge badge-lz77'>LZ77 — Lempel & Ziv, 1977</span><br><br>
        Algoritmo basado en diccionario deslizante. Busca coincidencias del texto actual dentro de una ventana de texto ya procesado y las reemplaza por referencias (offset, longitud).<br><br>
        <strong>Proceso:</strong><br>
        1. Mantener ventana deslizante<br>
        2. Buscar coincidencia en ventana<br>
        3. Emitir token (offset, length, char)<br>
        4. Avanzar posición<br><br>
        <strong>Base de:</strong> gzip, zlib, PNG, y la mayoría de compresores modernos.
        </div>
        """, unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='margin-top:3rem; border-color:rgba(0,212,255,0.08);'>
<div style='text-align:center; padding:1rem; color:#374151; font-size:0.78rem;'>
    CompresorLab · Implementación académica de Huffman Coding y LZ77 · 
    <span style='color:#6366f1;'>Compresión Sin Pérdida</span> · Teoría de la Información
</div>
""", unsafe_allow_html=True)
