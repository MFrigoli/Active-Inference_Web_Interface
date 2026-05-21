"""
app_streamlit.py
Web app interattiva per Railway Active Inference.

Avvio: streamlit run app_streamlit.py
"""

import random as _rnd
import streamlit as st
import plotly.graph_objects as go

from simulation import run_simulation, compute_f1, TRANSITION_WIN, MAX_TP
from figures    import build_figures, ACTION_COLORS, ACTION_LABELS
from presets    import (
    FALLACIOUS_PRESETS, _PRESET_HELP, _PRESET_KEYS, _BASE,
    apply_preset, _make_pick,
    _sync_attack_start, _sync_attack_end, _sync_sensor_noise,
    _sync_time_steps, _sync_seed,
)

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

st.title("Railway Active Inference — Demo interattiva")
st.markdown(
    "Modifica i parametri nella barra laterale. "
    "I grafici si aggiornano in tempo reale."
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## Sistema fallace")
    for _i, (_pname, _phelp) in enumerate(_PRESET_HELP.items()):
        st.checkbox(_pname, key=f"_pc_{_i}", help=_phelp, on_change=_make_pick(_i, _pname))

    st.divider()
    st.markdown("## Parametri simulazione")

    st.divider()
    st.subheader("Attacco FDIA")
    st.caption("Inizio attacco (t)")
    _sl1, _ni1 = st.columns([0.72, 0.28])
    with _ni1:
        attack_start = st.number_input(
            "as", min_value=0, max_value=45, step=1,
            key="s_attack_start", label_visibility="collapsed",
        )
    with _sl1:
        st.session_state["_sl_attack_start"] = st.session_state["s_attack_start"]
        st.slider("Inizio attacco (t)", 0, 45, key="_sl_attack_start",
                  on_change=_sync_attack_start, label_visibility="collapsed")

    st.caption("Fine attacco (t)")
    _sl2, _ni2 = st.columns([0.72, 0.28])
    with _ni2:
        attack_end = st.number_input(
            "ae", min_value=0, max_value=49, step=1,
            key="s_attack_end", label_visibility="collapsed",
        )
    with _sl2:
        st.session_state["_sl_attack_end"] = st.session_state["s_attack_end"]
        st.slider("Fine attacco (t)", 0, 49, key="_sl_attack_end",
                  on_change=_sync_attack_end, label_visibility="collapsed")

    if attack_end < attack_start:
        st.warning("Fine attacco deve essere ≥ inizio attacco.")

    st.caption("Valore iniettato dall'attacco")
    _atk_val_choice = st.radio(
        "Valore iniettato",
        options=[0.0, 1.0],
        format_func=lambda v: f"{v:.1f}  ({'nascosto: stesso stato reale' if v == 0.0 else 'opposto: massima discrepanza'})",
        key="s_attack_value",
        horizontal=True,
        label_visibility="collapsed",
    )
    attack_value = _atk_val_choice

    st.divider()
    st.subheader("Sensore e belief")
    _sl3, _ni3 = st.columns([0.72, 0.28])
    with _ni3:
        sensor_noise = st.number_input(
            "sn", min_value=0.0, max_value=0.30, step=0.01, format="%.2f",
            key="s_sensor_noise", label_visibility="collapsed",
        )
    with _sl3:
        st.session_state["_sl_sensor_noise"] = st.session_state["s_sensor_noise"]
        st.slider("Rumore sensore", 0.0, 0.30, step=0.01, key="_sl_sensor_noise",
                  on_change=_sync_sensor_noise,
                  help="Ampiezza del rumore uniforme [-n, +n] aggiunto alla lettura del sensore")

    st.divider()
    st.subheader("Costi azioni")
    _ca, _cb2, _cc = st.columns(3)
    with _ca:
        cost_maintain = st.number_input(
            "maintain", min_value=0.0, max_value=1.0, step=0.05,
            key="s_cost_maintain",
            help="Costo operativo per mantenere velocità nominale (default 0.1)",
        )
    with _cb2:
        cost_slow = st.number_input(
            "slow", min_value=0.0, max_value=1.0, step=0.05,
            key="s_cost_slow",
            help="Costo operativo per rallentare — azione epistemica (default 0.4)",
        )
    with _cc:
        cost_stop = st.number_input(
            "stop", min_value=0.0, max_value=1.0, step=0.05,
            key="s_cost_stop",
            help="Costo operativo per fermarsi — azione pragmatica (default 0.8)",
        )

    st.divider()
    st.subheader("Timestep e seed")
    _sl_ts, _ni_ts = st.columns([0.72, 0.28])
    with _ni_ts:
        time_steps = st.number_input(
            "ts", min_value=30, max_value=100, step=1,
            key="s_time_steps", label_visibility="collapsed",
        )
    with _sl_ts:
        st.session_state["_sl_time_steps"] = st.session_state["s_time_steps"]
        st.slider("Timestep totali", 30, 100, key="_sl_time_steps",
                  on_change=_sync_time_steps,
                  help="Durata totale della simulazione in passi temporali")

    fixed_seed = st.checkbox("Seed fisso", key="s_fixed_seed",
        help="Seed = numero iniziale che controlla il generatore di numeri casuali. "
             "Stesso seed → stesso rumore ad ogni run → simulazione riproducibile. "
             "Se spento, seed cambia ad ogni interazione → rumore diverso ogni volta.")
    st.caption("Seed")
    _sl_sd, _ni_sd = st.columns([0.72, 0.28])
    with _ni_sd:
        seed = st.number_input(
            "sd", min_value=0, max_value=9999, step=1,
            key="s_seed", label_visibility="collapsed", disabled=not fixed_seed,
        )
    with _sl_sd:
        st.session_state["_sl_seed"] = st.session_state["s_seed"]
        st.slider("Seed", 0, 9999, key="_sl_seed",
                  on_change=_sync_seed, label_visibility="collapsed",
                  disabled=not fixed_seed)

    st.divider()
    st.subheader("Componenti architetturali")

    _c1, _c2 = st.columns([0.55, 0.45])
    with _c1:
        enable_threshold = st.checkbox("Anomaly Threshold", key="s_enable_threshold",
            help="Soglia prediction error — Se off: nessuna anomalia rilevata")
    with _c2:
        anomaly_threshold = st.number_input(
            "thr", min_value=0.01, max_value=0.95, step=0.01,
            key="s_anomaly_threshold", label_visibility="collapsed",
            disabled=not enable_threshold,
        )

    _c1, _c2 = st.columns([0.55, 0.45])
    with _c1:
        enable_uncertainty = st.checkbox("Uncertainty dinamica", key="s_enable_uncertainty",
            help="Valore minimo incertezza — Se off: uncertainty fissa a 0")
    with _c2:
        min_uncertainty = st.number_input(
            "min", min_value=0.0, max_value=1.0, step=0.05,
            key="s_min_uncertainty", label_visibility="collapsed",
            disabled=not enable_uncertainty,
        )

    enable_model = st.checkbox("Modello interno", key="s_enable_model",
        help="Se off: expected=0 sempre")
    lucky_model = st.session_state.get("s_lucky_model", False)

    st.divider()
    st.subheader("Componenti EFE",
        help="L'agente sceglie l'azione con il costo totale più basso. Disattiva i componenti per vedere come cambia il comportamento.")
    enable_risk = st.checkbox("Pragmatic  (= Risk + Cost)", key="s_enable_risk",
        help="Il termine 'pratico': tiene conto del pericolo fisico e del costo dell'azione. Se disattivato, l'agente ignora completamente rischi e costi.")
    _, _cb = st.columns([0.08, 0.92])
    with _cb:
        enable_hazard = st.checkbox("Risk", key="s_enable_hazard", disabled=not enable_risk,
            help="Quanto è pericoloso trovarsi vicino alla zona di transizione dello scambio. Più ci si avvicina, più il rischio sale.")
        enable_cost   = st.checkbox("Cost", key="s_enable_cost",   disabled=not enable_risk,
            help="Ogni azione ha un costo fisso: mantieni (0.1) < rallenta (0.4) < fermati (0.8). Incentiva a non frenare inutilmente.")
    if not enable_risk:
        enable_hazard = False
        enable_cost   = False
    enable_epistemic = st.checkbox("Epistemic", key="s_enable_epistemic",
        help="Premia l'azione 'rallenta' quando il sistema è incerto: rallentare permette di osservare meglio lo scambio e ridurre il dubbio. Se disattivato, l'agente non esplora mai.")

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

# Baseline fisso per calcolo degradazione
log_baseline = run_simulation(
    anomaly_threshold=0.30, sensor_noise=0.05,
    attack_start=22, attack_end=28, time_steps=50,
    enable_hazard=True, enable_cost=True, enable_epistemic=True,
    cost_maintain=0.1, cost_slow=0.4, cost_stop=0.8,
    seed=42,
    enable_threshold=True, enable_uncertainty=True, enable_model=True,
    min_uncertainty=0.1, lucky_model=False,
)
f1_baseline = compute_f1(log_baseline)

n_anomalies  = sum(1 for d in log if d["anomaly"])
tp           = sum(1 for d in log if d["velocity"] < 10 and TRANSITION_WIN[0] <= d["t"] <= TRANSITION_WIN[1])
fp           = sum(1 for d in log if d["velocity"] < 10 and not (TRANSITION_WIN[0] <= d["t"] <= TRANSITION_WIN[1]))
fn           = MAX_TP - tp
prec         = tp / (tp + fp) if (tp + fp) > 0 else 0.0
f1           = compute_f1(log)
degradazione = (1 - f1 / f1_baseline) * 100 if f1_baseline > 0 else 0.0

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
col1.metric("Anomalie", n_anomalies,
            help="Totale timestep in cui il belief ha rilevato un'anomalia")
col2.metric("TP", tp, f"/{MAX_TP} max",
            help="Timestep in cui il treno rallenta nella finestra di transizione [20,30]")
col3.metric("FP", fp,
            help="Timestep in cui il treno rallenta inutilmente fuori dalla finestra di transizione [20,30]")
col4.metric("FN", fn,
            help="Timestep in cui il treno non rallenta quando dovrebbe (11 − TP)")
col5.metric("F1-score", f"{f1:.0%}",
            help="Media tra precisione e recall: misura quanto il sistema è sia preciso sia completo nel reagire al pericolo. 100% = reazione perfetta, 0% = nessuna reazione utile.")
col6.metric("Precisione", f"{prec:.0%}",
            help="Quante delle volte in cui il treno ha rallentato, lo ha fatto davvero per un pericolo reale. Bassa = troppi falsi allarmi.")
col7.metric("Degradazione", f"{degradazione:.1f}%",
            help="Quanto peggiora il sistema rispetto alla configurazione completa (baseline). 0% = nessuna perdita, 100% = il sistema non funziona più.")

st.divider()

# ---------------------------------------------------------------------------
# Grafici
# ---------------------------------------------------------------------------

layers, overview = build_figures(log, attack_start, attack_end, anomaly_threshold)

tab_overview, tab_layers, tab_abl1, tab_abl2 = st.tabs(
    ["GRAFICI PANORAMICI", "PERCORSO DECISIONALE", "ABLAZIONE 1", "ABLAZIONE 2"]
)

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

    st.markdown("""
### Come leggere i grafici

| Grafico | Cosa mostra | Come leggerlo |
|---|---|---|
| **Stato switch:**<br>reale vs stimato vs sensore | Il confronto tra lo stato reale dello scambio (ground truth), la lettura del sensore (che può essere compromessa) e la stima interna del sistema (belief). | Quando sensore e stato reale divergono (durante l'attacco), il sistema dovrebbe ignorare il sensore e usare la propria stima. I marker × rossi indicano i momenti di anomalia rilevata. |
| **Velocità treno e azione scelta** | La velocità del treno ad ogni istante, colorata per azione: verde = mantieni (10), arancio = rallenta (4), rosso = fermati (0). | Verde dominante = comportamento normale. Se arancio/rosso compaiono nella finestra t=20–30, l'agente ha reagito correttamente al pericolo. Se compaiono anche fuori, ci sono falsi allarmi. |
| **Incertezza epistemica nel tempo** | Quanto il sistema è "confuso" sullo stato dello scambio in ogni istante. | Picchi alti = il sistema è incerto e cerca informazioni. Se l'incertezza sale durante l'attacco, il sistema ha riconosciuto che qualcosa non va. Se rimane bassa, ha accettato i dati falsi del sensore. |
| **Valori EFE per azione** | I valori di Expected Free Energy per le tre azioni (mantieni, rallenta, fermati). L'agente sceglie sempre l'azione con EFE minimo. | La curva più in basso ad ogni istante indica l'azione scelta. Quando *slow* scende sotto *maintain*, l'agente rallenta. Quando le curve si incrociano, cambia l'azione preferita. |
""", unsafe_allow_html=True)

with tab_layers:
    _cfg = {"displayModeBar": False}
    for fig in layers:
        st.plotly_chart(fig, width="stretch", config=_cfg)

    st.markdown("""
### Come leggere i grafici

| Grafico | Cosa mostra | Come leggerlo |
|---|---|---|
| **1. Stato fisico** | Lo stato reale dello scambio confrontato con la lettura del sensore. | Divergenza tra le due linee = il sensore è compromesso dall'attacco. Il sistema deve ignorare il sensore e affidarsi al modello interno. |
| **2. Inference Layer: belief** | La stima interna (belief) sullo stato dello scambio, con l'incertezza (area grigia) e i momenti di anomalia rilevata (× rossi). | Quando il belief si discosta dal sensore e segue il modello interno, il sistema ha capito che i dati sono corrotti. Più × rossi durante l'attacco, meglio. |
| **3. Prediction Error vs Soglia** | L'errore di predizione (quanto il sensore si discosta dall'atteso) confrontato con la soglia di anomalia (linea tratteggiata rossa). | Ogni volta che la linea arancione supera la soglia, scatta il rilevamento anomalia. Più spesso supera durante l'attacco (e non fuori), migliore è il comportamento. |
| **4a. EFE Maintain** | Il calcolo EFE per l'azione "mantieni velocità": −PragmaticValue (rosso), Epistemic Value = 0, e la EFE risultante. | EFE basso = questa azione è conveniente in quel momento. Confrontalo con 4b e 4c per capire perché vince o perde. |
| **4b. EFE Slow** | Il calcolo EFE per "rallenta": −PragmaticValue (rosso), guadagno epistemico (viola) e EFE risultante. | Quando il termine epistemico (viola) è alto, l'azione slow diventa più conveniente delle altre. I punti indicano quando è stata scelta. |
| **4c. EFE Stop** | Il calcolo EFE per "fermati": −PragmaticValue alto (il costo di stop è 0.8) e EFE risultante. | Stop ha il costo operativo più alto, quindi vince solo quando il rischio fisico è molto elevato e supera lo svantaggio del costo. |
| **5. Decision Layer: EFE minimo** | I valori EFE delle tre azioni sovrapposti, con i marker dell'azione scelta. | L'azione scelta ad ogni istante è quella con la curva più in basso. Quando le curve si incrociano, cambia l'azione preferita dell'agente. |
| **6. Action Layer: velocità** | La velocità del treno con le aree colorate per azione: verde = mantieni, blu = rallenta, rosso = fermati. | Le aree colorate mostrano per quanto tempo ogni azione è stata attiva. Blu nella finestra t=20–30 = risposta corretta all'attacco. |
""")


with tab_abl1:
    st.markdown("## Ablazione 1 — Effetto della rimozione di ciascun componente architetturale")

    _times  = [d["t"]                   for d in log]
    _vel    = [d["velocity"]            for d in log]
    _perr   = [d["prediction_error"]    for d in log]
    _unc    = [d["uncertainty"]         for d in log]
    _epist  = [d["epistemic_slow_val"]  for d in log]
    _negpv  = [-d["pragmatic_value"]    for d in log]

    _tp_a1   = sum(1 for d in log if d["velocity"] < 10 and TRANSITION_WIN[0] <= d["t"] <= TRANSITION_WIN[1])
    _fp_a1   = sum(1 for d in log if d["velocity"] < 10 and not (TRANSITION_WIN[0] <= d["t"] <= TRANSITION_WIN[1]))
    _prec_a1 = _tp_a1 / (_tp_a1 + _fp_a1) if (_tp_a1 + _fp_a1) > 0 else 0.0

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
        _missing.append("EPISTEMIC VALUE")
    if not enable_threshold:
        _missing.append("ANOMALY THRESHOLD")
    if not enable_uncertainty:
        _missing.append("UNCERTAINTY DINAMICA")
    if not enable_model:
        _missing.append("MODELLO INTERNO")
    if lucky_model:
        _missing.append("LUCKY MODEL")
    if not enable_hazard:
        _missing.append("RISK")
    if not enable_cost:
        _missing.append("COST")

    if not _missing:
        _title_text  = "BASELINE (sistema completo)"
        _title_color = "#27ae60"
        _status      = "[OK]"
    else:
        _title_text  = "SENZA " + " + ".join(_missing)
        _title_color = "#e74c3c"
        _status      = "[FAIL]"

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
        yaxis=dict(range=[-0.5, 12], title="Velocità"),
        height=280, margin=dict(t=40, b=40, l=50, r=10), showlegend=False,
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    _fp2 = go.Figure()
    _fp2.add_shape(**_atk_r)
    _fp2.add_trace(go.Scatter(
        x=_times, y=_perr, name="Prediction error",
        line=dict(color="#27ae60", width=1.5),
        hovertemplate="t=%{x} | err=%{y:.3f}<extra></extra>",
    ))
    _fp2.add_trace(go.Scatter(
        x=_times, y=_unc, name="Uncertainty",
        line=dict(color="#2980b9", width=1.5, dash="dash"),
        hovertemplate="t=%{x} | unc=%{y:.3f}<extra></extra>",
    ))
    _fp2.add_trace(go.Scatter(
        x=_times, y=[anomaly_threshold] * len(_times),
        name=f"Soglia ({anomaly_threshold:.2f})",
        line=dict(color="#e74c3c", width=1, dash="dot"),
    ))
    _fp2.update_layout(
        title=dict(text="Prediction Error & Uncertainty", font=dict(size=12)),
        xaxis=dict(range=_xrng, dtick=10),
        yaxis=dict(range=[0, 1.15], title="Valore"),
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
        title=dict(text="Epistemic Value", font=dict(size=12)),
        xaxis=dict(range=_xrng, dtick=10),
        yaxis=dict(range=[0, 1.2], title="Valore"),
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
        title=dict(text="Pragmatic Value", font=dict(size=12)),
        xaxis=dict(range=_xrng, dtick=10),
        yaxis=dict(title="Valore"),
        height=280, margin=dict(t=40, b=40, l=50, r=10), showlegend=False,
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    st.plotly_chart(_fv,  use_container_width=True, config={"displayModeBar": False})
    st.plotly_chart(_fp2, use_container_width=True, config={"displayModeBar": False})
    st.plotly_chart(_fe,  use_container_width=True, config={"displayModeBar": False})
    st.plotly_chart(_fpv, use_container_width=True, config={"displayModeBar": False})

    st.divider()
    st.markdown("""
### Come leggere i grafici

| Grafico | Cosa mostra | Come leggerlo |
|---|---|---|
|  Azione (Velocità) | Velocità del treno ad ogni istante. Tre possibili azioni: mantieni (10), rallenta (4), fermati (0). | Se rallenta durante t=20–30 (transizione reale), il pericolo è stato rilevato. Se rimane a 10, nessuna reazione. Se rallenta anche fuori da quella finestra, ci sono falsi allarmi. |
|  Prediction Error & Uncertainty | Errore di predizione (linea continua) — quanto il sensore si discosta da ciò che il modello si aspettava — e incertezza della belief (linea tratteggiata) — quanto il sistema è "confuso" sullo stato dello scambio. | Quando l'errore supera la soglia (linea puntinata rossa), il sistema alza l'incertezza al massimo: è il segnale che innesca la risposta. Se l'errore non supera mai la soglia, l'anomalia non viene rilevata. |
|  Epistemic Value | Quanto vale "rallentare per guardare meglio". Premia l'azione *slow* quando l'incertezza è alta. | Picco alto → il sistema ha molto da guadagnare dall'esplorazione e sceglie di rallentare. Piatto a zero → l'epistemic value non influenza la scelta e il sistema tende a mantenere velocità. |
|  Pragmatic Value | Costo pragmatico dell'azione scelta: rischio fisico (vicinanza alla transizione) + costo operativo (maintain=0.1, slow=0.4, stop=0.8). | Sale vicino alla zona di pericolo o quando l'azione scelta è costosa. Un valore alto non è necessariamente sbagliato: il sistema sta pagando un costo per gestire una situazione rischiosa. |

### Effetto della rimozione di ciascun componente architetturale

| Componente rimosso | Effetto osservato |
|---|---|
| **Senza Epistemic Value** | Nessun incentivo a rallentare per ridurre l'incertezza. EFE = −PragmaticValue per tutte le azioni → maintain vince sempre (costo minimo). Velocità sempre 10, TP = 0. |
| **Senza Anomaly Threshold** | Il belief segue sempre il sensore, nessuna anomalia rilevata durante l'attacco. L'incertezza si alza comunque vicino a TRANSITION (0.5), quindi l'epistemic value può ancora far vincere slow — ma non correlato all'attacco FDIA. |
| **Senza Uncertainty dinamica** | Uncertainty fissa a 0 → epistemic value = 0 → maintain vince sempre. Il sistema non apprende dalla propria incertezza. |
| **Senza Modello interno** | Expected state sempre 0. Il sensore legge 0.5 durante la transizione → prediction_error > soglia fuori dall'attacco (FP alti). Durante l'attacco il sensore injetta 0.0 = expected → errore = 0 → nessuna anomalia rilevata (TP = 0). |
""")

with tab_abl2:
    st.markdown("## Ablazione 2 — Effetto della rimozione di ciascun componente EFE")

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
        yaxis=dict(range=[0, 12], title="Velocità (km/h)", showgrid=True),
        height=380,
        margin=dict(t=20, b=50, l=60, r=20),
        legend=dict(itemclick=False, itemdoubleclick=False),
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    st.plotly_chart(_v2_fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""
### Come leggere il grafico

| Grafico | Cosa mostra | Come leggerlo |
|---|---|---|
| **Azione (Velocità)** | Velocità del treno ad ogni istante in funzione della configurazione EFE attiva. I componenti attivi cambiano la formula di scelta dell'azione. | Confronta il comportamento con la configurazione FULL (tutti i componenti attivi). Se il treno rallenta nella finestra t=20–30 senza falsi allarmi, i componenti attivi sono sufficienti. Se rallenta sempre o mai, un componente essenziale manca. |
""")

    st.divider()
    st.markdown("""
### Formula EFE canonica

```
EFE(π)  =   -   Pragmatic Value (π)    -     Epistemic Value(π)
              └─────────────────────┘     └────────────────────┘
                  Pragmatic term              Epistemic term

Pragmatic value  =  - Risk(π)  - Cost(π)
```

| Componente | Descrizione |
|---|---|
| **Pragmatic Value** | Termine pragmatico (= -Risk -Cost): quanto è costoso agire in questo stato? |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ **Risk** | Rischio fisico di prossimità al punto critico (transizione dello scambio) |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ **Cost** | Costo operativo dell'azione: maintain (0.1) < slow (0.4) < stop (0.8) |
| **Epistemic Value** | Termine informativo: quanto riduce l'incertezza questa azione? |

---

### Effetto della rimozione di ciascun componente EFE

| Configurazione | Effetto osservato |
|---|---|
| **Senza Risk** (Cost + Epistemic attivi) | L'agente non percepisce la prossimità alla transizione. Può rallentare lo stesso grazie all'epistemic value, ma non per motivi di sicurezza — il rallentamento non è correlato al pericolo reale. |
| **Senza Cost** (Risk + Epistemic attivi) | Il costo operativo è 0 per tutte le azioni. L'epistemic value differenzia ancora slow da maintain/stop, quindi l'agente rallenta più facilmente del baseline anche in assenza di pericolo. |
| **Senza Epistemic** (Risk + Cost attivi) | Nessun incentivo a rallentare per ridurre l'incertezza. −PragmaticValue è identico per tutte le azioni, quindi vince sempre maintain (costo minimo 0.1). Velocità sempre 10, TP = 0. |
| **Senza −PragmaticValue** (Risk + Cost entrambi off, Epistemic attivo) | EFE(slow) = −uncertainty < 0, EFE(maintain) = EFE(stop) = 0 → slow vince sempre quando uncertainty > 0. L'agente rallenta in modo indiscriminato, anche fuori dall'attacco. |
| **Nessun componente** (tutti off) | EFE = 0 per tutte le azioni → maintain vince sempre (primo elemento nella lista). Il sistema è cieco: non reagisce né al pericolo né all'incertezza. |
""")
