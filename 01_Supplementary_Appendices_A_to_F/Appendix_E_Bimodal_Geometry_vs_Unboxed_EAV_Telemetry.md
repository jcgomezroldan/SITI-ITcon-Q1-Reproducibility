# Supplementary Appendix E: Physical Separation of Bimodal Geodesic Geometry from Unboxed Columnar Operational Telemetry in Layer 3 (C3)

**Manuscript Title:** *Orthogonal Ontology Factorization for Semantic Interoperability in Transport Infrastructure* (`ORTHOGONAL ONTOLOGY FACTORIZATION FOR SEMANTIC INTEROPERABILITY IN TRANSPORT INFRASTRUCTURE`)  
**Authors:** Juan C. Gómez (Corresponding Author; PhD candidate, Doctoral program in Technology Innovation Management, Universidad de los Andes, and National Infrastructure Agency (ANI), Bogotá, Colombia, `jc.gomez1988@uniandes.edu.co`), Rodrigo F. Herrera (Associate professor, School of Civil Engineering, Pontificia Universidad Católica de Valparaíso, Valparaíso, Chile, `rodrigo.herrera@pucv.cl`), Karen M. Castañeda (Assistant professor, School of Civil Engineering, Pontificia Universidad Católica de Valparaíso, Valparaíso, Chile, `karen.castaneda@pucv.cl`), and Juan F. Correal (Full professor, Department of Civil and Environmental Engineering, Universidad de los Andes, Bogotá, Colombia, `jcorreal@uniandes.edu.co`)  
**Reference:** Gómez, J. C., Herrera, R. F., Castañeda, K. M., & Correal, J. F. (2027). Orthogonal ontology factorization for semantic interoperability in transport infrastructure. *Journal of Information Technology in Construction (ITcon)*, 32, 1-X. https://doi.org/10.36680/j.itcon.2027.[added by editor]  
**Target Journal:** *Journal of Information Technology in Construction (ITcon)* — Q1 Peer-Reviewed Submission (Layer 3 Physical Decoupling and Columnar Telemetry Verification)  
**Active SITI CAS Semantic Publication:** `b6bd01f850790ad22d399b95545f73d2` (`Stage S4`)  
**Execution Timestamp (UTC):** `2026-11-02T21:14:29.212386+00:00`  
**Forensic Verification Protocol:** Strict `os.O_RDONLY` ingestion (`0` bytes modified across `siti_production_corpus/`, `bundles/`, `Kits_BIM/`, `Kits_GIS/`, and all 9 primary repositories), deterministic Abstract Syntax Tree (AST) live bipolar verification (`4/4` compliant methods, `39` live engine calls, `0` static JSON reads), and 100% programmatic Stage 5 (Automated Manuscript-to-Corpus Table Synchronization) synchronization.

---

## E.1 Architectural Rationale for Physical Geometry-versus-Operation Decoupling

Coupled monolithic geometry-and-telemetry architectures that load full 3D/2D coordinate meshes into memory alongside operational attributes (such as synthetic 4.35 GB monolithic workloads evaluated on 1 TB RAM servers) obscure the physical mechanism through which legacy civil infrastructure achieves scalable interoperability on commodity hardware. This appendix provides reproducible physical measurements over the audited SITI Layer 3 production lakehouse (`telemetry_parquet_store/`), testing the first pillar of the post-coordinated interoperability hypothesis:

> *For legacy infrastructure, semantic interoperability is achieved more effectively by separating geometric information from operational information and reconstructing relationships dynamically at query time.*

Across Colombia's national concessioned road, railway, and airport network (`N = 226,324` inventoried assets across `21` functional asset layers), separating geometric payloads from operational telemetry yields three mathematically governed advantages:

1. **Physical Storage and Bandwidth Asymmetry (`24.67×` on Disk, `32.11×` in Uncompressed RAM):**
   - The national spatial container `telemetry_parquet_store/assets_spatial_instances_ani.parquet` (`226,322` geometry instances carrying `MAGNA-SIRGAS EPSG:9377` and `WGS84 EPSG:4326` `GeoJSON`/coordinate payloads totaling `23,263,741` 2D vertices) occupies **`455,875,112` bytes (`455.88 MB`)** on disk (reported as `454.32 MB` in the Wave 1 nominal pre-index snapshot) and expands to **`1,394,990,868` bytes (`1,394.99 MB` / `1.395 GB`)** in uncompressed Arrow/Parquet memory, of which **`98.82%`** consists strictly of coordinate buffers.
   - Conversely, the decoupled operational inventory `telemetry_parquet_store/siti_ani_activos_principales.parquet` (`226,324` rows across `30` semantic, contractual, and condition columns—`21` core operational attributes plus `9` forensic lineage columns) occupies only **`18,480,056` bytes (`18.48 MB`)** on disk (`19.21 MB` nominal) and **`43,441,449` bytes (`43.44 MB`)** uncompressed—a **`24.67×` reduction in physical disk mass** (`23.65×` nominal) and a **`2,071.36×` (`99.95%`) I/O reduction** when projecting operational columns in `SoA` (`0.220 MB`). Similarly, national OETR toll telemetry (`peajes_ani_detalles_global.parquet` + `peajes_ani_encabezados_global.parquet`) occupies `4.48 MB`, and the decoupled INVIAS unit-price catalog (`siti_apu_invias_desacoplado_ab.parquet`, `526` national items representing `73,640` regional rows across `140` books) occupies `58.55 KB` deduplicated (`3.81 MB` expanded).
