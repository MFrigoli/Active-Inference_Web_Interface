"""
simulation.py
Logica di simulazione Railway Active Inference (parametrizzata).
"""

import random

TRANSITION_WIN = (20, 30)
MAX_TP = TRANSITION_WIN[1] - TRANSITION_WIN[0] + 1  # 11


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
                prox   = max(0.0, 1.0 - abs(belief_estimate - TRANSITION) * 2)
                unc_h  = uncertainty * 0.5
                hazard = min(1.5, prox + unc_h)
            else:
                prox = unc_h = hazard = 0.0

            cost = BASE_COSTS[action] if enable_cost else 0.0

            if enable_epistemic and action == "epistemic_slow":
                epistemic = uncertainty
            else:
                epistemic = 0.0

            return {
                "hazard": hazard, "hazard_prox": prox, "hazard_unc": unc_h,
                "cost": cost, "epistemic": epistemic,
                "efe": hazard + cost - epistemic,
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
        _h  = efe_vals["maintain"]["hazard"]  # identico per tutte le azioni
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
            "risk_maintain":     _h + efe_vals["maintain"]["cost"],
            "risk_slow":         _h + efe_vals["epistemic_slow"]["cost"],
            "risk_stop":         _h + efe_vals["pragmatic_stop"]["cost"],
            "epistemic_slow_val": efe_vals["epistemic_slow"]["epistemic"],
            "hazard":            ch["hazard"],
            "hazard_prox":       ch["hazard_prox"],
            "hazard_unc":        ch["hazard_unc"],
            "cost":              ch["cost"],
            "epistemic":         ch["epistemic"],
        })

    return log


def compute_f1(sim_log):
    _tp  = sum(1 for d in sim_log if d["velocity"] < 10 and TRANSITION_WIN[0] <= d["t"] <= TRANSITION_WIN[1])
    _fp  = sum(1 for d in sim_log if d["velocity"] < 10 and not (TRANSITION_WIN[0] <= d["t"] <= TRANSITION_WIN[1]))
    prec = _tp / (_tp + _fp) if (_tp + _fp) > 0 else 0.0
    rec  = _tp / MAX_TP
    return 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
