"""
presets.py
Preset sistemi fallaci e callback Streamlit.
"""

import streamlit as st

_BASE = dict(
    s_anomaly_threshold=0.30, s_sensor_noise=0.05,
    s_attack_start=22, s_attack_end=28,
    s_enable_risk=True, s_enable_hazard=True, s_enable_cost=True, s_enable_epistemic=True,
    s_enable_threshold=True, s_enable_uncertainty=True, s_enable_model=True,
    s_min_uncertainty=0.1, s_lucky_model=False,
    s_cost_maintain=0.1, s_cost_slow=0.4, s_cost_stop=0.8,
    s_time_steps=50, s_seed=42, s_fixed_seed=True,
    s_attack_value=0.0,
)

# Zero attacchi: attack_start == attack_end → attack = False per ogni t
_ZERO_ATK = {**_BASE, "s_attack_start": 0, "s_attack_end": 0, "s_attack_value": 0.0}

FALLACIOUS_PRESETS = {
    "Zero attacchi (sistema pronto, nessun attacco)": _ZERO_ATK,
    "✅ Baseline (sistema corretto)": _BASE,
    "⚠️ Paranoico — threshold troppo basso (0.01)": {
        **_BASE, "s_anomaly_threshold": 0.01,
    },
    "⚠️ Costo truccato — maintain costoso (0.9)": {
        **_BASE, "s_cost_maintain": 0.9,
    },
    "⚠️ Over-Cautious — incertezza sempre alta (0.9)": {
        **_BASE, "s_min_uncertainty": 0.9,
    },
    "⚠️ Lucky — modello hardcoded sul timing attacco": {
        **_BASE, "s_lucky_model": True,
    },
}

_PRESET_HELP = {
    "Zero attacchi (sistema pronto, nessun attacco)":
        "Tutti i componenti attivi, nessun attacco iniettato — il treno passa lo scambio rallentando per cautela epistemica, nessuna anomalia rilevata",
    "✅ Baseline (sistema corretto)":
        "Sistema Active Inference completo e corretto — tutti i componenti funzionano come previsto",
    "⚠️ Paranoico — threshold troppo basso (0.01)":
        "Threshold = 0.01 → rileva anomalie ovunque, incluso il normale rumore del sensore (falsi positivi continui)",
    "⚠️ Costo truccato — maintain costoso (0.9)":
        "Costo maintain = 0.9 → l'agente rallenta non per ragioni epistemiche ma perché mantenere velocità è artificialmente costoso",
    "⚠️ Over-Cautious — incertezza sempre alta (0.9)":
        "Incertezza bloccata a 0.9 → l'agente rallenta sempre per eccessiva cautela, anche senza attacco",
    "⚠️ Lucky — modello hardcoded sul timing attacco":
        "Modello interno hardcoded t=22-28 → funziona solo per questo scenario specifico, non generalizza",
}

_PRESET_KEYS = list(_PRESET_HELP.keys())


def apply_preset():
    name   = st.session_state.preset_selector
    params = FALLACIOUS_PRESETS.get(name)
    if params:
        for k, v in params.items():
            st.session_state[k] = v


def _sync_attack_start():
    st.session_state["s_attack_start"] = st.session_state["_sl_attack_start"]

def _sync_attack_end():
    st.session_state["s_attack_end"] = st.session_state["_sl_attack_end"]

def _sync_sensor_noise():
    st.session_state["s_sensor_noise"] = st.session_state["_sl_sensor_noise"]

def _sync_time_steps():
    st.session_state["s_time_steps"] = st.session_state["_sl_time_steps"]

def _sync_seed():
    st.session_state["s_seed"] = st.session_state["_sl_seed"]


def _make_pick(idx, pname):
    def _fn():
        if st.session_state.get(f"_pc_{idx}", False):
            st.session_state["preset_selector"] = pname
            for j in range(len(_PRESET_KEYS)):
                if j != idx:
                    st.session_state[f"_pc_{j}"] = False
            apply_preset()
        else:
            st.session_state["preset_selector"] = ""
            st.session_state["_pc_0"] = False
    return _fn
