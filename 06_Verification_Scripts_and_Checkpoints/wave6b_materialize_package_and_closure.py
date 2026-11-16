#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SITI ITcon Q1 Reproducibility Suite — Wave 6B of 7: Programmatic Materialization of
Manuscript Tables 1–8 (.csv, .md, .tex), Supplementary Appendix F, Cross-Deliverable
Verification Gate (G-SYNC-TABLE), and Wave 6 Final Checkpoint Closure.
"""

from __future__ import annotations

import csv
import datetime
import hashlib
import io
import json
import os
import statistics
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any, Dict, List, Sequence, Set, Tuple

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

SCRIPT_PATH = Path(__file__).resolve()
SCRIPTS_DIR = SCRIPT_PATH.parent
OLA6_DIR = SCRIPTS_DIR.parent
DATOS_OLA6_DIR = OLA6_DIR / "datos"
TABLAS_ITCON_DIR = OLA6_DIR / "tablas_manuscrito_itcon"
EXP_ROOT = OLA6_DIR.parent
ANEXOS_ITCON_DIR = EXP_ROOT / "anexos_oficiales_itcon"
CHECKPOINTS_DIR = EXP_ROOT / "checkpoints"
WORKSPACE_ROOT = EXP_ROOT.parents[1]
FASE_ACTIVA_DIR = WORKSPACE_ROOT / "Fase_activa_nueva"
SITI_DIR = FASE_ACTIVA_DIR / "SITI"

for _p in (
    str(SCRIPTS_DIR),
    str(SITI_DIR),
    str(SITI_DIR / "backend"),
    str(SITI_DIR / "capa1_ontologia"),
    str(SITI_DIR / "capa3_data_layer"),
    str(SITI_DIR / "pruebas_y_auditoria"),
):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wave6_longitudinal_sii_dirichlet_archetypes import (  # noqa: E402
    file_meta_rdonly,
    read_bytes_rdonly,
    read_json_rdonly,
    read_parquet_rdonly,
    verify_master_contract_for_ola6b,
    write_csv_and_parquet,
    write_json_fsync,
)
from wave6_report_generators import (  # noqa: E402
    compute_file_meta_rdonly,
    generate_8_manuscript_tables,
    generate_appendix_f_and_master_spanish_report,
    verify_g_sync_table_all_deliverables,
)
from siti_ast_anti_theater_gate import SitiAstAntiTheaterGate  # noqa: E402
from siti_publication import verify_three_layer_architectural_invariants  # noqa: E402
from siti_semantic_consumers import get_registry  # noqa: E402
from siti_unified_dashboard import UNIFIED_DASHBOARD  # noqa: E402

EXPECTED_REB08_RESOLUTION = (
    "Integrated 4 ANI rail corridors (1,502.7 km main / 1,634.9 km network, 914 mm gauge), "
    "IfcVehicle rolling stock (B30_015_020), AASHTO TAM (B50_030), and airports"
)
EXPECTED_MACRO_REGIME_KEYS = [
    "V1_EFFECTIVE",
    "V1_CONDITIONAL",
    "V2_SQL",
    "V3_RAW603",
    "V4_COMPOSITE",
]


# =============================================================================
# ÍNDICE DE ADYACENCIA EN RAM DE C2 Y VALIDADORES EN VIVO (CERO FUSE NOISE)
# =============================================================================
def build_c2_ram_index(c2_doc: Dict[str, Any]) -> Dict[str, Any]:
    """Construye en memoria el índice de adyacencia de C2 (16.232 nodos, 17.021 aristas)."""
    code_by_uuid: Dict[str, str] = {}
    nodes_by_code: Dict[str, Dict[str, Any]] = {}
    for n in c2_doc.get("nodes", []):
        c = str(n.get("codigoSITI") or n.get("code") or "")
        u = str(n.get("uuid") or "")
        if c:
            nodes_by_code[c] = n
        if u and c:
            code_by_uuid[u] = c

    parents_by_code: Dict[str, Set[str]] = {}
    children_by_code: Dict[str, Set[str]] = {}
    intertab_parents_by_target: Dict[str, Set[str]] = {}

    for e in c2_doc.get("edges", []):
        if e.get("type") == "SUBCLASE_DE":
            src_code = code_by_uuid.get(str(e.get("source") or ""), "")
            tgt_code = code_by_uuid.get(str(e.get("target") or ""), "")
            if src_code and tgt_code:
                parents_by_code.setdefault(src_code, set()).add(tgt_code)
                children_by_code.setdefault(tgt_code, set()).add(src_code)
        else:
            src = str(e.get("source_code") or "")
            tgt = str(e.get("target_code") or "")
            if src and tgt:
                parents_by_code.setdefault(tgt, set()).add(src)
                children_by_code.setdefault(src, set()).add(tgt)
                intertab_parents_by_target.setdefault(tgt, set()).add(src)

    recipes_map = {
        r["recipe_id"]: r
        for r in (c2_doc.get("intertabular_recipes") or c2_doc.get("assembly_recipes") or [])
    }

    return {
        "nodes_by_code": nodes_by_code,
        "parents_by_code": parents_by_code,
        "children_by_code": children_by_code,
        "intertab_parents_by_target": intertab_parents_by_target,
        "recipes_map": recipes_map,
        "total_nodes": len(c2_doc.get("nodes", [])),
    }


def expand_c2_markov_blanket_ram(c2_index: Dict[str, Any], target_code: str) -> List[str]:
    """
    Expande en RAM la Manta de Markov ∂M(v) = Pa(v) ∪ Ch(v) ∪ CoPa(v), reproduciendo
    exactamente la semántica de UNIFIED_DASHBOARD.compute_c2_markov_blanket sin releer disco.
    """
    if not target_code or target_code not in c2_index["nodes_by_code"]:
        raise ValueError(f"Código ancla ausente en el índice C2 en memoria: {target_code!r}")
    pa_set = c2_index["parents_by_code"].get(target_code, set())
    ch_set = c2_index["children_by_code"].get(target_code, set())
    intertab_pa = c2_index["intertab_parents_by_target"]
    copa_set: Set[str] = set()
    for ch in ch_set:
        for cp in intertab_pa.get(ch, set()):
            if cp != target_code:
                copa_set.add(cp)
    return sorted(pa_set | ch_set | copa_set)


def validate_archetype_latency_regime(
    archetype_rows: Sequence[Dict[str, Any]],
    max_mean_ms: float = 10.0,
) -> Dict[str, Any]:
    """Valida que ARCH-01..05 estén en régimen en memoria sub-ms / pocos ms y con SD < Mean."""
    if len(archetype_rows) != 5:
        raise ValueError(f"Se esperaban exactamente 5 arquetipos, recibidos: {len(archetype_rows)}")
    means: List[float] = []
    sds: List[float] = []
    for r in archetype_rows:
        aid = str(r.get("archetype_id", ""))
        m = float(r["latency_mean_ms"])
        s = float(r["latency_sd_ms"])
        if m <= 0.0 or m >= max_mean_ms:
            raise ValueError(f"Latencia media fuera de régimen en memoria en {aid}: {m:.4f} ms (límite {max_mean_ms} ms)")
        if s < 0.0 or s >= m:
            raise ValueError(f"Ruido espurio detectado en {aid}: latency_sd_ms ({s:.4f}) >= latency_mean_ms ({m:.4f})")
        means.append(m)
        sds.append(s)
    return {
        "archetypes_verified": len(archetype_rows),
        "global_mean_latency_ms": round(float(statistics.mean(means)), 4),
        "max_mean_latency_ms": round(max(means), 4),
        "all_sd_lt_mean": True,
    }


def validate_macro_regime_trajectory_rows(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Verifica las 5 filas iniciales de trayectoria macro (V1..V4) sin ceros espurios + 47 + 50 unidades."""
    if len(rows) != 102:
        raise ValueError(f"Se esperaban 102 filas (5 macro + 47 Panel A + 50 Panel B), encontradas: {len(rows)}")
    macro_rows = list(rows[:5])
    keys = [str(r.get("unit_key", "")) for r in macro_rows]
    if keys != EXPECTED_MACRO_REGIME_KEYS:
        raise ValueError(f"Claves macro inesperadas: {keys} != {EXPECTED_MACRO_REGIME_KEYS}")

    numeric_cols = (
        "sii_s0_pct",
        "sii_s1_pct",
        "sii_s2_pct",
        "sii_s3_pct",
        "sii_s4_pct",
        "delta_sii_s0_s4_pp",
        "sii_s4_design_pct",
    )
    for r in macro_rows:
        uk = str(r["unit_key"])
        for col in numeric_cols:
            val = float(r[col])
            if val <= 0.0:
                raise ValueError(f"Valor nulo/cero espurio detectado en fila macro {uk}.{col} = {val}")
        s_chain = [float(r[f"sii_s{i}_pct"]) for i in range(5)]
        if not (s_chain[0] < s_chain[1] < s_chain[2] < s_chain[3] < s_chain[4]):
            raise ValueError(f"Trayectoria macro no estrictamente creciente en {uk}: {s_chain}")

    panel_a_n = sum(1 for r in rows[5:] if str(r.get("cohort_type")) == "PANEL_A_47_PARTITION")
    panel_b_n = sum(1 for r in rows[5:] if str(r.get("cohort_type")) == "PANEL_B_50_MASTER")
    if panel_a_n != 47 or panel_b_n != 50:
        raise ValueError(f"Paneles alterados: Panel A={panel_a_n}, Panel B={panel_b_n}")

    return {
        "total_rows": len(rows),
        "macro_rows_verified": len(macro_rows),
        "panel_a_rows_verified": panel_a_n,
        "panel_b_rows_verified": panel_b_n,
        "zero_spurious_zeros_in_macro": True,
    }


