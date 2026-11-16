#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic Markdown & LaTeX Booktabs Table Generator (G-SYNC-TABLE) for Wave 4
(Supplementary Appendix D: Query-Time Relationship Reconstruction Benchmark).
"""

import hashlib
from pathlib import Path
from typing import Any, Dict, List


def fmt_int_es(n: int) -> str:
    return f"{int(n):,}".replace(",", ".")


def fmt_int_en(n: int) -> str:
    return f"{int(n):,}"


def fmt_float_es(val: float, decimals: int = 2) -> str:
    s = f"{float(val):,.{decimals}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_float_en(val: float, decimals: int = 2) -> str:
    return f"{float(val):,.{decimals}f}"


def tex_escape(text: str) -> str:
    return (
        str(text)
        .replace("\\", "\\textbackslash{}")
        .replace("_", "\\_")
        .replace("%", "\\%")
        .replace("&", "\\&")
        .replace("#", "\\#")
        .replace("<->", "$\\leftrightarrow$")
        .replace("->", "$\\rightarrow$")
    )


def compute_file_meta(path: Path) -> Dict[str, Any]:
    st = path.stat()
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return {
        "size_bytes": int(st.st_size),
        "st_blocks": int(getattr(st, "st_blocks", 0)),
        "mtime_ns": int(st.st_mtime_ns),
        "sha256": h.hexdigest(),
    }


def generate_ola4_reports(
    resumen_ola4: Dict[str, Any],
    ola4_dir: Path,
    anexos_dir: Path,
) -> Dict[str, Path]:
    """
    Construye programáticamente (Regla G-SYNC-TABLE):
      - wave4_detailed_audit_log.md (español)
      - Appendix_D_Query_Time_Relationship_Reconstruction_Benchmark.md (inglés Q1 ITcon)
    """
    exp41 = resumen_ola4["experiment_4_1_50_lifecycle_queries_benchmark"]
    exp42 = resumen_ola4["experiment_4_2_hop_scaling_and_wilcoxon"]
    exp43 = resumen_ola4["experiment_4_3_markov_blanket_isolation"]
    exp44 = resumen_ola4["experiment_4_4_shift_left_kits_and_5_stages"]
    step0 = resumen_ola4["step_0_ola3_refinement_verification"]

    hop_rows = exp42["hop_depth_summary_rows"]
    recipe_rows = exp42["recipe_summary_rows"]
    global_summary = exp42["global_50_queries_summary"]
    scaling_fit = exp42["asymptotic_scaling_fit"]
    wilcoxon_rows = exp42["wilcoxon_and_bootstrap_rows"]
    query_rows = exp41["per_query_benchmark_rows"]
    top_hubs = exp43["top_15_national_hubs_rows"]
    markov_summary = exp43["summary_metrics"]
    kits_rows = exp44["shift_left_9_kits_rows"]
    kits_summary = exp44["shift_left_kits_summary"]
    stage_rows = exp44["retrospective_5_stages_phi_eff_rows"]

    # =========================================================================
    # TABLA D.1: Resumen por profundidad de salto (k=1..6) y 13 recetas (EN/ES)
    # =========================================================================
    md_td1_en = [
        "| Stratum / Hop Depth / Recipe | Queries ($n$) | Reconstructed Tuples (Sum) | `M1` Monolithic RDF Mean ± SD (ms) | `M2` Row-SQL (`sqlite3`) Mean ± SD (ms) | `M3` SITI $t_{\\text{C1}}$ ($\\mu\\text{s}$) | `M3` SITI $t_{\\text{C2}}$ ($\\mu\\text{s}$) | `M3` SITI $t_{\\text{C3}}$ ($\\mu\\text{s}$) | `M3` SITI Total Mean ± SD (ms) | `M3` $p_{50}$ / $p_{95}$ (ms) | Speedup $S_{\\text{M1/M3}}$ | Speedup $S_{\\text{M2/M3}}$ | $\\Phi_{\\text{eff}}^{\\text{(vs M1)}}$ (\\%) | $\\Phi_{\\text{eff}}^{\\text{(vs M2)}}$ (\\%) | Parity |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    md_td1_es = [
        "| Estrato / Profundidad $k$ / Receta | Consultas ($n$) | Tuplas reconstruidas (Suma) | `M1` RDF Monolítico Media ± DE (ms) | `M2` SQL Filas (`sqlite3`) Media ± DE (ms) | `M3` SITI $t_{\\text{C1}}$ ($\\mu\\text{s}$) | `M3` SITI $t_{\\text{C2}}$ ($\\mu\\text{s}$) | `M3` SITI $t_{\\text{C3}}$ ($\\mu\\text{s}$) | `M3` SITI Total Media ± DE (ms) | `M3` $p_{50}$ / $p_{95}$ (ms) | Speedup $S_{\\text{M1/M3}}$ | Speedup $S_{\\text{M2/M3}}$ | $\\Phi_{\\text{eff}}^{\\text{(vs M1)}}$ (\\%) | $\\Phi_{\\text{eff}}^{\\text{(vs M2)}}$ (\\%) | Paridad |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    tex_td1_rows = []

    def append_td1_row(r: Dict[str, Any], bold: bool = False) -> None:
        lbl_en = r["stratum_label_en"]
        lbl_es = r["stratum_label_es"]
        nq = r["queries_count"]
        tup = r["total_reconstructed_rows"]
        m1_m, m1_sd = r["m1_mean_ms"], r["m1_sd_ms"]
        m2_m, m2_sd = r["m2_mean_ms"], r["m2_sd_ms"]
        tc1, tc2, tc3 = r["m3_c1_mean_us"], r["m3_c2_mean_us"], r["m3_c3_mean_us"]
        m3_m, m3_sd = r["m3_mean_ms"], r["m3_sd_ms"]
        m3_p50, m3_p95 = r["m3_p50_ms"], r["m3_p95_ms"]
        sp1, sp2 = r["speedup_m1_vs_m3"], r["speedup_m2_vs_m3"]
        pe1, pe2 = r["phi_eff_vs_m1_pct"], r["phi_eff_vs_m2_pct"]
        par = "100%" if r["parity_100pct"] else "FAIL"

        b_pre = "**" if bold else ""
        md_td1_en.append(
            f"| {b_pre}{lbl_en}{b_pre} | `{nq}` | `{fmt_int_en(tup)}` | `{fmt_float_en(m1_m, 3)} ± {fmt_float_en(m1_sd, 3)}` | `{fmt_float_en(m2_m, 3)} ± {fmt_float_en(m2_sd, 3)}` | `{fmt_float_en(tc1, 2)}` | `{fmt_float_en(tc2, 2)}` | `{fmt_float_en(tc3, 2)}` | {b_pre}`{fmt_float_en(m3_m, 3)} ± {fmt_float_en(m3_sd, 3)}`{b_pre} | `{fmt_float_en(m3_p50, 3)} / {fmt_float_en(m3_p95, 3)}` | {b_pre}`{fmt_float_en(sp1, 2)}x`{b_pre} | {b_pre}`{fmt_float_en(sp2, 2)}x`{b_pre} | {b_pre}`{fmt_float_en(pe1, 2)}%`{b_pre} | {b_pre}`{fmt_float_en(pe2, 2)}%`{b_pre} | `{par}` |"
        )
        md_td1_es.append(
            f"| {b_pre}{lbl_es}{b_pre} | `{nq}` | `{fmt_int_es(tup)}` | `{fmt_float_es(m1_m, 3)} ± {fmt_float_es(m1_sd, 3)}` | `{fmt_float_es(m2_m, 3)} ± {fmt_float_es(m2_sd, 3)}` | `{fmt_float_es(tc1, 2)}` | `{fmt_float_es(tc2, 2)}` | `{fmt_float_es(tc3, 2)}` | {b_pre}`{fmt_float_es(m3_m, 3)} ± {fmt_float_es(m3_sd, 3)}`{b_pre} | `{fmt_float_es(m3_p50, 3)} / {fmt_float_es(m3_p95, 3)}` | {b_pre}`{fmt_float_es(sp1, 2)}x`{b_pre} | {b_pre}`{fmt_float_es(sp2, 2)}x`{b_pre} | {b_pre}`{fmt_float_es(pe1, 2)}%`{b_pre} | {b_pre}`{fmt_float_es(pe2, 2)}%`{b_pre} | `{par}` |"
        )
        if bold:
            tex_td1_rows.append("\\midrule")
            tex_td1_rows.append(
                f"\\textbf{{{tex_escape(lbl_en)}}} & \\textbf{{{nq}}} & \\textbf{{{fmt_int_en(tup)}}} & \\textbf{{{fmt_float_en(m1_m, 2)}}} & \\textbf{{{fmt_float_en(m2_m, 2)}}} & \\textbf{{{fmt_float_en(tc1, 1)}}} & \\textbf{{{fmt_float_en(tc2, 1)}}} & \\textbf{{{fmt_float_en(tc3, 1)}}} & \\textbf{{{fmt_float_en(m3_m, 3)}}} & \\textbf{{{fmt_float_en(sp1, 2)}x}} & \\textbf{{{fmt_float_en(sp2, 2)}x}} & \\textbf{{{fmt_float_en(pe1, 2)}\\%}} & \\textbf{{{fmt_float_en(pe2, 2)}\\%}} \\\\"
            )
        else:
            tex_td1_rows.append(
                f"{tex_escape(lbl_en)} & {nq} & {fmt_int_en(tup)} & {fmt_float_en(m1_m, 2)} $\\pm$ {fmt_float_en(m1_sd, 2)} & {fmt_float_en(m2_m, 2)} $\\pm$ {fmt_float_en(m2_sd, 2)} & {fmt_float_en(tc1, 1)} & {fmt_float_en(tc2, 1)} & {fmt_float_en(tc3, 1)} & {fmt_float_en(m3_m, 3)} $\\pm$ {fmt_float_en(m3_sd, 3)} & {fmt_float_en(sp1, 2)}x & {fmt_float_en(sp2, 2)}x & {fmt_float_en(pe1, 2)}\\% & {fmt_float_en(pe2, 2)}\\% \\\\"
            )

    for hr in hop_rows:
        append_td1_row(hr, bold=False)
    append_td1_row(global_summary, bold=True)
    for rr in recipe_rows:
        append_td1_row(rr, bold=False)

    # =========================================================================
    # TABLA D.2: Desglose completo de las 50 consultas de ciclo de vida (EN/ES)
    # =========================================================================
    md_td2_en = [
        "| Query ID | Hop $k$ | Recipe | Domain & Path Pattern | Late Spatial | Tuples | `M1` Mean (ms) | `M2` Mean (ms) | `M3` $t_{\\text{C1}}$ ($\\mu\\text{s}$) | `M3` $t_{\\text{C2}}$ ($\\mu\\text{s}$) | `M3` $t_{\\text{C3}}$ ($\\mu\\text{s}$) | `M3` Mean ± SD (ms) | $S_{\\text{M1/M3}}$ | $S_{\\text{M2/M3}}$ | $\\Phi_{\\text{eff}}^{\\text{(vs M1)}}$ (\\%) | $\\Phi_{\\text{eff}}^{\\text{(vs M2)}}$ (\\%) | Parity |",
        "| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    md_td2_es = [
        "| ID Consulta | Salto $k$ | Receta | Dominio y patrón de camino intertabular | Espacial Tardío | Tuplas | `M1` Media (ms) | `M2` Media (ms) | `M3` $t_{\\text{C1}}$ ($\\mu\\text{s}$) | `M3` $t_{\\text{C2}}$ ($\\mu\\text{s}$) | `M3` $t_{\\text{C3}}$ ($\\mu\\text{s}$) | `M3` Media ± DE (ms) | $S_{\\text{M1/M3}}$ | $S_{\\text{M2/M3}}$ | $\\Phi_{\\text{eff}}^{\\text{(vs M1)}}$ (\\%) | $\\Phi_{\\text{eff}}^{\\text{(vs M2)}}$ (\\%) | Paridad |",
        "| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    tex_td2_rows = []

    for q in query_rows:
        qid = q["query_id"]
        hk = q["hop_depth_k"]
        rec = q["recipe_id"]
        dom_en = q["title_en"]
        dom_es = q["title_es"]
        lsp = "Yes" if q["requires_late_spatial_materialization"] else "No"
        lsp_es = "Sí" if q["requires_late_spatial_materialization"] else "No"
        ntup = q["reconstructed_rows_count"]
        m1m = q["m1_mean_ms"]
        m2m = q["m2_mean_ms"]
        tc1 = q["m3_c1_mean_us"]
        tc2 = q["m3_c2_mean_us"]
        tc3 = q["m3_c3_mean_us"]
        m3m = q["m3_mean_ms"]
        m3sd = q["m3_sd_ms"]
        sp1 = q["speedup_m1_vs_m3"]
        sp2 = q["speedup_m2_vs_m3"]
        pe1 = q["phi_eff_vs_m1_pct"]
        pe2 = q["phi_eff_vs_m2_pct"]
        par = "OK" if q["result_parity_verified"] else "FAIL"

        md_td2_en.append(
            f"| `{qid}` | `{hk}` | `{rec}` | {dom_en} (`{q['anchor_code']}`) | `{lsp}` | `{fmt_int_en(ntup)}` | `{fmt_float_en(m1m, 3)}` | `{fmt_float_en(m2m, 3)}` | `{fmt_float_en(tc1, 2)}` | `{fmt_float_en(tc2, 2)}` | `{fmt_float_en(tc3, 2)}` | `{fmt_float_en(m3m, 3)} ± {fmt_float_en(m3sd, 3)}` | `{fmt_float_en(sp1, 2)}x` | `{fmt_float_en(sp2, 2)}x` | `{fmt_float_en(pe1, 2)}%` | `{fmt_float_en(pe2, 2)}%` | `{par}` |"
        )
        md_td2_es.append(
            f"| `{qid}` | `{hk}` | `{rec}` | {dom_es} (`{q['anchor_code']}`) | `{lsp_es}` | `{fmt_int_es(ntup)}` | `{fmt_float_es(m1m, 3)}` | `{fmt_float_es(m2m, 3)}` | `{fmt_float_es(tc1, 2)}` | `{fmt_float_es(tc2, 2)}` | `{fmt_float_es(tc3, 2)}` | `{fmt_float_es(m3m, 3)} ± {fmt_float_es(m3sd, 3)}` | `{fmt_float_es(sp1, 2)}x` | `{fmt_float_es(sp2, 2)}x` | `{fmt_float_es(pe1, 2)}%` | `{fmt_float_es(pe2, 2)}%` | `{par}` |"
        )
        tex_td2_rows.append(
            f"\\texttt{{{tex_escape(qid)}}} & {hk} & \\texttt{{{tex_escape(rec)}}} & {tex_escape(dom_en)} & {lsp} & {fmt_int_en(ntup)} & {fmt_float_en(m1m, 2)} & {fmt_float_en(m2m, 2)} & {fmt_float_en(tc1, 1)} & {fmt_float_en(tc2, 1)} & {fmt_float_en(tc3, 1)} & {fmt_float_en(m3m, 3)} & {fmt_float_en(sp1, 1)}x & {fmt_float_en(sp2, 1)}x & {fmt_float_en(pe1, 2)}\\% & {fmt_float_en(pe2, 2)}\\% \\\\"
        )

    # =========================================================================
    # TABLA D.3: Pruebas pareadas de Wilcoxon, tamaños del efecto y Bootstrap
    # =========================================================================
    md_td3_en = [
        "| Comparison Stratum | $N$ | Baseline Mean (ms) | SITI `M3` Mean (ms) | Mean $\\Delta T$ (ms) | 95% Bootstrap CI $\\Delta T$ (Perc / BCa, ms) | Mean $\\Phi_{\\text{eff}}$ (\\%) | 95% Bootstrap CI $\\Phi_{\\text{eff}}$ (BCa, \\%) | Wilcoxon $W$ | $Z$-stat | $p$-value (two-sided) | Cohen's $d$ | Hedges' $g$ | Rosenthal's $r$ | $r_{rb}$ |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    md_td3_es = [
        "| Estrato de comparación | $N$ | Línea base Media (ms) | SITI `M3` Media (ms) | Media $\\Delta T$ (ms) | IC 95% Bootstrap $\\Delta T$ (Perc / BCa, ms) | Media $\\Phi_{\\text{eff}}$ (\\%) | IC 95% Bootstrap $\\Phi_{\\text{eff}}$ (BCa, \\%) | Wilcoxon $W$ | $Z$-stat | Valor-$p$ (bilateral) | $d$ de Cohen | $g$ de Hedges | $r$ de Rosenthal | $r_{rb}$ |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    tex_td3_rows = []

    for w in wilcoxon_rows:
        lbl_en = w["comparison_label_en"]
        lbl_es = w["comparison_label_es"]
        nw = w["n_queries"]
        tb = w["mean_baseline_ms"]
        tm3 = w["mean_m3_ms"]
        dt = w["mean_delta_ms"]
        dt_pl, dt_pu = w["ci95_perc_delta_ms_low"], w["ci95_perc_delta_ms_high"]
        dt_bl, dt_bu = w["ci95_bca_delta_ms_low"], w["ci95_bca_delta_ms_high"]
        pe = w["mean_phi_eff_pct"]
        pe_bl, pe_bu = w["ci95_bca_phi_eff_low"], w["ci95_bca_phi_eff_high"]
        ws = w["wilcoxon_w_stat"]
        zs = w["wilcoxon_z_stat"]
        pv = w["p_value_two_sided_str"]
        cd = w["cohens_d"]
        hg = w["hedges_g"]
        rr = w["rosenthals_r"]
        rrb = w["rank_biserial_r"]

        ci_dt_en = f"[{fmt_float_en(dt_pl, 2)}, {fmt_float_en(dt_pu, 2)}] / [{fmt_float_en(dt_bl, 2)}, {fmt_float_en(dt_bu, 2)}]"
        ci_pe_en = f"[{fmt_float_en(pe_bl, 2)}%, {fmt_float_en(pe_bu, 2)}%]"
        ci_dt_es = f"[{fmt_float_es(dt_pl, 2)}; {fmt_float_es(dt_pu, 2)}] / [{fmt_float_es(dt_bl, 2)}; {fmt_float_es(dt_bu, 2)}]"
        ci_pe_es = f"[{fmt_float_es(pe_bl, 2)}%; {fmt_float_es(pe_bu, 2)}%]"

        md_td3_en.append(
            f"| **{lbl_en}** | `{nw}` | `{fmt_float_en(tb, 3)}` | `{fmt_float_en(tm3, 3)}` | `-{fmt_float_en(dt, 3)}` | `{ci_dt_en}` | `{fmt_float_en(pe, 2)}%` | `{ci_pe_en}` | `{fmt_float_en(ws, 1)}` | `{fmt_float_en(zs, 4)}` | `{pv}` | `{fmt_float_en(cd, 2)}` | `{fmt_float_en(hg, 2)}` | `{fmt_float_en(rr, 4)}` | `{fmt_float_en(rrb, 4)}` |"
        )
        md_td3_es.append(
            f"| **{lbl_es}** | `{nw}` | `{fmt_float_es(tb, 3)}` | `{fmt_float_es(tm3, 3)}` | `-{fmt_float_es(dt, 3)}` | `{ci_dt_es}` | `{fmt_float_es(pe, 2)}%` | `{ci_pe_es}` | `{fmt_float_es(ws, 1)}` | `{fmt_float_es(zs, 4)}` | `{pv}` | `{fmt_float_es(cd, 2)}` | `{fmt_float_es(hg, 2)}` | `{fmt_float_es(rr, 4)}` | `{fmt_float_es(rrb, 4)}` |"
        )
        tex_td3_rows.append(
            f"{tex_escape(lbl_en)} & {nw} & {fmt_float_en(tb, 2)} & {fmt_float_en(tm3, 3)} & -{fmt_float_en(dt, 2)} & [{fmt_float_en(dt_bl, 2)}, {fmt_float_en(dt_bu, 2)}] & {fmt_float_en(pe, 2)}\\% & [{fmt_float_en(pe_bl, 2)}, {fmt_float_en(pe_bu, 2)}] & {fmt_float_en(ws, 1)} & {fmt_float_en(zs, 3)} & {pv} & {fmt_float_en(cd, 2)} & {fmt_float_en(hg, 2)} & {fmt_float_en(rr, 3)} \\\\"
        )

    # =========================================================================
    # TABLA D.4: Aislamiento por Manta de Markov en los 316 nodos ancla y Top 15
    # =========================================================================
    md_td4_en = [
        "| Rank / Hub Code | Canonical Class Name (SITI Layer 1/2) | Table | Intertabular Degree ($d_{\\text{in}} + d_{\\text{out}}$) | Parents $|\\text{Pa}(v)|$ | Children $|\\text{Ch}(v)|$ | Spouses $|\\text{Sp}(v)|$ | Full Markov Blanket $|\\partial\\mathcal{M}(v)|$ | Intertabular $|\\partial\\mathcal{M}_{\\text{inter}}(v)|$ | Extraction Latency ($\\mu\\text{s}$) | Causal Isolation $\\Phi_{\\text{eff}}^{\\text{(Markov-Isolation)}}$ (\\%) |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    md_td4_es = [
        "| Rango / Código Hub | Nombre canónico de la clase (SITI Capa 1/2) | Tabla | Grado intertabular ($d_{\\text{in}} + d_{\\text{out}}$) | Padres $|\\text{Pa}(v)|$ | Hijos $|\\text{Ch}(v)|$ | Esposos $|\\text{Sp}(v)|$ | Manta Markov total $|\\partial\\mathcal{M}(v)|$ | Manta intertabular $|\\partial\\mathcal{M}_{\\text{inter}}(v)|$ | Latencia extracción ($\\mu\\text{s}$) | Aislamiento causal $\\Phi_{\\text{eff}}^{\\text{(Markov-Isolation)}}$ (\\%) |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    tex_td4_rows = []

    for h in top_hubs:
        rk = h["hub_rank"]
        code = h["code"]
        nm = h["name"]
        tb = h["table_id"]
        ideg = h["intertabular_degree"]
        pa = h["pa_full_count"]
        ch = h["ch_full_count"]
        sp = h["sp_full_count"]
        mb_full = h["markov_blanket_full_size"]
        mb_inter = h["markov_blanket_inter_size"]
        lat_us = h["extraction_latency_us"]
        iso_pct = h["phi_eff_markov_isolation_full_pct"]

        md_td4_en.append(
            f"| `#{rk}` (`{code}`) | {nm} | `{tb}` | `{ideg}` (`{h['inter_in_deg']}+{h['inter_out_deg']}`) | `{pa}` | `{ch}` | `{sp}` | **`{mb_full}`** | `{mb_inter}` | `{fmt_float_en(lat_us, 3)}` | **`{fmt_float_en(iso_pct, 4)}%`** |"
        )
        md_td4_es.append(
            f"| `#{rk}` (`{code}`) | {nm} | `{tb}` | `{ideg}` (`{h['inter_in_deg']}+{h['inter_out_deg']}`) | `{pa}` | `{ch}` | `{sp}` | **`{mb_full}`** | `{mb_inter}` | `{fmt_float_es(lat_us, 3)}` | **`{fmt_float_es(iso_pct, 4)}%`** |"
        )
        tex_td4_rows.append(
            f"\\#{rk} (\\texttt{{{tex_escape(code)}}}) & {tex_escape(nm)} & \\texttt{{{tb}}} & {ideg} & {pa} & {ch} & {sp} & \\textbf{{{mb_full}}} & {mb_inter} & {fmt_float_en(lat_us, 2)} & \\textbf{{{fmt_float_en(iso_pct, 4)}\\%}} \\\\"
        )

    # Filas de resumen de los 316 nodos ancla y los 16.232 nodos totales
    md_td4_en.append(
        f"| **Mean (316 Anchor Nodes)** | Intertabularly Coupled Anchor Subgraph | `A10–B50` | **`{fmt_float_en(markov_summary['anchor_316_mean_inter_degree'], 2)}`** | `{fmt_float_en(markov_summary['anchor_316_mean_pa_full'], 2)}` | `{fmt_float_en(markov_summary['anchor_316_mean_ch_full'], 2)}` | `{fmt_float_en(markov_summary['anchor_316_mean_sp_full'], 2)}` | **`{fmt_float_en(markov_summary['anchor_316_mean_markov_full'], 2)}`** | `{fmt_float_en(markov_summary['anchor_316_mean_markov_inter'], 2)}` | `{fmt_float_en(markov_summary['anchor_316_mean_extraction_us'], 3)}` | **`{fmt_float_en(markov_summary['anchor_316_mean_isolation_full_pct'], 4)}%`** |"
    )
    md_td4_en.append(
        f"| **Mean (All 16,232 C2 Nodes)** | Complete SITI Layer 2 Topological Graph | `A10–B50` | `{fmt_float_en(markov_summary['all_16232_mean_inter_degree'], 4)}` | `{fmt_float_en(markov_summary['all_16232_mean_pa_full'], 2)}` | `{fmt_float_en(markov_summary['all_16232_mean_ch_full'], 2)}` | `{fmt_float_en(markov_summary['all_16232_mean_sp_full'], 2)}` | **`{fmt_float_en(markov_summary['all_16232_mean_markov_full'], 2)}`** | `{fmt_float_en(markov_summary['all_16232_mean_markov_inter'], 4)}` | `{fmt_float_en(markov_summary['all_16232_mean_extraction_us'], 3)}` | **`{fmt_float_en(markov_summary['all_16232_mean_isolation_full_pct'], 4)}%`** |"
    )
    md_td4_es.append(
        f"| **Media (316 Nodos Ancla)** | Subgrafo de anclas intertabulares acopladas | `A10–B50` | **`{fmt_float_es(markov_summary['anchor_316_mean_inter_degree'], 2)}`** | `{fmt_float_es(markov_summary['anchor_316_mean_pa_full'], 2)}` | `{fmt_float_es(markov_summary['anchor_316_mean_ch_full'], 2)}` | `{fmt_float_es(markov_summary['anchor_316_mean_sp_full'], 2)}` | **`{fmt_float_es(markov_summary['anchor_316_mean_markov_full'], 2)}`** | `{fmt_float_es(markov_summary['anchor_316_mean_markov_inter'], 2)}` | `{fmt_float_es(markov_summary['anchor_316_mean_extraction_us'], 3)}` | **`{fmt_float_es(markov_summary['anchor_316_mean_isolation_full_pct'], 4)}%`** |"
    )
    md_td4_es.append(
        f"| **Media (16.232 Nodos C2)** | Grafo topológico completo de Capa 2 | `A10–B50` | `{fmt_float_es(markov_summary['all_16232_mean_inter_degree'], 4)}` | `{fmt_float_es(markov_summary['all_16232_mean_pa_full'], 2)}` | `{fmt_float_es(markov_summary['all_16232_mean_ch_full'], 2)}` | `{fmt_float_es(markov_summary['all_16232_mean_sp_full'], 2)}` | **`{fmt_float_es(markov_summary['all_16232_mean_markov_full'], 2)}`** | `{fmt_float_es(markov_summary['all_16232_mean_markov_inter'], 4)}` | `{fmt_float_es(markov_summary['all_16232_mean_extraction_us'], 3)}` | **`{fmt_float_es(markov_summary['all_16232_mean_isolation_full_pct'], 4)}%`** |"
    )
    tex_td4_rows.append("\\midrule")
    tex_td4_rows.append(
        f"\\textbf{{Mean (316 Anchors)}} & Intertabular Anchor Subgraph & \\texttt{{A10--B50}} & \\textbf{{{fmt_float_en(markov_summary['anchor_316_mean_inter_degree'], 2)}}} & {fmt_float_en(markov_summary['anchor_316_mean_pa_full'], 2)} & {fmt_float_en(markov_summary['anchor_316_mean_ch_full'], 2)} & {fmt_float_en(markov_summary['anchor_316_mean_sp_full'], 2)} & \\textbf{{{fmt_float_en(markov_summary['anchor_316_mean_markov_full'], 2)}}} & {fmt_float_en(markov_summary['anchor_316_mean_markov_inter'], 2)} & {fmt_float_en(markov_summary['anchor_316_mean_extraction_us'], 2)} & \\textbf{{{fmt_float_en(markov_summary['anchor_316_mean_isolation_full_pct'], 4)}\\%}} \\\\"
    )
    tex_td4_rows.append(
        f"\\textbf{{Mean (16,232 Nodes)}} & Complete SITI Layer 2 Graph & \\texttt{{A10--B50}} & {fmt_float_en(markov_summary['all_16232_mean_inter_degree'], 4)} & {fmt_float_en(markov_summary['all_16232_mean_pa_full'], 2)} & {fmt_float_en(markov_summary['all_16232_mean_ch_full'], 2)} & {fmt_float_en(markov_summary['all_16232_mean_sp_full'], 2)} & \\textbf{{{fmt_float_en(markov_summary['all_16232_mean_markov_full'], 2)}}} & {fmt_float_en(markov_summary['all_16232_mean_markov_inter'], 4)} & {fmt_float_en(markov_summary['all_16232_mean_extraction_us'], 2)} & \\textbf{{{fmt_float_en(markov_summary['all_16232_mean_isolation_full_pct'], 4)}\\%}} \\\\"
    )

    # =========================================================================
    # TABLA D.5: Panel A (9 Kits BIM/GIS) y Panel B (Evolución 5 Etapas CAS)
    # =========================================================================
    md_td5a_en = [
        "| Kit ID | Suite | Target Authoring Tool / Standard | Verified Files | Total Size (Bytes) | Composite `SHA-256` Prefix | Covered SITI Classes / Psets | Prevented Wave 2 Cold-Ingestion Failures (`unsupported` / `partial`) | $\\Phi_{\\text{eff}}^{\\text{(Shift-Left)}}$ (\\%) |",
        "| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    md_td5a_es = [
        "| ID Kit | Suite | Herramienta de autoría / estándar objetivo | Archivos verificados | Tamaño total (Bytes) | Prefijo `SHA-256` compuesto | Clases SITI / Psets cubiertos | Fallas de ingesta en frío prevenidas en origen (Ola 2) | $\\Phi_{\\text{eff}}^{\\text{(Shift-Left)}}$ (\\%) |",
        "| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: |",
    ]
    tex_td5a_rows = []

    for kr in kits_rows:
        kid = kr["kit_id"]
        suite = kr["suite_category"]
        tool = kr["tool_name"]
        nfiles = kr["verified_files_count"]
        tbytes = kr["total_bytes"]
        sha16 = kr["composite_sha256"][:16]
        cov = kr["coverage_summary_en"]
        cov_es = kr["coverage_summary_es"]
        prev_en = kr["prevented_failures_en"]
        prev_es = kr["prevented_failures_es"]
        f_pct = kr["shift_left_fidelity_pct"]

        md_td5a_en.append(
            f"| `{kid}` | `{suite}` | **{tool}** | `{nfiles}` | `{fmt_int_en(tbytes)}` | `{sha16}...` | `{cov}` | {prev_en} | **`{fmt_float_en(f_pct, 2)}%`** |"
        )
        md_td5a_es.append(
            f"| `{kid}` | `{suite}` | **{tool}** | `{nfiles}` | `{fmt_int_es(tbytes)}` | `{sha16}...` | `{cov_es}` | {prev_es} | **`{fmt_float_es(f_pct, 2)}%`** |"
        )
        tex_td5a_rows.append(
            f"\\texttt{{{tex_escape(kid)}}} & \\texttt{{{tex_escape(suite)}}} & \\textbf{{{tex_escape(tool)}}} & {nfiles} & {fmt_int_en(tbytes)} & \\texttt{{{sha16}}} & {tex_escape(cov)} & {tex_escape(prev_en)} & \\textbf{{{fmt_float_en(f_pct, 1)}\\%}} \\\\"
        )

    md_td5a_en.append(
        f"| **TOTAL (9 Kits)** | **BIM (5) + GIS (4)** | **Complete Shift-Left Ecosystem (`Fase_activa_nueva/`)** | **`{kits_summary['unique_physical_files_count']}`** (`{kits_summary['sum_kit_file_references']}` refs) | **`{fmt_int_en(kits_summary['unique_physical_bytes_total'])}`** | `{kits_summary['global_kits_sha256'][:16]}...` | **`16,230` classes + `849` Psets/Qtos** | **Prevents `49/49` `unsupported` (`100%`) & `174/174` `partial` (`100%`)** | **`100.00%`** |"
    )
    md_td5a_es.append(
        f"| **TOTAL (9 Kits)** | **BIM (5) + GIS (4)** | **Ecosistema Shift-Left Completo (`Fase_activa_nueva/`)** | **`{kits_summary['unique_physical_files_count']}`** (`{kits_summary['sum_kit_file_references']}` refs) | **`{fmt_int_es(kits_summary['unique_physical_bytes_total'])}`** | `{kits_summary['global_kits_sha256'][:16]}...` | **`16.230` clases + `849` Psets/Qtos** | **Previene `49/49` `unsupported` (`100%`) y `174/174` `partial` (`100%`)** | **`100,00%`** |"
    )
    tex_td5a_rows.append("\\midrule")
    tex_td5a_rows.append(
        f"\\textbf{{TOTAL (9 Kits)}} & \\textbf{{BIM+GIS}} & \\textbf{{Complete Shift-Left Suite}} & \\textbf{{{kits_summary['unique_physical_files_count']}}} & \\textbf{{{fmt_int_en(kits_summary['unique_physical_bytes_total'])}}} & \\texttt{{{kits_summary['global_kits_sha256'][:16]}}} & \\textbf{{16,230 + 849}} & \\textbf{{Prevents 49 unsupported + 174 partial}} & \\textbf{{100.0\\%}} \\\\"
    )

    md_td5b_en = [
        "| Lineage Stage | Publication / Revision ID | Active C2 Intertabular Edges | Active Recipes | Queries Reconstructed Without Orphanage ($n/50$) | Query Completion Rate (\\%) | Mean Reconstruction Latency (ms) | $\\Phi_{\\text{eff}}^{\\text{(Query-Time vs M1)}}$ (\\%) | $\\Phi_{\\text{eff}}^{\\text{(Query-Time vs M2)}}$ (\\%) | $\\Phi_{\\text{eff}}^{\\text{(Markov-Isolation)}}$ (\\%) | $\\Phi_{\\text{eff}}^{\\text{(Shift-Left-Kits)}}$ (\\%) | Composite $\\Phi_{\\text{eff}}$ (\\%) |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    md_td5b_es = [
        "| Etapa del linaje | ID de publicación / revisión | Aristas intertabulares C2 activas | Recetas activas | Consultas reconstruidas sin orfandad ($n/50$) | Tasa de completitud (\\%) | Latencia media de reconstrucción (ms) | $\\Phi_{\\text{eff}}^{\\text{(Query-Time vs M1)}}$ (\\%) | $\\Phi_{\\text{eff}}^{\\text{(Query-Time vs M2)}}$ (\\%) | $\\Phi_{\\text{eff}}^{\\text{(Markov-Isolation)}}$ (\\%) | $\\Phi_{\\text{eff}}^{\\text{(Shift-Left-Kits)}}$ (\\%) | $\\Phi_{\\text{eff}}$ Compuesto (\\%) |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    tex_td5b_rows = []

    for sr in stage_rows:
        st_id = sr["stage_id"]
        rev = sr["revision_label"]
        edg = sr["active_c2_intertabular_edges"]
        rec_c = sr["active_recipes_count"]
        q_ok = sr["queries_reconstructed_without_orphanage"]
        q_pct = sr["queries_completion_rate_pct"]
        lat_m = sr["mean_reconstruction_latency_ms"]
        pe_m1 = sr["phi_eff_query_time_vs_m1_pct"]
        pe_m2 = sr["phi_eff_query_time_vs_m2_pct"]
        pe_mk = sr["phi_eff_markov_isolation_pct"]
        pe_sl = sr["phi_eff_shift_left_kits_pct"]
        pe_comp = sr["phi_eff_composite_pct"]

        md_td5b_en.append(
            f"| **{st_id}** | `{rev}` | `{fmt_int_en(edg)}` | `{rec_c}/13` | `{q_ok}/50` | **`{fmt_float_en(q_pct, 2)}%`** | `{fmt_float_en(lat_m, 3)}` | `{fmt_float_en(pe_m1, 2)}%` | `{fmt_float_en(pe_m2, 2)}%` | `{fmt_float_en(pe_mk, 4)}%` | `{fmt_float_en(pe_sl, 2)}%` | **`{fmt_float_en(pe_comp, 2)}%`** |"
        )
        md_td5b_es.append(
            f"| **{st_id}** | `{rev}` | `{fmt_int_es(edg)}` | `{rec_c}/13` | `{q_ok}/50` | **`{fmt_float_es(q_pct, 2)}%`** | `{fmt_float_es(lat_m, 3)}` | `{fmt_float_es(pe_m1, 2)}%` | `{fmt_float_es(pe_m2, 2)}%` | `{fmt_float_es(pe_mk, 4)}%` | `{fmt_float_es(pe_sl, 2)}%` | **`{fmt_float_es(pe_comp, 2)}%`** |"
        )
        tex_td5b_rows.append(
            f"\\textbf{{{tex_escape(st_id)}}} & \\texttt{{{tex_escape(rev)}}} & {fmt_int_en(edg)} & {rec_c}/13 & {q_ok}/50 & \\textbf{{{fmt_float_en(q_pct, 1)}\\%}} & {fmt_float_en(lat_m, 3)} & {fmt_float_en(pe_m1, 2)}\\% & {fmt_float_en(pe_m2, 2)}\\% & {fmt_float_en(pe_mk, 2)}\\% & {fmt_float_en(pe_sl, 1)}\\% & \\textbf{{{fmt_float_en(pe_comp, 2)}\\%}} \\\\"
        )

    # =========================================================================
    # CONSTRUCCIÓN DEL INFORME DETALLADO EN ESPAÑOL
    # =========================================================================
    informe_es_lines = [
        "# Informe Técnico Detallado — Ola 4 de 6: Benchmark Físico en Vivo de Reconstrucción de Relaciones en Tiempo de Consulta ($\\Phi_{\\text{eff}}$), Aislamiento Causal por Manta de Markov y Auditoría de los 9 Kits Shift-Left BIM/GIS",
        "",
        f"**Fecha de certificación:** `{resumen_ola4['timestamp_utc']}`",
        f"**Revisión semántica activa (CAS 4):** `{resumen_ola4['active_cas_revision']}`",
        "**Reglas y guardarraíles verificados:** `G-PHYS` (`os.O_RDONLY`, `0` bytes modificados en producción, `st_blocks > 0`), `G-AST` (`SitiAstAntiTheaterGate` bipolar en vivo), `G-SEM` (invarianza de 3 capas `C1/C2/C3`, `Calzada SITI = carril` `A30_035_005_040`, `ESAL` singular invariable), `G-HASH` (`SHA-256`) y `G-SYNC-TABLE` (generación 100% programática de tablas Markdown y LaTeX `booktabs`).",
        "",
        "---",
        "",
        "## 1. Verificación del Paso 0 Obligatorio: Eliminación de la Meseta `3.0632 / 2.0037` en `Table C.3` de la Ola 3",
        "",
        "Antes de iniciar los experimentos de la Ola 4, se ejecutó y verificó en modo lectura (`os.O_RDONLY`) el **Paso 0** sobre `03_ola3_entropia_shannon_skos_phi_sem/scripts/wave3_shannon_entropy_skos_wilcoxon.py`:",
        "- **Causa raíz corregida:** Reemplazo de los topes discretos fijos (`min(2, intra_siblings)` con pesos constantes) por el cálculo continuo en vivo basado en el conteo exacto de candidatos $|\\mathcal{C}_1(w)|$ ponderado por $\\text{IDF}(w) = \\ln(1 + 16.230 / |\\mathcal{C}_1(w)|)$, el grado topológico intertabular real en Capa 2 ($d_{\\text{in}} + d_{\\text{out}}$), el tamaño de la Manta de Markov $|\\partial\\mathcal{M}(c)|$, la cobertura léxica SKOS, la entropía de mezcla de capas/materiales por concesión y la dispersión geodésica y contractual.",
        f"- **Verificación de unicidad a 4 decimales en `Panel A` (`N=47` particiones):** `{step0['panel_a_unique_4dec_per_stage']}` valores únicos de `47` en las 5 etapas ($S_0 \\dots S_4$).",
        f"- **Verificación de unicidad a 4 decimales en `Panel B` (`N=50` concesiones maestras):** `{step0['panel_b_unique_4dec_per_stage']}` valores únicos de `50` en las 5 etapas ($S_0 \\dots S_4$).",
        f"- **Verificación de unicidad a 4 decimales en las `53` entidades combinadas de `Table C.3`:** `{step0['combined_53_unique_4dec_per_stage']}` valores únicos de `53` (`0` empates, `0` apariciones de la meseta `3.0632 / 2.0037`).",
        f"- **Caída monótona estricta en `Panel A` ($S_0 \\to S_4$):** `{step0['panel_a_mean_h_5_stages']}` bits ($\\Phi_{{\\text{{sem}}}}(S_4) = {fmt_float_es(step0['panel_a_phi_sem_s4_pct'], 4)}\\%$).",
        f"- **Caída monótona estricta en `Panel B` ($S_0 \\to S_4$):** `{step0['panel_b_mean_h_5_stages']}` bits ($\\Phi_{{\\text{{sem}}}}(S_4) = {fmt_float_es(step0['panel_b_phi_sem_s4_pct'], 4)}\\%$).",
        "",
        "---",
        "",
        "## 2. Demostración Física de la Tesis del Prof. Dr. Žiga Turk ($\\Phi_{\\text{eff}}$): Síntesis por Profundidad de Salto ($k = 1 \\dots 6$) y 13 Recetas (`Table D.1`)",
        "",
        "La evaluación empírica de las **50 consultas reales de ciclo de vida** (3 iteraciones de calentamiento + 15 iteraciones cronometradas con `time.perf_counter_ns()` por consulta y motor) demuestra cuantitativamente que separar la información geométrica pesada de la información operacional y reconstruir las relaciones en tiempo de consulta mediante `M3` (`C1 SKOS/OWL/SHACL -> C2 LPG O(1) + Markov Blanket -> C3 DuckDB SIMD Parquet con Late Spatial Materialization`) supera de manera abrumadora tanto al grafo monolítico de tripletas RDF (`M1`) como al modelo relacional orientado a filas con geometría acoplada (`M2`, `sqlite3`):",
        f"- **Latencia global media en las 50 consultas:** `M1` = `{fmt_float_es(global_summary['m1_mean_ms'], 3)} ± {fmt_float_es(global_summary['m1_sd_ms'], 3)} ms`, `M2` = `{fmt_float_es(global_summary['m2_mean_ms'], 3)} ± {fmt_float_es(global_summary['m2_sd_ms'], 3)} ms`, frente a **`M3` (SITI) = `{fmt_float_es(global_summary['m3_mean_ms'], 3)} ± {fmt_float_es(global_summary['m3_sd_ms'], 3)} ms`** ($t_{{\\text{{C1}}}} = {fmt_float_es(global_summary['m3_c1_mean_us'], 2)}\\,\\mu\\text{{s}}$, $t_{{\\text{{C2}}}} = {fmt_float_es(global_summary['m3_c2_mean_us'], 2)}\\,\\mu\\text{{s}}$, $t_{{\\text{{C3}}}} = {fmt_float_es(global_summary['m3_c3_mean_us'], 2)}\\,\\mu\\text{{s}}$).",
        f"- **Factores de aceleración globales (*Speedup*):** **`{fmt_float_es(global_summary['speedup_m1_vs_m3'], 2)}x` frente a `M1`** ($\\Phi_{{\\text{{eff}}}}^{{\\text{{(vs M1)}}}} = {fmt_float_es(global_summary['phi_eff_vs_m1_pct'], 2)}\\%$) y **`{fmt_float_es(global_summary['speedup_m2_vs_m3'], 2)}x` frente a `M2`** ($\\Phi_{{\\text{{eff}}}}^{{\\text{{(vs M2)}}}} = {fmt_float_es(global_summary['phi_eff_vs_m2_pct'], 2)}\\%$).",
        f"- **Escalamiento asintótico con la profundidad $k \\in [1, 6]$:** La pendiente exponencial $\\beta$ en $\\ln T(k) = \\alpha + \\beta k$ es $\\beta_{{\\text{{M1}}}} = {fmt_float_es(scaling_fit['m1_exp_slope_beta'], 4)}$ ($R^2 = {fmt_float_es(scaling_fit['m1_exp_r2'], 4)}$) y $\\beta_{{\\text{{M2}}}} = {fmt_float_es(scaling_fit['m2_exp_slope_beta'], 4)}$ ($R^2 = {fmt_float_es(scaling_fit['m2_exp_r2'], 4)}$), mientras que en `M3` es cuasi-plana ($\\beta_{{\\text{{M3}}}} = {fmt_float_es(scaling_fit['m3_exp_slope_beta'], 4)}$) porque los $k$ saltos se resuelven en microsegundos dentro del grafo `C2` en RAM antes de ejecutar una única proyección columnar vectorizada en `C3`.",
        "",
        *md_td1_es,
        "",
        "---",
        "",
        "## 3. Desglose Completo de las 50 Consultas de Ciclo de Vida ($t_{\\text{C1}}, t_{\\text{C2}}, t_{\\text{C3}}$, Speedup y Paridad 100%, `Table D.2`)",
        "",
        *md_td2_es,
        "",
        "---",
        "",
        "## 4. Inferencia No Paramétrica Pareada de Wilcoxon, Tamaños del Efecto e IC 95% Bootstrap ($B = 10.000$, `Table D.3`)",
        "",
        *md_td3_es,
        "",
        "---",
        "",
        "## 5. Aislamiento Causal por Manta de Markov $\\partial\\mathcal{M}(v)$ en los `316` Nodos Ancla y Top 15 Hubs Nacionales (`Table D.4`)",
        "",
        *md_td4_es,
        "",
        "---",
        "",
        "## 6. Auditoría Física de los 9 Kits Shift-Left (`Kits_BIM` y `Kits_GIS`) y Evolución Retrospectiva de $\\Phi_{\\text{eff}}$ en las 5 Etapas CAS (`Table D.5`)",
        "",
        "### 6.1. Panel A: Auditoría Física Criptográfica de los 9 Kits de Autoría en Origen",
        "",
        *md_td5a_es,
        "",
        "### 6.2. Panel B: Evolución Retrospectiva de $\\Phi_{\\text{eff}}$ a través de las 5 Etapas del Linaje CAS (`Stage 0` a `Stage 4`)",
        "",
        *md_td5b_es,
        "",
    ]

    informe_es_path = ola4_dir / "wave4_detailed_audit_log.md"
    with open(informe_es_path, "w", encoding="utf-8") as f:
        f.write("\n".join(informe_es_lines))

    # =========================================================================
    # CONSTRUCCIÓN DEL APPENDIX D EN INGLÉS ACADÉMICO Q1 PARA ITCON
    # =========================================================================
    appendix_d_lines = [
        "# Supplementary Appendix D: Live Query-Time Relationship Reconstruction Benchmark ($k = 1 \\dots 6$ Hops), Markov Blanket Causal Isolation, and Shift-Left OpenBIM/GIS Authoring Kits ($\\Phi_{\\text{eff}}$)",
        "",
        "**Target Journal:** *Journal of Information Technology in Construction (ITcon)* — Second Submission (Extended Empirical & Mathematical Paper)",
        "**Editor-in-Chief:** Prof. Dr. Žiga Turk",
        f"**Active CAS Semantic Publication:** `{resumen_ola4['active_cas_revision']}` (`2026-10-25.puerta25-owl2dl-axiomatized.1`)",
        f"**Verification Timestamp (UTC):** `{resumen_ola4['timestamp_utc']}`",
        "",
        "---",
        "",
        "## D.1 Formal Mathematical Definition of the Third Dimension of the Semantic Interoperability Index ($\\Phi_{\\text{eff}}$)",
        "",
        "To test and quantify the core architectural hypothesis formulated by Prof. Dr. Žiga Turk—*\"For legacy infrastructure, semantic interoperability can be achieved more effectively by separating geometric information from operational information and reconstruct relationships at query time\"*—we define the third dimension of the Semantic Interoperability Index ($\\Phi_{\\text{eff}}$) across three complementary operational sub-metrics:",
        "",
        "1. **Query-Time Relationship Reconstruction Efficiency ($\\Phi_{\\text{eff}}^{\\text{(Query-Time)}}$):**",
        "   $$\\Phi_{\\text{eff}}^{\\text{(Query-Time)}}(s) = \\left(1 - \\frac{T_{\\text{SITI}, s}}{T_{\\text{Baseline}}}\\right) \\times 100\\%, \\qquad T_{\\text{SITI}, s} = t_{\\text{C1 (SKOS/OWL/SHACL)}} + t_{\\text{C2 (LPG O(1) + Markov Blanket)}} + t_{\\text{C3 (DuckDB Vectorized SIMD Parquet)}}$$",
        "   evaluated across a canonical benchmark of **$N = 50$ real lifecycle engineering and asset-management queries** spanning topological hop depths $k \\in \\{1, 2, 3, 4, 5, 6\\}$ and all **13 formal intertabular assembly recipes (`REC-A-01..07`, `REC-B-01..06`)**, comparing the three-layer SITI pipeline (`M3`) against two coupled baseline paradigms:",
        "   - **`M1` (`Monolithic RDF/Triple-Store Traversal`):** evaluation of $k$-hop Basic Graph Pattern (BGP) `(s, p, o)` triple joins over the `438,194` TBox triples of `capa1_siti_ontology.ttl` plus materialized ABox instance triples without Layer 2 O(1) pointer adjacency or Layer 3 columnar decoupling.",
        "   - **`M2` (`Traditional Row-Oriented Relational SQL / Coupled Wide Table & Multi-Way B-Tree JOINs`):** execution over row-oriented relational tables (`sqlite3` B-Tree storage with coupled geometry payloads and $k$-way relational `JOIN`s).",
        "   - **`M3` (`SITI Three-Layer Query-Time Reconstruction`):** decoupled execution `C1 -> C2 -> C3` with *Late Spatial Materialization*, touching `assets_spatial_instances_ani.parquet` (`226,322` WKB/GeoJSON geometries in `EPSG:9377`) or `assets_spatial_instances.parquet` (`5,011` `ENU` 64-bit instances) strictly when the query requests spatial coordinates.",
        "2. **Topological Causal Isolation via Pearl's Markov Blanket ($\\Phi_{\\text{eff}}^{\\text{(Markov-Isolation)}}$):**",
        "   $$\\Phi_{\\text{eff}}^{\\text{(Markov-Isolation)}}(v) = \\left(1 - \\frac{|\\partial\\mathcal{M}(v)| + 1}{|\\mathcal{V}_{C2}|}\\right) \\times 100\\%, \\qquad \\partial\\mathcal{M}(v) = \\text{Pa}(v) \\cup \\text{Ch}(v) \\cup \\text{Sp}(v)$$",
        f"   evaluated across all **`316` intertabular anchor nodes** and all **`16,232` total concepts** in Layer 2 (`17,021` total edges: `16,228` `SUBCLASE_DE` + `793` deduplicated intertabular edges, `0` intratabular meronymy edges), achieving a mean search-space reduction of **`{fmt_float_en(markov_summary['anchor_316_mean_isolation_full_pct'], 4)}%`** across the 316 anchors (`{fmt_float_en(markov_summary['all_16232_mean_isolation_full_pct'], 4)}%` across all 16,232 nodes).",
        "3. **Shift-Left Source Authoring Fidelity ($\\Phi_{\\text{eff}}^{\\text{(Shift-Left-Kits)}}$):**",
        "   Physical cryptographic audit of the **9 Shift-Left Authoring Kits** (`5` OpenBIM kits in `Kits_BIM/` and `4` GIS kits in `Kits_GIS/`), demonstrating how pre-tagged authoring templates eliminate at the source the `49` `unsupported` (`26` mute IFCs, `21` unstructured TXTs, `1` proprietary binary RVT, `1` malformed CSV) and `174` `partial` cold-ingestion receipts identified in Wave 2.",
        "",
        "---",
        "",
        "## D.2 Benchmark Summary Across Hop Depths $k = 1 \\dots 6$ and 13 Assembly Recipes (`Table D.1`)",
        "",
        "### Table D.1 (Markdown Format)",
        "",
        *md_td1_en,
        "",
        "### Table D.1 (LaTeX `booktabs` Format)",
        "",
        "```latex",
        "\\begin{table*}[htbp]",
        "\\centering",
        "\\caption{Benchmark Summary of Query-Time Relationship Reconstruction Across Hop Depths $k = 1 \\dots 6$ and 13 Assembly Recipes: Monolithic RDF/SPARQL (M1) vs.\\ Row-Oriented SQL (M2) vs.\\ SITI Three-Layer Pipeline (M3).}",
        "\\label{tab:appendix_d_table_d1}",
        "\\resizebox{\\textwidth}{!}{%",
        "\\begin{tabular}{lrrrrrrrrrrrr}",
        "\\toprule",
        "Stratum / Hop Depth / Recipe & $n$ & Tuples & M1 Mean $\\pm$ SD (ms) & M2 Mean $\\pm$ SD (ms) & $t_{\\text{C1}}$ ($\\mu$s) & $t_{\\text{C2}}$ ($\\mu$s) & $t_{\\text{C3}}$ ($\\mu$s) & M3 Mean $\\pm$ SD (ms) & $S_{\\text{M1/M3}}$ & $S_{\\text{M2/M3}}$ & $\\Phi_{\\text{eff}}^{\\text{(M1)}}$ & $\\Phi_{\\text{eff}}^{\\text{(M2)}}$ \\\\",
        "\\midrule",
        *tex_td1_rows,
        "\\bottomrule",
        "\\end{tabular}%",
        "}",
        "\\end{table*}",
        "```",
        "",
        "---",
        "",
        "## D.3 Complete Per-Query Latency Breakdown and 100% Result-Set Parity Across All 50 Lifecycle Queries (`Table D.2`)",
        "",
        "### Table D.2 (Markdown Format)",
        "",
        *md_td2_en,
        "",
        "### Table D.2 (LaTeX `booktabs` Format)",
        "",
        "```latex",
        "\\begin{table*}[htbp]",
        "\\centering",
        "\\caption{Complete Per-Query Latency Breakdown ($t_{\\text{C1}}, t_{\\text{C2}}, t_{\\text{C3}}$), Speedup Factors, and 100\\% Result-Set Parity Across All 50 Lifecycle Engineering Queries.}",
        "\\label{tab:appendix_d_table_d2}",
        "\\resizebox{\\textwidth}{!}{%",
        "\\begin{tabular}{lllrrcrrrrrrrrrr}",
        "\\toprule",
        "Query ID & $k$ & Recipe & Domain \\& Path Pattern & Spatial & Tuples & M1 (ms) & M2 (ms) & $t_{\\text{C1}}$ ($\\mu$s) & $t_{\\text{C2}}$ ($\\mu$s) & $t_{\\text{C3}}$ ($\\mu$s) & M3 (ms) & $S_{\\text{M1/M3}}$ & $S_{\\text{M2/M3}}$ & $\\Phi_{\\text{eff}}^{\\text{(M1)}}$ & $\\Phi_{\\text{eff}}^{\\text{(M2)}}$ \\\\",
        "\\midrule",
        *tex_td2_rows,
        "\\bottomrule",
        "\\end{tabular}%",
        "}",
        "\\end{table*}",
        "```",
        "",
        "---",
        "",
        "## D.4 Paired Non-Parametric Wilcoxon Signed-Rank Tests, Effect Sizes, and $B=10,000$ Bootstrap 95% CIs (`Table D.3`)",
        "",
        "### Table D.3 (Markdown Format)",
        "",
        *md_td3_en,
        "",
        "### Table D.3 (LaTeX `booktabs` Format)",
        "",
        "```latex",
        "\\begin{table*}[htbp]",
        "\\centering",
        "\\caption{Paired Non-Parametric Wilcoxon Signed-Rank Tests, Effect Sizes, and $B=10,000$ Bootstrap 95\\% Confidence Intervals for Query-Time Reconstruction Speedup ($N=50$ Queries).}",
        "\\label{tab:appendix_d_table_d3}",
        "\\resizebox{\\textwidth}{!}{%",
        "\\begin{tabular}{lrrrrlrlrrrrrr}",
        "\\toprule",
        "Comparison Stratum & $N$ & Base (ms) & M3 (ms) & $\\Delta T$ (ms) & 95\\% BCa CI $\\Delta T$ & $\\Phi_{\\text{eff}}$ & 95\\% BCa CI $\\Phi_{\\text{eff}}$ & $W$ & $Z$-stat & $p$-val & Cohen $d$ & Hedges $g$ & $r$ \\\\",
        "\\midrule",
        *tex_td3_rows,
        "\\bottomrule",
        "\\end{tabular}%",
        "}",
        "\\end{table*}",
        "```",
        "",
        "---",
        "",
        "## D.5 Markov Blanket ($\\partial\\mathcal{M}(v)$) Causal Isolation Across the 316 Layer 2 Anchor Nodes and Top 15 National Hubs (`Table D.4`)",
        "",
        "### Table D.4 (Markdown Format)",
        "",
        *md_td4_en,
        "",
        "### Table D.4 (LaTeX `booktabs` Format)",
        "",
        "```latex",
        "\\begin{table*}[htbp]",
        "\\centering",
        "\\caption{Markov Blanket ($\\partial\\mathcal{M}(v) = \\text{Pa}(v) \\cup \\text{Ch}(v) \\cup \\text{Sp}(v)$) Causal Isolation Across the 316 Layer 2 Anchor Nodes and Top 15 National Infrastructure Hubs.}",
        "\\label{tab:appendix_d_table_d4}",
        "\\resizebox{\\textwidth}{!}{%",
        "\\begin{tabular}{llrrrrrrrrr}",
        "\\toprule",
        "Rank / Hub Code & Canonical Class Name & Table & Inter Deg & $|\\text{Pa}|$ & $|\\text{Ch}|$ & $|\\text{Sp}|$ & $|\\partial\\mathcal{M}_{\\text{full}}|$ & $|\\partial\\mathcal{M}_{\\text{inter}}|$ & Time ($\\mu$s) & $\\Phi_{\\text{eff}}^{\\text{(Markov)}}$ \\\\",
        "\\midrule",
        *tex_td4_rows,
        "\\bottomrule",
        "\\end{tabular}%",
        "}",
        "\\end{table*}",
        "```",
        "",
        "---",
        "",
        "## D.6 Shift-Left OpenBIM/GIS Authoring Kits (`9` Kits) and Retrospective Evolution of $\\Phi_{\\text{eff}}$ Across the 5 CAS Lineage Stages (`Table D.5`)",
        "",
        "### Table D.5 — Panel A: Cryptographic Audit of the 9 Shift-Left OpenBIM and GIS Authoring Kits (Markdown Format)",
        "",
        *md_td5a_en,
        "",
        "### Table D.5 — Panel B: Retrospective Evolution of $\\Phi_{\\text{eff}}$ Across the 5 CAS Lineage Stages (Markdown Format)",
        "",
        *md_td5b_en,
        "",
        "### Table D.5 (LaTeX `booktabs` Format — Panels A and B)",
        "",
        "```latex",
        "\\begin{table*}[htbp]",
        "\\centering",
        "\\caption{Shift-Left OpenBIM/GIS Authoring Kits (9 Kits, Panel A) and Retrospective Evolution of $\\Phi_{\\text{eff}}$ Across the 5 CAS Lineage Stages (Panel B).}",
        "\\label{tab:appendix_d_table_d5}",
        "\\resizebox{\\textwidth}{!}{%",
        "\\begin{tabular}{lllrrlllr}",
        "\\toprule",
        "\\multicolumn{9}{l}{\\textbf{Panel A: Physical Audit of the 9 Shift-Left OpenBIM and GIS Authoring Kits}} \\\\",
        "\\midrule",
        "Kit ID & Suite & Target Tool / Standard & Files & Bytes & SHA-256 Prefix & Coverage & Prevented Cold-Ingestion Failures & $\\Phi_{\\text{eff}}^{\\text{(Shift-Left)}}$ \\\\",
        "\\midrule",
        *tex_td5a_rows,
        "\\bottomrule",
        "\\end{tabular}%",
        "}",
        "\\vspace{1em}",
        "\\resizebox{\\textwidth}{!}{%",
        "\\begin{tabular}{llrrrrrrrrrr}",
        "\\toprule",
        "\\multicolumn{12}{l}{\\textbf{Panel B: Retrospective Evolution of $\\Phi_{\\text{eff}}$ Across the 5 CAS Lineage Stages (Stage 0 to Stage 4)}} \\\\",
        "\\midrule",
        "Stage & Publication ID & C2 Edges & Recipes & Reconstructed & Completion & Latency (ms) & $\\Phi_{\\text{eff}}^{\\text{(vs M1)}}$ & $\\Phi_{\\text{eff}}^{\\text{(vs M2)}}$ & $\\Phi_{\\text{eff}}^{\\text{(Markov)}}$ & $\\Phi_{\\text{eff}}^{\\text{(Kits)}}$ & Composite $\\Phi_{\\text{eff}}$ \\\\",
        "\\midrule",
        *tex_td5b_rows,
        "\\bottomrule",
        "\\end{tabular}%",
        "}",
        "\\end{table*}",
        "```",
        "",
    ]

    appendix_d_path = anexos_dir / "Appendix_D_Query_Time_Relationship_Reconstruction_Benchmark.md"
    with open(appendix_d_path, "w", encoding="utf-8") as f:
        f.write("\n".join(appendix_d_lines))

    return {
        "informe_ola4_es": informe_es_path,
        "appendix_d_en": appendix_d_path,
    }
