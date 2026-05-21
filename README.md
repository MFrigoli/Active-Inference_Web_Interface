# Railway Active Inference — Web Interface

| 🇮🇹 Italiano | 🇬🇧 English |
|---|---|
| Demo interattiva del sistema Active Inference per la sicurezza ferroviaria. Visualizza in tempo reale come un agente basato sul Free Energy Principle (FEP) rileva attacchi FDIA (False Data Injection Attack) e sceglie l'azione ottimale. | Interactive demo of an Active Inference system for railway safety. Visualizes in real time how an agent based on the Free Energy Principle (FEP) detects FDIA (False Data Injection Attack) and selects the optimal action. |

> 📄 Documentazione completa in italiano: [README.it.md](README.it.md)

---

## Quick Start

```bash
streamlit run app_streamlit.py
```

Requirements: `streamlit`, `plotly`

---

## Files

| File | Role |
|------|------|
| `app_streamlit.py` | Entry point — layout, sidebar, metrics, tabs |
| `figures.py` | Builds all Plotly charts (8 layers + 4 overview) |
| `simulation.py` | Simulation loop and F1 computation |
| `presets.py` | Fallacious system presets and slider/number-input callbacks |
| `translations.py` | All UI strings in Italian and English |

---

## Sidebar

### Language
Toggle between **Italiano** and **English** at the top of the sidebar. All UI text, chart labels, and explanations update instantly.

### Fallacious System
Six mutually exclusive checkboxes that load predefined presets:

| Preset | What it does |
|--------|-------------|
| Zero attacks | No attack injected — train crosses the switch normally |
| Baseline | Correct system with all components active |
| Paranoid | Threshold = 0.01 → continuous false positives on normal noise |
| Biased cost | Cost(maintain) = 0.9 → train slows due to distorted cost, not epistemic reasons |
| Over-Cautious | Uncertainty locked at 0.9 → always slows, even without attack |
| Lucky | Internal model hardcoded on timing t=22–28 — works only for that exact scenario |

### FDIA Attack
- **Attack start / end**: slider + number input for the attack time window (default 22–28)
- **Injected value**: `0.0` (hidden: same real state) or `1.0` (opposite: maximum detectable discrepancy)

### Sensor & Belief
- **Sensor noise**: amplitude of uniform noise `[-n, +n]` on normal readings (default 0.05)

### Action Costs
Three numeric values for operational costs in the EFE:

| Action | Default | Meaning |
|--------|---------|---------|
| maintain | 0.1 | Keep nominal speed — cheap |
| slow | 0.4 | Slow down to gather information — moderate |
| stop | 0.8 | Full stop — expensive, schedule delay |

### Timesteps & Seed
- **Total timesteps**: simulation duration (30–100, default 50)
- **Fixed seed** (on by default): reproduces the same noise sequence every run; if disabled, noise varies each interaction

### Architectural Components
Enable/disable parts of the inference pipeline:

| Component | Effect if disabled |
|-----------|-------------------|
| Anomaly Threshold | No anomaly detected — belief always follows sensor |
| Dynamic Uncertainty | Uncertainty fixed at 0 → epistemic value = 0 → maintain always wins |
| Internal Model | Expected state always 0 → false positives in stable phase, no detection during attack |

### EFE Components
Enable/disable terms of the formula `EFE(π) = −PragmaticValue(π) − EpistemicValue(π)`:

| Component | Effect if disabled |
|-----------|-------------------|
| Pragmatic (= Risk + Cost) | EFE = −EpistemicValue → slow always wins when there is uncertainty |
| Risk | Agent does not perceive physical proximity to the transition zone |
| Cost | Operational cost = 0 for all actions |
| Epistemic | No incentive to slow down to reduce uncertainty → maintain always wins |

---

## Quick Metrics (header)

Seven cards updated in real time after each parameter change:

| Metric | Definition |
|--------|-----------|
| **Anomalies** | Total timesteps in which the belief detected an anomaly |
| **TP** | Timesteps in which the train slows in the transition window [20, 30] |
| **FP** | Timesteps in which the train slows unnecessarily outside the transition window [20, 30] |
| **FN** | Missed timesteps: attack in window, train does not slow (11 − TP) |
| **F1-score** | `2*prec*rec / (prec+rec)` — balanced measure of precision and recall |
| **Precision** | `TP / (TP + FP)` — how many slowdowns are correct |
| **Degradation** | `(1 − F1_variant / F1_baseline) * 100` — how much the system worsens vs baseline |

---

## Tabs

### Overview
Four high-level summary charts:

1. **Switch state** — real vs belief estimate vs sensor; red `×` markers indicate anomalies
2. **Train velocity** — bar chart colored by action (green = maintain, orange = slow, red = stop)
3. **Epistemic uncertainty** — uncertainty over time (orange area fill)
4. **Comparative EFE values** — the three EFE(maintain/slow/stop) curves; agent picks the minimum

### Decision Path
Eight stacked charts showing each level of the pipeline:

| Chart | Content |
|-------|---------|
| 1. Physical state | Ground truth vs sensor reading (highlights FDIA manipulation) |
| 2. Inference Layer | Belief state + uncertainty + anomaly markers; hover shows prediction error and TRUST_MODEL/TRUST_SENSOR decision |
| 3. Prediction Error | `(sensor − model)` vs threshold — red zone indicates detected anomaly |
| 4a. EFE Maintain | −PragmaticValue and epistemic value for maintain; dot = timestep when chosen |
| 4b. EFE Slow | −PragmaticValue and epistemic value for epistemic_slow |
| 4c. EFE Stop | −PragmaticValue and epistemic value for pragmatic_stop |
| 5. Decision Layer | All three EFE curves overlaid — shows which action wins at each step |
| 6. Action Layer | Resulting velocity with colored background per action |

### Ablation 1 — Architectural Components
Shows the effect of the components selected in the sidebar on the inference pipeline.
The velocity chart title changes color (green = full baseline, red = missing component).

Four dynamic charts:
- **Velocity** with optional blue markers for `epistemic_slow` timesteps
- **Prediction Error & Uncertainty** — two curves + horizontal threshold
- **Epistemic Value** — epistemic term value over time
- **Pragmatic Value** — pragmatic cost of the chosen action (Risk + Cost) over time

Fixed summary table describing the theoretical effect of each removal.

### Ablation 2 — EFE Components
Shows the effect of the active combination of Risk/Cost/Epistemic.
Configuration name (e.g. `NO_RISK | C − E`) and metrics `TP/FP/Prec` shown above the chart.

Single velocity chart with blue fill and two background bands:
- Yellow: mechanical transition window [20, 30]
- Red: FDIA attack window

Fixed summary table with notable configurations (FULL, NO_RISK, NO_COST, NO_EPISTEMIC, NONE).

---

## EFE Formula

```
EFE(π) = −PragmaticValue(π) − EpistemicValue(π)

PragmaticValue(π) = −Risk(π) − Cost(π)

Risk      = min(1.5, proximity + 0.5 * uncertainty)
proximity = max(0,  1 − 2 * |belief − TRANSITION|)

EpistemicValue = uncertainty   if π = epistemic_slow, else 0
```

The agent executes `π* = argmin_π EFE(π)` at each timestep.