def audit_zero_obsolete_labels_in_deliverables(
    anexos_dir: Path,
    tablas_dir: Path,
    expected_s4_sii_str: str = "96.92%",
) -> Dict[str, Any]:
    """
    Audita la ausencia total de etiquetas obsoletas ('14,000x', '<0.022 mm', '1,573.6 km')
    en las 24 tablas del manuscrito y en Appendix_C..F (así como '14,000x' y '<0.022 mm' en Appendix_A..B).
    """
    table_files = sorted(tablas_dir.glob("Table_*.*"))
    if len(table_files) != 24:
        raise ValueError(f"Se esperaban 24 archivos en {tablas_dir}, encontrados: {len(table_files)}")

    for tf in table_files:
        txt = tf.read_text(encoding="utf-8")
        for bad in ("14,000x", "<0.022 mm", "1,573.6 km"):
            if bad in txt:
                raise ValueError(f"Etiqueta obsoleta '{bad}' detectada en {tf.name}")
        if tf.name.startswith("Table_6_"):
            needle = expected_s4_sii_str.replace("%", "\\%") if tf.suffix == ".tex" else expected_s4_sii_str
            if needle not in txt:
                raise ValueError(f"Table_6 no contiene el SII canónico Stage 4 ({needle}): {tf.name}")

    app_files = sorted(anexos_dir.glob("Appendix_*.md"))
    if len(app_files) != 6:
        raise ValueError(f"Se esperaban 6 anexos oficiales en {anexos_dir}, encontrados: {len(app_files)}")

    for af in app_files:
        txt = af.read_text(encoding="utf-8")
        for bad_global in ("14,000x", "<0.022 mm"):
            if bad_global in txt:
                raise ValueError(f"Etiqueta obsoleta '{bad_global}' detectada en {af.name}")
        if af.name.startswith(("Appendix_C", "Appendix_D", "Appendix_E", "Appendix_F")):
            if "1,573.6 km" in txt:
                raise ValueError(f"Etiqueta '1,573.6 km' no unificada detectada en {af.name}")
        if af.name.startswith("Appendix_F") and expected_s4_sii_str not in txt:
            raise ValueError(f"Appendix_F no contiene el SII canónico Stage 4 ({expected_s4_sii_str})")

    return {
        "tables_checked": len(table_files),
        "appendices_checked": len(app_files),
        "zero_obsolete_labels": True,
        "canonical_stage4_sii_present": True,
    }


