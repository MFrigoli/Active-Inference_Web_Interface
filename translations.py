"""
translations.py
Stringhe UI in italiano e inglese per Railway Active Inference.
Uso: from translations import T; t = T[lang]
"""

T = {
    # ─────────────────────────────────────────────────────────────────────────
    # ITALIANO
    # ─────────────────────────────────────────────────────────────────────────
    "it": {
        # Page
        "page_title":    "Railway Active Inference — Demo interattiva",
        "page_subtitle": "Modifica i parametri nella barra laterale. I grafici si aggiornano in tempo reale.",

        # Sidebar headers
        "sb_fallace": "## Sistema fallace",
        "sb_params":  "## Parametri simulazione",
        "sb_fdia":    "Attacco FDIA",
        "sb_sensor":  "Sensore e stima",
        "sb_costs":   "Costi azioni",
        "sb_time":    "Timestep e seed",
        "sb_arch":    "Componenti architetturali",
        "sb_efe":     "Componenti EFE",

        # Attack
        "atk_start_cap":  "Inizio attacco (t)",
        "atk_end_cap":    "Fine attacco (t)",
        "atk_warning":    "Fine attacco deve essere ≥ inizio attacco.",
        "atk_val_cap":    "Valore iniettato dall'attacco",
        "atk_val_hidden": "nascosto: stesso stato reale",
        "atk_val_opp":    "opposto: massima discrepanza",

        # Sensor
        "noise_help": "Ampiezza del rumore uniforme [-n, +n] aggiunto alla lettura del sensore",

        # Costs
        "cost_maintain_help": "Costo operativo per mantenere velocità nominale (default 0.1)",
        "cost_slow_help":     "Costo operativo per rallentare — azione epistemica (default 0.4)",
        "cost_stop_help":     "Costo operativo per fermarsi — azione pragmatica (default 0.8)",

        # Seed / timestep
        "timestep_help": "Durata totale della simulazione in passi temporali",
        "seed_fixed":    "Seed fisso",
        "seed_help":     ("Seed = numero iniziale che controlla il generatore di numeri casuali. "
                          "Stesso seed → stesso rumore ad ogni run → simulazione riproducibile. "
                          "Se spento, seed cambia ad ogni interazione → rumore diverso ogni volta."),
        "seed_cap":      "Seed",

        # Architectural components
        "arch_threshold_label":   "Soglia anomalia",
        "arch_threshold_help":    "Soglia prediction error — Se off: nessuna anomalia rilevata",
        "arch_uncertainty_label": "Incertezza dinamica",
        "arch_uncertainty_help":  "Valore minimo incertezza — Se off: uncertainty fissa a 0",
        "arch_model_label":       "Modello interno",
        "arch_model_help":        "Se off: expected=0 sempre",

        # EFE components
        "efe_help":            ("L'agente sceglie l'azione con il costo totale più basso. "
                                "Disattiva i componenti per vedere come cambia il comportamento."),
        "efe_pragmatic_label":  "Pragmatic  (= Risk + Cost)",
        "efe_pragmatic_help":  ("Il termine 'pratico': tiene conto del pericolo fisico e del costo dell'azione. "
                                "Se disattivato, l'agente ignora completamente rischi e costi."),
        "efe_risk_label":      "Risk",
        "efe_risk_help":       ("Quanto è pericoloso trovarsi vicino alla zona di transizione dello scambio. "
                                "Più ci si avvicina, più il rischio sale."),
        "efe_cost_label":      "Cost",
        "efe_cost_help":       ("Ogni azione ha un costo fisso: mantieni (0.1) < rallenta (0.4) < fermati (0.8). "
                                "Incentiva a non frenare inutilmente."),
        "efe_epistemic_label": "Epistemic",
        "efe_epistemic_help":  ("Premia l'azione 'rallenta' quando il sistema è incerto: rallentare permette "
                                "di osservare meglio lo scambio e ridurre il dubbio. "
                                "Se disattivato, l'agente non esplora mai."),

        # Metrics
        "m_anomalies":      "Anomalie",
        "m_anomalies_help": "Totale timestep in cui il belief ha rilevato un'anomalia",
        "m_tp_help":        "Timestep in cui il treno rallenta nella finestra di transizione [20,30]",
        "m_fp_help":        "Timestep in cui il treno rallenta inutilmente fuori dalla finestra di transizione [20,30]",
        "m_fn_help":        "Timestep in cui il treno non rallenta quando dovrebbe (11 − TP)",
        "m_f1":             "F1-score",
        "m_f1_help":        ("Media tra precisione e recall: misura quanto il sistema è sia preciso sia completo "
                             "nel reagire al pericolo. 100% = reazione perfetta, 0% = nessuna reazione utile."),
        "m_prec":           "Precisione",
        "m_prec_help":      ("Quante delle volte in cui il treno ha rallentato, lo ha fatto davvero per un pericolo reale. "
                             "Bassa = troppi falsi allarmi."),
        "m_deg":            "Degradazione",
        "m_deg_help":       ("Quanto peggiora il sistema rispetto alla configurazione completa (baseline). "
                             "0% = nessuna perdita, 100% = il sistema non funziona più."),

        # Tabs
        "tab_overview": "GRAFICI PANORAMICI",
        "tab_layers":   "PERCORSO DECISIONALE",
        "tab_abl1":     "ABLAZIONE 1",
        "tab_abl2":     "ABLAZIONE 2",

        # Ablation 1 status strings
        "abl1_title":                "## Ablazione 1 — Effetto della rimozione di ciascun componente architetturale",
        "abl1_baseline":             "BASELINE (sistema completo)",
        "abl1_without":              "SENZA ",
        "abl1_ok":                   "[OK]",
        "abl1_fail":                 "[FAIL]",
        "abl1_miss_epistemic":       "VALORE EPISTEMICO",
        "abl1_miss_threshold":       "SOGLIA ANOMALIA",
        "abl1_miss_uncertainty":     "INCERTEZZA DINAMICA",
        "abl1_miss_model":           "MODELLO INTERNO",
        "abl1_miss_lucky":           "MODELLO FORTUNATO",
        "abl1_miss_risk":            "RISK",
        "abl1_miss_cost":            "COST",
        "abl1_miss_threshold_low":  "SOGLIA TROPPO BASSA",
        "abl1_miss_cost_high":      "COSTO MANTIENI ALTO",
        "abl1_miss_unc_locked":     "INCERTEZZA BLOCCATA",

        # Ablation 1 chart axis / trace labels
        "abl1_vel_axis":   "Velocità",
        "abl1_val_axis":   "Valore",
        "abl1_threshold":  "Soglia",
        "abl1_pred_err":   "Prediction error",
        "abl1_unc":        "Incertezza",

        # Ablation 2
        "abl2_title":    "## Ablazione 2 — Effetto della rimozione di ciascun componente EFE",
        "abl2_vel_axis": "Velocità (km/h)",

        # Figures — common
        "fig_fdia_label":   "Periodo FDIA Attack",
        "fig_time_axis":    "Tempo (steps)",
        "fig_switch_axis":  "Stato dello scambio",
        "fig_belief_axis":  "Belief State",
        "fig_pred_axis":    "Errore di predizione",
        "fig_efe_axis":     "Expected Free Energy",
        "fig_vel_axis":     "Velocità",
        "fig_vel_kmh":      "Velocità (km/h)",
        "fig_val_axis":     "Valore",
        "fig_state_axis":   "Stato",
        "fig_unc_axis":     "Incertezza",
        "fig_efe_y":        "EFE",

        # Figures — trace names
        "fig_ground_truth":  "Ground Truth (stato reale)",
        "fig_sensor":        "Sensore (può essere compromesso)",
        "fig_uncertainty":   "Incertezza",
        "fig_belief":        "Belief (stima interna)",
        "fig_anomaly_mk":    "Anomalia rilevata",
        "fig_anomaly_sq":    "Anomalia rilevata (errore > soglia)",
        "fig_pred_trace":    "Errore di predizione |sensore − modello|",
        "fig_threshold":     "Soglia anomalia = {}",
        "fig_chosen":        "Azione scelta",
        "fig_vel_trace":     "Velocità",
        "fig_neg_pv":        "−PragmaticValue",
        "fig_epist":         "Valore epistemico",

        # Figures — chart titles (layers)
        "fig1_title":     "1. Stato fisico: realtà vs sensore",
        "fig2_title":     "2. Livello di inferenza: come interpreta i dati?",
        "fig3_title":     "3. Errore di predizione vs Soglia di Anomalia",
        "fig4a_title":    "4a. EFE Mantieni  (v=10)",
        "fig4b_title":    "4b. EFE Rallenta  (v=4)",
        "fig4c_title":    "4c. EFE Fermati  (v=0)",
        "fig4a_efe_lbl":  "EFE mantieni (= −PV−E)",
        "fig4b_efe_lbl":  "EFE epistemico (= −PV−E)",
        "fig4c_efe_lbl":  "EFE pragmatico (= −PV−E)",
        "fig5_title":     "5. Livello decisionale: quale azione ha EFE minima?",
        "fig6_title":     "6. Livello di azione: cosa fa l'agente?",

        # Figures — overview chart titles / axes
        "ov_state_title": "Stato scambio: reale vs stimato vs sensore",
        "ov_vel_title":   "Velocità treno e azione scelta",
        "ov_unc_title":   "Incertezza epistemica nel tempo",
        "ov_efe_title":   "Valori EFE per azione (l'agente sceglie il minimo)",
        "ov_atk_label":   "⚡ Attacco FDIA",
        "ov_state_yaxis": "Stato",
        "ov_vel_yaxis":   "Velocità (km/h)",
        "ov_unc_yaxis":   "Incertezza",
        "ov_efe_yaxis":   "EFE",

        # Trust labels (hover tooltip)
        "trust_model":  "TRUST_MODEL",
        "trust_sensor": "TRUST_SENSOR",

        # Action labels (also used as cost input labels)
        "act_maintain": "Mantieni",
        "act_slow":     "Rallenta",
        "act_stop":     "Fermati",
        "cost_maintain_cap": "Mantieni",
        "cost_slow_cap":     "Rallenta",
        "cost_stop_cap":     "Fermati",

        # Ablation 1 chart titles
        "abl1_pred_err_unc_title": "Errore di predizione & Incertezza",
        "abl1_epist_val_title":    "Valore epistemico",
        "abl1_prag_val_title":     "Valore pragmatico",

        # Preset display names (same order as _PRESET_KEYS)
        "preset_names": [
            "Zero attacchi (sistema pronto, nessun attacco)",
            "✅ Baseline (sistema corretto)",
            "⚠️ Paranoico — soglia troppo bassa (0.01)",
            "⚠️ Costo truccato — mantieni costoso (0.9)",
            "⚠️ Eccessivamente cauto — incertezza sempre alta (0.9)",
            "⚠️ Fortunato — modello fisso sul timing attacco",
        ],
        "preset_helps": [
            "Tutti i componenti attivi, nessun attacco iniettato — il treno passa lo scambio rallentando per cautela epistemica, nessuna anomalia rilevata",
            "Sistema Active Inference completo e corretto — tutti i componenti funzionano come previsto",
            "Threshold = 0.01 → rileva anomalie ovunque, incluso il normale rumore del sensore (falsi positivi continui)",
            "Costo maintain = 0.9 → l'agente rallenta non per ragioni epistemiche ma perché mantenere velocità è artificialmente costoso",
            "Incertezza bloccata a 0.9 → l'agente rallenta sempre per eccessiva cautela, anche senza attacco",
            "Modello interno hardcoded t=22-28 → funziona solo per questo scenario specifico, non generalizza",
        ],

        # ── Markdown sections ─────────────────────────────────────────────────

        "overview_md": """\
### Come leggere i grafici

| Grafico | Cosa mostra | Come leggerlo |
|---|---|---|
| **Stato scambio:**<br>reale vs stimato vs sensore | Il confronto tra lo stato reale dello scambio (ground truth), la lettura del sensore (che può essere compromessa) e la stima interna del sistema (belief). | Quando sensore e stato reale divergono (durante l'attacco), il sistema dovrebbe ignorare il sensore e usare la propria stima. I marker × rossi indicano i momenti di anomalia rilevata. |
| **Velocità treno e azione scelta** | La velocità del treno ad ogni istante, colorata per azione: verde = mantieni (10), arancio = rallenta (4), rosso = fermati (0). | Verde dominante = comportamento normale. Se arancio/rosso compaiono nella finestra t=20–30, l'agente ha reagito correttamente al pericolo. Se compaiono anche fuori, ci sono falsi allarmi. |
| **Incertezza epistemica nel tempo** | Quanto il sistema è "confuso" sullo stato dello scambio in ogni istante. | Picchi alti = il sistema è incerto e cerca informazioni. Se l'incertezza sale durante l'attacco, il sistema ha riconosciuto che qualcosa non va. Se rimane bassa, ha accettato i dati falsi del sensore. |
| **Valori EFE per azione** | I valori di Expected Free Energy per le tre azioni (mantieni, rallenta, fermati). L'agente sceglie sempre l'azione con EFE minimo. | La curva più in basso ad ogni istante indica l'azione scelta. Quando *rallenta* scende sotto *mantieni*, l'agente sceglie di rallentare. Quando le curve si incrociano, cambia l'azione preferita. |
""",

        "layers_md": """\
### Come leggere i grafici

| Grafico | Cosa mostra | Come leggerlo |
|---|---|---|
| **1. Stato fisico** | Lo stato reale dello scambio confrontato con la lettura del sensore. | Divergenza tra le due linee = il sensore è compromesso dall'attacco. Il sistema deve ignorare il sensore e affidarsi al modello interno. |
| **2. Livello di inferenza: stima** | La stima interna (belief) sullo stato dello scambio, con l'incertezza (area grigia) e i momenti di anomalia rilevata (× rossi). | Quando il belief si discosta dal sensore e segue il modello interno, il sistema ha capito che i dati sono corrotti. Più × rossi durante l'attacco, meglio. |
| **3. Errore di predizione vs Soglia** | L'errore di predizione (quanto il sensore si discosta dall'atteso) confrontato con la soglia di anomalia (linea tratteggiata rossa). | Ogni volta che la linea arancione supera la soglia, scatta il rilevamento anomalia. Più spesso supera durante l'attacco (e non fuori), migliore è il comportamento. |
| **4a. EFE Maintain** | Il calcolo EFE per l'azione "mantieni velocità": −PragmaticValue (rosso), Epistemic Value = 0, e la EFE risultante. | EFE basso = questa azione è conveniente in quel momento. Confrontalo con 4b e 4c per capire perché vince o perde. |
| **4b. EFE Slow** | Il calcolo EFE per "rallenta": −PragmaticValue (rosso), guadagno epistemico (viola) e EFE risultante. | Quando il termine epistemico (viola) è alto, l'azione slow diventa più conveniente delle altre. I punti indicano quando è stata scelta. |
| **4c. EFE Stop** | Il calcolo EFE per "fermati": −PragmaticValue alto (il costo di stop è 0.8) e EFE risultante. | Stop ha il costo operativo più alto, quindi vince solo quando il rischio fisico è molto elevato e supera lo svantaggio del costo. |
| **5. Livello decisionale: EFE minimo** | I valori EFE delle tre azioni sovrapposti, con i marker dell'azione scelta. | L'azione scelta ad ogni istante è quella con la curva più in basso. Quando le curve si incrociano, cambia l'azione preferita dell'agente. |
| **6. Livello di azione: velocità** | La velocità del treno con le aree colorate per azione: verde = mantieni, blu = rallenta, rosso = fermati. | Le aree colorate mostrano per quanto tempo ogni azione è stata attiva. Blu nella finestra t=20–30 = risposta corretta all'attacco. |
""",

        "abl1_md": """\
### Come leggere i grafici

| Grafico | Cosa mostra | Come leggerlo |
|---|---|---|
| **Azione (Velocità)** | Velocità del treno ad ogni istante. Tre possibili azioni: mantieni (10), rallenta (4), fermati (0). | Se rallenta durante t=20–30 (transizione reale), il pericolo è stato rilevato. Se rimane a 10, nessuna reazione. Se rallenta anche fuori da quella finestra, ci sono falsi allarmi. |
| **Errore di predizione & Incertezza** | Errore di predizione (linea continua) — quanto il sensore si discosta da ciò che il modello si aspettava — e incertezza della belief (linea tratteggiata) — quanto il sistema è "confuso" sullo stato dello scambio. | Quando l'errore supera la soglia (linea puntinata rossa), il sistema alza l'incertezza al massimo: è il segnale che innesca la risposta. Se l'errore non supera mai la soglia, l'anomalia non viene rilevata. |
| **Valore epistemico** | Quanto vale "rallentare per guardare meglio". Premia l'azione *slow* quando l'incertezza è alta. | Picco alto → il sistema ha molto da guadagnare dall'esplorazione e sceglie di rallentare. Piatto a zero → il valore epistemico non influenza la scelta e il sistema tende a mantenersi a velocità nominale. |
| **Valore pragmatico** | Costo pragmatico dell'azione scelta: rischio fisico (vicinanza alla transizione) + costo operativo (mantieni=0.1, rallenta=0.4, fermati=0.8). | Sale vicino alla zona di pericolo o quando l'azione scelta è costosa. Un valore alto non è necessariamente sbagliato: il sistema sta pagando un costo per gestire una situazione rischiosa. |

### Effetto della rimozione di ciascun componente architetturale

| Componente rimosso | Effetto osservato |
|---|---|
| **Senza Valore epistemico** | Nessun incentivo a rallentare per ridurre l'incertezza. EFE = −PragmaticValue per tutte le azioni → mantieni vince sempre (costo minimo). Velocità sempre 10, TP = 0. |
| **Senza Soglia anomalia** | Il belief segue sempre il sensore, nessuna anomalia rilevata durante l'attacco. L'incertezza si alza comunque vicino a TRANSITION (0.5), quindi il valore epistemico può ancora far vincere rallenta — ma non correlato all'attacco FDIA. |
| **Senza Incertezza dinamica** | Incertezza fissa a 0 → valore epistemico = 0 → mantieni vince sempre. Il sistema non apprende dalla propria incertezza. |
| **Senza Modello interno** | Expected state sempre 0. Il sensore legge 0.5 durante la transizione → prediction_error > soglia fuori dall'attacco (FP alti). Durante l'attacco il sensore injetta 0.0 = expected → errore = 0 → nessuna anomalia rilevata (TP = 0). |
""",

        "abl2_how_to_md": """\
### Come leggere il grafico

| Grafico | Cosa mostra | Come leggerlo |
|---|---|---|
| **Azione (Velocità)** | Velocità del treno ad ogni istante in funzione della configurazione EFE attiva. I componenti attivi cambiano la formula di scelta dell'azione. | Confronta il comportamento con la configurazione FULL (tutti i componenti attivi). Se il treno rallenta nella finestra t=20–30 senza falsi allarmi, i componenti attivi sono sufficienti. Se rallenta sempre o mai, un componente essenziale manca. |
""",

        "abl2_formula_md": """\
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
| &nbsp;&nbsp;&nbsp;&nbsp;↳ **Cost** | Costo operativo dell'azione: mantieni (0.1) < rallenta (0.4) < fermati (0.8) |
| **Epistemic Value** | Termine informativo: quanto riduce l'incertezza questa azione? |

---

### Effetto della rimozione di ciascun componente EFE

| Configurazione | Effetto osservato |
|---|---|
| **Senza Risk** (Cost + Epistemic attivi) | L'agente non percepisce la prossimità alla transizione. Può rallentare lo stesso grazie all'epistemic value, ma non per motivi di sicurezza — il rallentamento non è correlato al pericolo reale. |
| **Senza Cost** (Risk + Epistemic attivi) | Il costo operativo è 0 per tutte le azioni. Il valore epistemico differenzia ancora rallenta da mantieni/fermati, quindi l'agente rallenta più facilmente del baseline anche in assenza di pericolo. |
| **Senza Epistemic** (Risk + Cost attivi) | Nessun incentivo a rallentare per ridurre l'incertezza. −PragmaticValue è identico per tutte le azioni, quindi vince sempre mantieni (costo minimo 0.1). Velocità sempre 10, TP = 0. |
| **Senza −PragmaticValue** (Risk + Cost entrambi off, Epistemic attivo) | EFE(rallenta) = −incertezza < 0, EFE(mantieni) = EFE(fermati) = 0 → rallenta vince sempre quando incertezza > 0. L'agente rallenta in modo indiscriminato, anche fuori dall'attacco. |
| **Nessun componente** (tutti off) | EFE = 0 per tutte le azioni → mantieni vince sempre (primo elemento nella lista). Il sistema è cieco: non reagisce né al pericolo né all'incertezza. |
""",
    },

    # ─────────────────────────────────────────────────────────────────────────
    # ENGLISH
    # ─────────────────────────────────────────────────────────────────────────
    "en": {
        # Page
        "page_title":    "Railway Active Inference — Interactive Demo",
        "page_subtitle": "Modify the parameters in the sidebar. Charts update in real time.",

        # Sidebar headers
        "sb_fallace": "## Fallacious System",
        "sb_params":  "## Simulation Parameters",
        "sb_fdia":    "FDIA Attack",
        "sb_sensor":  "Sensor & Belief",
        "sb_costs":   "Action Costs",
        "sb_time":    "Timesteps & Seed",
        "sb_arch":    "Architectural Components",
        "sb_efe":     "EFE Components",

        # Attack
        "atk_start_cap":  "Attack start (t)",
        "atk_end_cap":    "Attack end (t)",
        "atk_warning":    "Attack end must be ≥ attack start.",
        "atk_val_cap":    "Injected attack value",
        "atk_val_hidden": "hidden: same real state",
        "atk_val_opp":    "opposite: maximum discrepancy",

        # Sensor
        "noise_help": "Amplitude of uniform noise [-n, +n] added to sensor readings",

        # Costs
        "cost_maintain_help": "Operational cost for maintaining nominal speed (default 0.1)",
        "cost_slow_help":     "Operational cost for slowing down — epistemic action (default 0.4)",
        "cost_stop_help":     "Operational cost for stopping — pragmatic action (default 0.8)",

        # Seed / timestep
        "timestep_help": "Total duration of the simulation in time steps",
        "seed_fixed":    "Fixed seed",
        "seed_help":     ("Seed = initial number controlling the random number generator. "
                          "Same seed → same noise every run → reproducible simulation. "
                          "If off, seed changes each interaction → different noise each time."),
        "seed_cap":      "Seed",

        # Architectural components
        "arch_threshold_label":   "Anomaly Threshold",
        "arch_threshold_help":    "Prediction error threshold — If off: no anomaly detected",
        "arch_uncertainty_label": "Dynamic Uncertainty",
        "arch_uncertainty_help":  "Minimum uncertainty value — If off: uncertainty fixed at 0",
        "arch_model_label":       "Internal Model",
        "arch_model_help":        "If off: expected state = 0 always",

        # EFE components
        "efe_help":            ("The agent picks the action with the lowest total cost. "
                                "Disable components to see how behavior degrades."),
        "efe_pragmatic_label":  "Pragmatic  (= Risk + Cost)",
        "efe_pragmatic_help":  ("The 'practical' term: accounts for physical danger and action cost. "
                                "If disabled, the agent ignores risks and costs entirely."),
        "efe_risk_label":      "Risk",
        "efe_risk_help":       ("How dangerous it is to be near the switch transition zone. "
                                "The closer the train, the higher the risk."),
        "efe_cost_label":      "Cost",
        "efe_cost_help":       ("Each action has a fixed cost: maintain (0.1) < slow (0.4) < stop (0.8). "
                                "Discourages unnecessary braking."),
        "efe_epistemic_label": "Epistemic",
        "efe_epistemic_help":  ("Rewards the 'slow' action when the system is uncertain: slowing down allows "
                                "better observation of the switch, reducing doubt. "
                                "If disabled, the agent never explores."),

        # Metrics
        "m_anomalies":      "Anomalies",
        "m_anomalies_help": "Total timesteps in which the belief detected an anomaly",
        "m_tp_help":        "Timesteps in which the train slows down in the transition window [20,30]",
        "m_fp_help":        "Timesteps in which the train slows down unnecessarily outside the transition window [20,30]",
        "m_fn_help":        "Missed timesteps: attack in window, train does not slow down (11 − TP)",
        "m_f1":             "F1-score",
        "m_f1_help":        ("Average of precision and recall: measures how precise and complete the system's "
                             "response to danger is. 100% = perfect response, 0% = no useful response."),
        "m_prec":           "Precision",
        "m_prec_help":      ("How many times the train slowed down for a real danger. "
                             "Low = too many false alarms."),
        "m_deg":            "Degradation",
        "m_deg_help":       ("How much the system worsens vs the full baseline configuration. "
                             "0% = no loss, 100% = system no longer works."),

        # Tabs
        "tab_overview": "OVERVIEW",
        "tab_layers":   "DECISION PATH",
        "tab_abl1":     "ABLATION 1",
        "tab_abl2":     "ABLATION 2",

        # Ablation 1 status strings
        "abl1_title":            "## Ablation 1 — Effect of removing each architectural component",
        "abl1_baseline":         "BASELINE (full system)",
        "abl1_without":          "WITHOUT ",
        "abl1_ok":               "[OK]",
        "abl1_fail":             "[FAIL]",
        "abl1_miss_epistemic":   "EPISTEMIC VALUE",
        "abl1_miss_threshold":   "ANOMALY THRESHOLD",
        "abl1_miss_uncertainty": "DYNAMIC UNCERTAINTY",
        "abl1_miss_model":       "INTERNAL MODEL",
        "abl1_miss_lucky":       "LUCKY MODEL",
        "abl1_miss_risk":        "RISK",
        "abl1_miss_cost":        "COST",
        "abl1_miss_threshold_low": "LOW THRESHOLD",
        "abl1_miss_cost_high":     "HIGH MAINTAIN COST",
        "abl1_miss_unc_locked":    "LOCKED UNCERTAINTY",

        # Ablation 1 chart axis / trace labels
        "abl1_vel_axis":  "Velocity",
        "abl1_val_axis":  "Value",
        "abl1_threshold": "Threshold",
        "abl1_pred_err":  "Prediction error",
        "abl1_unc":       "Uncertainty",

        # Ablation 2
        "abl2_title":    "## Ablation 2 — Effect of removing each EFE component",
        "abl2_vel_axis": "Velocity (km/h)",

        # Figures — common
        "fig_fdia_label":  "FDIA Attack period",
        "fig_time_axis":   "Time (steps)",
        "fig_switch_axis": "Switch state",
        "fig_belief_axis": "Stima interna",
        "fig_pred_axis":   "Prediction Error",
        "fig_efe_axis":    "Expected Free Energy",
        "fig_vel_axis":    "Velocity",
        "fig_vel_kmh":     "Velocity (km/h)",
        "fig_val_axis":    "Value",
        "fig_state_axis":  "State",
        "fig_unc_axis":    "Uncertainty",
        "fig_efe_y":       "EFE",

        # Figures — trace names
        "fig_ground_truth": "Ground Truth (real state)",
        "fig_sensor":       "Sensor (may be compromised)",
        "fig_uncertainty":  "Uncertainty",
        "fig_belief":       "Belief (internal estimate)",
        "fig_anomaly_mk":   "Detected anomaly",
        "fig_anomaly_sq":   "Detected anomaly (error > threshold)",
        "fig_pred_trace":   "Prediction Error |sensor − model|",
        "fig_threshold":    "Anomaly threshold = {}",
        "fig_chosen":       "Chosen action",
        "fig_vel_trace":    "Velocity",
        "fig_neg_pv":       "−PragmaticValue",
        "fig_epist":        "Epistemic Value",

        # Figures — chart titles (layers)
        "fig1_title":    "1. Physical state: reality vs sensor",
        "fig2_title":    "2. Inference Layer: how it interprets data?",
        "fig3_title":    "3. Prediction Error vs Anomaly Threshold",
        "fig4a_title":   "4a. EFE Maintain  (v=10)",
        "fig4b_title":   "4b. EFE Slow  (v=4)",
        "fig4c_title":   "4c. EFE Stop  (v=0)",
        "fig4a_efe_lbl": "EFE maintain (= −PV−E)",
        "fig4b_efe_lbl": "EFE epistemic (= −PV−E)",
        "fig4c_efe_lbl": "EFE pragmatic (= −PV−E)",
        "fig5_title":    "5. Decision Layer: which action has minimum EFE?",
        "fig6_title":    "6. Action Layer: what does the agent do?",

        # Figures — overview chart titles / axes
        "ov_state_title": "Switch state: real vs estimated vs sensor",
        "ov_vel_title":   "Train velocity and chosen action",
        "ov_unc_title":   "Epistemic uncertainty over time",
        "ov_efe_title":   "EFE values per action (agent picks minimum)",
        "ov_atk_label":   "⚡ FDIA Attack",
        "ov_state_yaxis": "State",
        "ov_vel_yaxis":   "Velocity (km/h)",
        "ov_unc_yaxis":   "Uncertainty",
        "ov_efe_yaxis":   "EFE",

        # Trust labels (hover tooltip)
        "trust_model":  "TRUST_MODEL",
        "trust_sensor": "TRUST_SENSOR",

        # Action labels (also used as cost input labels)
        "act_maintain": "Maintain",
        "act_slow":     "Slow",
        "act_stop":     "Stop",
        "cost_maintain_cap": "maintain",
        "cost_slow_cap":     "slow",
        "cost_stop_cap":     "stop",

        # Ablation 1 chart titles
        "abl1_pred_err_unc_title": "Prediction Error & Uncertainty",
        "abl1_epist_val_title":    "Epistemic Value",
        "abl1_prag_val_title":     "Pragmatic Value",

        # Preset display names (same order as _PRESET_KEYS)
        "preset_names": [
            "Zero attacks (system ready, no attack)",
            "✅ Baseline (correct system)",
            "⚠️ Paranoid — threshold too low (0.01)",
            "⚠️ Biased cost — maintain costly (0.9)",
            "⚠️ Over-Cautious — uncertainty always high (0.9)",
            "⚠️ Lucky — model hardcoded on attack timing",
        ],
        "preset_helps": [
            "All components active, no attack injected — train crosses the switch slowing for epistemic caution, no anomaly detected",
            "Complete and correct Active Inference system — all components work as intended",
            "Threshold = 0.01 → anomalies detected everywhere, including normal sensor noise (continuous false positives)",
            "Maintain cost = 0.9 → agent slows down not for epistemic reasons but because maintaining speed is artificially costly",
            "Uncertainty locked at 0.9 → agent always slows down out of excessive caution, even without attack",
            "Internal model hardcoded t=22-28 → works only for this specific scenario, does not generalize",
        ],

        # ── Markdown sections ─────────────────────────────────────────────────

        "overview_md": """\
### How to read the charts

| Chart | What it shows | How to read it |
|---|---|---|
| **Switch state:**<br>real vs estimated vs sensor | Comparison between the real switch state (ground truth), sensor reading (which may be compromised) and the system's internal estimate (belief). | When sensor and real state diverge (during attack), the system should ignore the sensor and use its own estimate. Red × markers indicate detected anomaly moments. |
| **Train velocity and chosen action** | Train velocity at each timestep, colored by action: green = maintain (10), orange = slow (4), red = stop (0). | Dominant green = normal behavior. If orange/red appear in window t=20–30, the agent correctly reacted to danger. If they also appear outside, there are false alarms. |
| **Epistemic uncertainty over time** | How "confused" the system is about the switch state at each timestep. | High peaks = system is uncertain and seeks information. If uncertainty rises during the attack, the system recognized something is wrong. If it stays low, it accepted the false sensor data. |
| **EFE values per action** | Expected Free Energy values for the three actions (maintain, slow, stop). The agent always picks the action with minimum EFE. | The lowest curve at each timestep indicates the chosen action. When *slow* drops below *maintain*, the agent slows down. When curves cross, the preferred action changes. |
""",

        "layers_md": """\
### How to read the charts

| Chart | What it shows | How to read it |
|---|---|---|
| **1. Physical state** | Real switch state compared with sensor reading. | Divergence between the two lines = sensor is compromised by the attack. The system must ignore the sensor and rely on the internal model. |
| **2. Inference Layer: belief** | Internal estimate (belief) of the switch state, with uncertainty (grey area) and detected anomaly moments (× red). | When belief diverges from sensor and follows the internal model, the system understood the data is corrupted. More × during attack = better. |
| **3. Prediction Error vs Threshold** | Prediction error (how much the sensor deviates from expected) compared with the anomaly threshold (red dashed line). | Each time the orange line exceeds the threshold, anomaly detection fires. More often during attack (and not outside) = better behavior. |
| **4a. EFE Maintain** | EFE calculation for "maintain speed": −PragmaticValue (red), Epistemic Value = 0, and the resulting EFE. | Low EFE = this action is convenient at that moment. Compare with 4b and 4c to understand why it wins or loses. |
| **4b. EFE Slow** | EFE calculation for "slow": −PragmaticValue (red), epistemic gain (purple) and resulting EFE. | When the epistemic term (purple) is high, slow becomes more convenient than other actions. Dots indicate when it was chosen. |
| **4c. EFE Stop** | EFE calculation for "stop": high −PragmaticValue (stop cost is 0.8) and resulting EFE. | Stop has the highest operational cost, so it wins only when physical risk is very high and overcomes the cost disadvantage. |
| **5. Decision Layer: minimum EFE** | EFE values for all three actions overlaid, with chosen action markers. | The chosen action at each timestep is the one with the lowest curve. When curves cross, the agent's preferred action changes. |
| **6. Action Layer: velocity** | Train velocity with colored areas per action: green = maintain, blue = slow, red = stop. | Colored areas show how long each action was active. Blue in window t=20–30 = correct response to the attack. |
""",

        "abl1_md": """\
### How to read the charts

| Chart | What it shows | How to read it |
|---|---|---|
| **Action (Velocity)** | Train velocity at each timestep. Three possible actions: maintain (10), slow (4), stop (0). | If it slows during t=20–30 (real transition), danger was detected. If it stays at 10, no reaction. If it slows outside that window, there are false alarms. |
| **Prediction Error & Uncertainty** | Prediction error (solid line) — how much the sensor deviates from the model's expectation — and belief uncertainty (dashed line) — how "confused" the system is about the switch state. | When error exceeds the threshold (red dotted line), the system raises uncertainty to maximum: this triggers the attack response. If error never exceeds the threshold, the anomaly goes undetected. |
| **Epistemic Value** | How much it is worth "slowing down to look more carefully". Rewards the *slow* action when uncertainty is high. | High peak → system has much to gain from exploration and chooses to slow down. Flat at zero → epistemic value does not influence the choice and the system tends to maintain speed. |
| **Pragmatic Value** | Pragmatic cost of the chosen action: physical risk (proximity to transition) + operational cost (maintain=0.1, slow=0.4, stop=0.8). | Rises near the danger zone or when the chosen action is costly. A high value is not necessarily wrong: the system is paying a cost to manage a risky situation. |

### Effect of removing each architectural component

| Removed component | Observed effect |
|---|---|
| **Without Epistemic Value** | No incentive to slow down to reduce uncertainty. EFE = −PragmaticValue for all actions → maintain always wins (minimum cost). Velocity always 10, TP = 0. |
| **Without Anomaly Threshold** | Belief always follows sensor, no anomaly detected during attack. Uncertainty still rises near TRANSITION (0.5), so epistemic value can still make slow win — but not correlated with FDIA attack. |
| **Without Dynamic Uncertainty** | Uncertainty fixed at 0 → epistemic value = 0 → maintain always wins. System does not learn from its own uncertainty. |
| **Without Internal Model** | Expected state always 0. Sensor reads 0.5 during transition → prediction_error > threshold outside attack (high FP). During attack, sensor injects 0.0 = expected → error = 0 → no anomaly detected (TP = 0). |
""",

        "abl2_how_to_md": """\
### How to read the chart

| Chart | What it shows | How to read it |
|---|---|---|
| **Action (Velocity)** | Train velocity at each timestep as a function of the active EFE configuration. Active components change the action selection formula. | Compare behavior with the FULL configuration (all components active). If the train slows in window t=20–30 without false alarms, the active components are sufficient. If it always or never slows, an essential component is missing. |
""",

        "abl2_formula_md": """\
### Canonical EFE Formula

```
EFE(π)  =   -   Pragmatic Value (π)    -     Epistemic Value(π)
              └─────────────────────┘     └────────────────────┘
                  Pragmatic term              Epistemic term

Pragmatic value  =  - Risk(π)  - Cost(π)
```

| Component | Description |
|---|---|
| **Pragmatic Value** | Pragmatic term (= -Risk -Cost): how costly is it to act in this state? |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ **Risk** | Physical proximity risk to the critical point (track switch transition) |
| &nbsp;&nbsp;&nbsp;&nbsp;↳ **Cost** | Operational cost of the action: maintain (0.1) < slow (0.4) < stop (0.8) |
| **Epistemic Value** | Informational term: how much does this action reduce uncertainty? |

---

### Effect of removing each EFE component

| Configuration | Observed effect |
|---|---|
| **Without Risk** (Cost + Epistemic active) | Agent does not perceive proximity to transition. May still slow down due to epistemic value, but not for safety reasons — braking is not correlated with real danger. |
| **Without Cost** (Risk + Epistemic active) | Operational cost = 0 for all actions. Epistemic value still differentiates slow from maintain/stop, so the agent slows more readily than baseline even without danger. |
| **Without Epistemic** (Risk + Cost active) | No incentive to slow down to reduce uncertainty. −PragmaticValue is identical for all actions, so maintain always wins (minimum cost 0.1). Velocity always 10, TP = 0. |
| **Without −PragmaticValue** (Risk + Cost both off, Epistemic active) | EFE(slow) = −uncertainty < 0, EFE(maintain) = EFE(stop) = 0 → slow always wins when uncertainty > 0. Agent brakes indiscriminately, even outside the attack. |
| **No components** (all off) | EFE = 0 for all actions → maintain always wins (first element in list). System is blind: reacts neither to danger nor to uncertainty. |
""",
    },
}
