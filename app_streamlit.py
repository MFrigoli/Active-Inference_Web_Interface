"""
app_streamlit.py
Web app interattiva per Railway Active Inference.

Avvio: streamlit run app_streamlit.py
"""

import random as _rnd
import streamlit as st
import plotly.graph_objects as go

from simulation  import run_simulation, compute_metrics, TRANSITION_WIN
from figures     import build_figures
from presets     import (
    _PRESET_KEYS, _BASE,
    _make_pick,
    _sync_attack_start, _sync_attack_end, _sync_sensor_noise,
    _sync_time_steps, _sync_seed,
)
from translations import T

# ---------------------------------------------------------------------------
# Session state init
# ---------------------------------------------------------------------------

for _k, _v in _BASE.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v
if "preset_selector" not in st.session_state:
    st.session_state["preset_selector"] = ""
_cur_preset = st.session_state.get("preset_selector", "")
for _i, _pname in enumerate(_PRESET_KEYS):
    if f"_pc_{_i}" not in st.session_state:
        st.session_state[f"_pc_{_i}"] = (_pname == _cur_preset)
if "lang" not in st.session_state:
    st.session_state["lang"] = "Italiano"

# ---------------------------------------------------------------------------
# Language
# ---------------------------------------------------------------------------

lang = "en" if st.session_state.get("lang") == "English" else "it"
t    = T[lang]