# =============================================================================
# STEP 1: EJECUCIÓN DE LAS CORRECCIONES 1, 2 Y 3 SOBRE datos/ (SIN PF1 NI OLA 5)
# =============================================================================
def apply_surgical_data_rectifications(master: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aplica en memoria y persiste en datos/ las correcciones 1, 2 y 3:
      1. Recronometraje en RAM (5 warmup + 25 iteraciones) de ARCH-01..ARCH-05 sobre
         índice C2 precargado en RAM y tablas Parquet de C3 precargadas en DuckDB :memory:.
      2. Unificación exacta de REB-08 a '1,502.7 km main / 1,634.9 km network, 914 mm gauge'.
      3. Reemplazo de las 5 filas MACRO_STAGE_SUMMARY con ceros por las 5 trayectorias
         completas V1_EFFECTIVE, V1_CONDITIONAL, V2_SQL, V3_RAW603 y V4_COMPOSITE.
    """
    # --- Corrección 1: Cronometraje en memoria de ARCH-01..ARCH-05 ---
    reg = get_registry(SITI_DIR, refresh=True)
    c2_doc = read_json_rdonly(SITI_DIR / "capa2_grafo_lpg/capa2_catalogo_lpg.json")
    c2_index = build_c2_ram_index(c2_doc)
    recipes_map = c2_index["recipes_map"]

    c3_parquet_sources = {
        "c3_activos": SITI_DIR / "capa3_data_layer/produccion_ani/siti_ani_activos_principales.parquet",
        "c3_apu": SITI_DIR / "capa3_data_layer/siti_apu_invias_desacoplado_ab.parquet",
        "c3_proyectos": SITI_DIR / "capa3_data_layer/produccion_ani/siti_ani_proyectos.parquet",
        "c3_ferreo_corredores": SITI_DIR / "capa3_data_layer/produccion_ani/siti_ani_corredores_ferreos.parquet",
        "c3_ferreo_rodante": SITI_DIR / "capa3_data_layer/produccion_ani/siti_ani_material_rodante_auditado.parquet",
        "c3_peajes_det": SITI_DIR / "capa3_data_layer/peajes_ani/peajes_ani_detalles_global.parquet",
        "c3_bup": SITI_DIR / "capa3_data_layer/produccion_ani/siti_ani_depreciacion_bup.parquet",
    }

    con = duckdb.connect(":memory:")
    try:
        for tbl_name, pq_path in c3_parquet_sources.items():
            arrow_tbl = pq.read_table(pa.BufferReader(read_bytes_rdonly(pq_path)))
            con.register("_tmp_arrow_src", arrow_tbl)
            con.execute(f"CREATE TEMP TABLE {tbl_name} AS SELECT * FROM _tmp_arrow_src")
            con.unregister("_tmp_arrow_src")

        nat_j = master["source_waves_summary"]["ola5"]["national_226322_jitter"]
        enu_j = master["source_waves_summary"]["ola5"]["topocentric_5011_enu_jitter"]
        pcs = master["source_waves_summary"]["ola5"]["physical_corpus_summary"]
        io_saved_pct = float(pcs["projected_soa_io_traffic_saved_pct"])

        archetypes_defs = [
            {
                "archetype_id": "ARCH-01",
                "archetype_title_en": "4G/5G Road Corridor, Traffic Lane (Calzada=Carril) & ESAL Fatigue",
                "recipes": ["REC-A-01", "REC-B-02", "REC-B-04"],
                "anchor_code": "A30_035_005_040",
                "chain_tokens": [
                    "A10_025_065_015",
                    "A20_035_005_020",
                    "A30_035_005_040",
                    "A40_045_005_030",
                    "A50_015_005_025",
                    "B30_010_030_170",
                    "B40_020_035_920",
                    "B50_010_035_005_005_035",
                ],
                "chain_a_codes": "A10_025_065_015 -> A20_035_005_020 -> A30_035_005_040 -> A40_045_005_030 -> A50_015_005_025",
                "chain_b_codes": "B30_010_030_170 | B40_020_035_920 | B50_010_035_005_005_035 (ESAL & IRI)",
                "sql_ram": """
                    SELECT
                        (SELECT COUNT(*) FROM c3_activos WHERE tabla_origen_ani IN ('calzada','berma','defensa_vial')) AS road_assets,
                        (SELECT COUNT(*) FROM c3_peajes_det) AS oetr_axle_rows,
                        (SELECT COUNT(*) FROM c3_apu WHERE a_intervened_asset_siti_code LIKE 'A40%' OR a_intervened_asset_siti_code LIKE 'A30%') AS apu_items
                """,
                "fmt_summary": lambda row: f"{int(row[0]):,} lane/shoulder/barrier assets + {int(row[1]):,} OETR ESAL axle rows + {int(row[2])} national APU items",
                "shacl_status": "SHACL IRI <= 2.5 m/km & NICSP 17 85/15 escrow verified",
            },
            {
                "archetype_id": "ARCH-02",
                "archetype_title_en": "Seismic Bridge/Viaduct (CCP-14) & Hydraulic Drainage (__occN)",
                "recipes": ["REC-A-02", "REC-A-05", "REC-B-05"],
                "anchor_code": "A40_085_005_005",
                "chain_tokens": [
                    "A10_025_065_015",
                    "A20_035_005_020",
                    "A30_035_005_070",
                    "A40_085_005_005",
                    "A50_045_005_035_005",
                    "B30_010_020_180",
                    "B40_020_035_930",
                    "B50_010_035_010_025",
                ],
                "chain_a_codes": "A10_025_065_015 -> A20_035_005_020 -> A30_035_005_070 -> A40_085_005_005 -> A50_045_005_035_005",
                "chain_b_codes": "B30_010_020_180 | B40_020_035_930 | B50_010_035_010_025",
                "sql_ram": """
                    SELECT
                        (SELECT COUNT(*) FROM c3_activos WHERE tabla_origen_ani = 'puente') AS bridges,
                        (SELECT COUNT(*) FROM c3_activos WHERE tabla_origen_ani IN ('cuneta','drenajes')) AS drainage_assets,
                        (SELECT COUNT(*) FROM c3_bup) AS bup_rows
                """,
                "fmt_summary": lambda row: f"{int(row[0]):,} bridges/viaducts + {int(row[1]):,} drainage assets (179 A50_045 __occN classes) + {int(row[2]):,} BUP records",
                "shacl_status": "SHACL structural clearance & NICSP 17 componentized BUP verified",
            },
            {
                "archetype_id": "ARCH-03",
                "archetype_title_en": "Road Tunnel, Electromechanical Ventilation & Electronic Toll/ITS",
                "recipes": ["REC-A-03", "REC-A-06", "REC-B-06"],
                "anchor_code": "A30_035_010_015",
                "chain_tokens": [
                    "A10_025_065_015",
                    "A20_035_005_020",
                    "A30_035_005_075",
                    "A40_065_005_075",
                    "A50_035_035_010",
                    "B30_015_015_040",
                    "B40_025_005_025",
                    "B50_035_055",
                ],
                "chain_a_codes": "A10_025_065_015 -> A20_035_005_020 -> A30_035_005_075 -> A40_065_005_075 -> A50_035_035_010",
                "chain_b_codes": "B30_015_015_040 | B40_025_005_025 | B50_035_055 (IP/REV & WIM)",
                "sql_ram": """
                    SELECT
                        (SELECT COUNT(*) FROM c3_activos WHERE tabla_origen_ani = 'dispositivo_its') AS its_devices,
                        (SELECT COUNT(*) FROM c3_activos WHERE tabla_origen_ani = 'luminarias') AS luminaires,
                        (SELECT COUNT(*) FROM c3_activos WHERE tabla_origen_ani = 'estacion_peaje') AS toll_plazas
                """,
                "fmt_summary": lambda row: f"{int(row[0]):,} ITS devices + {int(row[1]):,} luminaires + {int(row[2])} Colpass/WIM toll stations",
                "shacl_status": "SHACL AT4 availability/retroreflectivity & ISO 19650 CDE verified",
            },
            {
                "archetype_id": "ARCH-04",
                "archetype_title_en": "Narrow-Gauge Railway Corridor (914 mm) & Rolling Stock (IfcVehicle)",
                "recipes": ["REC-A-04", "REC-A-07"],
                "anchor_code": "A30_015_075",
                "chain_tokens": [
                    "A10_025_065_015",
                    "A20_040_070_010",
                    "A30_015_075",
                    "A40_140_010",
                    "A50_050_060_010",
                    "B30_015_020",
                    "B40_025_005_015",
                    "B50_010_015_015_005",
                ],
                "chain_a_codes": "A10_025_065_015 -> A20_040_070_010 -> A30_015_075 -> A40_140_010 -> A50_050_060_010",
                "chain_b_codes": "B30_015_020 (IfcVehicle) | B40_025_005_015 | B50_010_015_015_005",
                "sql_ram": """
                    SELECT
                        (SELECT COUNT(*) FROM c3_ferreo_corredores) AS rail_corridors,
                        (SELECT ROUND(SUM(longitud_corredor_principal_km), 1) FROM c3_ferreo_corredores) AS rail_main_km,
                        (SELECT ROUND(SUM(longitud_total_red_ramales_km), 1) FROM c3_ferreo_corredores) AS rail_total_km,
                        (SELECT COUNT(*) FROM c3_ferreo_rodante) AS rolling_stock
                """,
                "fmt_summary": lambda row: f"{int(row[0])} ANI rail corridors ({float(row[1]):,.1f} km main / {float(row[2]):,.1f} km network, 914 mm gauge) + {int(row[3])} audited rolling-stock units",
                "shacl_status": "SHACL allValuesFrom modal gauge (914 mm) & rolling-stock decoupled",
            },
            {
                "archetype_id": "ARCH-05",
                "archetype_title_en": "Concessioned Airport Terminal, Airside Pavement & Land Release",
                "recipes": ["REC-A-07", "REC-B-01", "REC-B-03"],
                "anchor_code": "A20_020_005",
                "chain_tokens": [
                    "A10_005_005",
                    "A20_020_005",
                    "A30_015_075",
                    "A40_090_005",
                    "A50_050_060_010",
                    "B20_025_005_00024",
                    "B40_010_020_015",
                    "B50_025_005",
                ],
                "chain_a_codes": "A10_005_005 -> A20_020_005 -> A30_015_075 -> A40_090_005 -> A50_050_060_010",
                "chain_b_codes": "B20_025_005_00024 (ANI) | B40_010_020_015 | B50_025_005 (PDET/ZOMAC)",
                "sql_ram": """
                    SELECT
                        (SELECT COUNT(*) FROM c3_proyectos WHERE LOWER(modo) LIKE '%aerop%') AS air_concessions,
                        (SELECT COUNT(*) FROM c3_activos WHERE tabla_origen_ani = 'predio') AS cadastre_parcels,
                        (SELECT COUNT(*) FROM c3_proyectos) AS total_ani_concessions
                """,
                "fmt_summary": lambda row: f"{int(row[0])} airport concessions (within {int(row[2])} ANI master projects) + {int(row[1]):,} AT7 cadastral parcels",
                "shacl_status": "SHACL PBAC/ABAC spatial geofence & AT7 cadastral reversibility verified",
            },
        ]

        prev_arch_by_id = {
            r["archetype_id"]: r
            for r in master["experiment_6_3_identity_pf1_pf5_and_5_archetypes"]["five_handover_archetypes"]
        }

        updated_archetypes: List[Dict[str, Any]] = []
        for arch in archetypes_defs:
            # Verification única fuera del bucle cronometrado contra UNIFIED_DASHBOARD
            ref_mb = UNIFIED_DASHBOARD.compute_c2_markov_blanket({"code": arch["anchor_code"]})
            ref_card = int(ref_mb["markov_blanket"]["blanket_cardinality"])
            ram_codes_check = expand_c2_markov_blanket_ram(c2_index, arch["anchor_code"])
            if len(ram_codes_check) != ref_card:
                raise AssertionError(
                    f"Discrepancia de Manta de Markov en {arch['archetype_id']}: "
                    f"RAM={len(ram_codes_check)} vs Dashboard={ref_card}"
                )

            # 5 iteraciones de calentamiento en memoria
            for _ in range(5):
                _ = reg.lookup(arch["anchor_code"])
                _ = [reg.lookup(tok) for tok in arch["chain_tokens"]]
                _ = [recipes_map[rid] for rid in arch["recipes"] if rid in recipes_map]
                _ = expand_c2_markov_blanket_ram(c2_index, arch["anchor_code"])
                _ = con.execute(arch["sql_ram"]).fetchone()

            # 25 iteraciones medidas con time.perf_counter_ns() para R_Q = Pi_C3 o Gamma_C2 o Sigma_C1
            samples_ms: List[float] = []
            mb_codes: List[str] = []
            sql_row: Tuple[Any, ...] = ()
            for _ in range(25):
                t_ns = time.perf_counter_ns()
                c1_anchor = reg.lookup(arch["anchor_code"])
                if c1_anchor is None:
                    raise AssertionError(f"Ancla C1 no encontrada: {arch['anchor_code']}")
                _ = [reg.lookup(tok) for tok in arch["chain_tokens"]]
                _ = [recipes_map[rid] for rid in arch["recipes"] if rid in recipes_map]
                mb_codes = expand_c2_markov_blanket_ram(c2_index, arch["anchor_code"])
                sql_row = con.execute(arch["sql_ram"]).fetchone()
                samples_ms.append((time.perf_counter_ns() - t_ns) / 1e6)

            mb_card = len(mb_codes)
            mb_iso_pct = round(100.0 * (1.0 - mb_card / 16232.0), 4)
            summary_str = arch["fmt_summary"](sql_row)
            prev_summary = prev_arch_by_id[arch["archetype_id"]]["c3_reconstructed_summary_en"]
            if summary_str != prev_summary:
                raise AssertionError(
                    f"Paridad de tuplas alterada en {arch['archetype_id']}: {summary_str!r} != {prev_summary!r}"
                )

            updated_archetypes.append(
                {
                    "archetype_id": arch["archetype_id"],
                    "archetype_title_en": arch["archetype_title_en"],
                    "recipes_str": " + ".join(arch["recipes"]),
                    "anchor_code": arch["anchor_code"],
                    "chain_a_codes": arch["chain_a_codes"],
                    "chain_b_codes": arch["chain_b_codes"],
                    "markov_blanket_size": mb_card,
                    "markov_isolation_pct": mb_iso_pct,
                    "c3_reconstructed_summary_en": summary_str,
                    "latency_mean_ms": round(float(statistics.mean(samples_ms)), 4),
                    "latency_sd_ms": round(float(statistics.stdev(samples_ms)), 4),
                    "io_saved_vs_coupled_pct": round(io_saved_pct, 4),
                    "direct_f32_mean_mm": round(float(nat_j["direct_f32_mean_mm"]), 4),
                    "bimodal_enu_mean_mm": round(float(enu_j["bimodal_enu_mean_mm"]), 4),
                    "jitter_gain_x": round(float(enu_j["error_reduction_factor_x"]), 2),
                    "shacl_and_nicsp17_status_en": arch["shacl_status"],
                }
            )
    finally:
        con.close()

    validate_archetype_latency_regime(updated_archetypes, max_mean_ms=10.0)

    # Persistir wave6_5_national_handover_archetypes_end_to_end.csv y .json preservando PF1/PF5 intactos
    write_csv_and_parquet(
        updated_archetypes,
        DATOS_OLA6_DIR / "wave6_5_national_handover_archetypes_end_to_end.csv",
        parquet_path=None,
    )
    traz_json = read_json_rdonly(DATOS_OLA6_DIR / "wave6_5_national_handover_archetypes_end_to_end.json")
    traz_json["five_handover_archetypes"] = updated_archetypes
    write_json_fsync(traz_json, DATOS_OLA6_DIR / "wave6_5_national_handover_archetypes_end_to_end.json")
    master["experiment_6_3_identity_pf1_pf5_and_5_archetypes"]["five_handover_archetypes"] = updated_archetypes

    # --- Corrección 2: Unificar al decimal REB-08 con ARCH-04 y Table 1 ---
    reb_found = False
    for rr in master["paper1_vs_paper2_rebuttal_rows"]:
        if rr.get("rebuttal_id") == "REB-08":
            rr["paper2_resolution_en"] = EXPECTED_REB08_RESOLUTION
            reb_found = True
    if not reb_found:
        raise AssertionError("No se encontró la fila REB-08 en paper1_vs_paper2_rebuttal_rows")

    # --- Corrección 3: Reemplazar las 5 filas MACRO_STAGE_SUMMARY por los 5 regímenes completos ---
    existing_sii_rows = read_parquet_rdonly(DATOS_OLA6_DIR / "wave6_sii_evolution_5_stages_and_50_concessions.parquet")
    unit_rows_preserved = [
        r for r in existing_sii_rows if str(r.get("cohort_type")) in ("PANEL_A_47_PARTITION", "PANEL_B_50_MASTER")
    ]
    by_st = master["experiment_6_1_longitudinal_sii"]["by_stage_summary"]
    macro_regimes_spec = [
        (
            "V1_EFFECTIVE",
            "Strict Primary Empirical SII — Effective vs. M1 Monolithic RDF (Canonical)",
            "sii_v1_eff_equal_pct",
            "sii_v1_eff_design_pct",
        ),
        (
            "V1_CONDITIONAL",
            "Strict Primary Empirical SII — Conditional on Completed Queries vs. M1 RDF",
            "sii_v1_cond_equal_pct",
            "sii_v1_cond_design_pct",
        ),
        (
            "V2_SQL",
            "Strict Primary Empirical SII — Effective vs. M2 Coupled Row-SQL AoS",
            "sii_v2_eff_equal_pct",
            "sii_v2_eff_design_pct",
        ),
        (
            "V3_RAW603",
            "Cold-Ingestion Inclusive SII — Raw 603 CDE Receipts (Phi_ont = 97.97%)",
            "sii_v3_raw603_equal_pct",
            "sii_v3_raw603_design_pct",
        ),
        (
            "V4_COMPOSITE",
            "Comprehensive Multi-Submetric Composite SII (All Dimension Submetrics)",
            "sii_v4_comp_equal_pct",
            "sii_v4_comp_design_pct",
        ),
    ]
    new_macro_rows: List[Dict[str, Any]] = []
    for reg_key, reg_name_en, eq_col, ds_col in macro_regimes_spec:
        s0_v = float(by_st["S0"][eq_col])
        s4_v = float(by_st["S4"][eq_col])
        new_macro_rows.append(
            {
                "cohort_type": "MACRO_REGIME_TRAJECTORY",
                "unit_key": reg_key,
                "project_id": -1,
                "unit_name": reg_name_en,
                "mode_and_phase": "National 3-Layer CAS Trajectory (S0..S4)",
                "asset_count": 226324,
                "distinct_layers": 21,
                "sii_s0_pct": round(s0_v, 4),
                "sii_s1_pct": round(float(by_st["S1"][eq_col]), 4),
                "sii_s2_pct": round(float(by_st["S2"][eq_col]), 4),
                "sii_s3_pct": round(float(by_st["S3"][eq_col]), 4),
                "sii_s4_pct": round(s4_v, 4),
                "delta_sii_s0_s4_pp": round(s4_v - s0_v, 4),
                "sii_s4_design_pct": round(float(by_st["S4"][ds_col]), 4),
            }
        )

    rectified_sii_rows = new_macro_rows + unit_rows_preserved
    validate_macro_regime_trajectory_rows(rectified_sii_rows)
    write_csv_and_parquet(
        rectified_sii_rows,
        DATOS_OLA6_DIR / "wave6_sii_evolution_5_stages_and_50_concessions.csv",
        DATOS_OLA6_DIR / "wave6_sii_evolution_5_stages_and_50_concessions.parquet",
    )

    return master


def collect_all_waves_inventory_rdonly() -> List[Dict[str, Any]]:
    """Recopila el inventario criptográfico completo (size_bytes, st_blocks, sha256) de las Olas 1 a 6."""
    wave_prefixes = [
        ("OLA_1", EXP_ROOT / "01_ola1_censo_masivo_y_bundles"),
        ("OLA_2", EXP_ROOT / "02_ola2_desacoplamiento_ab_phi_ont"),
        ("OLA_3", EXP_ROOT / "03_ola3_entropia_shannon_skos_phi_sem"),
        ("OLA_4", EXP_ROOT / "04_ola4_reconstruccion_query_time_phi_eff"),
        ("OLA_5", EXP_ROOT / "05_ola5_separacion_geometria_vs_operacion_soa"),
        ("OLA_6", EXP_ROOT / "06_ola6_evolucion_longitudinal_sii_y_paquete_itcon"),
        ("ANEXOS_ITCON", ANEXOS_ITCON_DIR),
        ("CHECKPOINTS", CHECKPOINTS_DIR),
    ]
    inventory: List[Dict[str, Any]] = []
    for wave_lbl, folder in wave_prefixes:
        if not folder.exists():
            continue
        for p in sorted(folder.rglob("*")):
            if not p.is_file():
                continue
            if "__pycache__" in p.parts or p.name.startswith(".") or p.suffix == ".pyc":
                continue
            if p.name in ("wave6_master_experiment_sha256_log.md", "wave6_final_checkpoint.json"):
                continue
            meta = compute_file_meta_rdonly(p)
            inventory.append(
                {
                    "wave": wave_lbl,
                    "rel_path": p.relative_to(WORKSPACE_ROOT).as_posix(),
                    "size_bytes": meta["size_bytes"],
                    "st_blocks": meta["st_blocks"],
                    "sha256": meta["sha256"],
                }
            )
    return inventory


# =============================================================================
# SUITE UNITTEST BIPOLAR EN VIVO DE 3 PRUEBAS (AUDITADA POR SitiAstAntiTheaterGate)
# =============================================================================
class TestOla6bManuscriptDeliverablesBipolar(unittest.TestCase):
    """
    3 pruebas bipolares en vivo sin lecturas estáticas json.load / json.loads:
      1. Sincronización .csv == .md == .tex de las 8 tablas y ausencia de etiquetas obsoletas.
      2. Ausencia total de ceros espurios (0.0) en las 5 filas macro de evolucion_sii_5_etapas_y_50_concesiones.
      3. Coherencia de latencias en memoria (SD < Mean, sub-ms/pocos ms) y Manta de Markov de ARCH-01..05.
    """

    def test_01_manuscript_8_tables_csv_md_tex_sync_bipolar(self) -> None:
        sync_res = verify_g_sync_table_all_deliverables(
            anexos_dir=ANEXOS_ITCON_DIR,
            tablas_dir=TABLAS_ITCON_DIR,
            expected_stage4_v1_sii_str="96.92%",
            expected_enu_gain_str="25,697x Gain",
        )
        obs_res = audit_zero_obsolete_labels_in_deliverables(
            anexos_dir=ANEXOS_ITCON_DIR,
            tablas_dir=TABLAS_ITCON_DIR,
            expected_s4_sii_str="96.92%",
        )
        self.assertTrue(sync_res["all_6_appendices_synced_and_nonempty"])
        self.assertTrue(sync_res["all_8_tables_24_files_synced_and_nonempty"])
        self.assertEqual(sync_res["manuscript_table_files_count"], 24)
        self.assertTrue(obs_res["zero_obsolete_labels"])

        with tempfile.TemporaryDirectory(prefix="siti_ola6b_trap_sync_") as tmp_d:
            tmp_tablas = Path(tmp_d) / "tablas"
            tmp_tablas.mkdir(parents=True, exist_ok=True)
            bad_stem = "Table_1_Master_Corpus_and_Denominators"
            (tmp_tablas / f"{bad_stem}.csv").write_text("col1,col2\na,1\nb,2\n", encoding="utf-8")
            (tmp_tablas / f"{bad_stem}.md").write_text("| col1 | col2 |\n| --- | --- |\n| a | 1 |\n", encoding="utf-8")
            (tmp_tablas / f"{bad_stem}.tex").write_text("\\toprule\n\\textbf{col1} \\\\\n\\midrule\na & 1 \\\\\n\\bottomrule\n", encoding="utf-8")
            with self.assertRaises((AssertionError, FileNotFoundError)):
                verify_g_sync_table_all_deliverables(
                    anexos_dir=ANEXOS_ITCON_DIR,
                    tablas_dir=tmp_tablas,
                    expected_stage4_v1_sii_str="96.92%",
                    expected_enu_gain_str="25,697x Gain",
                )

    def test_02_macro_regime_rows_zero_spurious_zeros_bipolar(self) -> None:
        sii_rows = read_parquet_rdonly(DATOS_OLA6_DIR / "wave6_sii_evolution_5_stages_and_50_concessions.parquet")
        val_info = validate_macro_regime_trajectory_rows(sii_rows)
        self.assertEqual(val_info["total_rows"], 102)
        self.assertEqual(val_info["macro_rows_verified"], 5)
        self.assertTrue(val_info["zero_spurious_zeros_in_macro"])

        corrupted_rows = [dict(r) for r in sii_rows]
        corrupted_rows[0]["sii_s1_pct"] = 0.0
        with self.assertRaises(ValueError):
            validate_macro_regime_trajectory_rows(corrupted_rows)

    def test_03_arch01_to_05_in_memory_latency_coherence_bipolar(self) -> None:
        arch_csv_path = DATOS_OLA6_DIR / "wave6_5_national_handover_archetypes_end_to_end.csv"
        with open(arch_csv_path, "r", encoding="utf-8", newline="") as f:
            arch_rows = list(csv.DictReader(f))
        lat_audit = validate_archetype_latency_regime(arch_rows, max_mean_ms=10.0)
        self.assertEqual(lat_audit["archetypes_verified"], 5)
        self.assertTrue(lat_audit["all_sd_lt_mean"])
        self.assertLess(lat_audit["max_mean_latency_ms"], 10.0)

        fake_c2 = build_c2_ram_index(
            {
                "nodes": [{"codigoSITI": "A30_035_005_040", "uuid": "u1"}, {"codigoSITI": "A40_045_005_030", "uuid": "u2"}],
                "edges": [{"type": "TIENE_ELEMENTO", "source_code": "A30_035_005_040", "target_code": "A40_045_005_030"}],
            }
        )
        mb_live = expand_c2_markov_blanket_ram(fake_c2, "A30_035_005_040")
        self.assertIn("A40_045_005_030", mb_live)

        fuse_spike_rows = [dict(r) for r in arch_rows]
        fuse_spike_rows[3]["latency_mean_ms"] = 184.3809
        fuse_spike_rows[3]["latency_sd_ms"] = 502.1898
        with self.assertRaises(ValueError):
            validate_archetype_latency_regime(fuse_spike_rows, max_mean_ms=10.0)
        with self.assertRaises(ValueError):
            expand_c2_markov_blanket_ram(fake_c2, "CODIGO_INEXISTENTE_999")


# =============================================================================
# ORQUESTACIÓN PRINCIPAL DE LA OLA 6B Y SELLO DEFINITIVO DEL ARNÉS DE 6 OLAS
# =============================================================================
def main() -> None:
    t0 = time.perf_counter()

    # Guardián estricto de inmutabilidad sobre producción, bundles, Kits y Olas 1..5 selladas
    immutable_targets = [
        SITI_DIR / "capa1_ontologia/capa1_siti_ontology.ttl",
        SITI_DIR / "capa1_ontologia/capa1_shacl_shapes.ttl",
        SITI_DIR / "capa2_grafo_lpg/capa2_catalogo_lpg.json",
        SITI_DIR / "capa3_data_layer/produccion_ani/siti_ani_activos_principales.parquet",
        SITI_DIR / "capa3_data_layer/produccion_ani/assets_spatial_instances_ani.parquet",
        FASE_ACTIVA_DIR / "Kits_GIS/QGIS/SITI_Plantilla_Oficial_MAGNA9377.gpkg",
        *(CHECKPOINTS_DIR / f"checkpoint_itcon_ola{i}.json" for i in range(1, 6)),
        ANEXOS_ITCON_DIR / "Appendix_A_Three_Layer_Corpus_and_CAS_Lineage.md",
        ANEXOS_ITCON_DIR / "Appendix_B_Orthogonal_AB_Decoupling_and_Phi_Ont.md",
        ANEXOS_ITCON_DIR / "Appendix_C_Shannon_Entropy_SKOS_and_Phi_Sem.md",
        ANEXOS_ITCON_DIR / "Appendix_D_Query_Time_Relationship_Reconstruction_Benchmark.md",
        ANEXOS_ITCON_DIR / "Appendix_E_Bimodal_Geometry_vs_Unboxed_EAV_Telemetry.md",
        EXP_ROOT / "05_ola5_separacion_geometria_vs_operacion_soa/datos/wave5_geometry_vs_operation_master_summary.json",
    ]
    pre_immutable_hashes = {str(p): file_meta_rdonly(p)["sha256"] for p in immutable_targets}

    print("[OLA 6B] 1/6 Aplicando correcciones quirúrgicas 1, 2 y 3 en datos/ y validando contrato maestro...")
    master_path = DATOS_OLA6_DIR / "wave6_global_sii_master_summary.json"
    master = read_json_rdonly(master_path)

    # Auditar AST de ola6a y ola6b antes de persistir el maestro rectificado
    ola6a_script = SCRIPTS_DIR / "wave6_longitudinal_sii_dirichlet_archetypes.py"
    ast_ola6a = SitiAstAntiTheaterGate.audit_test_file(str(ola6a_script))
    ast_ola6b = SitiAstAntiTheaterGate.audit_test_file(str(SCRIPT_PATH))

    master = apply_surgical_data_rectifications(master)
    master["ast_anti_theater_audit"] = ast_ola6a
    master["ola6b_ast_anti_theater_audit"] = ast_ola6b
    master["ola6b_rectified_timestamp_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    verify_master_contract_for_ola6b(master)
    master_meta = write_json_fsync(master, master_path)

    print("[OLA 6B] 2/6 Materializando las 24 tablas oficiales del manuscrito (Table_1..8 en .csv, .md y .tex)...")
    generated_tables = generate_8_manuscript_tables(master, TABLAS_ITCON_DIR)
    for t_key, paths_map in generated_tables.items():
        for ext, p_file in paths_map.items():
            with open(p_file, "rb") as fh:
                os.fsync(fh.fileno())
            m_t = compute_file_meta_rdonly(p_file)
            if m_t["st_blocks"] <= 0 or m_t["size_bytes"] <= 0:
                raise AssertionError(f"Tabla {t_key}.{ext} sin bloques físicos en disco")

    print("[OLA 6B] 3/6 Materializando Appendix_F (EN Q1) e wave6_master_experiment_sha256_log.md (ES)...")
    # Pasada 1 para materializar Appendix_F en disco y poder incluir su SHA-256 exacto en el inventario del Informe Maestro
    _ = generate_appendix_f_and_master_spanish_report(master, OLA6_DIR, ANEXOS_ITCON_DIR, [])
    all_wave_files_inventory = collect_all_waves_inventory_rdonly()
    reports_out = generate_appendix_f_and_master_spanish_report(
        master,
        OLA6_DIR,
        ANEXOS_ITCON_DIR,
        all_wave_files_inventory,
    )
    for r_path in reports_out.values():
        with open(r_path, "rb") as fh:
            os.fsync(fh.fileno())

    print("[OLA 6B] 4/6 Auditando G-SYNC-TABLE sobre Appendix_A..F y los 24 archivos de Table_1..8...")
    s4_v1_str = f"{master['experiment_6_1_longitudinal_sii']['by_stage_summary']['S4']['sii_v1_eff_equal_pct']:.2f}%"
    enu_gain_str = f"{int(round(master['prerequisites_and_step0']['step_0_ola5_refinement']['enu_gain_factor_x'])):,}x Gain"
    gsync_audit = verify_g_sync_table_all_deliverables(
        anexos_dir=ANEXOS_ITCON_DIR,
        tablas_dir=TABLAS_ITCON_DIR,
        expected_stage4_v1_sii_str=s4_v1_str,
        expected_enu_gain_str=enu_gain_str,
    )
    obsolete_audit = audit_zero_obsolete_labels_in_deliverables(
        anexos_dir=ANEXOS_ITCON_DIR,
        tablas_dir=TABLAS_ITCON_DIR,
        expected_s4_sii_str=s4_v1_str,
    )

    print("[OLA 6B] 5/6 Ejecutando SitiAstAntiTheaterGate y la suite unittest bipolar en vivo (3 pruebas)...")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestOla6bManuscriptDeliverablesBipolar)
    buf = io.StringIO()
    runner = unittest.TextTestRunner(stream=buf, verbosity=2)
    ut_res = runner.run(suite)
    if not ut_res.wasSuccessful():
        raise AssertionError(f"Fallo en TestOla6bManuscriptDeliverablesBipolar:\n{buf.getvalue()}")

    print("[OLA 6B] 6/6 Verificando invariantes arquitectónicas tricapa (os.O_RDONLY) y sellando checkpoint final...")
    inv_report = verify_three_layer_architectural_invariants(SITI_DIR, raise_on_error=True)
    if not inv_report.get("all_invariants_satisfied"):
        raise AssertionError(f"Invariantes tricapa no satisfechas: {inv_report}")

    for p in immutable_targets:
        post_sha = file_meta_rdonly(p)["sha256"]
        if post_sha != pre_immutable_hashes[str(p)]:
            raise AssertionError(f"VIOLACIÓN DE INMUTABILIDAD detectada en {p}")

    inf_es_meta = compute_file_meta_rdonly(reports_out["informe_maestro_es"])
    ola6_data_sealed: Dict[str, Any] = {}
    for df in sorted(DATOS_OLA6_DIR.glob("*")):
        if df.is_file():
            m = compute_file_meta_rdonly(df)
            ola6_data_sealed[df.relative_to(WORKSPACE_ROOT).as_posix()] = {
                "size_bytes": m["size_bytes"],
                "st_blocks": m["st_blocks"],
                "sha256": m["sha256"],
            }
    ola6_data_sealed[reports_out["informe_maestro_es"].relative_to(WORKSPACE_ROOT).as_posix()] = {
        "size_bytes": inf_es_meta["size_bytes"],
        "st_blocks": inf_es_meta["st_blocks"],
        "sha256": inf_es_meta["sha256"],
    }

    by_st = master["experiment_6_1_longitudinal_sii"]["by_stage_summary"]
    pa_t = master["experiment_6_1_longitudinal_sii"]["paired_inferential_tests"]["panel_a_47_s0_to_s4"]
    pb_t = master["experiment_6_1_longitudinal_sii"]["paired_inferential_tests"]["panel_b_50_s0_to_s4"]
    dom_v1 = master["experiment_6_2_dirichlet_and_ablation"]["dominance_probabilities"]["V1_EFFECTIVE"]
    e63 = master["experiment_6_3_identity_pf1_pf5_and_5_archetypes"]

    final_checkpoint = {
        "checkpoint_id": "ITCON_Q1_WAVE_6_OF_7_FINAL_CLOSURE",
        "wave_id": "OLA_6_DE_6_FINAL",
        "wave_title": (
            "Cierre Definitivo del Arnés Experimental Doctoral de 6 Olas para ITcon (Q1): "
            "Síntesis Longitudinal del SII (S0..S4, V1..V4), Sensibilidad Dirichlet (B=10.000), "
            "Ablación Tricapa (Abl-1..Abl-6), Triple Identidad Disjunta, Evolución en Caliente PF1/PF5, "
            "5 Arquetipos Nacionales en RAM (ARCH-01..05), 24 Tablas Oficiales (Table_1..8), "
            "6 Anexos (Appendix_A..F) e Informe Maestro SHA-256"
        ),
        "status": "PASS",
        "active_cas_revision": master["active_cas_revision"],
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ola6b_elapsed_seconds": round(time.perf_counter() - t0, 3),
        "all_6_waves_checkpoints_status": {
            "ola1": master["prerequisites_and_step0"]["checkpoints_verified"]["ola1"],
            "ola2": master["prerequisites_and_step0"]["checkpoints_verified"]["ola2"],
            "ola3": master["prerequisites_and_step0"]["checkpoints_verified"]["ola3"],
            "ola4": master["prerequisites_and_step0"]["checkpoints_verified"]["ola4"],
            "ola5": master["prerequisites_and_step0"]["checkpoints_verified"]["ola5"],
            "ola6_final": "PASS",
        },
        "guardrails_compliance": {
            "G-PHYS_os_O_RDONLY_enforced": True,
            "G-PHYS_production_and_sealed_waves_bytes_modified": 0,
            "G-PHYS_all_artifacts_st_blocks_gt_0": True,
            "G-SYNC-TABLE_all_6_appendices_and_24_table_files_synced": True,
            "G-SYNC-TABLE_zero_obsolete_labels_14000x_0022mm_1573km": obsolete_audit["zero_obsolete_labels"],
            "G-AST_anti_theater_gate_ola6a": ast_ola6a,
            "G-AST_anti_theater_gate_ola6b": ast_ola6b,
            "G-SEM_three_layer_architectural_invariants": {
                "all_invariants_satisfied": bool(inv_report["all_invariants_satisfied"]),
                "metrics": inv_report["metrics"],
            },
        },
        "six_waves_headline_scientific_summary": {
            "wave1_corpus_and_cas": {
                "c1_active_unique_classes": 16230,
                "c1_skos_expressions": 2892,
                "c1_rdf_triples": 438194,
                "c1_owl_restrictions": 814,
                "c1_shacl_shapes": 104,
                "c2_lpg_nodes": 16232,
                "c2_intertabular_edges": 793,
                "c3_core_domain_parquets": 824,
                "c3_core_domain_rows": 2510964,
                "primary_libraries_preserved_bytes": 5765230336,
            },
            "wave2_orthogonal_ab_and_phi_ont": {
                "bipartite_compression_c1_x": 3332.96,
                "c2_deduplication_compression_x": 112.35,
                "phi_ont_core3_s0_to_s4_pct": [23.85, 42.3, 81.05, 100.0, 100.0],
                "phi_ont_raw603_s4_pct": 97.97,
                "orphan_siti_codes_in_226324_assets": 0,
            },
            "wave3_shannon_entropy_and_phi_sem": {
                "panel_a_47_h_bits_s0_to_s4": [2.8878, 1.7277, 0.7992, 0.2294, 0.1578],
                "panel_a_47_phi_sem_s0_to_s4_pct": [17.02, 50.06, 76.9, 93.37, 95.47],
                "shacl_bipolar_240_cases_f1_pct": 100.0,
            },
            "wave4_query_time_reconstruction_and_phi_eff": {
                "m3_mean_ms_50_queries": 0.705,
                "m1_mean_ms_50_queries": 14.957,
                "m2_mean_ms_50_queries": 8.286,
                "speedup_m1_vs_m3_x": 21.21,
                "speedup_m2_vs_m3_x": 11.75,
                "phi_eff_vs_m1_s4_pct": 95.29,
                "markov_blanket_mean_isolation_pct": 99.92,
            },
            "wave5_geometry_vs_operation_separation": {
                "disk_mass_asymmetry_wkb_vs_activos_x": 24.67,
                "non_spatial_io_saved_pct": 99.95,
                "unboxed_eav_ram_compression_vs_e1a_x": 244.2,
                "bimodal_enu_max_jitter_mm": 0.0123,
                "national_225244_bimodal_max_jitter_mm": 0.0131,
                "enu_precision_gain_x": 25697.39,
                "national_precision_gain_x": 26358.07,
            },
            "wave6_longitudinal_sii_dirichlet_and_archetypes": {
                "sii_v1_canonical_equal_s0_to_s4_pct": [
                    by_st[sc]["sii_v1_eff_equal_pct"] for sc in ("S0", "S1", "S2", "S3", "S4")
                ],
                "sii_v1_design_s0_to_s4_pct": [
                    by_st[sc]["sii_v1_eff_design_pct"] for sc in ("S0", "S1", "S2", "S3", "S4")
                ],
                "sii_s4_regimes_equal_pct": {
                    "V1_EFFECTIVE": by_st["S4"]["sii_v1_eff_equal_pct"],
                    "V1_CONDITIONAL": by_st["S4"]["sii_v1_cond_equal_pct"],
                    "V2_SQL": by_st["S4"]["sii_v2_eff_equal_pct"],
                    "V3_RAW603": by_st["S4"]["sii_v3_raw603_equal_pct"],
                    "V4_COMPOSITE": by_st["S4"]["sii_v4_comp_equal_pct"],
                },
                "panel_a_47_wilcoxon_s0_s4": pa_t,
                "panel_b_50_wilcoxon_s0_s4": pb_t,
                "dirichlet_10000_strict_dominance_prob_pct": dom_v1[
                    "prob_strict_chain_s4_gt_s3_gt_s2_gt_s1_gt_s0_pct"
                ],
                "disjoint_uuids_audited": e63["triple_identity_audit"]["total_distinct_uuids_audited"],
                "pf1_hot_evolution_elapsed_s": e63["pf1_hot_ontology_evolution"]["elapsed_seconds"],
                "pf1_c3_spatial_bytes_rewritten": e63["pf1_hot_ontology_evolution"]["c3_spatial_bytes_rewritten"],
                "arch01_to_05_in_memory_latencies": [
                    {
                        "archetype_id": ar["archetype_id"],
                        "latency_mean_ms": ar["latency_mean_ms"],
                        "latency_sd_ms": ar["latency_sd_ms"],
                        "markov_blanket_size": ar["markov_blanket_size"],
                    }
                    for ar in e63["five_handover_archetypes"]
                ],
            },
        },
        "sealed_appendices_6": gsync_audit["appendices"],
        "sealed_manuscript_tables_24": gsync_audit["manuscript_tables"],
        "sealed_wave6_artifacts": ola6_data_sealed,
        "total_waves_1_to_6_inventoried_files": len(all_wave_files_inventory) + 1,
    }

    cp_final_path = CHECKPOINTS_DIR / "wave6_final_checkpoint.json"
    cp_final_meta = write_json_fsync(final_checkpoint, cp_final_path)

    # Reporte ejecutivo en pantalla
    print("\n" + "=" * 96)
    print("CIERRE DEFINITIVO OLA 6B — ARNÉS EXPERIMENTAL Q1 (ITCON) COMPLETADO Y SELLADO (PASS)")
    print("=" * 96)
    print("\n1) LATENCIAS EN MEMORIA CORREGIDAS DE ARCH-01..ARCH-05 (5 warmup + 25 iteraciones, C2+C3 en RAM):")
    for ar in e63["five_handover_archetypes"]:
        print(
            f"   - {ar['archetype_id']}: {ar['latency_mean_ms']:.4f} ± {ar['latency_sd_ms']:.4f} ms "
            f"(SD < Mean: {ar['latency_sd_ms'] < ar['latency_mean_ms']}) | |dM|={ar['markov_blanket_size']} "
            f"({ar['markov_isolation_pct']:.2f}% isol.) | {ar['c3_reconstructed_summary_en']}"
        )

    print("\n2) LAS 24 TABLAS OFICIALES DEL MANUSCRITO (Table_1..Table_8 en .csv, .md, .tex):")
    for fname, meta in sorted(gsync_audit["manuscript_tables"].items()):
        print(
            f"   - {fname:<62} | {meta['size_bytes']:>7,} B | blocks={meta['st_blocks']:>2} | sha256={meta['sha256'][:16]}..."
        )

    print("\n3) LOS 6 ANEXOS OFICIALES DE ITCON (Appendix_A..Appendix_F):")
    for aname, meta in sorted(gsync_audit["appendices"].items()):
        print(
            f"   - {aname:<58} | {meta['size_bytes']:>7,} B | blocks={meta['st_blocks']:>3} | sha256={meta['sha256']}"
        )

    print("\n4) INFORME MAESTRO EN ESPAÑOL Y CHECKPOINT FINAL DEFINITIVO:")
    print(
        f"   - wave6_master_experiment_sha256_log.md : "
        f"{inf_es_meta['size_bytes']:,} B | blocks={inf_es_meta['st_blocks']} | sha256={inf_es_meta['sha256']}"
    )
    print(
        f"   - wave6_global_sii_master_summary.json            : "
        f"{master_meta['size_bytes']:,} B | blocks={master_meta['st_blocks']} | sha256={master_meta['sha256']}"
    )
    print(
        f"   - wave6_final_checkpoint.json                : "
        f"{cp_final_meta['size_bytes']:,} B | blocks={cp_final_meta['st_blocks']} | sha256={cp_final_meta['sha256']}"
    )
    print("=" * 96)


if __name__ == "__main__":
    main()
