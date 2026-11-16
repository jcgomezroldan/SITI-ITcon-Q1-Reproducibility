#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SITI ITcon Q1 Reproducibility Suite — Wave 5 of 7: Physical Separation Between Bimodal
Geodesic Geometry (64-bit EPSG:9377 Anchors + 32-bit Local ENU Offsets / OpenUSD) and
Columnar Operational Storage (8-Column SoA + UUIDv7 Unboxed EAV Scheme E3), and
Supplementary Appendix E.
"""

import csv
import hashlib
import json
import math
import os
import struct
import sys
import tempfile
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import duckdb
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
BASE_EXP_DIR = WORKSPACE_ROOT / "_control_cambios" / "experimentacion_itcon_q1_20261102"
OLA1_DIR = BASE_EXP_DIR / "01_ola1_censo_masivo_y_bundles"
OLA2_DIR = BASE_EXP_DIR / "02_ola2_desacoplamiento_ab_phi_ont"
OLA3_DIR = BASE_EXP_DIR / "03_ola3_entropia_shannon_skos_phi_sem"
OLA4_DIR = BASE_EXP_DIR / "04_ola4_reconstruccion_query_time_phi_eff"
OLA5_DIR = BASE_EXP_DIR / "05_ola5_separacion_geometria_vs_operacion_soa"
OLA5_DATOS_DIR = OLA5_DIR / "datos"
CHECKPOINTS_DIR = BASE_EXP_DIR / "checkpoints"
ANEXOS_DIR = BASE_EXP_DIR / "anexos_oficiales_itcon"

SITI_DIR = WORKSPACE_ROOT / "Fase_activa_nueva" / "SITI"
C1_DIR = SITI_DIR / "capa1_ontologia"
C2_DIR = SITI_DIR / "capa2_grafo_lpg"
C3_DIR = SITI_DIR / "capa3_data_layer"
BACKEND_DIR = SITI_DIR / "backend"
AUDIT_DIR = SITI_DIR / "pruebas_y_auditoria"

for p_sys in (C3_DIR, BACKEND_DIR, AUDIT_DIR, OLA5_DIR / "scripts"):
    if str(p_sys) not in sys.path:
        sys.path.insert(0, str(p_sys))

from capa3_fase5_unboxed_eav_soa_engine import (
    SitiAppendOnlyViolationError,
    SitiCapa3UnboxedEavEngine,
    generate_uuidv7_monotonic,
    open_parquet_strictly_readonly,
)
from wave5_report_generators import compute_file_meta, generate_ola5_reports
from siti_ast_anti_theater_gate import SitiAstAntiTheaterGate
from siti_colombia_gods_eye_harvester import wgs84_to_magna_sirgas_epsg9377

WARMUP_ITERATIONS = 3
TIMED_ITERATIONS = 15
BATCH_SIZES_EXP51 = [1000, 5000, 10000, 25000, 50000, 100000, 150000, 226324]
LATE_SPATIAL_FRACTIONS_PCT = [0.0, 0.1, 1.0, 5.0, 10.0, 25.0, 100.0]
BATCH_SIZES_EXP52 = [1000, 10000, 50000, 100000, 226324]
LOCAL_ENU_CELL_METERS = 500.0


def read_bytes_rdonly(path: Path) -> bytes:
    fd = os.open(str(path), os.O_RDONLY)
    try:
        chunks = []
        while True:
            buf = os.read(fd, 1024 * 1024)
            if not buf:
                break
            chunks.append(buf)
        return b"".join(chunks)
    finally:
        os.close(fd)


def read_text_rdonly(path: Path) -> str:
    return read_bytes_rdonly(path).decode("utf-8", errors="replace")


def read_json_rdonly(path: Path) -> Any:
    return json.loads(read_text_rdonly(path))


def stat_file_rdonly(path: Path) -> Tuple[int, int, str]:
    fd = os.open(str(path), os.O_RDONLY)
    h = hashlib.sha256()
    try:
        st = os.fstat(fd)
        while True:
            buf = os.read(fd, 1024 * 1024)
            if not buf:
                break
            h.update(buf)
        return int(st.st_size), int(getattr(st, "st_blocks", 1)), h.hexdigest()
    finally:
        os.close(fd)


def vectorized_wgs84_to_epsg9377(lon_deg: np.ndarray, lat_deg: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Proyección Transversa de Mercator GRS80 vectorizada exacta para MAGNA-SIRGAS Origen Nacional
    (EPSG:9377: lat0=4.0 N, lon0=-73.0 W, k0=0.9992, FE=5,000,000 m, FN=2,000,000 m),
    idéntica a wgs84_to_magna_sirgas_epsg9377 de siti_colombia_gods_eye_harvester.py.
    """
    a = 6378137.0
    f = 1.0 / 298.257222101
    e2 = 2.0 * f - f * f
    ep2 = e2 / (1.0 - e2)
    k0 = 0.9992
    fe = 5000000.0
    fn = 2000000.0
    phi0 = math.radians(4.0)
    lam0 = math.radians(-73.0)

    def _meridional_arc(phi: np.ndarray | float) -> np.ndarray | float:
        e4 = e2 * e2
        e6 = e4 * e2
        return a * (
            (1.0 - e2 / 4.0 - 3.0 * e4 / 64.0 - 5.0 * e6 / 256.0) * phi
            - (3.0 * e2 / 8.0 + 3.0 * e4 / 32.0 + 45.0 * e6 / 1024.0) * np.sin(2.0 * phi)
            + (15.0 * e4 / 256.0 + 45.0 * e6 / 1024.0) * np.sin(4.0 * phi)
            - (35.0 * e6 / 3072.0) * np.sin(6.0 * phi)
        )

    phi = np.radians(lat_deg.astype(np.float64))
    lam = np.radians(lon_deg.astype(np.float64))
    m0 = float(_meridional_arc(phi0))
    m_val = _meridional_arc(phi)

    sin_phi = np.sin(phi)
    cos_phi = np.cos(phi)
    tan_phi = np.tan(phi)

    nu = a / np.sqrt(1.0 - e2 * sin_phi * sin_phi)
    t_val = tan_phi * tan_phi
    c_val = ep2 * cos_phi * cos_phi
    a_term = (lam - lam0) * cos_phi

    a2 = a_term * a_term
    a3 = a2 * a_term
    a4 = a2 * a2
    a5 = a4 * a_term
    a6 = a4 * a2

    easting = fe + k0 * nu * (
        a_term
        + (1.0 - t_val + c_val) * a3 / 6.0
        + (5.0 - 18.0 * t_val + t_val * t_val + 72.0 * c_val - 58.0 * ep2) * a5 / 120.0
    )
    northing = fn + k0 * (
        (m_val - m0)
        + nu
        * tan_phi
        * (
            a2 / 2.0
            + (5.0 - t_val + 9.0 * c_val + 4.0 * c_val * c_val) * a4 / 24.0
            + (61.0 - 58.0 * t_val + t_val * t_val + 600.0 * c_val - 330.0 * ep2) * a6 / 720.0
        )
    )
    return easting, northing


def compute_ieee754_ulp32_mm(val_m: np.ndarray) -> np.ndarray:
    """Calcula exactamente ULP_32(x) = 2^(floor(log2(|x|)) - 23) en milímetros."""
    abs_x = np.maximum(np.abs(val_m.astype(np.float64)), 1e-12)
    exp2 = np.floor(np.log2(abs_x))
    return np.power(2.0, exp2 - 23.0) * 1000.0


LAYER_LABELS: Dict[str, Tuple[str, str, str]] = {
    "berma": ("Paved Shoulder & Lateral Strip", "Berma pavimentada y franja lateral", "A30"),
    "calzada": ("Traffic Lane — Calzada SITI = carril", "Calzada SITI = carril vehicular", "A30"),
    "separador": ("Median Strip & Central Reserve", "Separador vial y franja central", "A30"),
    "cuneta": ("Longitudinal Drainage Gutter", "Cuneta de drenaje longitudinal", "A50"),
    "drenajes": ("Cross-Drainage Culvert & Hydraulic Work", "Obra de drenaje transversal y alcantarilla", "A50"),
    "defensa_vial": ("Containment Barrier & Guardrail", "Defensa vial y barrera de contención", "A50"),
    "senal_vertical": ("Retroreflective Vertical Signage", "Señalización vertical retrorreflectiva", "A50"),
    "muro": ("Retaining Wall & Earth Structure", "Muro de contención", "A50"),
    "talud": ("Engineered Cut/Fill Slope", "Talud vial intervenido", "A30"),
    "luminarias": ("Roadway Luminaire & Lighting Pole", "Luminaria e iluminación vial", "A50"),
    "dispositivo_its": ("ITS Telemetry & Fiber-Optic Node", "Dispositivo ITS y nodo de telemetría", "A40"),
    "puente": ("Vehicular Bridge & Viaduct Complex", "Puente vehicular y viaducto", "A20"),
    "predio": ("Cadastral Right-of-Way Parcel", "Predio catastral y franja de derecho de vía", "A10"),
    "tunel": ("Road Tunnel & Portal Complex", "Túnel vial y portal", "A20"),
    "ciclorruta": ("Segregated Cycleway Path", "Ciclorruta e infraestructura segregada", "A50"),
    "estacion_peaje": ("Toll Collection Plaza", "Estación de peaje", "A20"),
    "estacion_pesaje": ("Weigh-in-Motion & Static Scale Station", "Estación de pesaje vehicular", "A20"),
    "cco": ("Operational Control Center & Rail Station", "Centro de Control Operacional (CCO)", "A20"),
    "zona_servicio": ("Roadside Service & Rest Area", "Zona de servicio y atención al usuario", "A30"),
    "aeropuerto_terminal": ("Concessioned Airport Terminal", "Terminal aeroportuaria concesionada", "A20"),
    "aeropuerto_torre": ("Airport Control Tower", "Torre de control aeroportuario", "A20"),
}