# ---------------------------------------------------------------------------
# Page config + CSS
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Railway Active Inference",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stSidebar"] [data-testid="column"] {
    display: flex;
    align-items: flex-start;
}
[data-testid="stSidebar"] [data-testid="column"] > div {
    width: 100%;
}
button[data-testid="stNumberInputStepUp"],
button[data-testid="stNumberInputStepDown"] {
    display: none;
}
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
    display: none !important;
}
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] label,
[data-testid="stMetricLabel"] div {
    font-size: 1.3rem !important;
}
[data-testid="stMetricValue"] > div,
[data-testid="stMetricValue"] {
    font-size: 2.8rem !important;
}
[data-testid="stMetricDelta"] {
    font-size: 1rem !important;
}
li:has(button[data-testid="main-menu-clearCache"]),
li:has(button[data-testid="main-menu-print"]),
li:has(button[data-testid="main-menu-screencast"]) {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.title(t["page_title"])
st.markdown(t["page_subtitle"])

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.radio("", ["Italiano", "English"], horizontal=True,
             key="lang", label_visibility="collapsed")

    st.divider()
    st.markdown(t["sb_fallace"])
    for _i, _pname in enumerate(_PRESET_KEYS):
        st.checkbox(
            t["preset_names"][_i], key=f"_pc_{_i}",
            help=t["preset_helps"][_i],
            on_change=_make_pick(_i, _pname),
        )

    st.divider()
    st.markdown(t["sb_params"])

    st.divider()
    st.subheader(t["sb_fdia"])
    st.caption(t["atk_start_cap"])
    _sl1, _ni1 = st.columns([0.72, 0.28])
    with _ni1:
        attack_start = st.number_input(
            "as", min_value=0, max_value=45, step=1,
            key="s_attack_start", label_visibility="collapsed",
        )
    with _sl1:
        st.session_state["_sl_attack_start"] = st.session_state["s_attack_start"]
        st.slider(t["atk_start_cap"], 0, 45, key="_sl_attack_start",
                  on_change=_sync_attack_start, label_visibility="collapsed")

    st.caption(t["atk_end_cap"])
    _sl2, _ni2 = st.columns([0.72, 0.28])
    with _ni2:
        attack_end = st.number_input(
            "ae", min_value=0, max_value=49, step=1,
            key="s_attack_end", label_visibility="collapsed",
        )
    with _sl2:
        st.session_state["_sl_attack_end"] = st.session_state["s_attack_end"]
        st.slider(t["atk_end_cap"], 0, 49, key="_sl_attack_end",
                  on_change=_sync_attack_end, label_visibility="collapsed")

    if attack_end < attack_start:
        st.warning(t["atk_warning"])

    st.caption(t["atk_val_cap"])
    _atk_val_choice = st.radio(
        t["atk_val_cap"],
        options=[0.0, 1.0],
        format_func=lambda v: f"{v:.1f}  ({t['atk_val_hidden'] if v == 0.0 else t['atk_val_opp']})",
        key="s_attack_value",
        horizontal=True,
        label_visibility="collapsed",
    )
    attack_value = _atk_val_choice

    st.divider()
    st.subheader(t["sb_sensor"])
    _sl3, _ni3 = st.columns([0.72, 0.28])
    with _ni3:
        sensor_noise = st.number_input(
            "sn", min_value=0.0, max_value=0.30, step=0.01, format="%.2f",
            key="s_sensor_noise", label_visibility="collapsed",
        )
    with _sl3:
        st.session_state["_sl_sensor_noise"] = st.session_state["s_sensor_noise"]
        st.slider(t["sb_sensor"], 0.0, 0.30, step=0.01, key="_sl_sensor_noise",
                  on_change=_sync_sensor_noise,
                  help=t["noise_help"], label_visibility="collapsed")

    st.divider()
    st.subheader(t["sb_costs"])
    _ca, _cb2, _cc = st.columns(3)
    with _ca:
        cost_maintain = st.number_input(
            t["cost_maintain_cap"], min_value=0.0, max_value=1.0, step=0.05,
            key="s_cost_maintain",
            help=t["cost_maintain_help"],
        )
    with _cb2:
        cost_slow = st.number_input(
            t["cost_slow_cap"], min_value=0.0, max_value=1.0, step=0.05,
            key="s_cost_slow",
            help=t["cost_slow_help"],
        )
    with _cc:
        cost_stop = st.number_input(
            t["cost_stop_cap"], min_value=0.0, max_value=1.0, step=0.05,
            key="s_cost_stop",
            help=t["cost_stop_help"],
        )

    st.divider()
    st.subheader(t["sb_time"])
    _sl_ts, _ni_ts = st.columns([0.72, 0.28])
    with _ni_ts:
        time_steps = st.number_input(
            "ts", min_value=30, max_value=100, step=1,
            key="s_time_steps", label_visibility="collapsed",
        )
    with _sl_ts:
        st.session_state["_sl_time_steps"] = st.session_state["s_time_steps"]
        st.slider(t["sb_time"], 30, 100, key="_sl_time_steps",
                  on_change=_sync_time_steps,
                  help=t["timestep_help"], label_visibility="collapsed")

    fixed_seed = st.checkbox(t["seed_fixed"], key="s_fixed_seed", help=t["seed_help"])
    st.caption(t["seed_cap"])
    _sl_sd, _ni_sd = st.columns([0.72, 0.28])
    with _ni_sd:
        seed = st.number_input(
            "sd", min_value=0, max_value=9999, step=1,
            key="s_seed", label_visibility="collapsed", disabled=not fixed_seed,
        )
    with _sl_sd:
        st.session_state["_sl_seed"] = st.session_state["s_seed"]
        st.slider(t["seed_cap"], 0, 9999, key="_sl_seed",
                  on_change=_sync_seed, label_visibility="collapsed",
                  disabled=not fixed_seed)

    st.divider()
    st.subheader(t["sb_arch"])

    _c1, _c2 = st.columns([0.55, 0.45])
    with _c1:
        enable_threshold = st.checkbox(t["arch_threshold_label"], key="s_enable_threshold",
            help=t["arch_threshold_help"])
    with _c2:
        anomaly_threshold = st.number_input(
            "thr", min_value=0.01, max_value=0.95, step=0.01,
            key="s_anomaly_threshold", label_visibility="collapsed",
            disabled=not enable_threshold,
        )

    _c1, _c2 = st.columns([0.55, 0.45])
    with _c1:
        enable_uncertainty = st.checkbox(t["arch_uncertainty_label"], key="s_enable_uncertainty",
            help=t["arch_uncertainty_help"])
    with _c2:
        min_uncertainty = st.number_input(
            "min", min_value=0.0, max_value=1.0, step=0.05,
            key="s_min_uncertainty", label_visibility="collapsed",
            disabled=not enable_uncertainty,
        )

    enable_model = st.checkbox(t["arch_model_label"], key="s_enable_model",
        help=t["arch_model_help"])
    lucky_model = st.session_state.get("s_lucky_model", False)

    st.divider()
    st.subheader(t["sb_efe"], help=t["efe_help"])
    enable_risk = st.checkbox(t["efe_risk_label"], key="s_enable_risk",
        help=t["efe_risk_help"])
    _, _cb = st.columns([0.08, 0.92])
    with _cb:
        enable_hazard = st.checkbox(t["efe_hazard_label"], key="s_enable_hazard",
            disabled=not enable_risk, help=t["efe_hazard_help"])
        enable_cost   = st.checkbox(t["efe_cost_label"],   key="s_enable_cost",
            disabled=not enable_risk, help=t["efe_cost_help"])
    if not enable_risk:
        enable_hazard = False
        enable_cost   = False
    enable_epistemic = st.checkbox(t["efe_epistemic_label"], key="s_enable_epistemic",
        help=t["efe_epistemic_help"])

# ---------------------------------------------------------------------------
# Simulazione
# ---------------------------------------------------------------------------

_effective_seed = int(seed) if fixed_seed else _rnd.randint(0, 9999)
log = run_simulation(
    anomaly_threshold=anomaly_threshold,
    sensor_noise=sensor_noise,
    attack_start=attack_start,
    attack_end=attack_end,
    time_steps=time_steps,
    enable_hazard=enable_hazard,
    enable_cost=enable_cost,
    enable_epistemic=enable_epistemic,
    cost_maintain=cost_maintain,
    cost_slow=cost_slow,
    cost_stop=cost_stop,
    seed=_effective_seed,
    enable_threshold=enable_threshold,
    enable_uncertainty=enable_uncertainty,
    enable_model=enable_model,
    min_uncertainty=min_uncertainty,
    lucky_model=lucky_model,
    attack_value=attack_value,
)

# ---------------------------------------------------------------------------
# Metriche rapide
# ---------------------------------------------------------------------------

log_baseline = run_simulation(
    anomaly_threshold=0.30, sensor_noise=0.05,
    attack_start=22, attack_end=28, time_steps=50,
    enable_hazard=True, enable_cost=True, enable_epistemic=True,
    cost_maintain=0.1, cost_slow=0.4, cost_stop=0.8,
    seed=42,
    enable_threshold=True, enable_uncertainty=True, enable_model=True,
    min_uncertainty=0.1, lucky_model=False,
)
f1_baseline = compute_metrics(log_baseline)["f1"]

n_anomalies = sum(1 for d in log if d["anomaly"])
m           = compute_metrics(log)
tp          = m["tp"]
fp          = m["fp"]
fn          = m["fn"]
prec        = m["precision"]
f1          = m["f1"]
degradazione = (1 - f1 / f1_baseline) * 100 if f1_baseline > 0 else 0.0

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
col1.metric(t["m_anomalies"], n_anomalies, help=t["m_anomalies_help"])
col2.metric("TP", tp, f"/{m['max_tp']} max", help=t["m_tp_help"])
col3.metric("FP", fp,                      help=t["m_fp_help"])
col4.metric("FN", fn,                      help=t["m_fn_help"])
col5.metric(t["m_f1"],   f"{f1:.0%}",      help=t["m_f1_help"])
col6.metric(t["m_prec"], f"{prec:.0%}",    help=t["m_prec_help"])
col7.metric(t["m_deg"],  f"{degradazione:.1f}%", help=t["m_deg_help"])

st.divider()

# ---------------------------------------------------------------------------
# Grafici
# ---------------------------------------------------------------------------

layers, overview = build_figures(log, attack_start, attack_end, anomaly_threshold, lang=lang)

tab_overview, tab_layers, tab_abl1, tab_abl2 = st.tabs([
    t["tab_overview"], t["tab_layers"], t["tab_abl1"], t["tab_abl2"]
])

# ── GRAFICI PANORAMICI ────────────────────────────────────────────────────────
with tab_overview:
    ov_state, ov_vel, ov_unc, ov_efe = overview
    _cfg = {"displayModeBar": False}
    st.plotly_chart(ov_state, width="stretch", config=_cfg)
    col_v, col_u = st.columns(2)
    with col_v:
        st.plotly_chart(ov_vel, width="stretch", config=_cfg)
    with col_u:
        st.plotly_chart(ov_unc, width="stretch", config=_cfg)
    st.plotly_chart(ov_efe, width="stretch", config=_cfg)
    st.markdown(t["overview_md"], unsafe_allow_html=True)

# ── PERCORSO DECISIONALE ──────────────────────────────────────────────────────
with tab_layers:
    _cfg = {"displayModeBar": False}
    for fig in layers:
        st.plotly_chart(fig, width="stretch", config=_cfg)
    st.markdown(t["layers_md"])

# ── ABLAZIONE 1 ───────────────────────────────────────────────────────────────
with tab_abl1:
    st.markdown(t["abl1_title"])

    _times  = [d["t"]                   for d in log]
    _vel    = [d["velocity"]            for d in log]
    _perr   = [d["prediction_error"]    for d in log]
    _unc    = [d["uncertainty"]         for d in log]
    _epist  = [d["epistemic_slow_val"]  for d in log]
    _negpv  = [-d["pragmatic_value"]    for d in log]

    _xrng  = [-0.5, _times[-1] + 0.5]
    _atk_r = dict(type="rect", xref="x", yref="paper",
                  x0=attack_start - 0.5, x1=attack_end + 0.5,
                  y0=0, y1=1,
                  fillcolor="rgba(231,76,60,0.15)" if attack_start < attack_end else "rgba(0,0,0,0)",
                  line_width=0, layer="below")

    _slow_t = [d["t"]        for d in log if d["action"] == "epistemic_slow"]
    _slow_v = [d["velocity"] for d in log if d["action"] == "epistemic_slow"]

    _missing = []
    if not enable_epistemic:
        _missing.append(t["abl1_miss_epistemic"])
    if not enable_threshold:
        _missing.append(t["abl1_miss_threshold"])
    elif enable_threshold and anomaly_threshold < 0.05:
        _missing.append(t["abl1_miss_threshold_low"])
    if not enable_uncertainty:
        _missing.append(t["abl1_miss_uncertainty"])
    elif enable_uncertainty and min_uncertainty > 0.5:
        _missing.append(t["abl1_miss_unc_locked"])
    if not enable_model:
        _missing.append(t["abl1_miss_model"])
    if lucky_model:
        _missing.append(t["abl1_miss_lucky"])
    if not enable_hazard:
        _missing.append(t["abl1_miss_risk"])
    if not enable_cost:
        _missing.append(t["abl1_miss_cost"])
    if cost_maintain > 0.5:
        _missing.append(t["abl1_miss_cost_high"])

    if not _missing:
        _title_text  = t["abl1_baseline"]
        _title_color = "#27ae60"
        _status      = t["abl1_ok"]
    else:
        _title_text  = t["abl1_without"] + " + ".join(_missing)
        _title_color = "#e74c3c"
        _status      = t["abl1_fail"]

    _fv = go.Figure()
    _fv.add_shape(**_atk_r)
    _fv.add_trace(go.Scatter(
        x=_times, y=_vel, showlegend=False,
        line=dict(color="#27ae60", width=2),
        hovertemplate="t=%{x} | v=%{y}<extra></extra>",
    ))
    if _slow_t:
        _fv.add_trace(go.Scatter(
            x=_slow_t, y=_slow_v, mode="markers", showlegend=False,
            marker=dict(color="#2980b9", size=6, symbol="circle"),
        ))
    _fv.update_layout(
        title=dict(text=f"{_status} {_title_text}", font=dict(color=_title_color, size=12)),
        xaxis=dict(range=_xrng, dtick=10),
        yaxis=dict(range=[-0.5, 12], title=t["abl1_vel_axis"]),
        height=280, margin=dict(t=40, b=40, l=50, r=10), showlegend=False,
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    _fp2 = go.Figure()
    _fp2.add_shape(**_atk_r)
    _fp2.add_trace(go.Scatter(
        x=_times, y=_perr, name=t["abl1_pred_err"],
        line=dict(color="#27ae60", width=1.5),
        hovertemplate="t=%{x} | err=%{y:.3f}<extra></extra>",
    ))
    _fp2.add_trace(go.Scatter(
        x=_times, y=_unc, name=t["abl1_unc"],
        line=dict(color="#2980b9", width=1.5, dash="dash"),
        hovertemplate="t=%{x} | unc=%{y:.3f}<extra></extra>",
    ))
    _fp2.add_trace(go.Scatter(
        x=_times, y=[anomaly_threshold] * len(_times),
        name=f"{t['abl1_threshold']} ({anomaly_threshold:.2f})",
        line=dict(color="#e74c3c", width=1, dash="dot"),
    ))
    _fp2.update_layout(
        title=dict(text=t["abl1_pred_err_unc_title"], font=dict(size=12)),
        xaxis=dict(range=_xrng, dtick=10),
        yaxis=dict(range=[0, 1.15], title=t["abl1_val_axis"]),
        legend=dict(
            orientation="v", x=0.01, y=0.98,
            xanchor="left", yanchor="top",
            font=dict(size=12),
            bgcolor="rgba(0,0,0,0)",
            itemclick=False, itemdoubleclick=False,
        ),
        height=280, margin=dict(t=40, b=40, l=50, r=10),
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    _fe = go.Figure()
    _fe.add_shape(**_atk_r)
    _fe.add_trace(go.Scatter(
        x=_times, y=_epist, showlegend=False,
        line=dict(color="#8e44ad", width=2),
        hovertemplate="t=%{x} | epist=%{y:.3f}<extra></extra>",
    ))
    _fe.update_layout(
        title=dict(text=t["abl1_epist_val_title"], font=dict(size=12)),
        xaxis=dict(range=_xrng, dtick=10),
        yaxis=dict(range=[0, 1.2], title=t["abl1_val_axis"]),
        height=280, margin=dict(t=40, b=40, l=50, r=10), showlegend=False,
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    _fpv = go.Figure()
    _fpv.add_shape(**_atk_r)
    _fpv.add_trace(go.Scatter(
        x=_times, y=_negpv, showlegend=False,
        line=dict(color="#e67e22", width=2),
        hovertemplate="t=%{x} | −PV=%{y:.3f}<extra></extra>",
    ))
    _fpv.update_layout(
        title=dict(text=t["abl1_prag_val_title"], font=dict(size=12)),
        xaxis=dict(range=_xrng, dtick=10),
        yaxis=dict(title=t["abl1_val_axis"]),
        height=280, margin=dict(t=40, b=40, l=50, r=10), showlegend=False,
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    st.plotly_chart(_fv,  use_container_width=True, config={"displayModeBar": False})
    st.plotly_chart(_fp2, use_container_width=True, config={"displayModeBar": False})
    st.plotly_chart(_fe,  use_container_width=True, config={"displayModeBar": False})
    st.plotly_chart(_fpv, use_container_width=True, config={"displayModeBar": False})

    st.divider()
    st.markdown(t["abl1_md"])

# ── ABLAZIONE 2 ───────────────────────────────────────────────────────────────
with tab_abl2:
    st.markdown(t["abl2_title"])

    _h = enable_hazard
    _c = enable_cost
    _e = enable_epistemic

    if _h and _c and _e:
        _v2_name, _v2_formula = "FULL",           "−PV − E"
    elif not _h and _c and _e:
        _v2_name, _v2_formula = "NO_RISK",        "C − E"
    elif _h and not _c and _e:
        _v2_name, _v2_formula = "NO_COST",        "R − E"
    elif _h and _c and not _e:
        _v2_name, _v2_formula = "NO_EPISTEMIC",   "−PV"
    elif _h and not _c and not _e:
        _v2_name, _v2_formula = "ONLY_RISK",      "R"
    elif not _h and _c and not _e:
        _v2_name, _v2_formula = "ONLY_COST",      "C"
    elif not _h and not _c and _e:
        _v2_name, _v2_formula = "ONLY_EPISTEMIC", "−E"
    else:
        _v2_name, _v2_formula = "NONE",           "0"

    _v2_tp   = sum(1 for d in log if d["velocity"] < 10 and TRANSITION_WIN[0] <= d["t"] <= TRANSITION_WIN[1])
    _v2_fp   = sum(1 for d in log if d["velocity"] < 10 and not (TRANSITION_WIN[0] <= d["t"] <= TRANSITION_WIN[1]))
    _v2_prec = _v2_tp / (_v2_tp + _v2_fp) if (_v2_tp + _v2_fp) > 0 else 0.0

    _v2_times = [d["t"]        for d in log]
    _v2_vel   = [d["velocity"] for d in log]
    _v2_xrng  = [-0.5, _v2_times[-1] + 0.5]

    _v2_fig = go.Figure()
    _v2_fig.add_shape(
        type="rect", xref="x", yref="paper",
        x0=19.5, x1=30.5, y0=0, y1=1,
        fillcolor="rgba(255,230,150,0.35)", line_width=0, layer="below",
    )
    _v2_fig.add_shape(
        type="rect", xref="x", yref="paper",
        x0=attack_start - 0.5, x1=attack_end + 0.5, y0=0, y1=1,
        fillcolor="rgba(231,76,60,0.20)" if attack_start < attack_end else "rgba(0,0,0,0)",
        line_width=0, layer="below",
    )
    _v2_fig.add_trace(go.Scatter(
        x=_v2_times, y=_v2_vel,
        fill="tozeroy",
        fillcolor="rgba(100,160,220,0.25)",
        line=dict(color="#2980b9", width=2),
        showlegend=False,
        hovertemplate="t=%{x} | v=%{y} km/h<extra></extra>",
    ))

    _v2_color_css = "#27ae60" if _v2_name not in ("NONE",) else "#e74c3c"
    st.markdown(
        f"<div style='font-size:1.4rem; font-weight:700; color:{_v2_color_css}; margin-bottom:4px'>"
        f"{_v2_name} &nbsp;|&nbsp; "
        f"<span style='font-weight:400'>{_v2_formula}</span> &nbsp;|&nbsp; "
        f"<span style='font-size:1.1rem; color:#ccc'>TP={_v2_tp}/{MAX_TP} &nbsp; FP={_v2_fp} &nbsp; Prec={_v2_prec:.2f}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    _v2_fig.update_layout(
        xaxis=dict(range=_v2_xrng, dtick=10, showgrid=True),
        yaxis=dict(range=[0, 12], title=t["abl2_vel_axis"], showgrid=True),
        height=380,
        margin=dict(t=20, b=50, l=60, r=20),
        legend=dict(itemclick=False, itemdoubleclick=False),
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    st.plotly_chart(_v2_fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(t["abl2_how_to_md"])

    st.divider()
    st.markdown(t["abl2_formula_md"])
