# Railway Active Inference — Web Interface

Demo interattiva del sistema Active Inference per la sicurezza ferroviaria.
Visualizza in tempo reale come un agente basato su FEP (Free Energy Principle) rileva attacchi FDIA (False Data Injection Attack) e sceglie l'azione ottimale.

## Avvio

```bash
streamlit run app_streamlit.py
```

Requisiti: `streamlit`, `plotly`

---

## File

| File | Funzione |
|------|----------|
| `app_streamlit.py` | Entry point — layout, sidebar, metriche, schede |
| `figures.py` | Costruisce tutti i grafici Plotly (8 layer + 4 overview) |
| `simulation.py` | Loop di simulazione e calcolo F1 |
| `presets.py` | Preset sistemi fallaci e callback slider/number-input |

---

## Barra laterale

### Sistema fallace
Sei checkbox mutuamente esclusivi che caricano preset predefiniti:

| Preset | Cosa fa |
|--------|---------|
| Zero attacchi | Nessun attacco iniettato — il treno passa lo scambio normalmente |
| Baseline | Sistema corretto con tutti i componenti attivi |
| Paranoico | Threshold = 0.01 → falsi positivi continui sul rumore normale |
| Costo truccato | Cost(maintain) = 0.9 → il treno rallenta per costo distorto, non per ragioni epistemiche |
| Over-Cautious | Uncertainty bloccata a 0.9 → rallenta sempre, anche senza attacco |
| Lucky | Modello interno hardcoded sul timing t=22–28 — funziona solo per quel preciso scenario |

### Attacco FDIA
- **Inizio / Fine attacco**: slider + numero per la finestra temporale dell'attacco (default 22–28)
- **Valore iniettato**: `0.0` (stesso stato, attacco nascosto) oppure `1.0` (stato opposto, massima discrepanza rilevabile)

### Sensore e belief
- **Rumore sensore**: ampiezza del rumore uniforme `[-n, +n]` sulle letture normali (default 0.05)

### Costi azioni
Tre valori numerici per i costi operativi nella EFE:

| Azione | Default | Significato |
|--------|---------|-------------|
| maintain | 0.1 | Mantieni velocità nominale — economico |
| slow | 0.4 | Rallenta per raccogliere informazioni — moderato |
| stop | 0.8 | Fermata completa — costoso, ritardo orario |

### Timestep e seed
- **Timestep totali**: durata della simulazione (30–100, default 50)
- **Seed fisso** (attivo per default): riproduce la stessa sequenza di rumore ad ogni run; se disabilitato il rumore varia ad ogni interazione

### Componenti architetturali
Abilitano/disabilitano parti della pipeline di inferenza:

| Componente | Effetto se disabilitato |
|------------|------------------------|
| Anomaly Threshold | Nessuna anomalia rilevata — il belief segue sempre il sensore |
| Uncertainty dinamica | Uncertainty fissa a 0 → epistemic value = 0 → maintain vince sempre |
| Modello interno | Expected state sempre 0 → falsi positivi in fase stabile, nessun rilevamento durante attacco |

### Componenti EFE
Abilitano/disabilitano termini della formula `EFE(π) = −PragmaticValue(π) − EpistemicValue(π)`:

| Componente | Effetto se disabilitato |
|------------|------------------------|
| Pragmatic (= Risk + Cost) | EFE = −EpistemicValue → slow vince sempre quando c'è incertezza |
| Risk | L'agente non percepisce la prossimità fisica alla zona di transizione |
| Cost | Costo operativo = 0 per tutte le azioni |
| Epistemic | Nessun incentivo a rallentare per ridurre incertezza → maintain vince sempre |

---

## Metriche rapide (header)

Sette card aggiornate in tempo reale dopo ogni modifica ai parametri:

| Metrica | Definizione |
|---------|-------------|
| **Anomalie** | Totale timestep in cui il belief ha rilevato un'anomalia |
| **TP** | Timestep in cui il treno rallenta nella finestra [20, 30] durante l'attacco |
| **FP** | Timestep in cui il treno rallenta inutilmente fuori dalla finestra [20, 30] |
| **FN** | Timestep mancati: attacco in finestra, treno non rallenta (11 − TP) |
| **F1-score** |  misura bilanciata di precisione e recall |
| **Precisione** | quante rallentate sono corrette |
| **Degradazione** | quanto il sistema peggiora rispetto al baseline |

---

## Schede (tab)

### Grafici panoramici
Quattro grafici di sintesi ad alto livello:

1. **Stato switch** — stato reale vs stima belief vs lettura sensore; i marker `×` rossi indicano anomalie
2. **Velocità treno** — grafico a barre colorato per azione (verde = maintain, arancio = slow, rosso = stop)
3. **Incertezza epistemica** — andamento dell'incertezza nel tempo (area fill arancione)
4. **Valori EFE comparativi** — le tre curve EFE(maintain/slow/stop); l'agente sceglie il minimo

### Percorso decisionale
Otto grafici impilati che mostrano ogni livello della pipeline:

| Grafico | Contenuto |
|---------|-----------|
| 1. Stato fisico | Ground truth vs lettura sensore (evidenzia la manipolazione FDIA) |
| 2. Inference Layer | Belief state + incertezza + marker anomalia; hover mostra prediction error e decisione TRUST_MODEL/TRUST_SENSOR |
| 3. Prediction Error | '(sensore − modello)' vs soglia — la zona rossa indica anomalia rilevata |
| 4a. EFE Maintain | Pragmatic value e epistemic value per l'azione maintain; dot = timestep in cui è stata scelta |
| 4b. EFE Slow | Pragmatic value e epistemic value per l'azione epistemic_slow |
| 4c. EFE Stop | Pragmatic value e epistemic value per l'azione pragmatic_stop |
| 5. Decision Layer | Le tre curve EFE sovrapposte — visibile quale azione vince ad ogni step |
| 6. Action Layer | Velocità risultante con sfondo colorato per azione |

### Ablazione 1 — Componenti architetturali
Mostra l'effetto dei componenti selezionati nella sidebar sulla pipeline di inferenza.
Il titolo del grafico velocità cambia colore (verde = baseline completo, rosso = componente mancante).

Quattro grafici dinamici:
- **Velocità** con eventuale marker blu per i timestep `epistemic_slow`
- **Prediction Error & Uncertainty** — le due curve + soglia orizzontale
- **Epistemic Value** — valore del termine epistemico nel tempo
- **Pragmatic Value** — costo pragmatico dell'azione scelta (Risk + Cost) nel tempo

Tabella riepilogativa fissa che descrive l'effetto teorico di ciascuna rimozione.

### Ablazione 2 — Componenti EFE
Mostra l'effetto della combinazione attiva di Risk/Cost/Epistemic.
Il nome della configurazione (es. `NO_RISK | C − E`) e le metriche `TP/FP/Prec` sono mostrati sopra il grafico.

Un singolo grafico velocità con fill blu e due bande di sfondo:
- Gialla: finestra di transizione meccanica [20, 30]
- Rossa: finestra di attacco FDIA

Tabella riepilogativa fissa con le configurazioni notevoli (FULL, NO_RISK, NO_COST, NO_EPISTEMIC, NONE).

---

## Formula EFE

```
EFE(π) = −PragmaticValue(π) − EpistemicValue(π)

PragmaticValue(π) = −Risk(π) − Cost(π)

Risk      = min(1.5, proximity + 0.5 * uncertainty)
proximity = max(0,  1 − 2 * |belief − TRANSITION|)

EpistemicValue = uncertainty   se π = epistemic_slow, altrimenti 0
```

L'agente esegue `π* = argmin_π EFE(π)` ad ogni timestep.
