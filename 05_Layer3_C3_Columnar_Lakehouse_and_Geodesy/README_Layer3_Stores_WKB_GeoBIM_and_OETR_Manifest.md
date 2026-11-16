# SITI Layer 3 (C3) Columnar Lakehouse, Public Anonymization Protocol, and Cryptographic Manifest (ITcon Vol. 32, 2027)

## 1. Read-Only Reproducibility & Colombian Data-Protection Compliance (`C68`)
All empirical benchmarks in Waves 1–6 and the live six-paradigm ablation (`DR3-4`) accessed the production SITI Layer 3 (`C3`) lakehouse strictly via read-only file descriptors (`os.O_RDONLY`), mutating `0` bytes. Under Colombian data-protection regulations (Law 1581/2012 and Law 1712/2014), all `20` primary `C3` Parquet containers were forensically audited:
- **`18 / 20` containers hold zero tax or personal cadastral PII** (`measurement_unit` in `siti_apu_invias_desacoplado_ab.parquet` encodes physical engineering units `m`, `m2`, `m3`, `kg`, `ha`, `u`) and are distributed verbatim with bit-identical `SHA-256` digests.
- **`2 / 20` containers undergo deterministic `SHA-256` pseudonymization prior to public distribution** while preserving `100%` `Q15` analytical and topological parity:
  1. `siti_ani_proyectos.parquet` (internal `6,313` B, `032e0f8f67fca336`) -> **`siti_ani_proyectos_public_anonymized.parquet`** (`6,651` B, `48c07b0a2ce15783`, masking `nit` via `ANON_NIT_<SHA256[:12]>`). The unredacted internal `siti_ani_proyectos_maestros.parquet` is excluded from public archives.
  2. `assets_predios_cadastre.parquet` (internal `13,128` B, `888ccecc205df0fa`) -> **`assets_predios_cadastre_public_anonymized.parquet`** (`13,534` B, `72f552c4d4c67b96`, masking `cedula_catastral`, `folio_matricula`, and `propietario_titular`).

## 2. Included Layer 3 (`C3`) Containers in Subfolder `05_` (Exact Bit-Verified Digests)
- `siti_ani_activos_principales.parquet` (`18,480,056` B, `SHA-256[:16] = 93a4451ac1794a24`, `226,324` concessioned assets).
- `siti_ani_activos_principales_soa_8cols.parquet` (`225,011` B, `SHA-256[:16] = 0ed123eab69a0b13`, `8`-column projected SoA store (`220,085` B internal slice)).
- `siti_c3_unboxed_eav_b50_2715888_seed20261102.parquet` (`25,652,802` B, `SHA-256[:16] = 21059f48f53be866`, `2,715,888` Unboxed EAV `UUIDv7` telemetry tuples — `Scheme E3`).
- `assets_spatial_instances.parquet` (`971,910` B, `SHA-256[:16] = 8d4f1f55dd49cbf7`, `5,011` bimodal `64-bit EPSG:9377 + 32-bit local ENU` instances).
- `siti_ani_proyectos_public_anonymized.parquet` (`6,651` B, `SHA-256[:16] = 48c07b0a2ce15783`, `50` master concessions, PII-masked).
- `assets_predios_cadastre_public_anonymized.parquet` (`13,534` B, `SHA-256[:16] = 72f552c4d4c67b96`, `1,425` cadastral parcels, PII-masked).
- `siti_matriz_confrontacion_diferencial_ab.parquet` (`842,642` B, `SHA-256[:16] = d13a0f734fcebdfa`, `18,112` normative specification units).
- `siti_apu_invias_desacoplado_ab.parquet` (`58,551` B, `SHA-256[:16] = dff6acc882e7f050`, `526` base INVIAS APU items -> `73,640` regional compositions).
- `siti_ingesta_documental_grounding_tricapa.parquet` (`72,628` B, `SHA-256[:16] = ac59fc01cf88fc80`, `603` CDE reception envelopes).

## 3. External Large Spatial Store & Multi-File Collection Serialization Rules (`C71`)
- **Detached National OGC WKB Store (`assets_spatial_instances_ani.parquet`)**: `455,875,112` B (`SHA-256[:16] = 0d7d2f2ed178fe23`, `226,322` spatial rows / `225,244` `EPSG:9377` `WKB` geometries, `23,263,741` 2D vertices); layer-level byte profile in `07_Experiments_Waves_1_to_6_Empirical_Results_Datasets/Wave_5_Geometry_vs_Operation_and_Bimodal_ENU/perfil_masa_geometrica_21_capas_ani_wkb_vs_operacion.csv`.
- **`9` Shift-Left GeoBIM Kits (`51` unique files, `124,060,870` B)**: Wave 4 `<path>|<bytes>|<sha256><LF>` manifest `f8d93f7313919ca2`; portable relative POSIX `<relpath><TAB><bytes><TAB><sha256><LF>` manifest `a3069d09a8f053a7`.
- **`5` Canonical OETR Toll/WIM Parquets (`10,939,296` B, `360,157` rows)**: lexicographical `<relpath><TAB><bytes><TAB><sha256><LF>` manifest `09fdc02f478ce5c6` (`peajes_ani_detalles_global.parquet`: `e808d8a980b40102`; `peajes_ani_encabezados_global.parquet`: `63736bcba3c6c305`; `capa3_peajes_ani_serie_historica.parquet`: `5792f8c1ca7194f9`; `capa3_peajes_ani_estaciones_maestro.parquet`: `bc6c59f9f645ec01`; `capa3_peajes_ani_resumen_oetr.parquet`: `17a399726a83f5f8`).


## Additional Canonical OETR Toll/WIM & IoT Telemetry Containers (Table 8 Row 12)

When assembling the full-scale archive on the author workstation (`finalize_local_c3_and_build_single_zip.py`), the following read-only production containers (`os.O_RDONLY`) are verified against their **Table 8 Row 12** `SHA-256` digests and placed directly in this folder (`05_Layer3_C3_Columnar_Lakehouse_and_Geodesy/`):

| Canonical Filename | Rows | Exact Size (Bytes) | SHA-256 Prefix (Table 8 Row 12) |
| :--- | ---: | ---: | :--- |
| `peajes_ani_detalles_global.parquet` | 171,420 | 4,146,491 | `e808d8a980b40102` |
| `peajes_ani_encabezados_global.parquet` | 17,041 | 336,955 | `63736bcba3c6c305` |
| `capa3_peajes_ani_serie_historica.parquet` | 171,420 | 6,444,394 | `5792f8c1ca7194f9` |
| `capa3_peajes_ani_estaciones_maestro.parquet` | 197 | 7,455 | `bc6c59f9f645ec01` |
| `capa3_peajes_ani_resumen_oetr.parquet` | 79 | 4,001 | `17a399726a83f5f8` |
| `telemetry_iot_sensors.parquet` | 100,000 | 2,628,249 | `88a384d0d060c5b2` |