2. **Sparsity Collapse via `Unboxed EAV` in `SoA` (`99.90%` $\to$ `0.00%` Structural Null Padding):**
   - Coupling SITI Language B's `11,544` operational classes (or its `738` `B50` performance/cost indicator classes and `100` SHACL-governed parametric shapes `PAR_B50_0001..0100`) directly onto `226,324` physical assets creates a `2,617,437,060`-cell sparse matrix (`11,565` columns: `21` dense base + `11,544` `Language B`) with **`99.7147%` total-table `NULL` cells** (`99.8960%` across the `11,544` `Language B` columns; and **`95.6522%` total-table `NULL` cells** [`98.3740%` across `738` `B50` columns] for the `759`-column `B50` wide table). The Layer 3 Unboxed EAV columnar storage engine removes wide-table null bitmaps by storing strongly typed primitive vectors (`val_float64`, `val_int64`, `val_string`, `val_bool`) reconciled via immutable bitemporal windowing (`ROW_NUMBER() OVER (PARTITION BY asset_uuid, attribute_code_b50 ORDER BY valid_from_utc DESC, sys_created_at_utc DESC)`) with **`0` mutable `is_active` flags** and RFC 9562 `UUIDv7` + `SHA-256` cryptographic hash chaining.
3. **Suppression of IEEE 754 `Float32` *GPU Vertex Jitter* via Bimodal Geodesic Storage (`143.55 mm` $\to$ `0.0054 mm`):**
   - National `MAGNA-SIRGAS EPSG:9377` coordinates ($E \approx 4.88 \times 10^6\text{ m}, N \approx 2.06 \times 10^6\text{ m}$) exceed the 24-bit significand precision of `IEEE 754 Float32`, where $\text{ULP}_{32}(E) = 500.0\text{ mm}$ and $\text{ULP}_{32}(N) = 250.0\text{ mm}$, inducing **`143.55 mm` mean (`279.24 mm` single-vertex max; `543.29 mm` adjacent-vertex differential distortion)** in direct GPU rendering. SITI's bimodal architecture (`assets_spatial_instances.parquet`, `5,011` topocentric `ENU` / `OpenUSD` instances) retains `Float64` cell anchors $(E_0, N_0, U_0)$ on CPU while transmitting local offsets $(\Delta e, \Delta n, \Delta u)$ ($\|\Delta\mathbf{v}\|_{\infty} \le 250\text{ m}$ within $500\text{ m}$ topocentric corridor sectors) via $4 \times 4$ `Float32` affine matrices, compressing mean quantization error to **`0.0052 mm` (`25,697×` precision gain in `ENU`; `26,358×` across `225,244` national geometries)** while saving **`50.0%` of GPU vertex buffer VRAM**.

> **Cross-Layer Query Parity Note:** Across all `50/50` canonical lifecycle queries evaluated in `Appendix D` (`Q07` `ciclorruta` = `98` assets; `Q24` `dispositivo_its` = `6,552` assets), all six execution paradigms (`M1, M1b, M2, M2b, M2c, M3`) compute `row_count` and `agg_val` independently with `< 1e-5` numerical parity.

---

## E.2 Physical Payload Asymmetry Across All 21 National Infrastructure Asset Layers (`Table E.1`)

Just four linear/polygonal corridor layers—`berma`, `calzada`, `separador`, and `cuneta`—concentrate **`1,313.87 MB` (`94.19%`)** of the entire uncompressed national geometric payload. Dragging these multi-megabyte coordinate arrays during non-spatial accounting, toll revenue, or unit-price queries constitutes pure I/O waste.

### Table E.1: Physical Payload Asymmetry Across All 21 National Infrastructure Asset Layers ($N = 226,324$)

