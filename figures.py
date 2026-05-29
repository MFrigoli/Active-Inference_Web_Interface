"""
figures.py
Grafici Plotly per Railway Active Inference.
"""

import plotly.graph_objects as go
from translations import T

ACTION_COLORS = {
    "maintain":       "#2ecc71",
    "epistemic_slow": "#f39c12",
    "pragmatic_stop": "#e74c3c",
}

# Italian fallback kept for backward compatibility
ACTION_LABELS = {
    "maintain":       "Mantieni",
    "epistemic_slow": "Rallenta",
    "pragmatic_stop": "Fermati",
}


def build_figures(log, attack_start, attack_end, anomaly_threshold, lang="it"):
    t = T[lang]

    _action_labels = {
        "maintain":       t["act_maintain"],
        "epistemic_slow": t["act_slow"],
        "pragmatic_stop": t["act_stop"],
    }

    times        = [d["t"]                  for d in log]
    real         = [d["real_state"]         for d in log]
    sensor       = [d["sensor"]             for d in log]
    estimate     = [d["estimate"]           for d in log]
    pred_err     = [d["prediction_error"]   for d in log]
    uncertainty  = [d["uncertainty"]        for d in log]
    velocity     = [d["velocity"]           for d in log]
    actions      = [d["action"]             for d in log]
    efe_m        = [d["efe_maintain"]       for d in log]
    efe_s        = [d["efe_slow"]           for d in log]
    efe_st       = [d["efe_stop"]           for d in log]
    neg_pv_m     = [d["neg_pv_maintain"]    for d in log]
    neg_pv_s     = [d["neg_pv_slow"]        for d in log]
    neg_pv_st    = [d["neg_pv_stop"]        for d in log]
    epist_s      = [d["epistemic_slow_val"] for d in log]
    zero         = [0.0] * len(times)
    trust_labels = [t["trust_model"] if d["anomaly"] else t["trust_sensor"] for d in log]
    anom_t       = [d["t"] for d in log if d["anomaly"]]

    _has_attack = attack_start < attack_end

    def atk_shape():
        return dict(
            type="rect", xref="x", yref="paper",
            x0=attack_start - 0.5, x1=attack_end + 0.5,
            y0=0, y1=1,
            fillcolor="rgba(231,76,60,0.15)" if _has_attack else "rgba(0,0,0,0)",
            line_width=0, layer="below",
        )

    def anomaly_shapes():
        shapes, in_anom, t0 = [], False, None
        for d in log:
            if d["anomaly"] and not in_anom:
                in_anom, t0 = True, d["t"]
            elif not d["anomaly"] and in_anom:
                in_anom = False
                shapes.append(dict(
                    type="rect", xref="x", yref="paper",
                    x0=t0 - 0.5, x1=d["t"] - 0.5,
                    y0=0, y1=1, fillcolor="rgba(231,76,60,0.25)",
                    line_width=0, layer="below",
                ))
        if in_anom:
            shapes.append(dict(
                type="rect", xref="x", yref="paper",
                x0=t0 - 0.5, x1=log[-1]["t"] + 0.5,
                y0=0, y1=1, fillcolor="rgba(231,76,60,0.25)",
                line_width=0, layer="below",
            ))
        return shapes

    T_MAX   = times[-1]
    X_RANGE = [-0.5, T_MAX + 0.5]

    def layout(title, yaxis_title, y_range, last=False):
        return dict(
            title=title,
            xaxis=dict(range=X_RANGE, showgrid=True, dtick=10,
                       title=t["fig_time_axis"] if last else None),
            yaxis=dict(range=y_range, title=yaxis_title, showgrid=True),
            legend=dict(orientation="h", y=-0.22, itemclick=False, itemdoubleclick=False),
            margin=dict(b=70),
            height=290,
            hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
        )

    # 1. Stato fisico: realtà vs sensore
    fig1 = go.Figure()
    fig1.add_shape(**atk_shape())
    if _has_attack:
        fig1.add_annotation(
            x=(attack_start + attack_end) / 2, y=1.05, yref="paper",
            text=t["fig_fdia_label"], showarrow=False,
            font=dict(color="#e74c3c", size=11),
        )
    fig1.add_trace(go.Scatter(
        x=times, y=real, name=t["fig_ground_truth"],
        line=dict(color="#27ae60", width=2),
        hovertemplate="t=%{x} | " + t["fig_state_axis"] + "=%{y:.3f}<extra></extra>",
    ))
    fig1.add_trace(go.Scatter(
        x=times, y=sensor, name=t["fig_sensor"],
        line=dict(color="#e74c3c", width=1.5, dash="dash"),
        hovertemplate="t=%{x} | " + t["fig_sensor"].split(" ")[0].lower() + "=%{y:.3f}<extra></extra>",
    ))
    fig1.update_layout(**layout(t["fig1_title"], t["fig_switch_axis"], [-0.05, 1.1]))

    # 2. Detection Layer: prediction error vs soglia
    fig2 = go.Figure()
    for sh in anomaly_shapes():
        fig2.add_shape(**sh)
    fig2.add_trace(go.Scatter(
        x=times, y=pred_err,
        name=t["fig_pred_trace"],
        line=dict(color="#e67e22", width=2.5),
        customdata=trust_labels,
        hovertemplate="t=%{x} | err=%{y:.3f} → %{customdata}<extra></extra>",
    ))
    fig2.add_trace(go.Scatter(
        x=times, y=[anomaly_threshold] * len(times),
        name=t["fig_threshold"].format(anomaly_threshold),
        line=dict(color="#c0392b", width=2, dash="dash"),
        hovertemplate=t["fig_threshold"].split("=")[0] + "=%{y:.3f}<extra></extra>",
    ))
    fig2.add_trace(go.Scatter(
        x=[None], y=[None], name=t["fig_anomaly_sq"],
        mode="markers",
        marker=dict(size=10, color="rgba(231,76,60,0.4)", symbol="square"),
    ))
    fig2.update_layout(**layout(t["fig2_title"], t["fig_pred_axis"], [-0.05, 1.1]))

    # 3. Inference Layer: come interpreta i dati?
    anom_y = [estimate[t_] for t_ in anom_t]
    belief_custom = list(zip(
        pred_err, [d["expected"] for d in log], uncertainty, trust_labels
    ))

    fig3 = go.Figure()
    for sh in anomaly_shapes():
        fig3.add_shape(**sh)
    fig3.add_trace(go.Scatter(
        x=times, y=uncertainty, name=t["fig_uncertainty"],
        fill="tozeroy",
        line=dict(color="rgba(150,150,150,0.6)", width=1),
        fillcolor="rgba(150,150,150,0.25)",
        hovertemplate="t=%{x} | unc=%{y:.3f}<extra>" + t["fig_uncertainty"] + "</extra>",
    ))
    fig3.add_trace(go.Scatter(
        x=times, y=estimate, name=t["fig_belief"],
        line=dict(color="#2980b9", width=2),
        customdata=belief_custom,
        hovertemplate=(
            "<b>t=%{x}</b><br>" + t["fig_belief"].split(" ")[0] + ": %{y:.3f}<br>"
            "Exp: %{customdata[1]:.3f}<br>"
            "Pred.err: %{customdata[0]:.3f}<br>"
            "Unc: %{customdata[2]:.3f}<br>"
            "<b>→ %{customdata[3]}</b>"
            "<extra>" + t["fig_belief"].split(" ")[0] + "</extra>"
        ),
    ))
    if anom_t:
        fig3.add_trace(go.Scatter(
            x=anom_t, y=anom_y, name=t["fig_anomaly_mk"],
            mode="markers",
            marker=dict(symbol="x", size=9, color="#e74c3c", line_width=2),
            hovertemplate="t=%{x} → " + t["trust_model"] + "<extra></extra>",
        ))
    fig3.update_layout(**layout(t["fig3_title"], t["fig_belief_axis"], [-0.05, 1.1]))

    # Helper: EFE per-action graph
    def efe_action_fig(title, neg_pv_vals, epist_vals, efe_vals_list,
                       action_key, line_color, efe_label, efe_dash):
        ch_t = [d["t"] for d in log if d["action"] == action_key]
        ch_y = [efe_vals_list[d["t"]] for d in log if d["action"] == action_key]
        fig = go.Figure()
        fig.add_shape(**atk_shape())
        fig.add_trace(go.Scatter(
            x=times, y=neg_pv_vals, name=t["fig_neg_pv"],
            line=dict(color="#c0392b", width=2),
            hovertemplate="t=%{x} | −PV=%{y:.3f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=times, y=epist_vals, name=t["fig_epist"],
            line=dict(color="#8e44ad", width=1.5),
            hovertemplate="t=%{x} | Epist=%{y:.3f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=times, y=efe_vals_list, name=efe_label,
            line=dict(color=line_color, width=2, dash=efe_dash),
            hovertemplate="t=%{x} | EFE=%{y:.3f}<extra></extra>",
        ))
        if ch_t:
            fig.add_trace(go.Scatter(
                x=ch_t, y=ch_y, name=t["fig_chosen"],
                mode="markers",
                marker=dict(symbol="circle", size=8, color=line_color),
                hovertemplate="t=%{x} | " + t["fig_chosen"].lower() + "<extra></extra>",
            ))
        fig.update_layout(**layout(title, t["fig_efe_y"], [-0.1, 2.5]))
        return fig

    fig4a = efe_action_fig(
        t["fig4a_title"], neg_pv_m, zero, efe_m, "maintain",
        "#27ae60", t["fig4a_efe_lbl"], "dot",
    )
    fig4b = efe_action_fig(
        t["fig4b_title"], neg_pv_s, epist_s, efe_s, "epistemic_slow",
        "#2980b9", t["fig4b_efe_lbl"], "dash",
    )
    fig4c = efe_action_fig(
        t["fig4c_title"], neg_pv_st, zero, efe_st, "pragmatic_stop",
        "#c0392b", t["fig4c_efe_lbl"], "dash",
    )

    # 5. Decision Layer
    chosen_efe = [
        d["efe_slow"]     if d["action"] == "epistemic_slow"
        else d["efe_stop"] if d["action"] == "pragmatic_stop"
        else d["efe_maintain"]
        for d in log
    ]
    fig5 = go.Figure()
    fig5.add_shape(**atk_shape())
    fig5.add_trace(go.Scatter(
        x=times, y=efe_m, name=_action_labels["maintain"] + " (v=10)",
        line=dict(color="#27ae60", width=2),
        hovertemplate="t=%{x} | EFE maintain=%{y:.3f}<extra></extra>",
    ))
    fig5.add_trace(go.Scatter(
        x=times, y=efe_s, name=_action_labels["epistemic_slow"] + " (v=4)",
        line=dict(color="#2980b9", width=2),
        hovertemplate="t=%{x} | EFE slow=%{y:.3f}<extra></extra>",
    ))
    fig5.add_trace(go.Scatter(
        x=times, y=efe_st, name=_action_labels["pragmatic_stop"] + " (v=0)",
        line=dict(color="#c0392b", width=2),
        hovertemplate="t=%{x} | EFE stop=%{y:.3f}<extra></extra>",
    ))
    fig5.add_trace(go.Scatter(
        x=times, y=chosen_efe, name=t["fig_chosen"],
        mode="markers",
        marker=dict(symbol="circle", size=7, color="#2c3e50"),
        customdata=actions,
        hovertemplate="t=%{x} | EFE=%{y:.3f} | %{customdata}<extra></extra>",
    ))
    fig5.update_layout(**layout(t["fig5_title"], t["fig_efe_axis"], [-0.1, 2.5]))

    # 6. Action Layer
    action_fill = {
        "maintain":       "rgba(46,204,113,0.15)",
        "epistemic_slow": "rgba(52,152,219,0.15)",
        "pragmatic_stop": "rgba(231,76,60,0.15)",
    }
    fig6 = go.Figure()
    prev_a, seg_start = actions[0], times[0]
    for i in range(1, len(times) + 1):
        cur_a = actions[i] if i < len(times) else None
        if cur_a != prev_a:
            fig6.add_shape(
                type="rect", xref="x", yref="paper",
                x0=seg_start - 0.5, x1=times[i - 1] + 0.5,
                y0=0, y1=1, fillcolor=action_fill[prev_a],
                line_width=0, layer="below",
            )
            if i < len(times):
                prev_a, seg_start = cur_a, times[i]
    fig6.add_trace(go.Scatter(
        x=times, y=velocity, name=t["fig_vel_trace"],
        line=dict(color="#2980b9", width=3),
        customdata=actions,
        hovertemplate="t=%{x} | v=%{y} km/h | %{customdata}<extra></extra>",
    ))
    for action, color in ACTION_COLORS.items():
        fig6.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(size=10, color=color, symbol="square"),
            name=_action_labels[action],
        ))
    fig6.update_layout(**layout(t["fig6_title"], t["fig_vel_axis"], [-0.5, 11], last=True))

    # ── Overview figures ──────────────────────────────────────────────────────
    belief_custom = list(zip(
        pred_err, [d["expected"] for d in log], uncertainty, trust_labels
    ))
    ov_state = go.Figure()
    ov_state.add_shape(**atk_shape())
    if _has_attack:
        ov_state.add_annotation(
            x=(attack_start + attack_end) / 2, y=1.05, yref="paper",
            text=t["ov_atk_label"], showarrow=False,
            font=dict(color="#e74c3c", size=12),
        )
    ov_state.add_trace(go.Scatter(
        x=times, y=real, name=t["fig_ground_truth"],
        line=dict(color="#3498db", width=2, dash="dot"),
    ))
    ov_state.add_trace(go.Scatter(
        x=times, y=sensor, name=t["fig_sensor"],
        mode="markers+lines", marker=dict(size=4),
        line=dict(color="#95a5a6", width=1),
    ))
    ov_state.add_trace(go.Scatter(
        x=times, y=estimate, name=t["fig_belief"],
        line=dict(color="#9b59b6", width=2),
        customdata=belief_custom,
        hovertemplate=(
            "<b>t=%{x}</b><br>" + t["fig_belief"].split(" ")[0] + ": %{y:.3f}<br>"
            "Exp: %{customdata[1]:.3f}<br>"
            "Pred.err: %{customdata[0]:.3f}<br>"
            "Unc: %{customdata[2]:.3f}<br>"
            "<b>→ %{customdata[3]}</b><extra>" + t["fig_belief"].split(" ")[0] + "</extra>"
        ),
    ))
    if anom_t:
        ov_state.add_trace(go.Scatter(
            x=anom_t, y=[estimate[t_] for t_ in anom_t],
            name=t["fig_anomaly_mk"], mode="markers",
            marker=dict(symbol="x", size=10, color="#e74c3c"),
        ))
    ov_state.update_layout(
        title=t["ov_state_title"],
        yaxis_title=t["ov_state_yaxis"],
        legend=dict(orientation="h", y=-0.22, itemclick=False, itemdoubleclick=False),
        height=320, margin=dict(b=70),
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    ov_vel = go.Figure()
    ov_vel.add_shape(**atk_shape())
    ov_vel.add_trace(go.Bar(
        x=times, y=velocity,
        marker_color=[ACTION_COLORS[a] for a in actions],
        name=t["fig_vel_trace"], showlegend=False,
        customdata=actions,
        hovertemplate="t=%{x} | v=%{y} km/h | %{customdata}<extra></extra>",
    ))
    for action, color in ACTION_COLORS.items():
        ov_vel.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(size=10, color=color, symbol="square"),
            name=_action_labels[action],
        ))
    ov_vel.update_layout(
        title=t["ov_vel_title"],
        yaxis_title=t["ov_vel_yaxis"],
        legend=dict(orientation="h", y=-0.22, itemclick=False, itemdoubleclick=False),
        height=300, margin=dict(b=70),
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    ov_unc = go.Figure()
    ov_unc.add_shape(**atk_shape())
    ov_unc.add_trace(go.Scatter(
        x=times, y=uncertainty, name=t["fig_uncertainty"],
        fill="tozeroy",
        line=dict(color="#e67e22", width=2),
        fillcolor="rgba(230,126,34,0.2)",
        hovertemplate="t=%{x} | unc=%{y:.3f}<extra></extra>",
    ))
    ov_unc.update_layout(
        title=t["ov_unc_title"],
        yaxis_title=t["ov_unc_yaxis"], yaxis_range=[-0.05, 1.1],
        legend=dict(orientation="h", y=-0.22, itemclick=False, itemdoubleclick=False),
        height=280, margin=dict(b=70),
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    ov_efe = go.Figure()
    ov_efe.add_shape(**atk_shape())
    ov_efe.add_trace(go.Scatter(
        x=times, y=efe_m, name="EFE " + _action_labels["maintain"].lower(),
        line=dict(color="#2ecc71", width=2),
        hovertemplate="t=%{x} | EFE maintain=%{y:.3f}<extra></extra>",
    ))
    ov_efe.add_trace(go.Scatter(
        x=times, y=efe_s, name="EFE " + _action_labels["epistemic_slow"].lower(),
        line=dict(color="#f39c12", width=2),
        hovertemplate="t=%{x} | EFE slow=%{y:.3f}<extra></extra>",
    ))
    ov_efe.add_trace(go.Scatter(
        x=times, y=efe_st, name="EFE " + _action_labels["pragmatic_stop"].lower(),
        line=dict(color="#e74c3c", width=2),
        hovertemplate="t=%{x} | EFE stop=%{y:.3f}<extra></extra>",
    ))
    ov_efe.update_layout(
        title=t["ov_efe_title"],
        yaxis_title=t["ov_efe_yaxis"],
        legend=dict(orientation="h", y=-0.22, itemclick=False, itemdoubleclick=False),
        height=300, margin=dict(b=70),
        hoverlabel=dict(bgcolor="white", font_color="black", font_size=13),
    )

    layers   = (fig1, fig2, fig3, fig4a, fig4b, fig4c, fig5, fig6)
    overview = (ov_state, ov_vel, ov_unc, ov_efe)
    return layers, overview
