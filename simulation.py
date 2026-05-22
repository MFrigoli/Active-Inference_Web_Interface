"""
simulation.py
Logica di simulazione Railway Active Inference (parametrizzata).
"""

import random

TRANSITION_WIN = (20, 30)


def run_simulation(
    anomaly_threshold,
    sensor_noise,
    attack_start,
    attack_end,
    time_steps,
    enable_hazard,
    enable_cost,
    enable_epistemic,
    cost_maintain,
    cost_slow,
    cost_stop,
    seed,
    enable_threshold=True,
    enable_uncertainty=True,
    enable_model=True,
    min_uncertainty=0.1,
    lucky_model=False,
    attack_value=0.0,
):
    random.seed(seed)

    STABLE_A   = 0.0
    TRANSITION = 0.5
    STABLE_B   = 1.0
    V_NOMINAL  = 10
    V_SLOW     = 4
    V_STOP     = 0

    BASE_COSTS = {
        "maintain":       cost_maintain,
        "epistemic_slow": cost_slow,
        "pragmatic_stop": cost_stop,
    }

    switch_state     = STABLE_A
    belief_estimate  = STABLE_A
    uncertainty      = 0.1
    velocity         = V_NOMINAL
    anomaly_detected = False
    log              = []

    for t in range(time_steps):
        # --- Ambiente ---
        if 20 <= t <= 30:
            switch_state = TRANSITION
        elif t > 30:
            switch_state = STABLE_B
        else:
            switch_state = STABLE_A

        # --- Sensore ---
        attack = attack_start < attack_end and attack_start <= t <= attack_end
        if attack:
            sensor_value = attack_value
        else:
            noise        = random.uniform(-sensor_noise, sensor_noise)
            sensor_value = max(0.0, min(1.0, switch_state + noise))

        # --- Belief update ---
        # Lucky model: timing hardcoded su t=22-28 — funziona solo se l'attacco
        # coincide esattamente; qualsiasi altra finestra lo inganna
        if lucky_model:
            if 22 <= t <= 28:
                expected = TRANSITION
            elif t > 30:
                expected = STABLE_B
            else:
                expected = sensor_value
        elif enable_model:
            if 20 <= t <= 30:
                expected = TRANSITION
            elif t > 30:
                expected = STABLE_B
            else:
                expected = STABLE_A
        else:
            expected = STABLE_A

        prediction_error = abs(sensor_value - expected)

        if enable_threshold and prediction_error > anomaly_threshold:
            anomaly_detected = True
            belief_estimate  = expected
            uncertainty      = 1.0 if enable_uncertainty else 0.0
        else:
            anomaly_detected = False
            belief_estimate  = sensor_value
            if enable_uncertainty:
                raw_unc     = 1.0 - abs(belief_estimate - TRANSITION) * 2
                uncertainty = max(min_uncertainty, raw_unc)
            else:
                uncertainty = 0.0

        # --- EFE ---
        def calc_efe(action):
            if enable_hazard:
                risk_prox = max(0.0, 1.0 - abs(belief_estimate - TRANSITION) * 2)
                risk_unc  = uncertainty * 0.5
                risk      = min(1.5, risk_prox + risk_unc)
            else:
                risk_prox = risk_unc = risk = 0.0

            cost = BASE_COSTS[action] if enable_cost else 0.0

            if enable_epistemic and action == "epistemic_slow":
                epistemic = uncertainty
            else:
                epistemic = 0.0

            pragmatic_value = -(risk + cost)

            return {
                "risk": risk, "risk_prox": risk_prox, "risk_unc": risk_unc,
                "cost": cost, "epistemic": epistemic,
                "pragmatic_value": pragmatic_value,
                "efe": -pragmatic_value - epistemic,
            }

        efe_vals    = {a: calc_efe(a) for a in ["maintain", "epistemic_slow", "pragmatic_stop"]}
        best_action = min(efe_vals, key=lambda a: efe_vals[a]["efe"])

        if best_action == "maintain":
            velocity = V_NOMINAL
        elif best_action == "epistemic_slow":
            velocity = V_SLOW
        else:
            velocity = V_STOP

        ch  = efe_vals[best_action]
        log.append({
            "t":                 t,
            "real_state":        switch_state,
            "expected":          expected,
            "sensor":            sensor_value,
            "prediction_error":  prediction_error,
            "estimate":          belief_estimate,
            "uncertainty":       uncertainty,
            "anomaly":           anomaly_detected,
            "velocity":          velocity,
            "action":            best_action,
            "attack":            attack,
            "efe_maintain":      efe_vals["maintain"]["efe"],
            "efe_slow":          efe_vals["epistemic_slow"]["efe"],
            "efe_stop":          efe_vals["pragmatic_stop"]["efe"],
            "neg_pv_maintain":   -efe_vals["maintain"]["pragmatic_value"],
            "neg_pv_slow":       -efe_vals["epistemic_slow"]["pragmatic_value"],
            "neg_pv_stop":       -efe_vals["pragmatic_stop"]["pragmatic_value"],
            "epistemic_slow_val": efe_vals["epistemic_slow"]["epistemic"],
            "risk":              ch["risk"],
            "risk_prox":         ch["risk_prox"],
            "risk_unc":          ch["risk_unc"],
            "cost":              ch["cost"],
            "pragmatic_value":   ch["pragmatic_value"],
            "epistemic":         ch["epistemic"],
        })

    return log


def compute_metrics(sim_log):
    """Metriche di rilevamento basate sul flag anomaly (coerente con la tesi).

    TP = anomaly=True  AND  attack=True  AND  t in TRANSITION_WIN
    FP = anomaly=True  AND  attack=False  (qualsiasi t)
    FN = anomaly=False AND  attack=True   AND  t in TRANSITION_WIN
    """
    tp = fp = fn = 0
    for d in sim_log:
        t      = d["t"]
        anom   = d["anomaly"]
        attack = d["attack"]
        in_win = TRANSITION_WIN[0] <= t <= TRANSITION_WIN[1]

        if anom and attack and in_win:
            tp += 1
        elif anom and not attack:
            fp += 1
        elif not anom and attack and in_win:
            fn += 1

    max_tp = sum(
        1 for d in sim_log
        if d["attack"] and TRANSITION_WIN[0] <= d["t"] <= TRANSITION_WIN[1]
    )
    prec   = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1     = 2 * prec * recall / (prec + recall) if (prec + recall) > 0 else 0.0
    return {
        "tp": tp, "fp": fp, "fn": fn, "max_tp": max_tp,
        "precision": prec, "recall": recall, "f1": f1,
    }