| Rank | National Functional Layer (`tabla_origen_ani`) | SITI Table | Dominant Primitive | Operational Rows | Spatial Rows | Exact 2D Vertices | Mean Vertices / Asset | OGC `WKB` `Float64` (MB) | Uncompressed `GeoJSON` RAM (MB) | Est. Coupled Disk (MB) | Uncompressed Operational RAM (MB) | Est. Operational Disk (MB) | RAM Asymmetry Ratio | Share of National Geometry (\%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `1` | `berma` (Paved Shoulder & Lateral Strip) | `A30` | `MultiPolygon` | `22,420` | `22,419` | `12,670,122` | `565.1` | `203.22` | `743.87` | `243.09` | `3.598` | `1.531` | **`206.7×`** | `53.32%` |
| `2` | `calzada` (Traffic Lane — Calzada SITI = carril) | `A30` | `MultiPolygon` | `10,710` | `10,710` | `6,474,498` | `604.5` | `103.83` | `380.00` | `124.18` | `1.801` | `0.766` | **`210.9×`** | `27.24%` |
| `3` | `separador` (Median Strip & Central Reserve) | `A30` | `MultiPolygon` | `6,149` | `6,149` | `2,457,832` | `399.7` | `39.46` | `144.66` | `47.27` | `1.078` | `0.459` | **`134.2×`** | `10.37%` |
| `4` | `cuneta` (Longitudinal Drainage Gutter) | `A50` | `MultiLineString` | `33,801` | `33,801` | `676,639` | `20.0` | `11.43` | `45.35` | `14.82` | `5.999` | `2.552` | **`7.6×`** | `3.25%` |
| `5` | `defensa_vial` (Containment Barrier & Guardrail) | `A50` | `MultiLineString` | `16,348` | `16,348` | `276,604` | `16.9` | `4.72` | `19.11` | `6.24` | `3.201` | `1.362` | **`6.0×`** | `1.37%` |
| `6` | `senal_vertical` (Retroreflective Vertical Signage) | `A50` | `Point` | `87,639` | `87,639` | `87,263` | `1.0` | `1.84` | `18.11` | `5.92` | `18.201` | `7.743` | **`1.0×`** | `1.30%` |
| `7` | `predio` (Cadastral Right-of-Way Parcel) | `A10` | `MultiPolygon` | `1,425` | `1,425` | `211,845` | `148.7` | `3.42` | `12.80` | `4.18` | `0.263` | `0.112` | **`48.7×`** | `0.92%` |
| `8` | `talud` (Engineered Cut/Fill Slope) | `A30` | `MultiPolygon` | `2,074` | `2,074` | `203,070` | `97.9` | `3.29` | `12.16` | `3.97` | `0.421` | `0.179` | **`28.9×`** | `0.87%` |
| `9` | `drenajes` (Cross-Drainage Culvert & Hydraulic Work) | `A50` | `Point` | `18,055` | `18,055` | `18,052` | `1.0` | `0.38` | `3.73` | `1.22` | `3.845` | `1.636` | **`1.0×`** | `0.27%` |
| `10` | `puente` (Vehicular Bridge & Viaduct Complex) | `A20` | `MultiPolygon` | `1,194` | `1,194` | `50,276` | `42.1` | `0.83` | `3.14` | `1.03` | `0.207` | `0.088` | **`15.2×`** | `0.22%` |
| `11` | `luminarias` (Roadway Luminaire & Lighting Pole) | `A50` | `Point` | `16,844` | `16,844` | `16,240` | `1.0` | `0.35` | `3.46` | `1.13` | `2.986` | `1.270` | **`1.2×`** | `0.25%` |
| `12` | `tunel` (Road Tunnel & Portal Complex) | `A20` | `MultiPolygon` | `62` | `62` | `38,589` | `622.4` | `0.62` | `2.26` | `0.74` | `0.011` | `0.005` | **`202.0×`** | `0.16%` |
| `13` | `ciclorruta` (Segregated Cycleway Path) | `A50` | `MultiPolygon` | `98` | `98` | `35,696` | `364.2` | `0.57` | `2.10` | `0.69` | `0.018` | `0.008` | **`117.6×`** | `0.15%` |
| `14` | `muro` (Retaining Wall & Earth Structure) | `A50` | `MultiLineString` | `2,744` | `2,744` | `26,347` | `9.6` | `0.47` | `2.02` | `0.66` | `0.521` | `0.222` | **`3.9×`** | `0.14%` |
| `15` | `dispositivo_its` (ITS Telemetry & Fiber-Optic Node) | `A40` | `Point` | `6,552` | `6,552` | `6,537` | `1.0` | `0.14` | `1.36` | `0.44` | `1.254` | `0.533` | **`1.1×`** | `0.10%` |
| `16` | `estacion_pesaje` (Weigh-in-Motion & Static Scale Station) | `A20` | `MultiPolygon` | `63` | `62` | `6,310` | `101.8` | `0.10` | `0.38` | `0.12` | `0.012` | `0.005` | **`31.8×`** | `0.03%` |
| `17` | `estacion_peaje` (Toll Collection Plaza) | `A20` | `MultiPolygon` | `79` | `79` | `4,603` | `58.3` | `0.08` | `0.28` | `0.09` | `0.014` | `0.006` | **`20.4×`** | `0.02%` |
| `18` | `zona_servicio` (Roadside Service & Rest Area) | `A30` | `MultiPolygon` | `27` | `27` | `1,874` | `69.4` | `0.03` | `0.11` | `0.04` | `0.005` | `0.002` | **`22.0×`** | `0.01%` |
| `19` | `cco` (Operational Control Center & Rail Station) | `A20` | `MultiPolygon` | `34` | `34` | `1,338` | `39.4` | `0.02` | `0.08` | `0.03` | `0.006` | `0.002` | **`15.1×`** | `0.01%` |
| `20` | `aeropuerto_terminal` (Concessioned Airport Terminal) | `A20` | `Point` | `4` | `4` | `4` | `1.0` | `0.00` | `0.00` | `0.00` | `0.001` | `0.000` | **`0.9×`** | `0.00%` |
| `21` | `aeropuerto_torre` (Airport Control Tower) | `A20` | `Point` | `2` | `2` | `2` | `1.0` | `0.00` | `0.00` | `0.00` | `0.000` | `0.000` | **`0.9×`** | `0.00%` |
| **TOTAL** | **All 21 National Functional Layers (`telemetry_parquet_store/`)** | **`A10–A50`** | **Mixed 2D/3D** | **`226,324`** | **`226,322`** | **`23,263,741`** | **`102.8`** | **`374.81`** | **`1,394.99`** | **`455.88`** | **`43.44`** | **`18.48`** | **`32.11×` RAM / `24.67×` Disk** | **`100.00%`** |

---

## E.3 Empirical Scalability ($N = 1,000 \dots 226,324$) and Selective Query-Time Late Spatial Materialization (`Table E.2`)

At full national scale ($N = 226,324$, `3` warmup + `15` timed iterations via `time.perf_counter_ns()`), decoupled operational scanning (`R2`, `0%` geometry) executes in **`3.728 ± 0.628 ms`**, achieving a **`22.27×` speedup** and **`99.97%` memory footprint reduction** relative to monolithic coupled geometry+operation scanning (`R1`, `83.00 ± 2.39 ms`). When spatial reconstruction is selectively required (`R3`), materializing `1.0%` (`2,263` assets) or `5.0%` (`11,316` assets) of geometries at query time retains **`12.16×`** and **`10.35×`** speedups while saving **`98.99%`** and **`95.15%`** of disk I/O traffic, respectively.

### Table E.2 (Panel A): Batch Scalability ($N = 1,000 \dots 226,324$)

| Batch Size $N$ | `R1` Coupled Disk I/O (MB) | `R1` Uncompressed RAM (MB) | `R1` Latency Mean ± SD (ms) | `R1` $p_{50} / p_{95} / p_{99}$ (ms) | `R1` Throughput (MB/s) | `R2` Decoupled Disk I/O (MB) | `R2` Uncompressed RAM (MB) | `R2` Latency Mean ± SD (ms) | `R2` $p_{50} / p_{95} / p_{99}$ (ms) | `R2` Throughput (MB/s) | Speedup $S_{\text{R1/R2}}$ | RAM Saved (\%) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `1,000` | `2.10` | `6.39` | `7.02 ± 0.64` | `6.92 / 8.01 / 8.29` | `910.2` | `0.001` | `0.002` | `1.772 ± 0.507` | `1.597 / 2.482 / 2.955` | `0.9` | **`3.96×`** | **`99.97%`** |
| `5,000` | `10.48` | `29.20` | `7.28 ± 0.52` | `7.08 / 8.24 / 8.28` | `4,012.2` | `0.005` | `0.008` | `1.875 ± 0.487` | `1.937 / 2.735 / 2.751` | `4.3` | **`3.88×`** | **`99.97%`** |
| `10,000` | `20.96` | `58.96` | `8.22 ± 0.54` | `8.10 / 9.16 / 9.28` | `7,172.5` | `0.010` | `0.016` | `1.782 ± 0.367` | `1.696 / 2.358 / 2.460` | `9.0` | **`4.61×`** | **`99.97%`** |
| `25,000` | `52.40` | `156.20` | `13.95 ± 0.82` | `13.71 / 15.43 / 15.68` | `11,197.7` | `0.024` | `0.040` | `2.370 ± 0.708` | `2.308 / 3.567 / 3.650` | `17.0` | **`5.89×`** | **`99.97%`** |
| `50,000` | `104.80` | `311.05` | `23.87 ± 1.02` | `23.73 / 25.49 / 25.50` | `13,029.0` | `0.049` | `0.081` | `2.565 ± 0.494` | `2.543 / 3.186 / 3.195` | `31.4` | **`9.31×`** | **`99.97%`** |
| `100,000` | `209.59` | `620.91` | `41.79 ± 1.37` | `41.86 / 43.75 / 43.92` | `14,857.5` | `0.097` | `0.161` | `3.098 ± 0.587` | `2.947 / 3.893 / 4.009` | `52.0` | **`13.49×`** | **`99.97%`** |
| `150,000` | `314.39` | `932.31` | `59.45 ± 1.85` | `60.04 / 61.32 / 61.65` | `15,682.9` | `0.146` | `0.242` | `2.944 ± 0.374` | `2.978 / 3.471 / 3.552` | `82.1` | **`20.19×`** | **`99.97%`** |
| `226,324` | `474.36` | `1,398.40` | `83.00 ± 2.39` | `82.58 / 86.45 / 86.86` | `16,847.8` | `0.220` | `0.365` | `3.728 ± 0.628` | `3.603 / 4.805 / 5.000` | `97.8` | **`22.27×`** | **`99.97%`** |

### Table E.2 (Panel B): Selective Query-Time Late Spatial Materialization ($p = 0.0\% \dots 100.0\%$ at $N = 226,324$)

| Spatial Predicate Selectivity $p$ (\%) | Regime | Reconstructed Spatial Assets | Total Disk I/O Read (MB) | Materialized Geometry Buffer in RAM (MB) | Latency Mean ± SD (ms) | $p_{50} / p_{95} / p_{99}$ (ms) | Speedup vs. Monolithic `R1` | Disk I/O Traffic Saved vs. `R1` (\%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `0.0%` | `R2 (0% Geometry)` | `0` | `0.220` | `0.000` | `2.842 ± 0.237` | `2.796 / 3.218 / 3.518` | **`29.20×`** | **`99.95%`** |
| `0.1%` | `R3 (Late p=0.1%)` | `226` | `0.676` | `0.546` | `6.542 ± 0.474` | `6.383 / 7.511 / 7.553` | **`12.69×`** | **`99.86%`** |
| `1.0%` | `R3 (Late p=1.0%)` | `2,263` | `4.779` | `6.816` | `6.828 ± 0.278` | `6.886 / 7.203 / 7.289` | **`12.16×`** | **`98.99%`** |
| `5.0%` | `R3 (Late p=5.0%)` | `11,316` | `23.014` | `35.677` | `8.021 ± 0.636` | `7.852 / 8.922 / 8.938` | **`10.35×`** | **`95.15%`** |
| `10.0%` | `R3 (Late p=10.0%)` | `22,632` | `45.808` | `73.354` | `10.627 ± 0.747` | `10.421 / 11.992 / 12.083` | **`7.81×`** | **`90.34%`** |
| `25.0%` | `R3 (Late p=25.0%)` | `56,581` | `114.189` | `178.236` | `17.180 ± 0.910` | `16.852 / 18.494 / 19.356` | **`4.83×`** | **`75.93%`** |
| `100.0%` | `R3 (Late p=100.0%)` | `226,324` | `456.095` | `721.266` | `47.442 ± 1.385` | `47.030 / 49.255 / 49.425` | **`1.75×`** | **`3.85%`** |

---

## E.4 `Unboxed EAV` in `SoA` (`UUIDv7` + `ROW_NUMBER()` Windowing) vs. Coupled Wide Sparse Tables (`Table E.3`)

### Table E.3: Unboxed EAV in SoA (UUIDv7 + ROW_NUMBER() Windowing) vs. Coupled Wide Sparse Tables

| Asset Batch $N$ | Storage Architecture & Temporal Model | Schema Width (Cols) | Total Matrix Cells / Tuples | Non-Null Active Cells | Structural `NULL` Sparsity (\%) | Wasted Null-Bitmap & Pointer RAM (MB) | Total In-Memory Footprint (MB) | ZSTD Parquet Disk Size (MB) | Vectorized SIMD Scan Mean ± SD (ms) | Temporal State Update / Window Reconciliation (ms) | `UUIDv7` + `SHA-256` Chain Audit (ms) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `1,000` | **E1a: Language B Wide Sparse Columnar Arrow (11,565 cols)** | `11,565` | `11,565,000` | `33,000` | **`99.7147%` (`99.8960%` B-cols)** | `93.70` | `93.77` | `4.03` | `19.878 ± 0.373` | `276.359` | `N/A (Mutable)` |
| `1,000` | **E1b: B50 Indicator Wide Sparse Columnar Arrow (759 cols)** | `759` | `759,000` | `33,000` | **`95.6522%` (`98.3740%` B50-cols)** | `5.90` | `6.15` | `0.53` | `1.467 ± 0.132` | `23.346` | `N/A (Mutable)` |
| `1,000` | **E2: Traditional Boxed VARCHAR EAV + Mutable is_active** | `5` | `12,000` | `12,000` | **`0.0000%`** | `0.35` | `0.73` | `0.09` | `0.354 ± 0.021` | `2.291` | `N/A (Mutable)` |
| `1,000` | **E3: SITI Unboxed EAV in SoA (UUIDv7 + ROW_NUMBER(), 0 is_active)** | `5` | `12,000` | `12,000` | **`0.0000%`** | `0.00` | `0.38` | `0.15` | `0.283 ± 0.093` | `1.823` | `0.06` |
| `10,000` | **E1a: Language B Wide Sparse Columnar Arrow (11,565 cols)** | `11,565` | `115,650,000` | `330,000` | **`99.7147%` (`99.8960%` B-cols)** | `936.98` | `937.73` | `8.41` | `35.420 ± 2.118` | `730.708` | `N/A (Mutable)` |
| `10,000` | **E1b: B50 Indicator Wide Sparse Columnar Arrow (759 cols)** | `759` | `7,590,000` | `330,000` | **`95.6522%` (`98.3740%` B50-cols)** | `58.99` | `61.52` | `3.24` | `4.179 ± 0.392` | `63.323` | `N/A (Mutable)` |
| `10,000` | **E2: Traditional Boxed VARCHAR EAV + Mutable is_active** | `5` | `120,000` | `120,000` | **`0.0000%`** | `3.48` | `7.32` | `0.80` | `2.375 ± 0.185` | `14.046` | `N/A (Mutable)` |
| `10,000` | **E3: SITI Unboxed EAV in SoA (UUIDv7 + ROW_NUMBER(), 0 is_active)** | `5` | `120,000` | `120,000` | **`0.0000%`** | `0.00` | `3.84` | `1.53` | `1.509 ± 0.153` | `2.275` | `0.58` |
| `50,000` | **E1a: Language B Wide Sparse Columnar Arrow (11,565 cols)** | `11,565` | `578,250,000` | `1,650,000` | **`99.7147%` (`99.8960%` B-cols)** | `4,684.88` | `4,688.67` | `29.19` | `168.338 ± 2.419` | `2,703.341` | `N/A (Mutable)` |
| `50,000` | **E1b: B50 Indicator Wide Sparse Columnar Arrow (759 cols)** | `759` | `37,950,000` | `1,650,000` | **`95.6522%` (`98.3740%` B50-cols)** | `294.94` | `307.60` | `15.56` | `16.831 ± 0.474` | `261.460` | `N/A (Mutable)` |
| `50,000` | **E2: Traditional Boxed VARCHAR EAV + Mutable is_active** | `5` | `600,000` | `600,000` | **`0.0000%`** | `17.39` | `36.60` | `3.40` | `2.542 ± 0.080` | `61.692` | `N/A (Mutable)` |
| `50,000` | **E3: SITI Unboxed EAV in SoA (UUIDv7 + ROW_NUMBER(), 0 is_active)** | `5` | `600,000` | `600,000` | **`0.0000%`** | `0.00` | `19.20` | `5.83` | `1.709 ± 0.068` | `3.172` | `2.83` |
| `100,000` | **E1a: Language B Wide Sparse Columnar Arrow (11,565 cols)** | `11,565` | `1,156,500,000` | `3,300,000` | **`99.7147%` (`99.8960%` B-cols)** | `9,369.75` | `9,377.34` | `55.57` | `306.055 ± 2.580` | `5,075.312` | `N/A (Mutable)` |
| `100,000` | **E1b: B50 Indicator Wide Sparse Columnar Arrow (759 cols)** | `759` | `75,900,000` | `3,300,000` | **`95.6522%` (`98.3740%` B50-cols)** | `589.88` | `615.20` | `31.14` | `31.451 ± 1.991` | `422.398` | `N/A (Mutable)` |
| `100,000` | **E2: Traditional Boxed VARCHAR EAV + Mutable is_active** | `5` | `1,200,000` | `1,200,000` | **`0.0000%`** | `34.79` | `73.19` | `6.81` | `3.844 ± 0.112` | `116.355` | `N/A (Mutable)` |
| `100,000` | **E3: SITI Unboxed EAV in SoA (UUIDv7 + ROW_NUMBER(), 0 is_active)** | `5` | `1,200,000` | `1,200,000` | **`0.0000%`** | `0.00` | `38.40` | `11.67` | `2.530 ± 0.125` | `4.951` | `5.78` |
| `226,324` | **E1a: Language B Wide Sparse Columnar Arrow (11,565 cols)** | `11,565` | `2,617,437,060` | `7,468,692` | **`99.7147%` (`99.8960%` B-cols)** | `21,205.99` | `21,223.17` | `120.35` | `666.736 ± 11.469` | `11,490.853` | `N/A (Mutable)` |
| `226,324` | **E1b: B50 Indicator Wide Sparse Columnar Arrow (759 cols)** | `759` | `171,779,916` | `7,468,692` | **`95.6522%` (`98.3740%` B50-cols)** | `1,335.03` | `1,392.35` | `67.00` | `77.214 ± 26.645` | `949.905` | `N/A (Mutable)` |
| `226,324` | **E2: Traditional Boxed VARCHAR EAV + Mutable is_active** | `5` | `2,715,888` | `2,715,888` | **`0.0000%`** | `78.74` | `165.65` | `15.22` | `7.109 ± 0.104` | `257.614` | `N/A (Mutable)` |
| `226,324` | **E3: SITI Unboxed EAV in SoA (UUIDv7 + ROW_NUMBER(), 0 is_active)** | `5` | `2,715,888` | `2,715,888` | **`0.0000%`** | `0.00` | `86.91` | `25.65` | `4.712 ± 0.210` | `9.036` | `12.78` |

---

## E.5 Geodesic IEEE 754 Quantization Audit (*GPU Vertex Jitter*) Across 226,322 National Assets and 5,011 Topocentric `ENU` / `OpenUSD` Instances (`Table E.4`)

For any coordinate $x \in \mathbb{R} \setminus \{0\}$, the IEEE 754 binary32 (`Float32`, $p = 24$ significand bits) unit in the last place is $\text{ULP}_{32}(x) = 2^{\lfloor \log_2 |x| \rfloor - 23}$. Across Colombia's `MAGNA-SIRGAS Origen Nacional (EPSG:9377)` planar grid (`225,244` non-empty georeferenced features out of `226,322` spatial rows; `1,078` legacy records carrying empty `"coordinates":[]` preserved as unlocated without Null-Island projection; $E \in [4,480,725.1, 5,102,162.4]\text{ m}$, $N \in [708,640.9, 3,875,010.2]\text{ m}$), $2^{22} = 4,194,304 \le E < 8,388,608 = 2^{23}$ yields $\text{ULP}_{32}(E) = 2^{-1}\text{ m} = 500.0\text{ mm}$ (`250.0 mm` half-ULP rounding bound), while $N$ spans the $2^{20}\text{--}2^{22}\text{ m}$ binade boundary ($\text{ULP}_{32}(N) \in \{125.0, 250.0\}\text{ mm}$). Under SITI's bimodal topocentric `ENU` decomposition ($|\Delta e|, |\Delta n| \le 250\text{ m}$ within $500\text{ m}$ corridor sectors anchored at `Float64` origins $(E_0, N_0, U_0)$), $\text{ULP}_{32}(\Delta) \le 2^{7 - 23} = 0.01526\text{ mm}$, suppressing *GPU Vertex Jitter* by more than four orders of magnitude.

### Table E.4: Geodesic IEEE 754 Quantization Audit (GPU Vertex Jitter) Across 226,322 National Assets and 5,011 Bimodal Local ENU / OpenUSD Instances

| Layer / Spatial Corpus | Instances $N$ | Mean Easting $E$ (m) | Mean Northing $N$ (m) | $\text{ULP}_{32}(E) / \text{ULP}_{32}(N)$ (mm) | Direct `Float32` Radial Error Mean ± SD (mm) | Direct `Float32` $p_{50} / p_{95} / \max$ (mm) | Differential Segment Peak Jitter (mm) | SITI Bimodal `ENU` Mean ± SD (mm) | SITI Bimodal `ENU` $p_{95} / \max$ (mm) | Precision Gain Factor | GPU Vertex VRAM Saved (\%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| senal_vertical (Retroreflective Vertical Signage, A50) | `87,263` | `4,808,517.2` | `2,251,357.4` | `500 / 250` | `142.36 ± 65.58` | `139.60 / 245.03 / 279.06` | `530.20` | **`0.0055 ± 0.0023`** | **`0.0093 / 0.0129`** | **`26,001×`** | **`50.0%`** |
| cuneta (Longitudinal Drainage Gutter, A50) | `33,773` | `4,799,480.1` | `2,234,456.4` | `500 / 250` | `145.30 ± 64.84` | `143.77 / 247.10 / 278.85` | `524.83` | **`0.0056 ± 0.0023`** | **`0.0094 / 0.0127`** | **`25,975×`** | **`50.0%`** |
| berma (Paved Shoulder & Lateral Strip, A30) | `22,419` | `4,783,637.8` | `2,244,666.5` | `500 / 250` | `143.10 ± 65.39` | `141.28 / 245.58 / 278.31` | `527.89` | **`0.0053 ± 0.0023`** | **`0.0090 / 0.0130`** | **`27,203×`** | **`50.0%`** |
| drenajes (Cross-Drainage Culvert & Hydraulic Work, A50) | `18,052` | `4,821,853.1` | `2,312,222.7` | `500 / 250` | `145.38 ± 64.44` | `144.16 / 246.26 / 278.57` | `528.09` | **`0.0055 ± 0.0023`** | **`0.0093 / 0.0131`** | **`26,635×`** | **`50.0%`** |
| defensa_vial (Containment Barrier & Guardrail, A50) | `16,335` | `4,772,736.3` | `2,178,449.3` | `500 / 250` | `142.48 ± 65.86` | `140.38 / 245.27 / 279.15` | `528.98` | **`0.0056 ± 0.0023`** | **`0.0093 / 0.0128`** | **`25,563×`** | **`50.0%`** |
| luminarias (Roadway Luminaire & Lighting Pole, A50) | `16,240` | `4,757,100.9` | `2,284,849.8` | `500 / 250` | `144.68 ± 65.04` | `142.11 / 247.14 / 279.24` | `522.48` | **`0.0052 ± 0.0023`** | **`0.0090 / 0.0126`** | **`27,607×`** | **`50.0%`** |
| calzada (Traffic Lane — Calzada SITI = carril, A30) | `10,710` | `4,794,024.4` | `2,254,921.5` | `500 / 250` | `143.58 ± 65.56` | `141.89 / 245.59 / 278.42` | `531.67` | **`0.0053 ± 0.0023`** | **`0.0090 / 0.0121`** | **`27,218×`** | **`50.0%`** |
| dispositivo_its (ITS Telemetry & Fiber-Optic Node, A40) | `6,537` | `4,782,897.6` | `2,264,474.1` | `500 / 250` | `145.18 ± 64.30` | `142.84 / 247.56 / 278.08` | `515.28` | **`0.0054 ± 0.0023`** | **`0.0091 / 0.0124`** | **`26,996×`** | **`50.0%`** |
| separador (Median Strip & Central Reserve, A30) | `6,149` | `4,785,993.7` | `2,223,683.2` | `500 / 250` | `142.13 ± 65.35` | `139.30 / 244.95 / 278.19` | `520.01` | **`0.0052 ± 0.0023`** | **`0.0091 / 0.0123`** | **`27,172×`** | **`50.0%`** |
| muro (Retaining Wall & Earth Structure, A50) | `2,712` | `4,820,243.7` | `2,219,758.9` | `500 / 250` | `143.96 ± 64.44` | `143.13 / 244.34 / 277.97` | `502.16` | **`0.0056 ± 0.0023`** | **`0.0094 / 0.0123`** | **`25,715×`** | **`50.0%`** |
| talud (Engineered Cut/Fill Slope, A30) | `2,074` | `4,852,361.6` | `2,312,327.9` | `500 / 250` | `147.86 ± 63.28` | `145.82 / 247.38 / 277.24` | `501.28` | **`0.0060 ± 0.0023`** | **`0.0096 / 0.0119`** | **`24,835×`** | **`50.0%`** |
| predio (Cadastral Right-of-Way Parcel, A10) | `1,425` | `4,826,626.4` | `2,255,478.0` | `500 / 250` | `148.19 ± 62.90` | `145.26 / 249.69 / 276.53` | `508.33` | **`0.0055 ± 0.0023`** | **`0.0093 / 0.0124`** | **`26,805×`** | **`50.0%`** |
| puente (Vehicular Bridge & Viaduct Complex, A20) | `1,187` | `4,773,737.8` | `2,207,227.7` | `500 / 250` | `146.16 ± 65.24` | `143.80 / 245.90 / 275.80` | `497.63` | **`0.0053 ± 0.0023`** | **`0.0088 / 0.0119`** | **`27,757×`** | **`50.0%`** |
| ciclorruta (Segregated Cycleway Path, A50) | `98` | `4,834,522.7` | `2,068,379.6` | `500 / 125` | `135.81 ± 68.63` | `142.50 / 239.46 / 257.28` | `449.62` | **`0.0054 ± 0.0025`** | **`0.0094 / 0.0114`** | **`25,250×`** | **`50.0%`** |
| estacion_peaje (Toll Collection Plaza, A20) | `79` | `4,772,047.0` | `2,331,527.2` | `500 / 250` | `145.71 ± 67.65` | `142.11 / 247.26 / 264.84` | `460.17` | **`0.0048 ± 0.0024`** | **`0.0086 / 0.0105`** | **`30,484×`** | **`50.0%`** |
| tunel (Road Tunnel & Portal Complex, A20) | `62` | `4,808,661.2` | `2,107,365.2` | `500 / 250` | `145.82 ± 62.09` | `152.47 / 239.70 / 240.81` | `456.47` | **`0.0053 ± 0.0020`** | **`0.0078 / 0.0090`** | **`27,331×`** | **`50.0%`** |
| estacion_pesaje (Weigh-in-Motion & Static Scale Station, A20) | `62` | `4,828,051.3` | `2,293,507.2` | `500 / 250` | `142.21 ± 71.78` | `151.33 / 243.99 / 262.70` | `405.41` | **`0.0050 ± 0.0024`** | **`0.0082 / 0.0104`** | **`28,501×`** | **`50.0%`** |
| cco (Operational Control Center & Rail Station, A20) | `34` | `4,792,133.4` | `2,195,079.5` | `500 / 250` | `135.28 ± 60.05` | `126.59 / 228.38 / 231.19` | `424.78` | **`0.0056 ± 0.0020`** | **`0.0092 / 0.0095`** | **`23,958×`** | **`50.0%`** |
| zona_servicio (Roadside Service & Rest Area, A30) | `27` | `4,814,746.2` | `2,263,587.3` | `500 / 250` | `139.99 ± 62.21` | `133.38 / 245.61 / 257.72` | `396.56` | **`0.0051 ± 0.0020`** | **`0.0082 / 0.0085`** | **`27,523×`** | **`50.0%`** |
| aeropuerto_terminal (Concessioned Airport Terminal, A20) | `4` | `4,811,170.0` | `2,044,995.3` | `500 / 125` | `112.08 ± 82.67` | `87.87 / 210.80 / 231.35` | `248.65` | **`0.0057 ± 0.0032`** | **`0.0090 / 0.0092`** | **`19,554×`** | **`50.0%`** |
| aeropuerto_torre (Airport Control Tower, A20) | `2` | `4,749,102.5` | `2,013,711.2` | `500 / 125` | `72.82 ± 26.82` | `72.82 / 89.89 / 91.79` | `145.34` | **`0.0056 ± 0.0041`** | **`0.0081 / 0.0084`** | **`13,120×`** | **`50.0%`** |
| **ALL 21 NATIONAL LAYERS (225,244 non-empty geometries in assets_spatial_instances_ani.parquet)** | `225,244` | `4,797,883.1` | `2,249,839.5` | `500 / 250` | `143.55 ± 65.26` | `141.48 / 245.82 / 279.24` | `543.29` | **`0.0054 ± 0.0023`** | **`0.0092 / 0.0131`** | **`26,358×`** | **`50.0%`** |
| Topocentric ENU / OpenUSD Subset — SITI Table A20 | `1` | `4,905,169.6` | `2,041,377.9` | `500 / 125` | `117.70 ± 0.00` | `117.70 / 117.70 / 117.70` | `235.40` | **`0.0069 ± 0.0000`** | **`0.0069 / 0.0069`** | **`17,091×`** | **`50.0%`** |
| Topocentric ENU / OpenUSD Subset — SITI Table A30 | `2` | `4,902,392.1` | `2,034,974.4` | `500 / 125` | `74.57 ± 30.29` | `74.57 / 93.84 / 95.98` | `57.29` | **`0.0031 ± 0.0010`** | **`0.0038 / 0.0039`** | **`23,988×`** | **`50.0%`** |
| Topocentric ENU / OpenUSD Subset — SITI Table A40 | `5` | `4,892,659.1` | `2,174,190.5` | `500 / 125` | `126.66 ± 52.57` | `129.32 / 174.53 / 176.99` | `291.61` | **`0.0024 ± 0.0017`** | **`0.0039 / 0.0040`** | **`52,867×`** | **`50.0%`** |
| Topocentric ENU / OpenUSD Subset — SITI Table A50 | `5,003` | `4,904,680.5` | `2,035,582.3` | `500 / 125` | `133.02 ± 67.69` | `130.73 / 241.16 / 256.47` | `494.23` | **`0.0052 ± 0.0024`** | **`0.0090 / 0.0123`** | **`25,688×`** | **`50.0%`** |
| **ALL 5,011 BIMODAL 64-BIT EPSG:9377 ANCHOR + 32-BIT LOCAL ENU / OPENUSD INSTANCES (assets_spatial_instances.parquet)** | `5,011` | `4,904,667.7` | `2,035,721.6` | `500 / 125` | `132.99 ± 67.66` | `130.65 / 241.14 / 256.47` | `494.23` | **`0.0052 ± 0.0024`** | **`0.0090 / 0.0123`** | **`25,697×`** | **`50.0%`** |

---

## E.6 Longitudinal Evolution Across the 5 CAS Lineage Stages (`Stage S0` (initial baseline) to `Stage 4` Active Release, `Table E.5`)

### Table E.5: Longitudinal Hardware Envelope, Storage Mass Asymmetry, and 3D Spatial Precision Evolution Across the 5 CAS Lineage Stages

| Lineage Stage | Publication / Architecture Paradigm | Hardware & RAM Envelope | Spatial Storage Mass (MB) | Operational Storage Mass (MB) | Disk Mass Asymmetry Ratio | Non-Spatial I/O Traffic Saved (\%) | Operational Table `NULL` Sparsity (\%) | Mean / Max 3D Spatial Jitter (mm) | Temporal Auditability |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Stage S0 (initial baseline)** | Original Monolithic Coupled Baseline ('4.35 GB in 1 TB RAM') | `1,024 GB (1 TB) Server RAM / 4,350 MB Coupled` | `4,350.00` | `4,350.00` | **`1.00× (Coupled)`** | **`0.00%`** | `99.90%` | `143.5 / 543.3 mm (Float32 EPSG:9377)` | None (Mutable In-Place Overwrite) |
| **Stage 1 (CAS 1: 340ed011)** | Initial Bimodal Separation (Road + 914 mm Rail + DuckDB Parquet) | `Commodity Workstation (< 2 GB Peak, 43.4 MB Oper. RAM)` | `455.88` | `18.48` | **`24.67×`** | **`95.95%`** | `98.37%` | `0.0052 / 0.0123 mm (Bimodal 64-bit EPSG:9377 + 32-bit ENU)` | Append-Only Parquet Snapshots |
| **Stage 2 (CAS 2: 9a3cc6d9)** | Expanded C1/C2 Coupling + Decoupled 5D APU & CDE Grounding | `Commodity Laptop (< 1.5 GB Spatial / 43.4 MB Oper. RAM)` | `456.85` | `18.48` | **`24.72×`** | **`95.95%`** | `0.00%` | `0.0052 / 0.0123 mm (ENU + OpenUSD)` | CAS SHA-256 + Grounding Receipts |
| **Stage 3 (CAS 3: 55e94d32)** | OWL 2 DL Axiomatization + 104 W3C SHACL Shapes (PAR_B50_0001..0100) | `Commodity Laptop (0.49 MB Projected SoA Oper. RAM)` | `456.85` | `18.48` | **`24.67× (2071× SoA)`** | **`99.95%`** | `0.00%` | `0.0052 / 0.0123 mm (Affine 4x4 F32)` | SHACL CWA + Unboxed EAV SoA |
| **Stage 4 (CAS 4: b6bd01f8)** | Active Production Closure: Bimodal ENU/WKB + Unboxed EAV SoA + UUIDv7 | `Commodity Laptop (18.48 MB Disk / 0.22 MB Projected I/O)` | `456.85` | `18.48` | **`24.67× (2071× SoA)`** | **`99.95%`** | `0.00%` | `0.0052 / 0.0123 mm (25,697× Gain)` | Immutable UUIDv7 + ROW_NUMBER() + SHA-256 (0 is_active) |

---