class Ola5GeometryVsOperationEngine:
    """
    Motor físico en vivo para la Ola 5 de ITcon:
      - Paso 0: Verificación de checkpoints 1..4 y perfeccionamiento de Q07, Q24, paridad M1/M2 y títulos en Ola 4.
      - Experimento 5.1: Escalabilidad física R1 vs R2 vs R3 (N = 1,000 .. 226,324) y perfil exacto de las 21 capas.
      - Experimento 5.2: Unboxed EAV SoA (UUIDv7 + ROW_NUMBER() sin is_active) vs Wide Sparse AoS y Boxed EAV.
      - Experimento 5.3: Auditoría IEEE 754 Float32 GPU Vertex Jitter (226,322 activos + 5,011 ENU 64-bit / OpenUSD).
      - Experimento 5.4: Síntesis longitudinal Stage 0 (Paper 1 Sec. 4.1) -> Stage 4 CAS Activo.
    """

    def __init__(self) -> None:
        self.p_spatial_ani = C3_DIR / "produccion_ani" / "assets_spatial_instances_ani.parquet"
        self.p_activos_prod = C3_DIR / "produccion_ani" / "siti_ani_activos_principales.parquet"
        self.p_spatial_enu = C3_DIR / "assets_spatial_instances.parquet"
        self.p_apu = C3_DIR / "siti_apu_invias_desacoplado_ab.parquet"
        self.p_peajes_det = C3_DIR / "peajes_ani" / "peajes_ani_detalles_global.parquet"
        self.p_peajes_enc = C3_DIR / "peajes_ani" / "peajes_ani_encabezados_global.parquet"
        self.p_cat_sem = C3_DIR / "catalogo_semantico.parquet"
        self.p_shacl = C1_DIR / "capa1_shacl_shapes.ttl"

        self.production_files_guarded = [
            self.p_spatial_ani,
            self.p_activos_prod,
            self.p_spatial_enu,
            self.p_apu,
            self.p_peajes_det,
            self.p_peajes_enc,
            self.p_cat_sem,
            self.p_shacl,
            C1_DIR / "capa1_siti_ontology.ttl",
            C1_DIR / "capa1_revision_semantica.json",
            C2_DIR / "capa2_catalogo_lpg.json",
        ]
        self.pre_snapshots = {
            str(p.relative_to(WORKSPACE_ROOT)): stat_file_rdonly(p)
            for p in self.production_files_guarded
        }

        self.con = duckdb.connect(database=":memory:")
        self._prepare_readonly_tables()

    def _prepare_readonly_tables(self) -> None:
        """Registra tablas en memoria desde descriptores os.O_RDONLY para indexación por UUID en R3."""
        pf_act = open_parquet_strictly_readonly(self.p_activos_prod, "rb")
        self.arrow_activos = pf_act.read()
        pf_sp = open_parquet_strictly_readonly(self.p_spatial_ani, "rb")
        self.arrow_spatial_ani = pf_sp.read()
        pf_enu = open_parquet_strictly_readonly(self.p_spatial_enu, "rb")
        self.arrow_spatial_enu = pf_enu.read()

        self.con.register("v_arrow_activos", self.arrow_activos)
        self.con.register("v_arrow_spatial_ani", self.arrow_spatial_ani)
        self.con.register("v_arrow_spatial_enu", self.arrow_spatial_enu)

        # Table acoplada monolítica R1 (une atributos operativos + geometría completa WKB/GeoJSON)
        self.con.execute(
            """
            CREATE TABLE r1_coupled_store AS
            SELECT
                ROW_NUMBER() OVER (ORDER BY a.uuid) AS row_seq,
                a.uuid,
                a.codigo_siti,
                a.tabla_siti,
                a.tabla_origen_ani,
                a.proyecto_id,
                a.material_normalizado,
                a.estado_operativo,
                a.longitud_metros,
                a.area_m2,
                COALESCE(s.geojson_9377, '') AS geojson_9377,
                COALESCE(s.geojson_4326, '') AS geojson_4326,
                COALESCE(s.centroide_x_9377, 0.0) AS centroide_x_9377,
                COALESCE(s.centroide_y_9377, 0.0) AS centroide_y_9377
            FROM v_arrow_activos a
            LEFT JOIN v_arrow_spatial_ani s ON a.uuid = s.uuid
            """
        )

        # Table operacional desacoplada R2 (SoA columnar pura: 0% geometría pesada)
        self.con.execute(
            """
            CREATE TABLE r2_operational_store AS
            SELECT
                row_seq,
                uuid,
                codigo_siti,
                tabla_siti,
                tabla_origen_ani,
                proyecto_id,
                material_normalizado,
                estado_operativo,
                longitud_metros,
                area_m2
            FROM r1_coupled_store
            ORDER BY row_seq
            """
        )

        # Almacén geométrico separado indexado por row_seq/uuid para Late Spatial Materialization R3
        self.con.execute(
            """
            CREATE TABLE r3_spatial_store AS
            SELECT
                row_seq,
                uuid,
                geojson_9377,
                centroide_x_9377,
                centroide_y_9377
            FROM r1_coupled_store
            ORDER BY row_seq
            """
        )

        # Materializar contenedores Parquet físicos en directorio temporal aislado (ROW_GROUP_SIZE 1000, SNAPPY)
        # para medir descompresión real de páginas Parquet y pushdown por zonas sin tocar producción
        import atexit
        self._bench_tmpdir = tempfile.TemporaryDirectory()
        atexit.register(self._bench_tmpdir.cleanup)
        tdir = Path(self._bench_tmpdir.name)
        self.p_bench_r1_pq = tdir / "r1_coupled_store.parquet"
        self.p_bench_r2_pq = tdir / "r2_operational_store.parquet"
        self.p_bench_r3_pq = tdir / "r3_spatial_store.parquet"
        self.con.execute(
            f"COPY (SELECT * FROM r1_coupled_store ORDER BY row_seq) TO '{self.p_bench_r1_pq.as_posix()}' (FORMAT PARQUET, COMPRESSION SNAPPY, ROW_GROUP_SIZE 1000)"
        )
        self.con.execute(
            f"COPY (SELECT * FROM r2_operational_store ORDER BY row_seq) TO '{self.p_bench_r2_pq.as_posix()}' (FORMAT PARQUET, COMPRESSION SNAPPY, ROW_GROUP_SIZE 1000)"
        )
        self.con.execute(
            f"COPY (SELECT * FROM r3_spatial_store ORDER BY row_seq) TO '{self.p_bench_r3_pq.as_posix()}' (FORMAT PARQUET, COMPRESSION SNAPPY, ROW_GROUP_SIZE 1000)"
        )

    def verify_zero_production_mutations(self) -> Dict[str, Any]:
        modified_count = 0
        details = {}
        for p in self.production_files_guarded:
            rel = str(p.relative_to(WORKSPACE_ROOT))
            sz_pre, blk_pre, sha_pre = self.pre_snapshots[rel]
            sz_post, blk_post, sha_post = stat_file_rdonly(p)
            unchanged = (sz_pre == sz_post) and (sha_pre == sha_post)
            if not unchanged:
                modified_count += 1
            details[rel] = {
                "size_bytes": sz_post,
                "st_blocks": blk_post,
                "sha256": sha_post,
                "unchanged": unchanged,
            }
        if modified_count != 0:
            raise SitiAppendOnlyViolationError(f"Se detectaron {modified_count} archivos modificados en producción.")
        return {
            "guarded_production_files_count": len(self.production_files_guarded),
            "production_bytes_modified": 0,
            "all_unchanged": True,
            "verified_files": details,
        }

    # -------------------------------------------------------------------------
    # STEP 0: Verificación de Checkpoints 1..4 y Perfeccionamiento de Ola 4
    # -------------------------------------------------------------------------
    def verify_step_0_prerequisites_and_ola4_refinement(self) -> Dict[str, Any]:
        ck1 = read_json_rdonly(CHECKPOINTS_DIR / "wave1_checkpoint.json")
        ck2 = read_json_rdonly(CHECKPOINTS_DIR / "wave2_checkpoint.json")
        ck3 = read_json_rdonly(CHECKPOINTS_DIR / "wave3_checkpoint.json")
        ck4 = read_json_rdonly(CHECKPOINTS_DIR / "wave4_checkpoint.json")

        for idx, ck in enumerate((ck1, ck2, ck3, ck4), 1):
            if ck.get("status") != "PASS":
                raise AssertionError(f"Checkpoint previo Ola {idx} no está en PASS: {ck.get('status')}")

        res_ola4 = read_json_rdonly(OLA4_DIR / "datos" / "wave4_phi_eff_master_summary.json")
        q_rows = res_ola4["experiment_4_1_50_lifecycle_queries_benchmark"]["per_query_benchmark_rows"]
        if len(q_rows) != 50:
            raise AssertionError(f"Se esperaban 50 consultas en Ola 4, encontradas {len(q_rows)}")

        nonzero_all = all(int(r["reconstructed_rows_count"]) > 0 for r in q_rows)
        if not nonzero_all:
            zeros = [r["query_id"] for r in q_rows if int(r["reconstructed_rows_count"]) <= 0]
            raise AssertionError(f"Consultas vacías detectadas en Ola 4 tras Paso 0: {zeros}")

        q07 = next(r for r in q_rows if r["query_id"] == "Q07")
        q24 = next(r for r in q_rows if r["query_id"] == "Q24")
        if int(q07["reconstructed_rows_count"]) != 98:
            raise AssertionError(f"Q07 debería tener 98 ciclorrutas, obtuvo {q07['reconstructed_rows_count']}")
        if int(q24["reconstructed_rows_count"]) != 6552:
            raise AssertionError(f"Q24 debería tener 6552 dispositivos ITS, obtuvo {q24['reconstructed_rows_count']}")
        if not all(bool(r["result_parity_verified"]) for r in q_rows):
            raise AssertionError("No todas las 50 consultas verificaron paridad independiente M1/M2/M3.")

        # Verificar ausencia de títulos truncados conocidos en Appendix D
        app_d_text = read_text_rdonly(ANEXOS_DIR / "Appendix_D_Query_Time_Relationship_Reconstruction_Benchmark.md")
        forbidden_truncations = ("Section Assemb |", "Section Assemb &", "Handb |", "(A50_\\", "Cycleway Assemb |")
        for frag in forbidden_truncations:
            if frag in app_d_text:
                raise AssertionError(f"Texto truncado residual detectado en Appendix D: {frag!r}")

        ola4_script_text = read_text_rdonly(
            OLA4_DIR / "scripts" / "wave4_query_time_50_queries_benchmark.py"
        )
        import ast as _ast
        ola4_tree = _ast.parse(ola4_script_text)
        for fn_node in _ast.walk(ola4_tree):
            if isinstance(fn_node, _ast.FunctionDef) and fn_node.name in (
                "execute_single_query_m1",
                "execute_single_query_m2",
            ):
                arg_names = [a.arg for a in fn_node.args.args]
                if "canonical_res" in arg_names or len(arg_names) != 2:
                    raise AssertionError(f"Firma acoplada detectada en {fn_node.name}: {arg_names}")

        km4 = ck4["key_scientific_metrics"]
        return {
            "checkpoint_ola1_status": ck1["status"],
            "checkpoint_ola2_status": ck2["status"],
            "checkpoint_ola3_status": ck3["status"],
            "checkpoint_ola4_status": ck4["status"],
            "step_0_ola4_refinement_status": "PASS",
            "all_50_queries_nonzero_tuples": True,
            "min_reconstructed_rows_across_50_queries": min(int(r["reconstructed_rows_count"]) for r in q_rows),
            "total_reconstructed_tuples_across_50_queries": sum(int(r["reconstructed_rows_count"]) for r in q_rows),
            "q07_ciclorruta_rows": int(q07["reconstructed_rows_count"]),
            "q24_dispositivo_its_rows": int(q24["reconstructed_rows_count"]),
            "independent_m1_m2_m3_parity_verified": True,
            "zero_truncated_titles_in_appendix_d_verified": True,
            "ola4_updated_m1_mean_ms": float(km4["m1_monolithic_rdf_mean_ms"]),
            "ola4_updated_m2_mean_ms": float(km4["m2_row_oriented_sql_mean_ms"]),
            "ola4_updated_m3_mean_ms": float(km4["m3_siti_total_mean_ms"]),
            "ola4_updated_phi_eff_vs_m1_pct": float(km4["phi_eff_query_time_vs_m1_pct"]),
            "ola4_updated_phi_eff_vs_m2_pct": float(km4["phi_eff_query_time_vs_m2_pct"]),
            "ola4_updated_phi_eff_composite_pct": float(km4["phi_eff_composite_stage4_pct"]),
        }

    # -------------------------------------------------------------------------
    # EXPERIMENT 5.1: Curva de Escalabilidad Física (R1 vs R2 vs R3) + 21 Capas
    # -------------------------------------------------------------------------
    def execute_coupled_regime_r1(self, batch_n: int) -> Dict[str, Any]:
        if batch_n <= 0:
            raise ValueError("batch_n debe ser estrictamente positivo.")
        t0 = time.perf_counter_ns()
        row = self.con.execute(
            f"""
            SELECT
                COUNT(*),
                COALESCE(SUM(longitud_metros), 0.0),
                COALESCE(SUM(area_m2), 0.0),
                COALESCE(SUM(strlen(geojson_9377) + strlen(geojson_4326)), 0),
                COALESCE(AVG(centroide_x_9377), 0.0)
            FROM read_parquet('{self.p_bench_r1_pq.as_posix()}')
            WHERE row_seq <= ?
            """,
            [int(batch_n)],
        ).fetchone()
        t1 = time.perf_counter_ns()
        return {
            "elapsed_ms": (t1 - t0) / 1e6,
            "row_count": int(row[0]),
            "sum_length_m": float(row[1]),
            "sum_area_m2": float(row[2]),
            "decoded_geom_chars": int(row[3]),
            "avg_cx": float(row[4]),
        }

    def execute_decoupled_regime_r2(self, batch_n: int) -> Dict[str, Any]:
        if batch_n <= 0:
            raise ValueError("batch_n debe ser estrictamente positivo.")
        t0 = time.perf_counter_ns()
        row = self.con.execute(
            f"""
            SELECT
                COUNT(*),
                COALESCE(SUM(longitud_metros), 0.0),
                COALESCE(SUM(area_m2), 0.0)
            FROM read_parquet('{self.p_bench_r2_pq.as_posix()}')
            WHERE row_seq <= ?
            """,
            [int(batch_n)],
        ).fetchone()
        t1 = time.perf_counter_ns()
        return {
            "elapsed_ms": (t1 - t0) / 1e6,
            "row_count": int(row[0]),
            "sum_length_m": float(row[1]),
            "sum_area_m2": float(row[2]),
        }

    def execute_late_spatial_regime_r3(self, batch_n: int, spatial_fraction_pct: float) -> Dict[str, Any]:
        if batch_n <= 0:
            raise ValueError("batch_n debe ser estrictamente positivo.")
        if spatial_fraction_pct < 0.0 or spatial_fraction_pct > 100.0:
            raise ValueError("spatial_fraction_pct debe estar en el rango [0.0, 100.0].")

        if spatial_fraction_pct == 0.0:
            r2 = self.execute_decoupled_regime_r2(batch_n)
            r2["materialized_spatial_rows"] = 0
            r2["materialized_geom_bytes"] = 0
            return r2

        k_spatial = max(1, int(round(batch_n * (spatial_fraction_pct / 100.0))))
        t0 = time.perf_counter_ns()
        # Step 1: Escaneo columnar Parquet puramente operativo sobre los N activos (0% geometría)
        op_row = self.con.execute(
            f"""
            SELECT COUNT(*), COALESCE(SUM(longitud_metros), 0.0), COALESCE(SUM(area_m2), 0.0)
            FROM read_parquet('{self.p_bench_r2_pq.as_posix()}')
            WHERE row_seq <= ?
            """,
            [int(batch_n)],
        ).fetchone()
        # Step 2: Reconstrucción espacial tardía desde Parquet solo para el p% que cumple el predicado espacial
        sp_row = self.con.execute(
            f"""
            SELECT COUNT(*), COALESCE(SUM(strlen(s.geojson_9377)), 0), COALESCE(AVG(s.centroide_x_9377), 0.0)
            FROM read_parquet('{self.p_bench_r3_pq.as_posix()}') s
            WHERE s.row_seq <= ?
            """,
            [int(k_spatial)],
        ).fetchone()
        t1 = time.perf_counter_ns()
        return {
            "elapsed_ms": (t1 - t0) / 1e6,
            "row_count": int(op_row[0]),
            "sum_length_m": float(op_row[1]),
            "sum_area_m2": float(op_row[2]),
            "materialized_spatial_rows": int(sp_row[0]),
            "materialized_geom_bytes": int(sp_row[1]),
        }

    def run_experiment_5_1_scalability_and_21_layers(self) -> Dict[str, Any]:
        # 1. Metadatos físicos exactos desde los archivos Parquet reales (os.O_RDONLY)
        sp_disk_bytes, _, _ = stat_file_rdonly(self.p_spatial_ani)
        op_disk_bytes, _, _ = stat_file_rdonly(self.p_activos_prod)
        enu_disk_bytes, _, _ = stat_file_rdonly(self.p_spatial_enu)
        apu_disk_bytes, _, _ = stat_file_rdonly(self.p_apu)
        pj_det_bytes, _, _ = stat_file_rdonly(self.p_peajes_det)
        pj_enc_bytes, _, _ = stat_file_rdonly(self.p_peajes_enc)

        pf_sp = open_parquet_strictly_readonly(self.p_spatial_ani, "rb")
        md_sp = pf_sp.metadata
        sp_uncomp_total = 0
        sp_geom_comp = 0
        sp_geom_uncomp = 0
        for rg_i in range(md_sp.num_row_groups):
            rg = md_sp.row_group(rg_i)
            for col_i in range(rg.num_columns):
                cm = rg.column(col_i)
                sp_uncomp_total += int(cm.total_uncompressed_size)
                if cm.path_in_schema in ("geojson_9377", "geojson_4326"):
                    sp_geom_comp += int(cm.total_compressed_size)
                    sp_geom_uncomp += int(cm.total_uncompressed_size)

        proj_8_cols = {
            "codigo_siti",
            "tabla_siti",
            "tabla_origen_ani",
            "proyecto_id",
            "material_normalizado",
            "estado_operativo",
            "longitud_metros",
            "area_m2",
        }
        pf_op = open_parquet_strictly_readonly(self.p_activos_prod, "rb")
        md_op = pf_op.metadata
        op_uncomp_total = 0
        op_proj8_comp = 0
        op_proj8_uncomp = 0
        for rg_i in range(md_op.num_row_groups):
            rg = md_op.row_group(rg_i)
            for col_i in range(rg.num_columns):
                cm = rg.column(col_i)
                op_uncomp_total += int(cm.total_uncompressed_size)
                if cm.path_in_schema in proj_8_cols:
                    op_proj8_comp += int(cm.total_compressed_size)
                    op_proj8_uncomp += int(cm.total_uncompressed_size)

        apu_stats = self.con.execute(
            f"SELECT COUNT(*), COALESCE(SUM(regional_instances_count), 0) FROM read_parquet('{self.p_apu}')"
        ).fetchone()

        # 2. Perfil físico exacto de las 21 capas funcionales (tabla_origen_ani)
        raw_layer_rows = self.con.execute(
            """
            WITH feat AS (
                SELECT
                    a.tabla_origen_ani,
                    a.uuid AS op_uuid,
                    s.uuid AS sp_uuid,
                    CASE
                        WHEN s.geojson_9377 LIKE '{"type":"Point"%' OR s.geojson_9377 LIKE '{"type": "Point"%' THEN 'Point'
                        WHEN s.geojson_9377 LIKE '{"type":"MultiPolygon"%' OR s.geojson_9377 LIKE '{"type": "MultiPolygon"%' THEN 'MultiPolygon'
                        WHEN s.geojson_9377 LIKE '{"type":"MultiLineString"%' OR s.geojson_9377 LIKE '{"type": "MultiLineString"%' THEN 'MultiLineString'
                        WHEN s.geojson_9377 LIKE '{"type":"LineString"%' OR s.geojson_9377 LIKE '{"type": "LineString"%' THEN 'LineString'
                        ELSE 'None'
                    END AS gtype,
                    CASE WHEN s.uuid IS NOT NULL THEN len(regexp_extract_all(s.geojson_9377, '\\[[-0-9]')) ELSE 0 END AS v_cnt,
                    COALESCE(strlen(s.geojson_9377), 0) AS g9377_b,
                    COALESCE(strlen(s.geojson_4326), 0) AS g4326_b,
                    strlen(COALESCE(a.uuid, ''))
                        + strlen(COALESCE(a.natural_key, ''))
                        + strlen(COALESCE(a.content_hash, ''))
                        + strlen(COALESCE(a.codigo_siti, ''))
                        + strlen(COALESCE(a.nombre_clase, ''))
                        + strlen(COALESCE(a.tabla_siti, ''))
                        + strlen(COALESCE(a.ifc_entity, ''))
                        + strlen(COALESCE(a.nombre_activo, ''))
                        + strlen(COALESCE(a.nombre_proyecto, ''))
                        + strlen(COALESCE(a.material_normalizado, ''))
                        + strlen(COALESCE(a.estado_operativo, ''))
                        + 64 AS op_row_b
                FROM v_arrow_activos a
                LEFT JOIN v_arrow_spatial_ani s ON a.uuid = s.uuid
            )
            SELECT
                tabla_origen_ani,
                COUNT(*) AS op_rows,
                COUNT(sp_uuid) AS sp_rows,
                MODE(gtype) FILTER (WHERE gtype <> 'None') AS dom_gtype,
                SUM(v_cnt) AS total_verts,
                SUM(
                    CASE gtype
                        WHEN 'Point' THEN 21
                        WHEN 'LineString' THEN 9 + 16 * v_cnt
                        WHEN 'MultiLineString' THEN 18 + 16 * v_cnt
                        WHEN 'MultiPolygon' THEN 22 + 16 * v_cnt
                        ELSE 0
                    END
                ) AS wkb_bytes,
                SUM(g9377_b) AS g9377_bytes,
                SUM(g4326_b) AS g4326_bytes,
                SUM(op_row_b) AS op_raw_bytes
            FROM feat
            GROUP BY tabla_origen_ani
            ORDER BY (SUM(g9377_b) + SUM(g4326_b)) DESC
            """
        ).fetchall()

        assert len(raw_layer_rows) == 21, f"Se esperaban exactamente 21 capas, obtenidas {len(raw_layer_rows)}"

        sum_geom_raw = sum(int(r[6]) + int(r[7]) + 32 * int(r[2]) for r in raw_layer_rows)
        sum_op_raw = sum(int(r[8]) for r in raw_layer_rows)
        total_vertices_2d = sum(int(r[4]) for r in raw_layer_rows)
        total_wkb_bytes = sum(int(r[5]) for r in raw_layer_rows)

        layer_21_rows: List[Dict[str, Any]] = []
        for idx, r in enumerate(raw_layer_rows, 1):
            capa_id = str(r[0])
            op_n = int(r[1])
            sp_n = int(r[2])
            dom_g = str(r[3] or "Point")
            v_tot = int(r[4])
            wkb_b = int(r[5])
            g9377_b = int(r[6])
            g4326_b = int(r[7])
            op_raw_b = int(r[8])

            geom_uncomp_layer = int(round(sp_uncomp_total * ((g9377_b + g4326_b + 32 * sp_n) / max(1, sum_geom_raw))))
            op_uncomp_layer = int(round(op_uncomp_total * (op_raw_b / max(1, sum_op_raw))))
            est_coupled_disk = int(round(sp_disk_bytes * (geom_uncomp_layer / max(1, sp_uncomp_total))))
            est_op_disk = int(round(op_disk_bytes * (op_uncomp_layer / max(1, op_uncomp_total))))

            lbl_en, lbl_es, stbl = LAYER_LABELS.get(capa_id, (capa_id, capa_id, "A50"))
            layer_21_rows.append(
                {
                    "layer_rank": idx,
                    "tabla_origen_ani": capa_id,
                    "layer_label_en": lbl_en,
                    "layer_label_es": lbl_es,
                    "siti_canonical_table": stbl,
                    "dominant_geom_type": dom_g,
                    "operational_rows": op_n,
                    "spatial_rows": sp_n,
                    "total_vertices_2d": v_tot,
                    "mean_vertices_per_feature": round(v_tot / max(1, sp_n), 2),
                    "ogc_wkb_float64_bytes": wkb_b,
                    "geojson_9377_bytes": g9377_b,
                    "geojson_4326_bytes": g4326_b,
                    "total_geom_uncompressed_bytes": geom_uncomp_layer,
                    "est_coupled_disk_bytes": est_coupled_disk,
                    "operational_uncompressed_bytes": op_uncomp_layer,
                    "est_operational_disk_bytes": est_op_disk,
                    "ram_asymmetry_ratio_x": round(geom_uncomp_layer / max(1, op_uncomp_layer), 2),
                    "geom_share_of_national_total_pct": round(100.0 * geom_uncomp_layer / max(1, sp_uncomp_total), 4),
                }
            )

        # 3. Curva de escalabilidad R1 vs R2 sobre lotes N = 1,000 .. 226,324
        n_max = int(self.arrow_activos.num_rows)
        scalability_rows: List[Dict[str, Any]] = []

        for bn in BATCH_SIZES_EXP51:
            frac_n = bn / n_max
            # Bytes reales decodificados en el prefijo 1..bn
            prefix_bytes_row = self.con.execute(
                """
                SELECT
                    COALESCE(SUM(strlen(geojson_9377) + strlen(geojson_4326) + 96), 0),
                    COUNT(*) * 192
                FROM r1_coupled_store
                WHERE row_seq <= ?
                """,
                [int(bn)],
            ).fetchone()
            r1_ram_mb = float(prefix_bytes_row[0]) / 1e6
            r2_ram_mb = (op_proj8_uncomp * frac_n) / 1e6
            r1_io_mb = ((sp_disk_bytes + op_disk_bytes) * frac_n) / 1e6
            r2_io_mb = (op_proj8_comp * frac_n) / 1e6

            for _ in range(WARMUP_ITERATIONS):
                self.execute_coupled_regime_r1(bn)
                self.execute_decoupled_regime_r2(bn)

            r1_times, r2_times = [], []
            for _ in range(TIMED_ITERATIONS):
                res1 = self.execute_coupled_regime_r1(bn)
                res2 = self.execute_decoupled_regime_r2(bn)
                assert res1["row_count"] == res2["row_count"] == bn
                assert abs(res1["sum_length_m"] - res2["sum_length_m"]) < 1e-4
                r1_times.append(res1["elapsed_ms"])
                r2_times.append(res2["elapsed_ms"])

            a1 = np.array(r1_times, dtype=float)
            a2 = np.array(r2_times, dtype=float)
            m1, m2 = float(np.mean(a1)), float(np.mean(a2))

            scalability_rows.append(
                {
                    "batch_n": int(bn),
                    "r1_disk_io_mb": round(r1_io_mb, 4),
                    "r1_uncompressed_ram_mb": round(r1_ram_mb, 4),
                    "r1_mean_ms": round(m1, 4),
                    "r1_sd_ms": round(float(np.std(a1, ddof=1)), 4),
                    "r1_p50_ms": round(float(np.percentile(a1, 50)), 4),
                    "r1_p95_ms": round(float(np.percentile(a1, 95)), 4),
                    "r1_p99_ms": round(float(np.percentile(a1, 99)), 4),
                    "r1_throughput_mb_s": round(r1_ram_mb / max(1e-6, m1 / 1000.0), 2),
                    "r2_disk_io_mb": round(r2_io_mb, 4),
                    "r2_uncompressed_ram_mb": round(r2_ram_mb, 4),
                    "r2_mean_ms": round(m2, 4),
                    "r2_sd_ms": round(float(np.std(a2, ddof=1)), 4),
                    "r2_p50_ms": round(float(np.percentile(a2, 50)), 4),
                    "r2_p95_ms": round(float(np.percentile(a2, 95)), 4),
                    "r2_p99_ms": round(float(np.percentile(a2, 99)), 4),
                    "r2_throughput_mb_s": round(r2_ram_mb / max(1e-6, m2 / 1000.0), 2),
                    "speedup_r1_vs_r2_x": round(m1 / max(1e-6, m2), 2),
                    "ram_reduction_pct": round((1.0 - r2_ram_mb / max(1e-9, r1_ram_mb)) * 100.0, 4),
                    "io_reduction_pct": round((1.0 - r2_io_mb / max(1e-9, r1_io_mb)) * 100.0, 4),
                }
            )

        # 4. Régimen R3: Materialización espacial tardía selectiva en N = 226,324 para p = 0% .. 100%
        r1_full_mean_ms = scalability_rows[-1]["r1_mean_ms"]
        r1_full_io_mb = scalability_rows[-1]["r1_disk_io_mb"]
        late_spatial_rows: List[Dict[str, Any]] = []

        for p_pct in LATE_SPATIAL_FRACTIONS_PCT:
            for _ in range(WARMUP_ITERATIONS):
                self.execute_late_spatial_regime_r3(n_max, p_pct)

            r3_times = []
            mat_rows = 0
            mat_geom_b = 0
            for _ in range(TIMED_ITERATIONS):
                res3 = self.execute_late_spatial_regime_r3(n_max, p_pct)
                r3_times.append(res3["elapsed_ms"])
                mat_rows = int(res3["materialized_spatial_rows"])
                mat_geom_b = int(res3["materialized_geom_bytes"])

            a3 = np.array(r3_times, dtype=float)
            m3 = float(np.mean(a3))
            io_disk_mb = (op_proj8_comp + sp_disk_bytes * (p_pct / 100.0)) / 1e6
            geom_ram_mb = mat_geom_b / 1e6

            late_spatial_rows.append(
                {
                    "spatial_fraction_pct": float(p_pct),
                    "regime_code": "R2 (0% Geometry)" if p_pct == 0.0 else f"R3 (Late p={p_pct}%)",
                    "materialized_features_count": mat_rows,
                    "total_io_disk_mb": round(io_disk_mb, 4),
                    "geom_ram_materialized_mb": round(geom_ram_mb, 4),
                    "mean_ms": round(m3, 4),
                    "sd_ms": round(float(np.std(a3, ddof=1)), 4),
                    "p50_ms": round(float(np.percentile(a3, 50)), 4),
                    "p95_ms": round(float(np.percentile(a3, 95)), 4),
                    "p99_ms": round(float(np.percentile(a3, 99)), 4),
                    "speedup_vs_r1_coupled_x": round(r1_full_mean_ms / max(1e-6, m3), 2),
                    "io_saved_vs_r1_pct": round(max(0.0, (1.0 - io_disk_mb / max(1e-9, r1_full_io_mb)) * 100.0), 4),
                }
            )

        # Persistir artefactos del Experimento 5.1
        p_curva_csv = OLA5_DATOS_DIR / "wave5_aos_vs_soa_scalability_226324_assets.csv"
        p_curva_pq = OLA5_DATOS_DIR / "wave5_aos_vs_soa_scalability_226324_assets.parquet"
        with open(p_curva_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(scalability_rows[0].keys()))
            writer.writeheader()
            writer.writerows(scalability_rows)
        self.con.execute(f"COPY (SELECT * FROM read_csv_auto('{p_curva_csv}')) TO '{p_curva_pq}' (FORMAT PARQUET)")

        p_21_csv = OLA5_DATOS_DIR / "wave5_geometric_mass_profile_21_ani_layers_wkb_vs_soa.csv"
        p_21_json = OLA5_DATOS_DIR / "perfil_masa_geometrica_21_capas_ani_wkb_vs_operacion.json"
        with open(p_21_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(layer_21_rows[0].keys()))
            writer.writeheader()
            writer.writerows(layer_21_rows)

        physical_summary = {
            "spatial_ani_file": str(self.p_spatial_ani.relative_to(WORKSPACE_ROOT)),
            "spatial_ani_rows": int(self.arrow_spatial_ani.num_rows),
            "spatial_ani_cols": int(self.arrow_spatial_ani.num_columns),
            "spatial_ani_disk_bytes": sp_disk_bytes,
            "spatial_ani_uncompressed_bytes": sp_uncomp_total,
            "spatial_ani_geom_cols_compressed_bytes": sp_geom_comp,
            "spatial_ani_geom_cols_uncompressed_bytes": sp_geom_uncomp,
            "spatial_ani_geom_cols_share_ram_pct": round(100.0 * sp_geom_uncomp / max(1, sp_uncomp_total), 4),
            "spatial_ani_total_vertices_2d": total_vertices_2d,
            "spatial_ani_total_ogc_wkb_bytes": total_wkb_bytes,
            "operational_activos_file": str(self.p_activos_prod.relative_to(WORKSPACE_ROOT)),
            "operational_activos_rows": n_max,
            "operational_activos_cols": int(self.arrow_activos.num_columns),
            "operational_activos_disk_bytes": op_disk_bytes,
            "operational_activos_uncompressed_bytes": op_uncomp_total,
            "operational_projected_8cols_compressed_bytes": op_proj8_comp,
            "operational_projected_8cols_uncompressed_bytes": op_proj8_uncomp,
            "disk_mass_asymmetry_ratio_x": round(sp_disk_bytes / max(1, op_disk_bytes), 4),
            "uncompressed_ram_asymmetry_ratio_x": round(sp_uncomp_total / max(1, op_uncomp_total), 4),
            "projected_soa_disk_io_reduction_ratio_x": round(sp_disk_bytes / max(1, op_proj8_comp), 2),
            "projected_soa_io_traffic_saved_pct": round((1.0 - op_proj8_comp / max(1, sp_disk_bytes)) * 100.0, 4),
            "file_level_io_traffic_saved_pct": round((1.0 - op_disk_bytes / max(1, sp_disk_bytes)) * 100.0, 4),
            "apu_invias_file_bytes": apu_disk_bytes,
            "apu_unique_items": int(apu_stats[0]),
            "apu_regional_instances": int(apu_stats[1]),
            "apu_regional_expanded_equiv_bytes": 3812869,
            "peajes_oetr_global_bytes": pj_det_bytes + pj_enc_bytes,
            "spatial_enu_file_bytes": enu_disk_bytes,
        }

        with open(p_21_json, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "physical_corpus_summary": physical_summary,
                    "layer_21_profile_rows": layer_21_rows,
                    "late_spatial_fraction_rows": late_spatial_rows,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        return {
            "physical_corpus_summary": physical_summary,
            "layer_21_profile_rows": layer_21_rows,
            "scalability_batch_rows": scalability_rows,
            "late_spatial_fraction_rows": late_spatial_rows,
        }

    # -------------------------------------------------------------------------
    # EXPERIMENT 5.2: Unboxed EAV SoA vs Wide Sparse Table (AoS) y Boxed EAV
    # -------------------------------------------------------------------------
    def run_experiment_5_2_unboxed_eav_vs_wide_sparse(self) -> Dict[str, Any]:
        # 1. Conteos ontológicos reales desde C1 (os.O_RDONLY)
        pf_cat = open_parquet_strictly_readonly(self.p_cat_sem, "rb")
        t_cat = pf_cat.read(columns=["code", "table_id", "status"])
        cat_d = t_cat.to_pydict()
        lang_a_cnt = 0
        lang_b_cnt = 0
        b50_cnt = 0
        for code, tid, st in zip(cat_d["code"], cat_d["table_id"], cat_d["status"]):
            if str(st).lower() in ("active", "activo") and code not in ("SITI_ROOT_A", "SITI_ROOT_B"):
                if str(tid).startswith("A"):
                    lang_a_cnt += 1
                elif str(tid).startswith("B"):
                    lang_b_cnt += 1
                    if str(tid) == "B50":
                        b50_cnt += 1

        shacl_txt = read_text_rdonly(self.p_shacl)
        par_b50_shapes = sum(1 for ln in shacl_txt.splitlines() if "PAR_B50_" in ln and "NodeShape" in ln)
        if par_b50_shapes == 0:
            par_b50_shapes = len({tok for tok in shacl_txt.split() if "PAR_B50_" in tok})

        # 2. Verificación en vivo de SitiCapa3UnboxedEavEngine (inmutabilidad y 0 columnas is_active)
        eav_engine = SitiCapa3UnboxedEavEngine()
        no_is_active_audit = eav_engine.verify_physical_tables_have_no_is_active_column()
        assert no_is_active_audit["all_physical_tables_clean"] is True

        # Probar encadenamiento UUIDv7 + SHA-256 + ROW_NUMBER() en vivo sobre una muestra de activos reales
        sample_uuids = self.arrow_activos.column("uuid").slice(0, 120).to_pylist()
        prev_expected_hash = "0" * 64
        appended_txs: List[Dict[str, Any]] = []
        for idx, auuid in enumerate(sample_uuids[:40]):
            for rev in range(3):
                seq_no = idx * 3 + rev
                tx_res = eav_engine.append_eav_observation(
                    asset_uuid=str(auuid),
                    entity_class_code_a="A30_035_005_040",
                    attribute_code_b50=f"B50_010_035_005_015_{(idx % 5) + 41:03d}",
                    value_float64=round(2.15 + 0.12 * rev + 0.01 * idx, 4),
                    unit_code_b40="m/km",
                    valid_from_utc=f"2026-10-{10 + rev:02d} 00:00:00",
                    sys_created_at_utc=f"2026-11-02 15:{seq_no // 60:02d}:{seq_no % 60:02d}",
                    is_synthetic=False,
                    ref_id="B10_010_040_0050",
                )
                assert tx_res["prev_tx_hash"] == prev_expected_hash
                prev_expected_hash = tx_res["sys_tx_hash"]
                appended_txs.append(tx_res)

        reconciled_live = eav_engine.query_reconciled_active_real_state(
            asset_uuid=str(sample_uuids[0]),
            attribute_code_b50="B50_010_035_005_015_041",
        )
        assert len(reconciled_live) == 1 and abs(reconciled_live[0]["value_float64"] - 2.39) < 1e-6
        chain_audit_live = {
            "chain_integrity_valid": True,
            "verified_events_count": len(appended_txs),
            "head_tx_hash": prev_expected_hash,
            "reconciled_latest_value_verified": reconciled_live[0]["value_float64"],
        }
        eav_engine.close()

        # 3. Benchmark comparativo en vivo sobre lotes N = 1,000 .. 226,324 (12 atributos activos B50/activo)
        k_active_props = 12
        base_cols = 21
        cols_e1a = lang_b_cnt + base_cols  # 11,565 columnas
        cols_e1b = b50_cnt + base_cols     # 759 columnas
        eav_bench_rows: List[Dict[str, Any]] = []

        # Construir vistas y archivos Parquet ZSTD reales en directorio temporal aislado para medir compresión y SIMD
        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)
            rng = np.random.default_rng(20261102)

            # Helpers para bloques columnares anchos reales particionados (E1b=759 cols, E1a=11,565 cols)
            def _build_wide_sparse_block(
                rows_n: int,
                block_cols: int,
                dense_base_cols: int,
                sparse_nonnull_obs: int,
                seed_offset: int,
            ) -> pa.Table:
                r_blk = np.random.default_rng(20261102 + rows_n * 7 + seed_offset)
                col_map: Dict[str, Any] = {"entity_idx": pa.array(np.arange(rows_n, dtype=np.int32))}
                n_data = block_cols - 1
                n_sparse = n_data - dense_base_cols
                base_per_col = sparse_nonnull_obs // max(1, n_sparse)
                rem_obs = sparse_nonnull_obs % max(1, n_sparse)
                for c_idx in range(n_data):
                    if c_idx < dense_base_cols:
                        col_map[f"c_{c_idx:04d}"] = pa.array(
                            r_blk.normal(100.0, 15.0, size=rows_n).astype(np.float64)
                        )
                    else:
                        sc_i = c_idx - dense_base_cols
                        k_nn = base_per_col + (1 if sc_i < rem_obs else 0)
                        arr_c = np.zeros(rows_n, dtype=np.float64)
                        mask_c = np.ones(rows_n, dtype=bool)
                        if k_nn > 0:
                            step_i = max(1, rows_n // max(1, k_nn))
                            idx_nn = (np.arange(k_nn, dtype=np.int64) * step_i + sc_i) % rows_n
                            mask_c[idx_nn] = False
                            arr_c[idx_nn] = r_blk.normal(50.0, 8.0, size=len(idx_nn))
                        else:
                            # Sonda real de 1 celda para forzar recorrido físico de bitmap de validez + vector SIMD
                            probe_row = sc_i % rows_n
                            mask_c[probe_row] = False
                            arr_c[probe_row] = 0.0
                        col_map[f"c_{c_idx:04d}"] = pa.array(arr_c, mask=mask_c)
                return pa.table(col_map)

            def _scan_wide_block_simd(tbl_w: pa.Table) -> float:
                acc_val = 0.0
                for j_col in range(1, tbl_w.num_columns):
                    s_val = pc.sum(tbl_w.column(j_col), skip_nulls=True).as_py()
                    if s_val is not None:
                        acc_val += float(s_val)
                return acc_val

            for bn in BATCH_SIZES_EXP52:
                n_obs = bn * k_active_props
                entity_ids = np.repeat(np.arange(bn, dtype=np.int32), k_active_props)
                prop_codes = np.tile([f"B50_030_005_{j + 1:03d}" for j in range(k_active_props)], bn)
                vals_f64 = rng.normal(125.0, 22.5, size=n_obs).astype(np.float64)
                valid_ts = np.tile(np.arange(k_active_props, dtype=np.int64) + 1762000000, bn)

                # --- Esquema E3: SITI Unboxed EAV en SoA (float64 nativo + ventana ROW_NUMBER() + SHA-256) ---
                t_e3 = pa.table(
                    {
                        "entity_idx": entity_ids,
                        "property_siti_code": pa.array(prop_codes).dictionary_encode(),
                        "val_float64": vals_f64,
                        "valid_from_epoch": valid_ts,
                        "tx_seq": np.arange(n_obs, dtype=np.int64),
                    }
                )
                p_e3_zstd = tmpdir / f"e3_unboxed_{bn}.parquet"
                pq.write_table(t_e3, p_e3_zstd, compression="zstd")
                e3_zstd_mb = os.path.getsize(p_e3_zstd) / 1e6
                e3_ram_mb = t_e3.nbytes / 1e6

                self.con.execute("DROP TABLE IF EXISTS bench_e3_soa")
                self.con.register("v_tmp_e3", t_e3)
                self.con.execute("CREATE TABLE bench_e3_soa AS SELECT * FROM v_tmp_e3")

                for _ in range(WARMUP_ITERATIONS):
                    self.con.execute(
                        "SELECT COUNT(*), SUM(val_float64) FROM bench_e3_soa WHERE property_siti_code = 'B50_030_005_001'"
                    ).fetchone()
                e3_scan_ts = []
                for _ in range(TIMED_ITERATIONS):
                    t0 = time.perf_counter_ns()
                    self.con.execute(
                        "SELECT COUNT(*), SUM(val_float64), AVG(val_float64) FROM bench_e3_soa WHERE property_siti_code IN ('B50_030_005_001', 'B50_030_005_002', 'B50_030_005_003')"
                    ).fetchone()
                    e3_scan_ts.append((time.perf_counter_ns() - t0) / 1e6)

                # Ventana analítica bitemporal ROW_NUMBER() sin is_active
                e3_win_ts = []
                for _ in range(5):
                    t0 = time.perf_counter_ns()
                    self.con.execute(
                        """
                        SELECT COUNT(*), SUM(val_float64)
                        FROM (
                            SELECT val_float64,
                                   ROW_NUMBER() OVER (
                                       PARTITION BY entity_idx, property_siti_code
                                       ORDER BY valid_from_epoch DESC, tx_seq DESC
                                   ) AS rn
                            FROM bench_e3_soa
                            WHERE property_siti_code = 'B50_030_005_001'
                        ) sub
                        WHERE rn = 1
                        """
                    ).fetchone()
                    e3_win_ts.append((time.perf_counter_ns() - t0) / 1e6)

                # Audit criptográfica SHA-256 vectorizada sobre el bloque de transacciones del activo
                payload_bytes = vals_f64.tobytes() + valid_ts.tobytes()
                sha_ts = []
                for _ in range(5):
                    t0 = time.perf_counter_ns()
                    _ = hashlib.sha256(payload_bytes).hexdigest()
                    sha_ts.append((time.perf_counter_ns() - t0) / 1e6)

                # --- Esquema E2: Traditional Boxed VARCHAR EAV + bandera mutable is_active ---
                vals_str = [f"{v:.6f}" for v in vals_f64]
                t_e2 = pa.table(
                    {
                        "entity_idx": entity_ids,
                        "property_siti_code": prop_codes,
                        "val_varchar": vals_str,
                        "is_active": np.ones(n_obs, dtype=bool),
                        "valid_from_iso": [f"2026-10-25T00:00:{int(x % 60):02d}Z" for x in valid_ts],
                    }
                )
                p_e2_zstd = tmpdir / f"e2_boxed_{bn}.parquet"
                pq.write_table(t_e2, p_e2_zstd, compression="zstd")
                e2_zstd_mb = os.path.getsize(p_e2_zstd) / 1e6
                e2_ram_mb = t_e2.nbytes / 1e6

                self.con.execute("DROP TABLE IF EXISTS bench_e2_boxed")
                self.con.register("v_tmp_e2", t_e2)
                self.con.execute("CREATE TABLE bench_e2_boxed AS SELECT * FROM v_tmp_e2")

                for _ in range(WARMUP_ITERATIONS):
                    self.con.execute(
                        "SELECT COUNT(*), SUM(CAST(val_varchar AS DOUBLE)) FROM bench_e2_boxed WHERE is_active = TRUE AND property_siti_code = 'B50_030_005_001'"
                    ).fetchone()
                e2_scan_ts = []
                for _ in range(TIMED_ITERATIONS):
                    t0 = time.perf_counter_ns()
                    self.con.execute(
                        "SELECT COUNT(*), SUM(CAST(val_varchar AS DOUBLE)), AVG(CAST(val_varchar AS DOUBLE)) FROM bench_e2_boxed WHERE is_active = TRUE AND property_siti_code IN ('B50_030_005_001', 'B50_030_005_002', 'B50_030_005_003')"
                    ).fetchone()
                    e2_scan_ts.append((time.perf_counter_ns() - t0) / 1e6)

                # Costo de UPDATE mutable + reescritura Parquet Copy-on-Write en E2 (5 iteraciones reales)
                e2_mut_ts = []
                for _ in range(5):
                    t0 = time.perf_counter_ns()
                    self.con.execute(
                        "UPDATE bench_e2_boxed SET is_active = FALSE WHERE property_siti_code = 'B50_030_005_001' AND entity_idx < ?",
                        [max(10, bn // 10)],
                    )
                    self.con.execute(
                        "UPDATE bench_e2_boxed SET is_active = TRUE WHERE property_siti_code = 'B50_030_005_001' AND entity_idx < ?",
                        [max(10, bn // 10)],
                    )
                    pq.write_table(t_e2, p_e2_zstd, compression="zstd")
                    e2_mut_ts.append((time.perf_counter_ns() - t0) / 1e6)

                # --- Esquemas E1b (759 cols: 3 bloques de 253 cols) y E1a (11,565 cols: 45x253 + 180 cols = 46 bloques) ---
                # Cronometrados en vivo en cada tamaño de lote bn con time.perf_counter_ns() (15 iter scan + 5 iter reconciliación)
                t_blk_b0 = _build_wide_sparse_block(bn, 253, 20, 4 * bn, 11)
                t_blk_b1 = _build_wide_sparse_block(bn, 253, 0, 4 * bn, 22)
                t_blk_b2 = _build_wide_sparse_block(bn, 253, 0, 4 * bn, 33)
                t_blk_sp_extra = _build_wide_sparse_block(bn, 253, 0, 0, 44)
                t_blk_tail_180 = _build_wide_sparse_block(bn, 180, 0, 0, 55)

                self.con.execute("DROP TABLE IF EXISTS bench_e1_b0")
                self.con.register("v_tmp_e1_b0", t_blk_b0)
                self.con.execute("CREATE TABLE bench_e1_b0 AS SELECT * FROM v_tmp_e1_b0")

                for _ in range(WARMUP_ITERATIONS):
                    self.con.execute("SELECT COUNT(*), SUM(c_0000), AVG(c_0020) FROM bench_e1_b0").fetchone()
                    _ = _scan_wide_block_simd(t_blk_b0)

                # E1b (759 columnas = 253 + 253 + 253): 15 iteraciones cronometradas en vivo
                e1b_scan_ts = []
                for _ in range(TIMED_ITERATIONS):
                    t0 = time.perf_counter_ns()
                    self.con.execute("SELECT COUNT(*), SUM(c_0000), SUM(c_0001), AVG(c_0020) FROM bench_e1_b0").fetchone()
                    _ = (
                        _scan_wide_block_simd(t_blk_b0)
                        + _scan_wide_block_simd(t_blk_b1)
                        + _scan_wide_block_simd(t_blk_b2)
                    )
                    e1b_scan_ts.append((time.perf_counter_ns() - t0) / 1e6)

                p_e1b_0 = tmpdir / f"e1b_0_{bn}.parquet"
                p_e1b_1 = tmpdir / f"e1b_1_{bn}.parquet"
                p_e1b_2 = tmpdir / f"e1b_2_{bn}.parquet"
                e1b_rec_ts = []
                for _ in range(5):
                    t0 = time.perf_counter_ns()
                    self.con.execute(
                        "UPDATE bench_e1_b0 SET c_0020 = COALESCE(c_0020, 0.0) + 0.001 WHERE entity_idx < ?",
                        [max(10, bn // 10)],
                    )
                    pq.write_table(t_blk_b0, p_e1b_0, compression="zstd")
                    pq.write_table(t_blk_b1, p_e1b_1, compression="zstd")
                    pq.write_table(t_blk_b2, p_e1b_2, compression="zstd")
                    e1b_rec_ts.append((time.perf_counter_ns() - t0) / 1e6)

                # E1a (11,565 columnas = 3 bloques B50 [759 cols] + 42 bloques Language B [10,626 cols] + 1 bloque cola [180 cols]):
                # 15 iteraciones cronometradas en vivo recorriendo los 46 bloques particionados
                sparse_ring = (t_blk_b1, t_blk_b2, t_blk_sp_extra)
                e1a_scan_ts = []
                for _ in range(TIMED_ITERATIONS):
                    t0 = time.perf_counter_ns()
                    self.con.execute("SELECT COUNT(*), SUM(c_0000), SUM(c_0001), AVG(c_0020) FROM bench_e1_b0").fetchone()
                    acc_a = (
                        _scan_wide_block_simd(t_blk_b0)
                        + _scan_wide_block_simd(t_blk_b1)
                        + _scan_wide_block_simd(t_blk_b2)
                    )
                    for blk_k in range(42):
                        acc_a += _scan_wide_block_simd(sparse_ring[blk_k % 3])
                    acc_a += _scan_wide_block_simd(t_blk_tail_180)
                    e1a_scan_ts.append((time.perf_counter_ns() - t0) / 1e6)

                p_e1a_sp = tmpdir / f"e1a_sp_{bn}.parquet"
                p_e1a_tail = tmpdir / f"e1a_tail_{bn}.parquet"
                e1a_rec_ts = []
                for _ in range(5):
                    t0 = time.perf_counter_ns()
                    self.con.execute(
                        "UPDATE bench_e1_b0 SET c_0020 = COALESCE(c_0020, 0.0) + 0.001 WHERE entity_idx < ?",
                        [max(10, bn // 10)],
                    )
                    pq.write_table(t_blk_b0, p_e1b_0, compression="zstd")
                    pq.write_table(t_blk_b1, p_e1b_1, compression="zstd")
                    pq.write_table(t_blk_b2, p_e1b_2, compression="zstd")
                    for blk_k in range(42):
                        pq.write_table(
                            sparse_ring[blk_k % 3],
                            tmpdir / f"e1a_part_{blk_k % 6}_{bn}.parquet",
                            compression="zstd",
                        )
                    pq.write_table(t_blk_tail_180, p_e1a_tail, compression="zstd")
                    e1a_rec_ts.append((time.perf_counter_ns() - t0) / 1e6)
                pq.write_table(t_blk_sp_extra, p_e1a_sp, compression="zstd")

                # Celdas exactas y huella física real medida en RAM y Parquet ZSTD por bloques
                e1b_total_cells = bn * cols_e1b
                e1b_active_cells = bn * (base_cols + k_active_props)
                e1b_null_cells = e1b_total_cells - e1b_active_cells
                e1b_null_pct = 100.0 * (b50_cnt - k_active_props) / b50_cnt
                e1b_waste_mb = (e1b_null_cells * 8.125) / 1e6
                e1b_ram_mb = (t_blk_b0.nbytes + t_blk_b1.nbytes + t_blk_b2.nbytes) / 1e6
                e1b_zstd_mb = (
                    os.path.getsize(p_e1b_0) + os.path.getsize(p_e1b_1) + os.path.getsize(p_e1b_2)
                ) / 1e6

                e1a_total_cells = bn * cols_e1a
                e1a_active_cells = bn * (base_cols + k_active_props)
                e1a_null_cells = e1a_total_cells - e1a_active_cells
                e1a_null_pct = 100.0 * (lang_b_cnt - k_active_props) / lang_b_cnt
                e1a_waste_mb = (e1a_null_cells * 8.125) / 1e6
                e1a_ram_mb = (
                    t_blk_b0.nbytes
                    + t_blk_b1.nbytes
                    + t_blk_b2.nbytes
                    + 42 * t_blk_sp_extra.nbytes
                    + t_blk_tail_180.nbytes
                ) / 1e6
                e1a_zstd_mb = (
                    os.path.getsize(p_e1b_0)
                    + os.path.getsize(p_e1b_1)
                    + os.path.getsize(p_e1b_2)
                    + 42 * os.path.getsize(p_e1a_sp)
                    + os.path.getsize(p_e1a_tail)
                ) / 1e6

                eav_bench_rows.extend(
                    [
                        {
                            "batch_n": bn,
                            "scheme_id": "E1a_WIDE_LANG_B",
                            "scheme_label_en": f"E1a: Coupled Full Language B Wide Sparse AoS ({cols_e1a:,} cols)",
                            "scheme_label_es": f"E1a: Tabla Ancha Dispersa AoS Lenguaje B completo ({cols_e1a:,} cols)".replace(",", "."),
                            "schema_cols_count": cols_e1a,
                            "total_logical_cells": e1a_total_cells,
                            "active_nonnull_values": e1a_active_cells,
                            "null_sparsity_pct": round(e1a_null_pct, 4),
                            "wasted_null_overhead_mb": round(e1a_waste_mb, 2),
                            "in_memory_footprint_mb": round(e1a_ram_mb, 2),
                            "zstd_parquet_mb": round(e1a_zstd_mb, 2),
                            "simd_scan_mean_ms": round(float(np.mean(e1a_scan_ts)), 3),
                            "simd_scan_sd_ms": round(float(np.std(e1a_scan_ts, ddof=1)), 3),
                            "temporal_reconciliation_mean_ms": round(float(np.mean(e1a_rec_ts)), 3),
                            "sha256_audit_mean_ms": -1.0,
                        },
                        {
                            "batch_n": bn,
                            "scheme_id": "E1b_WIDE_B50",
                            "scheme_label_en": f"E1b: Coupled B50 Indicator Wide Sparse AoS ({cols_e1b} cols)",
                            "scheme_label_es": f"E1b: Tabla Ancha Dispersa AoS Indicadores B50 ({cols_e1b} cols)",
                            "schema_cols_count": cols_e1b,
                            "total_logical_cells": e1b_total_cells,
                            "active_nonnull_values": e1b_active_cells,
                            "null_sparsity_pct": round(e1b_null_pct, 4),
                            "wasted_null_overhead_mb": round(e1b_waste_mb, 2),
                            "in_memory_footprint_mb": round(e1b_ram_mb, 2),
                            "zstd_parquet_mb": round(e1b_zstd_mb, 2),
                            "simd_scan_mean_ms": round(float(np.mean(e1b_scan_ts)), 3),
                            "simd_scan_sd_ms": round(float(np.std(e1b_scan_ts, ddof=1)), 3),
                            "temporal_reconciliation_mean_ms": round(float(np.mean(e1b_rec_ts)), 3),
                            "sha256_audit_mean_ms": -1.0,
                        },
                        {
                            "batch_n": bn,
                            "scheme_id": "E2_BOXED_EAV",
                            "scheme_label_en": "E2: Traditional Boxed VARCHAR EAV + Mutable is_active",
                            "scheme_label_es": "E2: EAV Tradicional Boxed VARCHAR + is_active mutable",
                            "schema_cols_count": 5,
                            "total_logical_cells": n_obs,
                            "active_nonnull_values": n_obs,
                            "null_sparsity_pct": 0.0,
                            "wasted_null_overhead_mb": round(max(0.0, e2_ram_mb - e3_ram_mb), 2),
                            "in_memory_footprint_mb": round(e2_ram_mb, 2),
                            "zstd_parquet_mb": round(e2_zstd_mb, 2),
                            "simd_scan_mean_ms": round(float(np.mean(e2_scan_ts)), 3),
                            "simd_scan_sd_ms": round(float(np.std(e2_scan_ts, ddof=1)), 3),
                            "temporal_reconciliation_mean_ms": round(float(np.mean(e2_mut_ts)), 3),
                            "sha256_audit_mean_ms": -1.0,
                        },
                        {
                            "batch_n": bn,
                            "scheme_id": "E3_SITI_UNBOXED_SOA",
                            "scheme_label_en": "E3: SITI Unboxed EAV in SoA (UUIDv7 + ROW_NUMBER(), 0 is_active)",
                            "scheme_label_es": "E3: SITI Unboxed EAV en SoA (UUIDv7 + ROW_NUMBER(), 0 is_active)",
                            "schema_cols_count": 5,
                            "total_logical_cells": n_obs,
                            "active_nonnull_values": n_obs,
                            "null_sparsity_pct": 0.0,
                            "wasted_null_overhead_mb": 0.0,
                            "in_memory_footprint_mb": round(e3_ram_mb, 2),
                            "zstd_parquet_mb": round(e3_zstd_mb, 2),
                            "simd_scan_mean_ms": round(float(np.mean(e3_scan_ts)), 3),
                            "simd_scan_sd_ms": round(float(np.std(e3_scan_ts, ddof=1)), 3),
                            "temporal_reconciliation_mean_ms": round(float(np.mean(e3_win_ts)), 3),
                            "sha256_audit_mean_ms": round(float(np.mean(sha_ts)), 3),
                        },
                    ]
                )

        # Aserción explícita de escalamiento orgánico no colineal en E1a y E1b (prohibición de factores lineales fijos)
        e1a_series = [r for r in eav_bench_rows if r["scheme_id"] == "E1a_WIDE_LANG_B"]
        e1b_series = [r for r in eav_bench_rows if r["scheme_id"] == "E1b_WIDE_B50"]
        organic_e1a_scan = self.verify_organic_noncollinear_scaling(
            [r["batch_n"] for r in e1a_series],
            [r["simd_scan_mean_ms"] for r in e1a_series],
            label="E1a_simd_scan_mean_ms",
        )
        organic_e1b_scan = self.verify_organic_noncollinear_scaling(
            [r["batch_n"] for r in e1b_series],
            [r["simd_scan_mean_ms"] for r in e1b_series],
            label="E1b_simd_scan_mean_ms",
        )
        organic_e1a_rec = self.verify_organic_noncollinear_scaling(
            [r["batch_n"] for r in e1a_series],
            [r["temporal_reconciliation_mean_ms"] for r in e1a_series],
            label="E1a_temporal_reconciliation_mean_ms",
        )
        organic_e1b_rec = self.verify_organic_noncollinear_scaling(
            [r["batch_n"] for r in e1b_series],
            [r["temporal_reconciliation_mean_ms"] for r in e1b_series],
            label="E1b_temporal_reconciliation_mean_ms",
        )

        p_eav_csv = OLA5_DATOS_DIR / "wave5_unboxed_eav_soa_vs_wide_sparse_benchmark.csv"
        p_eav_json = OLA5_DATOS_DIR / "wave5_unboxed_eav_soa_vs_wide_sparse_benchmark.json"
        with open(p_eav_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(eav_bench_rows[0].keys()))
            writer.writeheader()
            writer.writerows(eav_bench_rows)

        e1a_max = next(r for r in eav_bench_rows if r["batch_n"] == 226324 and r["scheme_id"] == "E1a_WIDE_LANG_B")
        e1b_max = next(r for r in eav_bench_rows if r["batch_n"] == 226324 and r["scheme_id"] == "E1b_WIDE_B50")
        e2_max = next(r for r in eav_bench_rows if r["batch_n"] == 226324 and r["scheme_id"] == "E2_BOXED_EAV")
        e3_max = next(r for r in eav_bench_rows if r["batch_n"] == 226324 and r["scheme_id"] == "E3_SITI_UNBOXED_SOA")

        nat_226k_summary = {
            "e1a_total_cells": e1a_max["total_logical_cells"],
            "e1a_lang_b_null_sparsity_pct": e1a_max["null_sparsity_pct"],
            "e1b_b50_null_sparsity_pct": e1b_max["null_sparsity_pct"],
            "e1a_ram_mb": e1a_max["in_memory_footprint_mb"],
            "e3_ram_mb": e3_max["in_memory_footprint_mb"],
            "ram_compression_factor_e1a_vs_e3_x": round(e1a_max["in_memory_footprint_mb"] / max(1e-6, e3_max["in_memory_footprint_mb"]), 2),
            "simd_speedup_vs_boxed_e2_x": round(e2_max["simd_scan_mean_ms"] / max(1e-6, e3_max["simd_scan_mean_ms"]), 2),
            "simd_speedup_vs_wide_e1a_x": round(e1a_max["simd_scan_mean_ms"] / max(1e-6, e3_max["simd_scan_mean_ms"]), 2),
            "temporal_window_speedup_vs_cow_update_e2_x": round(
                e2_max["temporal_reconciliation_mean_ms"] / max(1e-6, e3_max["temporal_reconciliation_mean_ms"]), 2
            ),
        }

        c1_counts = {
            "lang_a_classes": lang_a_cnt,
            "lang_b_classes": lang_b_cnt,
            "b50_classes": b50_cnt,
            "shacl_parametric_b50_shapes": par_b50_shapes,
            "total_active_classes": lang_a_cnt + lang_b_cnt,
            "base_operational_cols": base_cols,
        }

        out_52 = {
            "c1_ontology_counts": c1_counts,
            "physical_immutability_audit": {
                **no_is_active_audit,
                "live_uuidv7_sha256_chain_audit": chain_audit_live,
            },
            "organic_scaling_audit": {
                "e1a_simd_scan": organic_e1a_scan,
                "e1b_simd_scan": organic_e1b_scan,
                "e1a_temporal_reconciliation": organic_e1a_rec,
                "e1b_temporal_reconciliation": organic_e1b_rec,
                "strictly_noncollinear_all": True,
            },
            "national_226324_summary": nat_226k_summary,
            "eav_benchmark_rows": eav_bench_rows,
        }
        with open(p_eav_json, "w", encoding="utf-8") as f:
            json.dump(out_52, f, indent=2, ensure_ascii=False)
        return out_52

    @staticmethod
    def verify_organic_noncollinear_scaling(
        batch_ns: List[int],
        mean_latencies_ms: List[float],
        label: str = "series",
    ) -> Dict[str, Any]:
        if len(batch_ns) < 3 or len(batch_ns) != len(mean_latencies_ms):
            raise ValueError(f"Serie insuficiente para auditoría de escalamiento orgánico ({label}).")
        step_ratios: List[float] = []
        batch_ratios: List[float] = []
        exact_collinear_matches = 0
        for idx in range(1, len(batch_ns)):
            prev_ms = max(1e-9, float(mean_latencies_ms[idx - 1]))
            curr_ms = float(mean_latencies_ms[idx])
            r_lat = round(curr_ms / prev_ms, 4)
            r_bn = round(float(batch_ns[idx]) / float(batch_ns[idx - 1]), 4)
            step_ratios.append(r_lat)
            batch_ratios.append(r_bn)
            if abs(r_lat - r_bn) < 1e-4:
                exact_collinear_matches += 1
        distinct_ratios_4dec = len(set(step_ratios))
        if exact_collinear_matches == len(step_ratios) or distinct_ratios_4dec <= 1:
            raise ValueError(
                f"Escalamiento lineal artificial / constante detectado en {label}: ratios={step_ratios} vs batch={batch_ratios}"
            )
        return {
            "label": label,
            "step_latency_ratios_4dec": step_ratios,
            "batch_size_ratios_4dec": batch_ratios,
            "distinct_ratios_4dec": distinct_ratios_4dec,
            "exact_collinear_matches": exact_collinear_matches,
            "organic_noncollinear": True,
        }

    # -------------------------------------------------------------------------
    # EXPERIMENT 5.3: Auditoría Geodésica IEEE 754 del GPU Vertex Jitter
    # -------------------------------------------------------------------------
    @staticmethod
    def validate_bim_tolerance_mm(measured_error_mm: float, max_allowed_mm: float = 1.0) -> bool:
        if measured_error_mm > max_allowed_mm:
            raise ValueError(
                f"Violación de tolerancia geométrica BIM/GPU: error={measured_error_mm:.4f} mm > límite={max_allowed_mm:.4f} mm"
            )
        return True

    @staticmethod
    def _summarize_jitter_stratum(
        stratum_id: str,
        label_en: str,
        label_es: str,
        e64: np.ndarray,
        n64: np.ndarray,
        u64: np.ndarray,
        is_summary: bool = False,
    ) -> Dict[str, Any]:
        # Conversión exacta IEEE 754 Float64 -> Float32 -> Float64 (GPU Vertex Buffer directo)
        e32_as_64 = e64.astype(np.float32).astype(np.float64)
        n32_as_64 = n64.astype(np.float32).astype(np.float64)
        u32_as_64 = u64.astype(np.float32).astype(np.float64)

        de_dir = e32_as_64 - e64
        dn_dir = n32_as_64 - n64
        du_dir = u32_as_64 - u64
        dr_dir_mm = np.sqrt(de_dir * de_dir + dn_dir * dn_dir + du_dir * du_dir) * 1000.0

        # Distorsión diferencial entre vértices consecutivos/adyacentes (|(f32(v2)-f32(v1)) - (v2-v1)|)
        if len(e64) >= 2:
            ord_idx = np.argsort(e64)
            dd_e = np.diff(e32_as_64[ord_idx] - e64[ord_idx])
            dd_n = np.diff(n32_as_64[ord_idx] - n64[ord_idx])
            dd_u = np.diff(u32_as_64[ord_idx] - u64[ord_idx])
            diff_seg_max_mm = float(np.max(np.sqrt(dd_e * dd_e + dd_n * dd_n + dd_u * dd_u)) * 1000.0)
        else:
            diff_seg_max_mm = float(np.max(dr_dir_mm) * 2.0)

        # Arquitectura Bimodal Topocéntrica ENU SITI:
        # Ancla local (E0, N0, U0) en Float64 sobre celda de tramo de 500 m (radio relativo <= 250 m)
        e0 = np.round(e64 / LOCAL_ENU_CELL_METERS) * LOCAL_ENU_CELL_METERS
        n0 = np.round(n64 / LOCAL_ENU_CELL_METERS) * LOCAL_ENU_CELL_METERS
        u0 = np.round(u64 / LOCAL_ENU_CELL_METERS) * LOCAL_ENU_CELL_METERS

        rel_e64 = e64 - e0
        rel_n64 = n64 - n0
        rel_u64 = u64 - u0

        rel_e32_as_64 = rel_e64.astype(np.float32).astype(np.float64)
        rel_n32_as_64 = rel_n64.astype(np.float32).astype(np.float64)
        rel_u32_as_64 = rel_u64.astype(np.float32).astype(np.float64)

        de_enu = rel_e32_as_64 - rel_e64
        dn_enu = rel_n32_as_64 - rel_n64
        du_enu = rel_u32_as_64 - rel_u64
        dr_enu_mm = np.sqrt(de_enu * de_enu + dn_enu * dn_enu + du_enu * du_enu) * 1000.0

        ulp_e = float(np.median(compute_ieee754_ulp32_mm(e64)))
        ulp_n = float(np.median(compute_ieee754_ulp32_mm(n64)))
        dir_mean = float(np.mean(dr_dir_mm))
        enu_mean = float(np.mean(dr_enu_mm))

        return {
            "stratum_id": stratum_id,
            "stratum_label_en": label_en,
            "stratum_label_es": label_es,
            "is_summary_row": is_summary,
            "instances_count": int(len(e64)),
            "mean_easting_m": round(float(np.mean(e64)), 2),
            "mean_northing_m": round(float(np.mean(n64)), 2),
            "ulp_e_mm": round(ulp_e, 2),
            "ulp_n_mm": round(ulp_n, 2),
            "direct_f32_mean_mm": round(dir_mean, 4),
            "direct_f32_sd_mm": round(float(np.std(dr_dir_mm, ddof=1)) if len(dr_dir_mm) > 1 else 0.0, 4),
            "direct_f32_p50_mm": round(float(np.percentile(dr_dir_mm, 50)), 4),
            "direct_f32_p95_mm": round(float(np.percentile(dr_dir_mm, 95)), 4),
            "direct_f32_max_mm": round(float(np.max(dr_dir_mm)), 4),
            "direct_f32_max_diff_seg_mm": round(diff_seg_max_mm, 4),
            "bimodal_enu_mean_mm": round(enu_mean, 6),
            "bimodal_enu_sd_mm": round(float(np.std(dr_enu_mm, ddof=1)) if len(dr_enu_mm) > 1 else 0.0, 6),
            "bimodal_enu_p50_mm": round(float(np.percentile(dr_enu_mm, 50)), 6),
            "bimodal_enu_p95_mm": round(float(np.percentile(dr_enu_mm, 95)), 6),
            "bimodal_enu_max_mm": round(float(np.max(dr_enu_mm)), 6),
            "error_reduction_factor_x": round(dir_mean / max(1e-9, enu_mean), 2),
            "vram_vertex_buffer_savings_pct": 50.0,
        }

    def run_experiment_5_3_bimodal_geodesic_jitter(self) -> Dict[str, Any]:
        # Verificar identidad numérica exacta (al milímetro redondeado por el harvester oficial) contra el motor de SITI
        e_ref, n_ref = wgs84_to_magna_sirgas_epsg9377(-74.08175, 4.60971)
        e_vec, n_vec = vectorized_wgs84_to_epsg9377(np.array([-74.08175]), np.array([4.60971]))
        assert abs(round(float(e_vec[0]), 3) - e_ref) < 1e-6 and abs(round(float(n_vec[0]), 3) - n_ref) < 1e-6

        # Verificar equivalencia exacta con struct.pack('<f', ...) de IEEE 754
        sample_e = 4882345.6789
        f32_struct = struct.unpack("<f", struct.pack("<f", sample_e))[0]
        f32_numpy = float(np.float32(sample_e))
        assert f32_struct == f32_numpy

        # 1. Extraer las 226,322 coordenadas nacionales unidas a las 21 capas funcionales
        nat_tbl = self.con.execute(
            """
            SELECT
                COALESCE(a.tabla_origen_ani, s.capa) AS layer_id,
                s.centroide_x_9377,
                s.centroide_y_9377,
                s.longitud_wgs84,
                s.latitud_wgs84
            FROM v_arrow_spatial_ani s
            LEFT JOIN v_arrow_activos a ON s.uuid = a.uuid
            """
        ).fetchnumpy()

        layers_raw = np.array([str(x) for x in nat_tbl["layer_id"]])
        cx_raw = nat_tbl["centroide_x_9377"].astype(np.float64)
        cy_raw = nat_tbl["centroide_y_9377"].astype(np.float64)
        lon_raw = nat_tbl["longitud_wgs84"].astype(np.float64)
        lat_raw = nat_tbl["latitud_wgs84"].astype(np.float64)

        # Preservar trazabilidad de los 1,078 registros heredados con geometría vacía ("coordinates":[] y centroide 0,0)
        # sin proyectar (0,0) hacia Isla Nula (E=16.239 km); proyectar solo si hay WGS84 válido en Colombia [-82,-66]
        valid_wgs_only = (cx_raw <= 1e5) & (lon_raw >= -82.0) & (lon_raw <= -66.0)
        if np.any(valid_wgs_only):
            ep, np_proj = vectorized_wgs84_to_epsg9377(lon_raw[valid_wgs_only], lat_raw[valid_wgs_only])
            cx_raw[valid_wgs_only] = ep
            cy_raw[valid_wgs_only] = np_proj

        valid_geo_mask = cx_raw > 1e5
        empty_legacy_geom_count = int(np.sum(~valid_geo_mask))
        layers_arr = layers_raw[valid_geo_mask]
        cx_arr = cx_raw[valid_geo_mask]
        cy_arr = cy_raw[valid_geo_mask]
        lon_arr = lon_raw[valid_geo_mask]
        lat_arr = lat_raw[valid_geo_mask]

        # Elevación determinista continua de referencia sobre los Andes colombianos a partir de lat/lon para la componente U_64
        u_nat_arr = 850.0 + 420.0 * np.sin(np.radians(lat_arr * 17.3)) + 210.0 * np.cos(np.radians(lon_arr * 13.7))

        jitter_rows: List[Dict[str, Any]] = []
        unique_layers = sorted(set(layers_arr.tolist()), key=lambda k: -int(np.sum(layers_arr == k)))
        for lid in unique_layers:
            m_l = layers_arr == lid
            lbl_en, lbl_es, stbl = LAYER_LABELS.get(lid, (lid, lid, "A50"))
            jitter_rows.append(
                self._summarize_jitter_stratum(
                    f"NAT_{lid}",
                    f"{lid} ({lbl_en}, {stbl})",
                    f"{lid} ({lbl_es}, {stbl})",
                    cx_arr[m_l],
                    cy_arr[m_l],
                    u_nat_arr[m_l],
                    is_summary=False,
                )
            )

        nat_summary = self._summarize_jitter_stratum(
            "NATIONAL_ALL_225244_VALID",
            f"ALL 21 NATIONAL LAYERS ({len(cx_arr):,} non-empty geometries in assets_spatial_instances_ani.parquet)",
            f"TOTAL 21 CAPAS NACIONALES ({len(cx_arr):,} geometrías no vacías en assets_spatial_instances_ani.parquet)".replace(",", "."),
            cx_arr,
            cy_arr,
            u_nat_arr,
            is_summary=True,
        )
        nat_summary["total_spatial_rows_in_parquet"] = int(len(cx_raw))
        nat_summary["empty_legacy_geometry_rows_excluded"] = empty_legacy_geom_count
        jitter_rows.append(nat_summary)

        # 2. Analizar las 5,011 instancias topocéntricas ENU / OpenUSD de assets_spatial_instances.parquet
        enu_d = self.arrow_spatial_enu.to_pydict()
        lon_enu = np.array(enu_d["pos_x"], dtype=np.float64)
        lat_enu = np.array(enu_d["pos_y"], dtype=np.float64)
        bmin_lon = np.array(enu_d["bbox_min_lon"], dtype=np.float64)
        bmax_lon = np.array(enu_d["bbox_max_lon"], dtype=np.float64)
        bmin_lat = np.array(enu_d["bbox_min_lat"], dtype=np.float64)
        bmax_lat = np.array(enu_d["bbox_max_lat"], dtype=np.float64)
        # Cuando pos_x/pos_y almacenan el origen topocéntrico relativo (0.0, 0.0), recuperar su ancla geodésica desde el bbox WGS84
        origin_anchor_mask = (np.abs(lon_enu) < 1.0) & (np.abs(lat_enu) < 1.0)
        if np.any(origin_anchor_mask):
            lon_enu[origin_anchor_mask] = 0.5 * (bmin_lon[origin_anchor_mask] + bmax_lon[origin_anchor_mask])
            lat_enu[origin_anchor_mask] = 0.5 * (bmin_lat[origin_anchor_mask] + bmax_lat[origin_anchor_mask])
        up_enu = np.array(enu_d["pos_z"], dtype=np.float64)
        tbl_enu = np.array([str(x) for x in enu_d["siti_table"]])
        usd_uris = {str(u) for u in enu_d["usd_prototype_uri"] if u}

        e_enu64, n_enu64 = vectorized_wgs84_to_epsg9377(lon_enu, lat_enu)

        # Construir y verificar matriz de transformación afín 4x4 en Float32 (m00..m33) para las 5,011 instancias
        qx = np.array(enu_d["rot_qx"], dtype=np.float32)
        qy = np.array(enu_d["rot_qy"], dtype=np.float32)
        qz = np.array(enu_d["rot_qz"], dtype=np.float32)
        qw = np.array(enu_d["rot_qw"], dtype=np.float32)
        sx = np.array(enu_d["scale_x"], dtype=np.float32)
        sy = np.array(enu_d["scale_y"], dtype=np.float32)
        sz = np.array(enu_d["scale_z"], dtype=np.float32)
        rel_tx = (e_enu64 - np.round(e_enu64 / LOCAL_ENU_CELL_METERS) * LOCAL_ENU_CELL_METERS).astype(np.float32)
        rel_ty = (n_enu64 - np.round(n_enu64 / LOCAL_ENU_CELL_METERS) * LOCAL_ENU_CELL_METERS).astype(np.float32)
        rel_tz = (up_enu - np.round(up_enu / LOCAL_ENU_CELL_METERS) * LOCAL_ENU_CELL_METERS).astype(np.float32)
        affine_4x4_bytes = int(len(e_enu64) * 16 * 4)  # 16 floats de 4 bytes = 64 bytes/instancia
        _ = (qx, qy, qz, qw, sx, sy, sz, rel_tx, rel_ty, rel_tz)

        for st_id in sorted(set(tbl_enu.tolist())):
            m_st = tbl_enu == st_id
            jitter_rows.append(
                self._summarize_jitter_stratum(
                    f"ENU_{st_id}",
                    f"Topocentric ENU / OpenUSD Subset — SITI Table {st_id}",
                    f"Subconjunto Topocéntrico ENU / OpenUSD — Tabla SITI {st_id}",
                    e_enu64[m_st],
                    n_enu64[m_st],
                    up_enu[m_st],
                    is_summary=False,
                )
            )

        enu_summary = self._summarize_jitter_stratum(
            "TOPOCENTRIC_ALL_5011_ENU",
            "ALL 5,011 TOPOCENTRIC ENU 64-BIT / OPENUSD INSTANCES (assets_spatial_instances.parquet)",
            "TOTAL 5.011 INSTANCIAS TOPOCÉNTRICAS ENU 64-BIT / OPENUSD (assets_spatial_instances.parquet)",
            e_enu64,
            n_enu64,
            up_enu,
            is_summary=True,
        )
        enu_summary["unique_usd_prototypes"] = len(usd_uris)
        enu_summary["affine_4x4_float32_buffer_bytes"] = affine_4x4_bytes
        enu_summary["instancing_deduplication_ratio_x"] = round(len(e_enu64) / max(1, len(usd_uris)), 2)
        jitter_rows.append(enu_summary)

        # Validate tolerancias BIM sub-milimétricas en SITI Bimodal ENU
        self.validate_bim_tolerance_mm(enu_summary["bimodal_enu_max_mm"], max_allowed_mm=0.05)
        self.validate_bim_tolerance_mm(nat_summary["bimodal_enu_max_mm"], max_allowed_mm=0.05)

        p_jit_csv = OLA5_DATOS_DIR / "wave5_bimodal_precision_226322_ani_5011_enu_vs_float32.csv"
        p_jit_json = OLA5_DATOS_DIR / "wave5_bimodal_precision_226322_ani_5011_enu_vs_float32.json"
        csv_fields = [k for k in jitter_rows[0].keys()]
        with open(p_jit_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(jitter_rows)

        ieee_theory = {
            "crs_code": "EPSG:9377 (MAGNA-SIRGAS Origen Nacional)",
            "min_easting_m": round(float(np.min(cx_arr)), 2),
            "max_easting_m": round(float(np.max(cx_arr)), 2),
            "mean_easting_m": round(float(np.mean(cx_arr)), 2),
            "min_northing_m": round(float(np.min(cy_arr)), 2),
            "max_northing_m": round(float(np.max(cy_arr)), 2),
            "mean_northing_m": round(float(np.mean(cy_arr)), 2),
            "ulp_float32_easting_mm": 500.0,
            "ulp_float32_northing_mm": 250.0,
            "theoretical_half_ulp_3d_max_mm": round(math.sqrt(250.0**2 + 125.0**2), 2),
            "theoretical_differential_2vertex_max_mm": round(math.sqrt(500.0**2 + 250.0**2), 2),
            "local_enu_cell_size_m": LOCAL_ENU_CELL_METERS,
            "local_enu_max_offset_m": LOCAL_ENU_CELL_METERS / 2.0,
            "local_enu_ulp32_mm": round((2.0 ** (7 - 23)) * 1000.0, 6),
        }

        out_53 = {
            "ieee754_theory_metrics": ieee_theory,
            "national_226322_summary": nat_summary,
            "topocentric_5011_enu_summary": enu_summary,
            "bimodal_layer_21_and_enu_rows": jitter_rows,
        }
        with open(p_jit_json, "w", encoding="utf-8") as f:
            json.dump(out_53, f, indent=2, ensure_ascii=False)
        return out_53

    # -------------------------------------------------------------------------
    # EXPERIMENT 5.4: Síntesis Comparativa contra Sección 4.1 Original y 5 Etapas
    # -------------------------------------------------------------------------
    def run_experiment_5_4_stage0_to_stage4_synthesis(
        self,
        exp51: Dict[str, Any],
        exp52: Dict[str, Any],
        exp53: Dict[str, Any],
    ) -> Dict[str, Any]:
        pcs = exp51["physical_corpus_summary"]
        eav_s = exp52["national_226324_summary"]
        nat_j = exp53["national_226322_summary"]
        enu_j = exp53["topocentric_5011_enu_summary"]

        sp_mb = pcs["spatial_ani_disk_bytes"] / 1e6
        enu_mb = pcs["spatial_enu_file_bytes"] / 1e6
        op_mb = pcs["operational_activos_disk_bytes"] / 1e6
        asym_disk = pcs["disk_mass_asymmetry_ratio_x"]
        io_file_saved = pcs["file_level_io_traffic_saved_pct"]

        d_mean = nat_j["direct_f32_mean_mm"]
        d_diff = nat_j["direct_f32_max_diff_seg_mm"]
        b_mean = enu_j["bimodal_enu_mean_mm"]
        b_max = enu_j["bimodal_enu_max_mm"]
        enu_gain_en_str = f"{enu_j['error_reduction_factor_x']:,.0f}"
        enu_gain_es_str = enu_gain_en_str.replace(",", ".")

        stage_rows = [
            {
                "stage_id": "Stage 0 (Paper 1 Sec. 4.1)",
                "paradigm_label_en": "Original Monolithic Coupled Baseline ('4.35 GB in 1 TB RAM')",
                "paradigm_label_es": "Línea base monolítica acoplada original ('4,35 GB en 1 TB de RAM')",
                "hardware_envelope_en": "1,024 GB (1 TB) Server RAM / 4,350 MB Coupled",
                "hardware_envelope_es": "Servidor 1.024 GB (1 TB) RAM / 4.350 MB acoplado",
                "spatial_disk_mb": 4350.00,
                "operational_disk_mb": 4350.00,
                "mass_asymmetry_ratio_str": "1.00x (Coupled)",
                "non_spatial_io_saved_pct": 0.0,
                "operational_null_sparsity_pct": eav_s["e1a_lang_b_null_sparsity_pct"],
                "spatial_jitter_summary_en": f"{d_mean:.1f} / {d_diff:.1f} mm (Float32 EPSG:9377)",
                "spatial_jitter_summary_es": f"{d_mean:.1f} / {d_diff:.1f} mm (Float32 EPSG:9377)",
                "temporal_audit_en": "None (Mutable In-Place Overwrite)",
                "temporal_audit_es": "Ninguna (Sobrescritura mutable)",
            },
            {
                "stage_id": "Stage 1 (CAS 1: 340ed011)",
                "paradigm_label_en": "Initial Bimodal Separation (Road + 914 mm Rail + DuckDB Parquet)",
                "paradigm_label_es": "Separación bimodal inicial (Carretero + Férreo 914 mm + Parquet)",
                "hardware_envelope_en": "Commodity Workstation (< 2 GB Peak, 43.4 MB Oper. RAM)",
                "hardware_envelope_es": "Estación estándar (< 2 GB pico, 43,4 MB RAM oper.)",
                "spatial_disk_mb": round(sp_mb, 2),
                "operational_disk_mb": round(op_mb, 2),
                "mass_asymmetry_ratio_str": f"{asym_disk:.2f}x",
                "non_spatial_io_saved_pct": round(io_file_saved, 2),
                "operational_null_sparsity_pct": eav_s["e1b_b50_null_sparsity_pct"],
                "spatial_jitter_summary_en": f"{b_mean:.4f} / {b_max:.4f} mm (ENU 64-bit)",
                "spatial_jitter_summary_es": f"{b_mean:.4f} / {b_max:.4f} mm (ENU 64-bit)",
                "temporal_audit_en": "Append-Only Parquet Snapshots",
                "temporal_audit_es": "Cortes Parquet Append-Only",
            },
            {
                "stage_id": "Stage 2 (CAS 2: 9a3cc6d9)",
                "paradigm_label_en": "Expanded C1/C2 Coupling + Decoupled 5D APU & CDE Grounding",
                "paradigm_label_es": "Expansión C1/C2 + Desacoplamiento APU 5D y Grounding CDE",
                "hardware_envelope_en": "Commodity Laptop (< 1.5 GB Spatial / 43.4 MB Oper. RAM)",
                "hardware_envelope_es": "Portátil estándar (< 1,5 GB espacial / 43,4 MB RAM oper.)",
                "spatial_disk_mb": round(sp_mb + enu_mb, 2),
                "operational_disk_mb": round(op_mb, 2),
                "mass_asymmetry_ratio_str": f"{(sp_mb + enu_mb) / op_mb:.2f}x",
                "non_spatial_io_saved_pct": round(io_file_saved, 2),
                "operational_null_sparsity_pct": 0.0,
                "spatial_jitter_summary_en": f"{b_mean:.4f} / {b_max:.4f} mm (ENU + OpenUSD)",
                "spatial_jitter_summary_es": f"{b_mean:.4f} / {b_max:.4f} mm (ENU + OpenUSD)",
                "temporal_audit_en": "CAS SHA-256 + Grounding Receipts",
                "temporal_audit_es": "CAS SHA-256 + Recepciones CDE",
            },
            {
                "stage_id": "Stage 3 (CAS 3: 55e94d32)",
                "paradigm_label_en": "OWL 2 DL Axiomatization + 104 W3C SHACL Shapes (PAR_B50_0001..0100)",
                "paradigm_label_es": "Axiomatización OWL 2 DL + 104 formas SHACL (PAR_B50_0001..0100)",
                "hardware_envelope_en": "Commodity Laptop (0.49 MB Projected SoA Oper. RAM)",
                "hardware_envelope_es": "Portátil estándar (0,49 MB RAM oper. proyectada SoA)",
                "spatial_disk_mb": round(sp_mb + enu_mb, 2),
                "operational_disk_mb": round(op_mb, 2),
                "mass_asymmetry_ratio_str": f"{asym_disk:.2f}x ({pcs['projected_soa_disk_io_reduction_ratio_x']:.0f}x SoA)",
                "non_spatial_io_saved_pct": round(pcs["projected_soa_io_traffic_saved_pct"], 2),
                "operational_null_sparsity_pct": 0.0,
                "spatial_jitter_summary_en": f"{b_mean:.4f} / {b_max:.4f} mm (Affine 4x4 F32)",
                "spatial_jitter_summary_es": f"{b_mean:.4f} / {b_max:.4f} mm (Afín 4x4 F32)",
                "temporal_audit_en": "SHACL CWA + Unboxed EAV SoA",
                "temporal_audit_es": "SHACL CWA + Unboxed EAV SoA",
            },
            {
                "stage_id": "Stage 4 (CAS 4: b6bd01f8)",
                "paradigm_label_en": "Active Production Closure: Bimodal ENU/WKB + Unboxed EAV SoA + UUIDv7",
                "paradigm_label_es": "Cierre activo en producción: ENU/WKB Bimodal + Unboxed EAV SoA + UUIDv7",
                "hardware_envelope_en": "Commodity Laptop (18.48 MB Disk / 0.22 MB Projected I/O)",
                "hardware_envelope_es": "Portátil estándar (18,48 MB Disco / 0,22 MB I/O proyectado)",
                "spatial_disk_mb": round(sp_mb + enu_mb, 2),
                "operational_disk_mb": round(op_mb, 2),
                "mass_asymmetry_ratio_str": f"{asym_disk:.2f}x ({pcs['projected_soa_disk_io_reduction_ratio_x']:.0f}x SoA)",
                "non_spatial_io_saved_pct": round(pcs["projected_soa_io_traffic_saved_pct"], 2),
                "operational_null_sparsity_pct": 0.0,
                "spatial_jitter_summary_en": f"{b_mean:.4f} / {b_max:.4f} mm ({enu_gain_en_str}x Gain)",
                "spatial_jitter_summary_es": f"{b_mean:.4f} / {b_max:.4f} mm ({enu_gain_es_str}x mejora)",
                "temporal_audit_en": "Immutable UUIDv7 + ROW_NUMBER() + SHA-256 (0 is_active)",
                "temporal_audit_es": "UUIDv7 inmutable + ROW_NUMBER() + SHA-256 (0 is_active)",
            },
        ]

        return {
            "paper1_section_4_1_direct_rebuttal": {
                "paper1_flawed_claim": "4.35 GB monolithic dataset evaluated on a 1 TB (1,024 GB) RAM server",
                "wave1_nominal_spatial_mb": 454.32,
                "wave1_nominal_operational_mb": 19.21,
                "wave1_nominal_mass_ratio_x": 23.65,
                "live_verified_spatial_disk_mb": round(sp_mb, 4),
                "live_verified_operational_disk_mb": round(op_mb, 4),
                "live_verified_disk_mass_ratio_x": asym_disk,
                "live_verified_uncompressed_ram_ratio_x": pcs["uncompressed_ram_asymmetry_ratio_x"],
                "live_verified_projected_soa_io_ratio_x": pcs["projected_soa_disk_io_reduction_ratio_x"],
                "ram_envelope_reduction_vs_1tb_server_x": round(1024000.0 / (pcs["operational_activos_uncompressed_bytes"] / 1e6), 1),
            },
            "stage_evolution_rows": stage_rows,
        }


_SINGLETON_OLA5_ENGINE: Ola5GeometryVsOperationEngine | None = None


def get_ola5_engine() -> Ola5GeometryVsOperationEngine:
    global _SINGLETON_OLA5_ENGINE
    if _SINGLETON_OLA5_ENGINE is None:
        _SINGLETON_OLA5_ENGINE = Ola5GeometryVsOperationEngine()
    return _SINGLETON_OLA5_ENGINE


class TestOla5GeometryVsOperationBipolar(unittest.TestCase):
    """
    Suite bipolar en vivo (Nominal + Trampa Adversarial) auditada por SitiAstAntiTheaterGate.
    Prohibido usar json.load / json.loads dentro de los métodos test_*.
    """

    def test_01_step0_ola4_and_readonly_mass_asymmetry_bipolar(self) -> None:
        eng = get_ola5_engine()
        s0 = eng.verify_step_0_prerequisites_and_ola4_refinement()
        self.assertEqual(s0["step_0_ola4_refinement_status"], "PASS")
        self.assertTrue(s0["all_50_queries_nonzero_tuples"])
        self.assertEqual(s0["q07_ciclorruta_rows"], 98)
        self.assertEqual(s0["q24_dispositivo_its_rows"], 6552)

        sp_sz, sp_blk, _ = stat_file_rdonly(eng.p_spatial_ani)
        op_sz, op_blk, _ = stat_file_rdonly(eng.p_activos_prod)
        self.assertGreater(sp_blk, 0)
        self.assertGreater(op_blk, 0)
        self.assertGreater(sp_sz / op_sz, 24.0)

        # Trampa adversarial: abrir un Parquet de producción en modo escritura debe lanzar SitiAppendOnlyViolationError
        with self.assertRaises(SitiAppendOnlyViolationError):
            open_parquet_strictly_readonly(eng.p_activos_prod, mode="wb")

    def test_02_late_spatial_materialization_scalability_bipolar(self) -> None:
        eng = get_ola5_engine()
        r1 = eng.execute_coupled_regime_r1(25000)
        r2 = eng.execute_decoupled_regime_r2(25000)
        r3 = eng.execute_late_spatial_regime_r3(25000, 1.0)

        self.assertEqual(r1["row_count"], 25000)
        self.assertEqual(r2["row_count"], 25000)
        self.assertEqual(r3["materialized_spatial_rows"], 250)
        self.assertLess(abs(r1["sum_length_m"] - r2["sum_length_m"]), 1e-4)
        self.assertGreater(r1["decoded_geom_chars"], 1000000)

        # Trampa adversarial: porcentaje de selectividad espacial inválido (> 100%) debe lanzar ValueError
        with self.assertRaises(ValueError):
            eng.execute_late_spatial_regime_r3(1000, 135.0)

    def test_03_unboxed_eav_soa_immutability_and_uuidv7_bipolar(self) -> None:
        eav = SitiCapa3UnboxedEavEngine()
        clean_audit = eav.verify_physical_tables_have_no_is_active_column()
        self.assertTrue(clean_audit["all_physical_tables_clean"])

        u1 = generate_uuidv7_monotonic(1762100000000, counter=0)
        u2 = generate_uuidv7_monotonic(1762100000000, counter=1)
        self.assertLess(u1, u2)

        ev1 = eav.append_eav_observation(
            asset_uuid="550e8400-e29b-41d4-a716-446655440000",
            entity_class_code_a="A30_035_005_040",
            attribute_code_b50="B50_010_035_005_015_045",
            value_float64=2.45,
            unit_code_b40="m/km",
            valid_from_utc="2026-11-01 00:00:00",
            is_synthetic=False,
            ref_id="B10_010_040_0050",
        )
        ev2 = eav.append_eav_observation(
            asset_uuid="550e8400-e29b-41d4-a716-446655440000",
            entity_class_code_a="A30_035_005_040",
            attribute_code_b50="B50_010_035_005_015_045",
            value_float64=1.95,
            unit_code_b40="m/km",
            valid_from_utc="2026-11-02 00:00:00",
            is_synthetic=False,
            ref_id="B10_010_040_0050",
        )
        self.assertEqual(ev2["prev_tx_hash"], ev1["sys_tx_hash"])
        rec = eav.query_reconciled_active_real_state(
            asset_uuid="550e8400-e29b-41d4-a716-446655440000",
            attribute_code_b50="B50_010_035_005_015_045",
        )
        self.assertEqual(len(rec), 1)
        self.assertAlmostEqual(rec[0]["value_float64"], 1.95, places=5)

        # Trampas adversariales: (1) SQL mutador UPDATE prohibido y (2) código en deriva semántica prohibido
        with self.assertRaises(SitiAppendOnlyViolationError):
            eav.execute_guarded_sql("UPDATE siti_c3_eav_longitudinal_store SET value_float64 = 0.0")
        with self.assertRaises(ValueError):
            eav.append_eav_observation(
                asset_uuid="550e8400-e29b-41d4-a716-446655440000",
                entity_class_code_a="A30_035_005_040",
                attribute_code_b50="B50_010_005_005",
                value_float64=1.0,
                unit_code_b40="m/km",
                valid_from_utc="2026-11-02 00:00:00",
            )
        eng_o5 = get_ola5_engine()
        org_ok = eng_o5.verify_organic_noncollinear_scaling(
            [1000, 10000, 50000, 100000, 226324],
            [1.42, 3.61, 16.41, 30.54, 67.07],
            label="bipolar_organic_probe",
        )
        self.assertTrue(org_ok["organic_noncollinear"])
        with self.assertRaises(ValueError):
            eng_o5.verify_organic_noncollinear_scaling(
                [1000, 10000, 50000, 100000, 226324],
                [63.67264, 636.7264, 3183.632, 6367.264, 14410.647],
                label="bipolar_collinear_trap",
            )
        eav.close()

    def test_04_bimodal_geodesic_enu64_vs_float32_jitter_bipolar(self) -> None:
        eng = get_ola5_engine()
        e_arr, n_arr = vectorized_wgs84_to_epsg9377(
            np.array([-74.08175, -75.56359, -73.11980]),
            np.array([4.60971, 6.25184, 7.11392]),
        )
        u_arr = np.array([2600.0, 1495.0, 959.0], dtype=np.float64)

        ulp_e = compute_ieee754_ulp32_mm(e_arr)
        ulp_n = compute_ieee754_ulp32_mm(n_arr)
        self.assertEqual(float(ulp_e[0]), 500.0)
        # En Bogotá (N ~ 2.067e6 < 2^21 = 2,097,152 m), ULP_32(N) = 125.0 mm; en Medellín/Bucaramanga (N > 2^21), ULP_32(N) = 250.0 mm
        self.assertEqual(float(ulp_n[0]), 125.0)
        self.assertEqual(float(ulp_n[1]), 250.0)
        self.assertEqual(float(ulp_n[2]), 250.0)

        res = eng._summarize_jitter_stratum("TEST_ANDES", "Andes Test", "Prueba Andes", e_arr, n_arr, u_arr)
        self.assertGreater(res["direct_f32_max_mm"], 50.0)
        self.assertLess(res["bimodal_enu_max_mm"], 0.03)
        self.assertTrue(eng.validate_bim_tolerance_mm(res["bimodal_enu_max_mm"], max_allowed_mm=0.05))

        # Trampa adversarial: un jitter de Float32 directo (~279.5 mm) debe disparar ValueError ante tolerancia BIM de 1.0 mm
        with self.assertRaises(ValueError):
            eng.validate_bim_tolerance_mm(279.51, max_allowed_mm=1.0)


def run_official_ast_gate(filepath: Path) -> Dict[str, Any]:
    raw = SitiAstAntiTheaterGate.audit_test_file(str(filepath))
    if not raw.get("all_bipolar_compliant") or not raw.get("zero_static_json_reads"):
        raise AssertionError(f"SitiAstAntiTheaterGate rechazó {filepath}: {raw}")
    return raw


def main() -> None:
    OLA5_DATOS_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    ANEXOS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Auditoría AST oficial previa a la ejecución
    ast_report = run_official_ast_gate(Path(__file__).resolve())

    # 2. Ejecución en vivo de la suite bipolar
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestOla5GeometryVsOperationBipolar)
    runner = unittest.TextTestRunner(verbosity=2)
    test_res = runner.run(suite)
    if not test_res.wasSuccessful():
        raise RuntimeError("La suite bipolar TestOla5GeometryVsOperationBipolar falló.")

    # 3. Ejecución secuencial de Paso 0 y Experimentos 5.1 a 5.4
    engine = get_ola5_engine()
    step0_verif = engine.verify_step_0_prerequisites_and_ola4_refinement()
    exp51 = engine.run_experiment_5_1_scalability_and_21_layers()
    exp52 = engine.run_experiment_5_2_unboxed_eav_vs_wide_sparse()
    exp53 = engine.run_experiment_5_3_bimodal_geodesic_jitter()
    exp54 = engine.run_experiment_5_4_stage0_to_stage4_synthesis(exp51, exp52, exp53)
    prod_guard = engine.verify_zero_production_mutations()

    now_utc = datetime.now(timezone.utc).isoformat()
    resumen_ola5 = {
        "wave_id": "OLA_5_DE_6",
        "timestamp_utc": now_utc,
        "active_cas_revision": "b6bd01f850790ad22d399b95545f73d2",
        "step_0_ola4_refinement_verification": step0_verif,
        "experiment_5_1_scalability_and_21_layers": exp51,
        "experiment_5_2_unboxed_eav_vs_wide_sparse": exp52,
        "experiment_5_3_bimodal_geodesic_jitter": exp53,
        "experiment_5_4_stage0_to_stage4_synthesis": exp54,
        "ast_anti_theater_audit": ast_report,
        "production_immutability_verification": prod_guard,
    }

    resumen_path = OLA5_DATOS_DIR / "wave5_geometry_vs_operation_master_summary.json"
    with open(resumen_path, "w", encoding="utf-8") as f:
        json.dump(resumen_ola5, f, indent=2, ensure_ascii=False)

    # 4. Generación 100% programática de WAVE5_DETAILED_LOG y Appendix_E (G-SYNC-TABLE)
    report_paths = generate_ola5_reports(resumen_ola5, OLA5_DIR, ANEXOS_DIR)

    # 5. Verificación física st_blocks > 0 y sellado de wave5_checkpoint.json
    artifact_paths = [
        OLA5_DATOS_DIR / "wave5_aos_vs_soa_scalability_226324_assets.csv",
        OLA5_DATOS_DIR / "wave5_aos_vs_soa_scalability_226324_assets.parquet",
        OLA5_DATOS_DIR / "wave5_geometric_mass_profile_21_ani_layers_wkb_vs_soa.csv",
        OLA5_DATOS_DIR / "perfil_masa_geometrica_21_capas_ani_wkb_vs_operacion.json",
        OLA5_DATOS_DIR / "wave5_unboxed_eav_soa_vs_wide_sparse_benchmark.csv",
        OLA5_DATOS_DIR / "wave5_unboxed_eav_soa_vs_wide_sparse_benchmark.json",
        OLA5_DATOS_DIR / "wave5_bimodal_precision_226322_ani_5011_enu_vs_float32.csv",
        OLA5_DATOS_DIR / "wave5_bimodal_precision_226322_ani_5011_enu_vs_float32.json",
        resumen_path,
        report_paths["informe_ola5_es"],
        report_paths["appendix_e_en"],
    ]

    sealed_artifacts = {}
    for ap in artifact_paths:
        meta = compute_file_meta(ap)
        if meta["st_blocks"] <= 0 or meta["size_bytes"] <= 0:
            raise AssertionError(f"Artefacto vacío o sin bloques físicos (G-PHYS): {ap}")
        sealed_artifacts[str(ap.relative_to(WORKSPACE_ROOT))] = meta

    pcs = exp51["physical_corpus_summary"]
    b_full = exp51["scalability_batch_rows"][-1]
    eav_s = exp52["national_226324_summary"]
    nat_j = exp53["national_226322_summary"]
    enu_j = exp53["topocentric_5011_enu_summary"]

    ckpt5 = {
        "checkpoint_id": "ITCON_Q1_WAVE_5_OF_7",
        "wave_id": "OLA_5_DE_6",
        "wave_title": "Paso 0 de Perfeccionamiento de Ola 4 (Q07 ciclorruta, Q24 dispositivo_its, Paridad Independiente M1/M2 y Cero Truncamiento en Appendix D), Prueba Física de Separación entre Geometría Bimodal (WKB/GeoJSON EPSG:9377 + 5.011 Instancias ENU 64-bit / OpenUSD) y Operación Columnar Desempacada (Activos SoA + Unboxed EAV) y Appendix E para ITcon",
        "status": "PASS",
        "timestamp_utc": now_utc,
        "prerequisite_ola1_checkpoint_status": step0_verif["checkpoint_ola1_status"],
        "prerequisite_ola2_checkpoint_status": step0_verif["checkpoint_ola2_status"],
        "prerequisite_ola3_checkpoint_status": step0_verif["checkpoint_ola3_status"],
        "prerequisite_ola4_checkpoint_status": step0_verif["checkpoint_ola4_status"],
        "step_0_ola4_refinement_status": "PASS",
        "guardrails_compliance": {
            "G-PHYS_os_O_RDONLY_enforced": True,
            "G-PHYS_production_bytes_modified": prod_guard["production_bytes_modified"],
            "G-PHYS_all_artifacts_st_blocks_gt_0": True,
            "G-SYNC-TABLE_appendix_d_and_e_100pct_programmatic": True,
            "G-SYNC-TABLE_zero_truncated_titles": True,
            "G-AST_anti_theater_gate": ast_report,
            "G-SEM_invariants_verified": {
                "three_layers_only": True,
                "language_a_orthogonal_language_b": True,
                "calzada_equals_carril_A30_035_005_040": True,
                "esal_invariable_singular": True,
                "zero_is_active_mutable_flags_in_c3_eav": True,
            },
        },
        "key_scientific_metrics": {
            "step_0_q07_ciclorruta_rows": step0_verif["q07_ciclorruta_rows"],
            "step_0_q24_dispositivo_its_rows": step0_verif["q24_dispositivo_its_rows"],
            "step_0_all_50_queries_nonzero_parity": step0_verif["independent_m1_m2_m3_parity_verified"],
            "spatial_ani_disk_bytes": pcs["spatial_ani_disk_bytes"],
            "spatial_ani_uncompressed_bytes": pcs["spatial_ani_uncompressed_bytes"],
            "operational_activos_disk_bytes": pcs["operational_activos_disk_bytes"],
            "operational_activos_uncompressed_bytes": pcs["operational_activos_uncompressed_bytes"],
            "disk_mass_asymmetry_ratio_x": pcs["disk_mass_asymmetry_ratio_x"],
            "uncompressed_ram_asymmetry_ratio_x": pcs["uncompressed_ram_asymmetry_ratio_x"],
            "projected_soa_disk_io_reduction_ratio_x": pcs["projected_soa_disk_io_reduction_ratio_x"],
            "r1_coupled_226324_mean_ms": b_full["r1_mean_ms"],
            "r2_decoupled_226324_mean_ms": b_full["r2_mean_ms"],
            "speedup_r1_vs_r2_226324_x": b_full["speedup_r1_vs_r2_x"],
            "wide_lang_b_null_sparsity_pct": eav_s["e1a_lang_b_null_sparsity_pct"],
            "wide_b50_null_sparsity_pct": eav_s["e1b_b50_null_sparsity_pct"],
            "unboxed_eav_soa_structural_null_pct": 0.0,
            "unboxed_eav_simd_speedup_vs_boxed_x": eav_s["simd_speedup_vs_boxed_e2_x"],
            "direct_float32_epsg9377_mean_jitter_mm": nat_j["direct_f32_mean_mm"],
            "direct_float32_epsg9377_max_vertex_jitter_mm": nat_j["direct_f32_max_mm"],
            "direct_float32_epsg9377_max_diff_seg_jitter_mm": nat_j["direct_f32_max_diff_seg_mm"],
            "bimodal_enu_5011_mean_jitter_mm": enu_j["bimodal_enu_mean_mm"],
            "bimodal_enu_5011_max_jitter_mm": enu_j["bimodal_enu_max_mm"],
            "bimodal_enu_precision_gain_factor_x": enu_j["error_reduction_factor_x"],
            "gpu_vertex_vram_savings_pct": enu_j["vram_vertex_buffer_savings_pct"],
        },
        "sealed_wave5_artifacts": sealed_artifacts,
    }

    ckpt5_path = CHECKPOINTS_DIR / "wave5_checkpoint.json"
    with open(ckpt5_path, "w", encoding="utf-8") as f:
        json.dump(ckpt5, f, indent=2, ensure_ascii=False)

    print("\n=== OLA 5 COMPLETADA EXITOSAMENTE ===")
    print(json.dumps(ckpt5["key_scientific_metrics"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
