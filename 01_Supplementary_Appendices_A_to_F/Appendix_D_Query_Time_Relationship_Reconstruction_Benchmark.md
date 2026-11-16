# Supplementary Appendix D: Live Query-Time Relationship Reconstruction Benchmark ($k = 1 \dots 6$ Hops), Markov Blanket Causal Isolation, and Shift-Left OpenBIM/GIS Authoring Kits ($\Phi_{\text{eff}}$)

**Manuscript Title:** *Orthogonal Ontology Factorization for Semantic Interoperability in Transport Infrastructure* (`ORTHOGONAL ONTOLOGY FACTORIZATION FOR SEMANTIC INTEROPERABILITY IN TRANSPORT INFRASTRUCTURE`)  
**Authors:** Juan C. Gómez (Corresponding Author; PhD candidate, Doctoral program in Technology Innovation Management, Universidad de los Andes, and National Infrastructure Agency (ANI), Bogotá, Colombia, `jc.gomez1988@uniandes.edu.co`), Rodrigo F. Herrera (Associate professor, School of Civil Engineering, Pontificia Universidad Católica de Valparaíso, Valparaíso, Chile, `rodrigo.herrera@pucv.cl`), Karen M. Castañeda (Assistant professor, School of Civil Engineering, Pontificia Universidad Católica de Valparaíso, Valparaíso, Chile, `karen.castaneda@pucv.cl`), and Juan F. Correal (Full professor, Department of Civil and Environmental Engineering, Universidad de los Andes, Bogotá, Colombia, `jcorreal@uniandes.edu.co`)  
**Reference:** Gómez, J. C., Herrera, R. F., Castañeda, K. M., & Correal, J. F. (2027). Orthogonal ontology factorization for semantic interoperability in transport infrastructure. *Journal of Information Technology in Construction (ITcon)*, 32, 1-X. https://doi.org/10.36680/j.itcon.2027.[added by editor]  
**Target Journal:** *Journal of Information Technology in Construction (ITcon)* — Second Submission (Extended Empirical & Mathematical Paper)
**Active CAS Semantic Publication:** `b6bd01f850790ad22d399b95545f73d2` (`Stage S4`)
**Verification Timestamp (UTC):** `2026-11-02T19:58:30.528430+00:00`

---

## D.1 Formal Mathematical Definition of the Third Dimension of the Semantic Interoperability Index ($\Phi_{\text{eff}}$)

To test and quantify the core architectural hypothesis evaluated in this study—that for legacy infrastructure, semantic interoperability is achieved more effectively by separating geometric information from operational information and reconstructing relationships dynamically at query time—we define the third dimension of the Semantic Interoperability Index ($\Phi_{\text{eff}}$) across three complementary operational sub-metrics:

1. **Query-Time Relationship Reconstruction Efficiency ($\Phi_{\text{eff}}^{\text{(Query-Time)}}$):**
   $$\Phi_{\text{eff}}^{\text{(Query-Time)}}(s) = \left(1 - \frac{T_{\text{SITI}, s}}{T_{\text{Baseline}}}\right) \times 100\%, \qquad T_{\text{SITI}, s} = t_{\text{C1 (SKOS/OWL/SHACL)}} + t_{\text{C2 (LPG O(1) + Markov Blanket)}} + t_{\text{C3 (DuckDB Vectorized SIMD Parquet)}}$$
   evaluated across a canonical benchmark of **$N = 50$ real lifecycle engineering and asset-management queries** spanning topological hop depths $k \in \{1, 2, 3, 4, 5, 6\}$ and all **13 formal intertabular assembly recipes (`REC-A-01..07`, `REC-B-01..06`)**, comparing the three-layer SITI pipeline (`M3`) against coupled baselines (`M1`, `M2`) and controlled engine/LBD ablations (`M1b`, `M2b`, `M2c`, detailed in Section D.4B):
   - **`M1` (`Monolithic RDF/Triple-Store Traversal`):** evaluation of $k$-hop Basic Graph Pattern (BGP) `(s, p, o)` triple joins over the `438,194` TBox triples of `capa1_siti_ontology.ttl` plus materialized ABox instance triples without Layer 2 O(1) pointer adjacency or Layer 3 columnar decoupling.
   - **`M2` (`Traditional Row-Oriented Relational SQL / Coupled Wide Table & Multi-Way B-Tree JOINs`):** execution over row-oriented relational tables (`sqlite3` B-Tree storage with coupled geometry payloads and $k$-way relational `JOIN`s).
   - **`M3` (`SITI Three-Layer Query-Time Reconstruction`):** decoupled execution `C1 -> C2 -> C3` with *Late Spatial Materialization*, touching `assets_spatial_instances_ani.parquet` (`226,322` WKB/GeoJSON geometries in `EPSG:9377`) or `assets_spatial_instances.parquet` (`5,011` bimodal 64-bit EPSG:9377 anchor + 32-bit local ENU offset instances) strictly when the query requests spatial coordinates.
2. **Topological Causal Isolation via Pearl's Markov Blanket ($\Phi_{\text{eff}}^{\text{(Markov-Isolation)}}$):**
   $$\Phi_{\text{eff}}^{\text{(Markov-Isolation)}}(v) = \left(1 - \frac{|\partial\mathcal{M}(v)| + 1}{|\mathcal{V}_{C2}|}\right) \times 100\%, \qquad \partial\mathcal{M}(v) = \text{Pa}(v) \cup \text{Ch}(v) \cup \text{Sp}(v)$$
   evaluated across all **`316` intertabular anchor nodes** and all **`16,232` total concepts** in Layer 2 (`17,021` total edges: `16,228` `SUBCLASE_DE` + `793` deduplicated intertabular edges, `0` intratabular meronymy edges), achieving a mean search-space reduction of **`99.9152%`** across the 316 anchors (`99.9862%` across all 16,232 nodes).
3. **Shift-Left Source Authoring Fidelity ($\Phi_{\text{eff}}^{\text{(Shift-Left-Kits)}}$):**
   Physical cryptographic audit of the **9 Shift-Left Authoring Kits** (`5` OpenBIM kits in `Kits_BIM/` and `4` GIS kits in `Kits_GIS/`), demonstrating how pre-tagged authoring templates prevent at the source the `49` `unsupported` (`26` mute IFCs, `21` unstructured TXTs, `1` proprietary binary RVT, `1` malformed CSV) and `174` `partial` cold-ingestion receipts identified in Wave 2.

---

## D.2 Benchmark Summary Across Hop Depths $k = 1 \dots 6$ and 13 Assembly Recipes (`Table D.1`)

### Table D.1: Summary of Query-Time Reconstruction Latency Across Hop Depths $k \in \{1 \dots 6\}$ and Canonical Assembly Recipes

| Stratum / Hop Depth / Recipe | Queries ($n$) | Reconstructed Tuples (Sum) | `M1` Monolithic RDF Mean ± SD (ms) | `M2` Row-SQL (`sqlite3`) Mean ± SD (ms) | `M3` SITI $t_{\text{C1}}$ ($\mu\text{s}$) | `M3` SITI $t_{\text{C2}}$ ($\mu\text{s}$) | `M3` SITI $t_{\text{C3}}$ ($\mu\text{s}$) | `M3` SITI Total Mean ± SD (ms) | `M3` $p_{50}$ / $p_{95}$ (ms) | Speedup $S_{\text{M1/M3}}$ | Speedup $S_{\text{M2/M3}}$ | $\Phi_{\text{eff}}^{\text{(vs M1)}}$ (\%) | $\Phi_{\text{eff}}^{\text{(vs M2)}}$ (\%) | Parity |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Hop Depth k = 1 hop | `8` | `169,535` | `3.840 ± 0.162` | `3.810 ± 1.456` | `5.10` | `28.63` | `598.49` | `0.632 ± 0.109` | `0.636 / 0.758` | `6.07×` | `6.03×` | `83.54%` | `83.41%` | `100%` |
| Hop Depth k = 2 hops | `9` | `52,991` | `7.907 ± 0.469` | `4.208 ± 1.175` | `6.44` | `72.41` | `541.60` | `0.620 ± 0.269` | `0.517 / 1.044` | `12.74×` | `6.78×` | `92.15%` | `85.25%` | `100%` |
| Hop Depth k = 3 hops | `9` | `68,595` | `11.998 ± 0.213` | `7.032 ± 2.334` | `6.49` | `43.95` | `594.66` | `0.645 ± 0.195` | `0.590 / 0.935` | `18.60×` | `10.90×` | `94.62%` | `90.83%` | `100%` |
| Hop Depth k = 4 hops | `8` | `81,286` | `16.984 ± 0.214` | `9.345 ± 2.614` | `7.27` | `71.73` | `569.96` | `0.649 ± 0.279` | `0.550 / 1.080` | `26.17×` | `14.40×` | `96.18%` | `93.06%` | `100%` |
| Hop Depth k = 5 hops | `8` | `221,037` | `22.150 ± 0.503` | `11.508 ± 2.596` | `7.54` | `70.93` | `755.42` | `0.834 ± 0.126` | `0.810 / 1.010` | `26.56×` | `13.80×` | `96.24%` | `92.75%` | `100%` |
| Hop Depth k = 6 hops | `8` | `141,405` | `28.112 ± 0.645` | `14.450 ± 4.646` | `7.70` | `79.80` | `780.40` | `0.868 ± 0.157` | `0.902 / 1.045` | `32.39×` | `16.65×` | `96.91%` | `93.99%` | `100%` |
| **Global Mean / Total (50 Lifecycle Queries, k = 1..6)** | `50` | `734,849` | `14.957 ± 8.273` | `8.281 ± 4.597` | `6.74` | `61.12` | `637.21` | **`0.705 ± 0.217`** | `0.719 / 1.074` | **`21.21×`** | **`11.75×`** | **`95.29%`** | **`91.49%`** | `100%` |
| REC-A-01: Concessioned Highway & Pavement Section Assembly | `7` | `46,413` | `13.713 ± 9.262` | `7.910 ± 5.477` | `6.71` | `116.11` | `550.53` | `0.673 ± 0.163` | `0.703 / 0.886` | `20.37×` | `11.75×` | `95.09%` | `91.49%` | `100%` |
| REC-A-02: Vehicular Bridge, Viaduct & Road Tunnel Assembly | `4` | `88,957` | `12.775 ± 10.701` | `8.800 ± 9.918` | `6.30` | `18.90` | `569.88` | `0.595 ± 0.158` | `0.519 / 0.785` | `21.47×` | `14.79×` | `95.34%` | `93.24%` | `100%` |
| REC-A-03: Road Hydraulic & Cross-Drainage Assembly (A50_045) | `5` | `116,640` | `13.089 ± 10.107` | `10.043 ± 5.446` | `6.48` | `17.81` | `650.97` | `0.675 ± 0.091` | `0.685 / 0.770` | `19.38×` | `14.87×` | `94.84%` | `93.28%` | `100%` |
| REC-A-04: 914 mm Narrow-Gauge Railway Corridor & Rolling Stock | `3` | `610` | `19.160 ± 8.069` | `7.433 ± 2.490` | `6.16` | `24.21` | `635.33` | `0.666 ± 0.239` | `0.713 / 0.861` | `28.78×` | `11.17×` | `96.53%` | `91.04%` | `100%` |
| REC-A-05: Road Safety, Containment Barriers & Cycleway Assembly | `3` | `194,107` | `11.714 ± 10.222` | `8.605 ± 4.641` | `6.45` | `43.34` | `628.78` | `0.679 ± 0.189` | `0.737 / 0.823` | `17.26×` | `12.68×` | `94.21%` | `92.11%` | `100%` |
| REC-A-06: Electronic Toll Station & OETR Traffic-Revenue Assembly | `4` | `76,198` | `12.209 ± 6.562` | `5.675 ± 2.302` | `7.05` | `58.18` | `984.25` | `1.050 ± 0.045` | `1.065 / 1.083` | `11.63×` | `5.41×` | `91.40%` | `81.51%` | `100%` |
| REC-A-07: ITS, Fiber Optics, Road Lighting & CCO Assembly | `4` | `111,069` | `6.670 ± 3.832` | `6.086 ± 2.993` | `5.58` | `60.47` | `635.35` | `0.701 ± 0.106` | `0.746 / 0.767` | `9.51×` | `8.68×` | `89.48%` | `88.47%` | `100%` |
| REC-B-01: Strategic Portfolio Planning (PBIX) & DANE Equity | `4` | `1,310` | `23.426 ± 2.904` | `10.822 ± 2.427` | `7.88` | `48.82` | `747.53` | `0.804 ± 0.084` | `0.773 / 0.906` | `29.13×` | `13.46×` | `96.57%` | `92.57%` | `100%` |
| REC-B-02: INVIAS 5D Unit-Price Analysis (APU) Decoupling | `5` | `60,390` | `17.977 ± 5.757` | `8.862 ± 3.944` | `7.10` | `37.46` | `502.93` | `0.547 ± 0.248` | `0.445 / 0.888` | `32.84×` | `16.19×` | `96.95%` | `93.82%` | `100%` |
| REC-B-03: Cadastral Land Acquisition & Right-of-Way Governance | `2` | `1,455` | `10.163 ± 2.970` | `4.439 ± 1.231` | `5.95` | `17.61` | `415.36` | `0.439 ± 0.214` | `0.439 / 0.575` | `23.15×` | `10.12×` | `95.68%` | `90.11%` | `100%` |
| REC-B-04: IPSAS 17 (NICSP 17) BUP/PPE Accounting & Handback | `3` | `4,121` | `14.059 ± 7.229` | `5.825 ± 2.382` | `7.05` | `88.17` | `497.62` | `0.593 ± 0.066` | `0.591 / 0.653` | `23.71×` | `9.82×` | `95.78%` | `89.82%` | `100%` |
| REC-B-05: AASHTO TAM Lifecycle, ESAL Fatigue & 85/15 Escrow | `3` | `32,429` | `22.919 ± 6.313` | `11.807 ± 1.463` | `7.41` | `149.25` | `914.20` | `1.071 ± 0.151` | `1.077 / 1.205` | `21.40×` | `11.03×` | `95.33%` | `90.93%` | `100%` |
| REC-B-06: Zero-Trust Policy Access Forensic Audit & CDE Grounding | `3` | `1,150` | `17.439 ± 9.919` | `9.579 ± 5.601` | `7.33` | `90.43` | `543.60` | `0.641 ± 0.268` | `0.599 / 0.895` | `27.19×` | `14.94×` | `96.32%` | `93.30%` | `100%` |

---

## D.3 Complete Per-Query Latency Breakdown and 100% Result-Set Parity Across All 50 Lifecycle Queries (`Table D.2`)

### Table D.2: Complete 50-Query Lifecycle Benchmark Catalog (Q01–Q50)

| Query ID | Hop $k$ | Recipe | Domain & Path Pattern | Late Spatial | Tuples | `M1` Mean (ms) | `M2` Mean (ms) | `M3` $t_{\text{C1}}$ ($\mu\text{s}$) | `M3` $t_{\text{C2}}$ ($\mu\text{s}$) | `M3` $t_{\text{C3}}$ ($\mu\text{s}$) | `M3` Mean ± SD (ms) | $S_{\text{M1/M3}}$ | $S_{\text{M2/M3}}$ | $\Phi_{\text{eff}}^{\text{(vs M1)}}$ (\%) | $\Phi_{\text{eff}}^{\text{(vs M2)}}$ (\%) | Parity |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Q01` | `1` | `REC-A-01` | National traffic lane inventory scan (A30) (`A30_035_005_040`) | `No` | `10,710` | `3.666` | `2.217` | `5.32` | `105.57` | `613.49` | `0.724 ± 0.098` | `5.06×` | `3.06×` | `80.24%` | `67.32%` | `OK` |
| `Q02` | `1` | `REC-A-03` | Disambiguated longitudinal drainage gutters (__occ1 A50_045) (`A50_045_025_005__occ1`) | `No` | `33,801` | `4.053` | `4.816` | `5.23` | `6.95` | `673.22` | `0.685 ± 0.062` | `5.91×` | `7.03×` | `83.09%` | `85.77%` | `OK` |
| `Q03` | `1` | `REC-A-03` | Cross-drainage culverts and hydraulic works (A50_045) (`A50_045_025_010__occ1`) | `No` | `18,055` | `4.027` | `5.161` | `6.35` | `6.70` | `574.55` | `0.588 ± 0.067` | `6.85×` | `8.78×` | `85.41%` | `88.62%` | `OK` |
| `Q04` | `1` | `REC-A-02` | National bridge and viaduct complexes (A20) (`A20_005_020_010`) | `No` | `1,194` | `3.805` | `1.938` | `4.19` | `6.45` | `510.46` | `0.521 ± 0.065` | `7.30×` | `3.72×` | `86.31%` | `73.11%` | `OK` |
| `Q05` | `1` | `REC-A-07` | Retroreflective vertical road signage (A50) (`A50_080_015_010`) | `No` | `87,639` | `3.718` | `4.791` | `4.97` | `6.04` | `758.17` | `0.769 ± 0.071` | `4.83×` | `6.23×` | `79.31%` | `83.95%` | `OK` |
| `Q06` | `1` | `REC-A-07` | Late WKB spatial materialization of roadway luminaires (EPSG:9377) (`A50_060_045_005`) | `Yes` | `16,844` | `3.659` | `4.726` | `4.02` | `5.50` | `534.73` | `0.544 ± 0.056` | `6.72×` | `8.68×` | `85.12%` | `88.48%` | `OK` |
| `Q07` | `1` | `REC-A-05` | Segregated cycleways and non-motorized paths (A50) (`A50_015_005_025`) | `No` | `98` | `3.988` | `4.802` | `5.82` | `84.52` | `646.27` | `0.737 ± 0.093` | `5.41×` | `6.52×` | `81.53%` | `84.66%` | `OK` |
| `Q08` | `1` | `REC-A-01` | Late WKB spatial materialization of bridges in EPSG:9377 (A20) (`A20_005_020_010`) | `Yes` | `1,194` | `3.806` | `2.029` | `4.87` | `7.32` | `477.05` | `0.489 ± 0.078` | `7.78×` | `4.15×` | `87.15%` | `75.89%` | `OK` |
| `Q09` | `2` | `REC-A-06` | Direct A30/A40 <-> B50 toll booth and OETR traffic series join (`A20_020_015_045`) | `No` | `19,150` | `7.498` | `4.248` | `6.13` | `19.29` | `957.61` | `0.983 ± 0.070` | `7.63×` | `4.32×` | `86.89%` | `76.86%` | `OK` |
| `Q10` | `2` | `REC-A-06` | OETR traffic and revenue in heavy category V (5-axle trucks) (`A30_035_005_040`) | `No` | `19,038` | `7.891` | `3.674` | `6.62` | `135.59` | `943.15` | `1.085 ± 0.092` | `7.27×` | `3.39×` | `86.25%` | `70.46%` | `OK` |
| `Q11` | `2` | `REC-B-03` | Cadastral land-acquisition A10 <-> B10 <-> B20 cross-check (`A10_010_015_005`) | `No` | `30` | `8.062` | `3.569` | `5.86` | `16.09` | `265.66` | `0.288 ± 0.021` | `28.03×` | `12.41×` | `96.43%` | `91.94%` | `OK` |
| `Q12` | `2` | `REC-A-02` | Road tunnel complexes A20 -> A30 -> A40 ITS ventilation (`A20_010_015_015`) | `No` | `62` | `7.499` | `3.815` | `6.93` | `14.47` | `495.92` | `0.517 ± 0.050` | `14.50×` | `7.37×` | `93.10%` | `86.44%` | `OK` |
| `Q13` | `2` | `REC-A-07` | Operational Control Centers (CCO) A20 -> A40 -> B50 telemetry (`A40_045_005_030`) | `No` | `34` | `7.592` | `4.264` | `6.64` | `115.21` | `636.36` | `0.758 ± 0.074` | `10.01×` | `5.62×` | `90.01%` | `82.22%` | `OK` |
| `Q14` | `2` | `REC-B-04` | IPSAS 17 BUP/PPE accounting depreciation on lanes and bridges (`B10_010_030_015`) | `No` | `3,478` | `7.920` | `3.737` | `6.61` | `121.15` | `462.85` | `0.591 ± 0.049` | `13.41×` | `6.33×` | `92.54%` | `84.20%` | `OK` |
| `Q15` | `2` | `REC-B-06` | Zero-Trust policy access governance of A10 <-> B20 ANI jurisdictions (`B20_025_005_00024`) | `No` | `47` | `7.813` | `3.347` | `6.34` | `92.56` | `297.91` | `0.397 ± 0.039` | `19.69×` | `8.43×` | `94.92%` | `88.14%` | `OK` |
| `Q16` | `2` | `REC-A-05` | Late WKB spatial materialization of medians & barriers A30 -> A50 -> B30 (`A30_035_005_055`) | `Yes` | `6,149` | `7.850` | `7.238` | `6.18` | `14.28` | `446.40` | `0.467 ± 0.052` | `16.81×` | `15.50×` | `94.05%` | `93.55%` | `OK` |
| `Q17` | `2` | `REC-A-01` | Late bimodal 64-bit EPSG:9377 anchor + 32-bit local ENU offset spatial projection of BIM/GIS instances (`A30_035_005_040`) | `Yes` | `5,003` | `9.044` | `3.978` | `6.62` | `123.05` | `368.53` | `0.498 ± 0.056` | `18.15×` | `7.98×` | `94.49%` | `87.47%` | `OK` |
| `Q18` | `3` | `REC-A-04` | 914 mm railway mode: Corridor A20 -> Track A30 -> Fleet B30 -> AT4 B50 (`A20_005_005_005`) | `No` | `47` | `12.160` | `5.409` | `5.33` | `13.57` | `693.69` | `0.713 ± 0.165` | `17.06×` | `7.59×` | `94.14%` | `86.83%` | `OK` |
| `Q19` | `3` | `REC-A-01` | Road assembly A20 -> Lane A30 -> Pavement A50 -> Material B30 (`A30_035_005_040`) | `No` | `6,212` | `12.154` | `9.995` | `7.14` | `131.97` | `564.08` | `0.703 ± 0.050` | `17.28×` | `14.21×` | `94.21%` | `92.96%` | `OK` |
| `Q20` | `3` | `REC-A-03` | Road hydraulics A20 -> Zone A30 -> Gutter A50_045 -> Concrete B30 (`A50_045_025_005__occ1`) | `No` | `12,928` | `11.987` | `9.752` | `6.17` | `16.09` | `554.38` | `0.577 ± 0.069` | `20.79×` | `16.91×` | `95.19%` | `94.09%` | `OK` |
| `Q21` | `3` | `REC-B-02` | INVIAS APU chapters B20 -> Spec B10 -> Activity B40 -> Component A50 (`B40_005_025_015`) | `No` | `21,980` | `11.906` | `4.982` | `5.70` | `20.32` | `355.49` | `0.382 ± 0.090` | `31.21×` | `13.06×` | `96.80%` | `92.34%` | `OK` |
| `Q22` | `3` | `REC-B-04` | BUP asset handback A20 -> A30 -> Contract B10 -> Valuation B50 (`A20_005_020_010`) | `No` | `291` | `12.231` | `5.318` | `6.42` | `23.59` | `498.25` | `0.528 ± 0.063` | `23.15×` | `10.07×` | `95.68%` | `90.07%` | `OK` |
| `Q23` | `3` | `REC-A-06` | OETR toll reconciliation A20 -> Booth A40 -> Tariff B50 -> Contract B10 (`A20_020_015_045`) | `No` | `19,098` | `11.847` | `5.978` | `8.00` | `34.87` | `1,026.75` | `1.070 ± 0.113` | `11.08×` | `5.59×` | `90.97%` | `82.11%` | `OK` |
| `Q24` | `3` | `REC-A-07` | Fiber optics and ITS devices A20 -> System A40 -> Node A50 -> Indicator B50 (`A40_045_005_030`) | `No` | `6,552` | `11.712` | `10.561` | `6.67` | `115.13` | `612.16` | `0.734 ± 0.080` | `15.96×` | `14.39×` | `93.73%` | `93.05%` | `OK` |
| `Q25` | `3` | `REC-B-03` | Right-of-way and easements A10 -> A20 -> B10 -> Actor B20 (`A10_010_015_005`) | `No` | `1,425` | `12.263` | `5.310` | `6.03` | `19.14` | `565.05` | `0.590 ± 0.069` | `20.78×` | `9.00×` | `95.19%` | `88.88%` | `OK` |
| `Q26` | `3` | `REC-A-02` | Late WKB spatial materialization of tunnels A20 -> A30 -> A40 -> A50 (`A20_010_015_015`) | `Yes` | `62` | `11.721` | `5.979` | `6.91` | `20.89` | `482.10` | `0.510 ± 0.150` | `22.99×` | `11.73×` | `95.65%` | `91.47%` | `OK` |
| `Q27` | `4` | `REC-B-02` | 5D INVIAS APU budget: B20 -> B10 -> B40 -> B30 -> B50 (Pavements) (`B30_005_005_015`) | `No` | `14,420` | `16.874` | `6.501` | `6.91` | `40.55` | `376.48` | `0.424 ± 0.091` | `39.80×` | `15.34×` | `97.49%` | `93.48%` | `OK` |
| `Q28` | `4` | `REC-B-02` | 5D INVIAS APU budget: B20 -> B10 -> B40 -> B30 -> A50 (Earthworks) (`B40_005_010_005`) | `No` | `13,160` | `16.700` | `6.881` | `8.05` | `42.71` | `451.27` | `0.502 ± 0.143` | `33.27×` | `13.71×` | `96.99%` | `92.70%` | `OK` |
| `Q29` | `4` | `REC-B-02` | 5D INVIAS APU budget: B20 -> B10 -> B40 -> A50 -> B50 (Drainage works) (`A50_045_025_005__occ1`) | `No` | `8,680` | `16.854` | `11.584` | `6.71` | `30.28` | `408.26` | `0.445 ± 0.101` | `37.85×` | `26.02×` | `97.36%` | `96.16%` | `OK` |
| `Q30` | `4` | `REC-A-01` | Full physical DAG hierarchy A10 -> A20 -> A30 -> A40 -> A50 (4G Corridors) (`A30_035_005_040`) | `No` | `7,573` | `16.923` | `7.765` | `7.45` | `138.87` | `675.55` | `0.822 ± 0.055` | `20.59×` | `9.45×` | `95.14%` | `89.42%` | `OK` |
| `Q31` | `4` | `REC-A-04` | Rail-road intermodality A10 -> A20 -> A30 -> B30 -> B50 (`A20_005_005_005`) | `No` | `1` | `17.335` | `6.677` | `6.19` | `22.98` | `377.89` | `0.407 ± 0.086` | `42.59×` | `16.40×` | `97.65%` | `93.90%` | `OK` |
| `Q32` | `4` | `REC-B-05` | AASHTO ESAL fatigue audit A20 -> A30 -> A50 -> B40 -> B50 (`A30_035_005_040`) | `No` | `19,017` | `17.065` | `11.491` | `7.41` | `150.47` | `1,060.86` | `1.219 ± 0.189` | `14.00×` | `9.43×` | `92.86%` | `89.39%` | `OK` |
| `Q33` | `4` | `REC-B-06` | Three-layer documentary grounding B10 -> B20 -> A20 -> A50 -> B50 (603 receipts) (`B10_010_030_015`) | `No` | `380` | `16.878` | `11.196` | `7.76` | `124.91` | `466.15` | `0.599 ± 0.203` | `28.18×` | `18.70×` | `96.45%` | `94.65%` | `OK` |
| `Q34` | `4` | `REC-A-03` | Late WKB spatial materialization of hydraulic works A10 -> A20 -> A30 -> A50 -> B30 (`A50_045_025_010__occ1`) | `Yes` | `18,055` | `17.243` | `12.666` | `7.68` | `23.09` | `743.24` | `0.774 ± 0.198` | `22.28×` | `16.36×` | `95.51%` | `93.89%` | `OK` |
| `Q35` | `5` | `REC-B-01` | Prioritized regional development equity (170 municipalities): A10 -> A20 -> A30 -> B10 -> B20 -> B50 (`B50_025_005`) | `No` | `170` | `21.953` | `8.044` | `6.93` | `19.98` | `731.27` | `0.758 ± 0.182` | `28.95×` | `10.61×` | `96.55%` | `90.57%` | `OK` |
| `Q36` | `5` | `REC-B-01` | Conflict-recovery regional equity (344 municipalities): A10 -> A20 -> A50 -> B10 -> B20 -> B50 (`B50_025_010`) | `No` | `344` | `22.041` | `12.583` | `7.90` | `39.14` | `695.96` | `0.743 ± 0.169` | `29.67×` | `16.93×` | `96.63%` | `94.10%` | `OK` |
| `Q37` | `5` | `REC-B-01` | DANE border municipalities (173 municipalities): A10 -> A20 -> A30 -> A50 -> B20 -> B50 (`B50_025_015`) | `No` | `414` | `21.929` | `13.111` | `7.74` | `28.31` | `752.78` | `0.789 ± 0.172` | `27.80×` | `16.62×` | `96.40%` | `93.98%` | `OK` |
| `Q38` | `5` | `REC-B-05` | AASHTO TAM lifecycle and performance: A20 -> A30 -> A50 -> B30 -> B40 -> B50 (`A30_035_005_040`) | `No` | `2,275` | `22.084` | `13.403` | `7.20` | `144.72` | `764.50` | `0.916 ± 0.244` | `24.10×` | `14.62×` | `95.85%` | `93.16%` | `OK` |
| `Q39` | `5` | `REC-B-04` | BUP/PPE + Contract + Actor + Material reconciliation: A20 -> A30 -> B10 -> B20 -> B30 -> B50 (`B10_010_030_015`) | `No` | `352` | `22.026` | `8.419` | `8.12` | `119.78` | `531.78` | `0.660 ± 0.089` | `33.39×` | `12.76×` | `97.00%` | `92.16%` | `OK` |
| `Q40` | `5` | `REC-A-05` | Road safety and lighting: A10 -> A20 -> A30 -> A40 -> A50 -> B50 (`A50_060_045_005`) | `No` | `187,860` | `23.306` | `13.776` | `7.35` | `31.22` | `793.66` | `0.832 ± 0.130` | `28.00×` | `16.55×` | `96.43%` | `93.96%` | `OK` |
| `Q41` | `5` | `REC-A-06` | OETR category IV tariff and revenue: A10 -> A20 -> A40 -> B10 -> B20 -> B50 (`A20_020_015_045`) | `No` | `18,912` | `21.601` | `8.800` | `7.46` | `42.97` | `1,009.50` | `1.060 ± 0.173` | `20.38×` | `8.30×` | `95.09%` | `87.96%` | `OK` |
| `Q42` | `5` | `REC-A-01` | Late WKB spatial materialization of national lanes: A10 -> A20 -> A30 -> A50 -> B10 -> B50 (`A30_035_005_040`) | `Yes` | `10,710` | `22.263` | `13.928` | `7.65` | `141.33` | `763.93` | `0.913 ± 0.087` | `24.39×` | `15.26×` | `95.90%` | `93.45%` | `OK` |
| `Q43` | `6` | `REC-B-05` | 6-hop ESTADO_4 tuple reconstruction (A, B10, B20, B30, B40, B50) + 85/15 Smart Escrow (`A30_035_005_040`) | `No` | `11,137` | `29.607` | `10.527` | `7.63` | `152.56` | `917.24` | `1.077 ± 0.253` | `27.48×` | `9.77×` | `96.36%` | `89.77%` | `OK` |
| `Q44` | `6` | `REC-B-02` | Full 5D APU + Assets + Contracts chain: A20 -> A30 -> A50 -> B10 -> B20 -> B40 -> B50 (`B30_005_005_015`) | `No` | `2,150` | `27.549` | `14.363` | `8.14` | `53.46` | `923.15` | `0.985 ± 0.294` | `27.98×` | `14.58×` | `96.43%` | `93.14%` | `OK` |
| `Q45` | `6` | `REC-B-01` | ANI Power BI strategic planning + DANE + Contracts: A10 -> A20 -> B10 -> B20 -> B30 -> B40 -> B50 (`B20_025_005_00024`) | `No` | `382` | `27.782` | `9.552` | `8.96` | `107.86` | `810.09` | `0.927 ± 0.233` | `29.97×` | `10.31×` | `96.66%` | `90.30%` | `OK` |
| `Q46` | `6` | `REC-B-06` | Zero-Trust forensic audit + ANI/INVIAS Manuals: A10 -> A30 -> A50 -> B10 -> B20 -> B40 -> B50 (`A50_080_015_010`) | `No` | `723` | `27.628` | `14.194` | `7.87` | `53.82` | `866.73` | `0.928 ± 0.306` | `29.76×` | `15.29×` | `96.64%` | `93.46%` | `OK` |
| `Q47` | `6` | `REC-A-04` | Rail-port-road intermodal traceability: A10 -> A20 -> A30 -> A40 -> B10 -> B30 -> B50 (`A20_005_005_005`) | `No` | `562` | `27.985` | `10.214` | `6.94` | `36.08` | `834.40` | `0.877 ± 0.277` | `31.89×` | `11.64×` | `96.86%` | `91.41%` | `OK` |
| `Q48` | `6` | `REC-A-01` | 6-hop reconstruction with Late bimodal 64-bit EPSG:9377 anchor + 32-bit local ENU / OpenUSD Spatial Materialization (5,011 instances) (`A30_035_005_040`) | `Yes` | `5,011` | `28.134` | `15.456` | `7.89` | `164.62` | `391.11` | `0.564 ± 0.082` | `49.92×` | `27.42×` | `98.00%` | `96.35%` | `OK` |
| `Q49` | `6` | `REC-A-02` | 6-hop reconstruction with Late WKB Spatial Materialization of Signage & ITS (EPSG:9377) (`A50_080_015_010`) | `Yes` | `87,639` | `28.077` | `23.469` | `7.17` | `33.80` | `791.05` | `0.832 ± 0.107` | `33.75×` | `28.21×` | `97.04%` | `96.45%` | `OK` |
| `Q50` | `6` | `REC-A-03` | 6-hop reconstruction with Late WKB Spatial Materialization of A50_045 Gutters (EPSG:9377) (`A50_045_025_005__occ1`) | `Yes` | `33,801` | `28.134` | `17.821` | `6.95` | `36.24` | `709.47` | `0.753 ± 0.059` | `37.38×` | `23.68×` | `97.32%` | `95.78%` | `OK` |

---

## D.4 Paired Non-Parametric Wilcoxon Signed-Rank Tests, Effect Sizes, and $B=10,000$ Bootstrap 95% CIs (`Table D.3`)

### Table D.3: Non-Parametric Paired Wilcoxon Signed-Rank Tests and Bootstrap 95% Confidence Intervals Across Benchmark Strata

| Comparison Stratum | $N$ | Baseline Mean (ms) | SITI `M3` Mean (ms) | Mean $\Delta T$ (ms) | 95% Bootstrap CI $\Delta T$ (Perc / BCa, ms) | Mean $\Phi_{\text{eff}}$ (\%) | 95% Bootstrap CI $\Phi_{\text{eff}}$ (BCa, \%) | Wilcoxon $W$ | $Z$-stat | $p$-value (two-sided) | Cohen's $d$ | Hedges' $g$ | Rosenthal's $r$ | $r_{rb}$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **SITI M3 vs. M1 Monolithic RDF (All Queries, N=50)** | `50` | `14.957` | `0.705` | `-14.252` | `[12.06, 16.51] / [12.06, 16.51]` | `95.29%` | `[94.52%, 95.87%]` | `0.0` | `6.1540` | `7.56e-10` | `1.74` | `1.71` | `0.8703` | `1.0000` |
| **SITI M3 vs. M2 Row-Oriented SQL (All Queries, N=50)** | `50` | `8.281` | `0.705` | `-7.576` | `[6.36, 8.84] / [6.43, 8.91]` | `91.49%` | `[90.19%, 92.62%]` | `0.0` | `6.1540` | `7.56e-10` | `1.68` | `1.65` | `0.8703` | `1.0000` |
| **SITI M3 vs. M1 Monolithic RDF (Shallow Hops k=1..3, N=26)** | `26` | `8.072` | `0.633` | `-7.439` | `[6.16, 8.72] / [6.13, 8.70]` | `92.16%` | `[90.40%, 93.53%]` | `0.0` | `4.4573` | `8.30e-06` | `2.20` | `2.14` | `0.8742` | `1.0000` |
| **SITI M3 vs. M1 Monolithic RDF (Deep Hops k=4..6, N=24)** | `24` | `22.415` | `0.784` | `-21.632` | `[19.89, 23.47] / [19.90, 23.48]` | `96.50%` | `[96.07%, 96.82%]` | `0.0` | `4.2857` | `1.82e-05` | `4.72` | `4.57` | `0.8748` | `1.0000` |
| **SITI M3 vs. M2 Row-Oriented SQL (Shallow Hops k=1..3, N=26)** | `26` | `5.063` | `0.633` | `-4.430` | `[3.64, 5.34] / [3.72, 5.49]` | `87.51%` | `[84.97%, 89.69%]` | `0.0` | `4.4573` | `8.30e-06` | `2.01` | `1.95` | `0.8742` | `1.0000` |
| **SITI M3 vs. M2 Row-Oriented SQL (Deep Hops k=4..6, N=24)** | `24` | `11.768` | `0.784` | `-10.984` | `[9.58, 12.54] / [9.67, 12.68]` | `93.34%` | `[92.35%, 94.26%]` | `0.0` | `4.2857` | `1.82e-05` | `2.85` | `2.75` | `0.8748` | `1.0000` |
| **SITI M3 vs. M2 Row-SQL (Zero-Geometry Operational Queries, N=40)** | `40` | `7.669` | `0.723` | `-6.946` | `[5.85, 8.04] / [5.89, 8.10]` | `90.58%` | `[89.07%, 91.76%]` | `0.0` | `5.5109` | `3.57e-08` | `1.95` | `1.91` | `0.8714` | `1.0000` |
| **SITI M3 vs. M2 Row-SQL (Late Spatial Materialization Queries, N=10)** | `10` | `10.729` | `0.634` | `-10.095` | `[6.22, 14.15] / [6.50, 14.51]` | `94.09%` | `[92.04%, 95.48%]` | `0.0` | `2.8031` | `5.06e-03` | `1.47` | `1.34` | `0.8864` | `1.0000` |

---

## D.4B Controlled Six-Paradigm Ablation (`M1`, `M1b`, `M2`, `M2b`, `M2c`, `M3`) and OLS / ANCOVA Hop-Scaling Inference (`Table D.3B`)

To isolate execution-engine vectorization (`DuckDB 1.5.5` / `PyArrow 23.0.1` vs. `SQLite 3.53.2` and `RDFLib 7.6.0`), geometric `WKT` payload externalization (`113,199` chunked `WKT` triples removed in hybrid `LBD` baseline `M1b`), and schema-level $\Gamma_{C2}$ traversal (`16,232` class nodes vs. `913,296` lightweight `ABox` instance triples in `M1b` and `288`-row relational foreign-key bridge joins in `M2b`/`M2c`), all $N_q = 50$ queries (`Q01`–`Q50`, $15$ warm timed iterations per engine on an `Apple M4 Pro` `arm64` workstation, 12 cores [8P+4E], `24.0 GB` RAM, `macOS 27.2`, `Python 3.14.6`) were evaluated across six indexed paradigms with `100%` tuple and numerical parity ($\max|\Delta| < 10^{-5}$):

### Table D.3B: Controlled Six-Paradigm Latency Breakdown ($k = 1 \dots 6$), OLS Hop-Scaling Slopes, and Pooled ANCOVA Interaction Tests

| Hop Stratum / Statistical Test | `M1` Monolithic RDF (`619,962` triples, ms) | `M1b` Hybrid LBD ABox (`913,296` triples, `0` WKT) + DuckDB SoA (ms) | `M2` Coupled SQLite 3 AoS (ms) | `M2b` Same-Engine DuckDB Decoupled SoA FK (ms) | `M2c` Same-Engine DuckDB Coupled WKB + FK (ms) | `M3` SITI Sealed / Live $C_1+C_2+C_3$ (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Hop Depth $k = 1$ ($n = 8$) | `3.840 ± 0.162` (`3.913` live) | `2.427 ± 1.292` | `3.810 ± 1.456` (`3.816` live) | `2.334 ± 0.223` | `6.288 ± 0.779` | `0.632 ± 0.109` (`0.614 ± 0.119` live) |
| Hop Depth $k = 2$ ($n = 9$) | `7.907 ± 0.469` (`7.997` live) | `1.277 ± 1.243` | `4.208 ± 1.175` (`4.181` live) | `3.406 ± 0.260` | `10.197 ± 0.674` | `0.620 ± 0.269` (`0.638 ± 0.281` live) |
| Hop Depth $k = 3$ ($n = 9$) | `11.998 ± 0.213` (`12.176` live) | `2.156 ± 1.422` | `7.032 ± 2.334` (`7.001` live) | `4.990 ± 0.331` | `15.079 ± 0.607` | `0.645 ± 0.195` (`0.632 ± 0.191` live) |
| Hop Depth $k = 4$ ($n = 8$) | `16.984 ± 0.214` (`17.163` live) | `2.905 ± 1.621` | `9.345 ± 2.614` (`9.336` live) | `6.171 ± 0.357` | `18.882 ± 0.692` | `0.649 ± 0.279` (`0.616 ± 0.266` live) |
| Hop Depth $k = 5$ ($n = 8$) | `22.150 ± 0.503` (`22.256` live) | `2.495 ± 1.343` | `11.508 ± 2.596` (`11.545` live) | `7.619 ± 0.213` | `23.139 ± 0.440` | `0.834 ± 0.126` (`0.824 ± 0.168` live) |
| Hop Depth $k = 6$ ($n = 8$) | `28.112 ± 0.645` (`28.257` live) | `2.504 ± 1.333` | `14.450 ± 4.646` (`14.349` live) | `8.939 ± 0.734` | `27.228 ± 1.410` | `0.868 ± 0.157` (`0.858 ± 0.175` live) |
| **Global $N = 50$ Mean ± SD (ms)** | **`14.957 ± 8.273`** (`15.091` live) | **`2.271 ± 1.406`** (`1,762.3 µs` ABox + `508.8 µs` C3) | **`8.281 ± 4.597`** (`8.255` live) | **`5.521 ± 2.316`** (`5,083.2 µs` FK + `437.9 µs` C3) | **`16.636 ± 7.257`** | **`0.705 ± 0.217`** (`0.695 ± 0.228` live: `6.85+63.50+624.78 µs`) |
| **Speedup vs. `M3` Sealed / Live** | `21.21×` / `21.71×` | `3.22×` / `3.27×` (`27.75×` graph stage) | `11.75×` / `11.88×` | **`7.83×` / `7.94×`** | `23.59×` / `23.93×` | `1.00×` reference |
| **Workload $\Phi_{\text{eff}}^{\text{(QT)}}$ Sealed / Live** | `95.29%` / `95.39%` | `68.95%` / `69.39%` | `91.49%` / `91.58%` | **`87.23%` / `87.41%`** | `95.76%` / `95.82%` | — |
| **Paired Wilcoxon ($N = 50$) vs. `M3`** | $W=0$, $Z=6.154$, $p_{\text{exact}}=1.78\times 10^{-15}$ | $W=116$, $Z=5.034$, $p_{\text{exact}}=3.35\times 10^{-8}$ | $W=0$, $Z=6.154$, $p_{\text{exact}}=1.78\times 10^{-15}$ | $W=0$, $Z=6.154$, $p_{\text{exact}}=1.78\times 10^{-15}$ | $W=0$, $Z=6.154$, $p_{\text{exact}}=1.78\times 10^{-15}$ | Location-shift test (distinct from OLS) |
| **Stratum OLS Slope $\beta \pm \text{SE}$ (ms/hop, $df=4$)** | `4.8307 ± 0.1817` ($t=26.58$, $p=1.19\times 10^{-5}$) | `0.1367 ± 0.1310` ($t=1.04$, $p=0.356$) | `2.2118 ± 0.1714` ($t=12.90$, $p=2.08\times 10^{-4}$) | `1.3384 ± 0.0270` ($t=49.48$, $p=9.98\times 10^{-7}$) | `4.2094 ± 0.0587` ($t=71.69$, $p=2.27\times 10^{-7}$) | `0.05208 ± 0.01455` ($t=3.58$, $p=0.0232$) |
| **Slope Ratio & ANCOVA $F(1,8)$ vs. `M3`** | `92.75×` ($F=687.2$, $p=4.82\times 10^{-9}$) | `2.63×` ($F=0.41$, $p=0.538$; `35.56×` flatter than `M1`) | `42.47×` ($F=157.6$, $p=1.52\times 10^{-6}$) | **`25.70×` (`25.85×` live; $F=1,549.2$, $p=1.91\times 10^{-10}$)** | `80.83×` ($F=4,724.5$, $p=2.25\times 10^{-12}$) | Disaggregated $N=50$ ANCOVA $p \le 3.95\times 10^{-16}$ |

---

## D.5 Markov Blanket ($\partial\mathcal{M}(v)$) Causal Isolation Across the 316 Layer 2 Anchor Nodes and Top 15 National Hubs (`Table D.4`)

### Table D.4: Spectral Graph Theory ($L = D - W$) and Markov Blanket $\partial\mathcal{M}(u)$ Complexity Reduction

| Rank / Hub Code | Canonical Class Name (SITI Layer 1/2) | Table | Intertabular Degree ($d_{\text{in}} + d_{\text{out}}$) | Parents $|\text{Pa}(v)|$ | Children $|\text{Ch}(v)|$ | Spouses $|\text{Sp}(v)|$ | Full Markov Blanket $|\partial\mathcal{M}(v)|$ | Intertabular $|\partial\mathcal{M}_{\text{inter}}(v)|$ | Extraction Latency ($\mu\text{s}$) | Causal Isolation $\Phi_{\text{eff}}^{\text{(Markov-Isolation)}}$ (\%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `#1` (`A30_035_005_040`) | Calzada o carril vehicular | `A30` | `51` (`17+34`) | `18` | `32` | `61` | **`97`** | `96` | `25.000` | **`99.3963%`** |
| `#2` (`A40_045_005_030`) | Sistema de pavimento o calzada flexible | `A40` | `28` (`5+23`) | `6` | `22` | `55` | **`77`** | `76` | `15.959` | **`99.5195%`** |
| `#3` (`B10_010_030_015`) | Contrato de obra pública e interventoría de infraestructura vial y fluvial (INVIAS) | `B10` | `43` (`17+26`) | `17` | `24` | `36` | **`70`** | `69` | `18.084` | **`99.5626%`** |
| `#4` (`B40_020_035_920`) | Actividades de riegos bituminosos y capas de pavimentos asfálticos (Capítulo 400 INVIAS) | `B40` | `39` (`12+27`) | `13` | `27` | `40` | **`68`** | `67` | `17.083` | **`99.5749%`** |
| `#5` (`A40_140_010`) | Circuito de vía de audiofrecuencia sin juntas | `A40` | `28` (`11+17`) | `12` | `18` | `50` | **`67`** | `66` | `15.750` | **`99.5811%`** |
| `#6` (`B20_025_005_00024`) | Agencia Nacional de Infraestructura - ANI | `B20` | `38` (`0+38`) | `1` | `33` | `44` | **`65`** | `64` | `14.250` | **`99.5934%`** |
| `#7` (`B40_025_005_015`) | Limpieza hidrodinámica, descolmatación y conservación preventiva de obras de drenaje | `B40` | `25` (`13+12`) | `14` | `12` | `39` | **`62`** | `61` | `11.167` | **`99.6119%`** |
| `#8` (`B40_020_035_910`) | Actividades de explanación, excavación de cortes y conformación de terraplenes (Capítulo 200 INVIAS) | `B40` | `22` (`9+13`) | `10` | `13` | `50` | **`62`** | `61` | `12.583` | **`99.6119%`** |
| `#9` (`A40_085_005_005`) | Superestructura | `A40` | `22` (`4+18`) | `5` | `16` | `44` | **`59`** | `58` | `14.083` | **`99.6304%`** |
| `#10` (`B40_020_035_905`) | Actividades preliminares, desmonte, limpieza y demoliciones en carreteras (Capítulo 200 INVIAS) | `B40` | `16` (`4+12`) | `5` | `12` | `52` | **`59`** | `58` | `13.208` | **`99.6304%`** |
| `#11` (`A10_025_065_015`) | Predio e inmueble afectado por adquisición predial y derecho de vía | `A10` | `13` (`2+11`) | `3` | `11` | `47` | **`56`** | `55` | `16.917` | **`99.6488%`** |
| `#12` (`B40_020_035_930`) | Actividades de estructuras de concreto, acero, cimentaciones profundas y puentes (Capítulo 600 INVIAS) | `B40` | `22` (`7+15`) | `8` | `15` | `37` | **`54`** | `53` | `11.583` | **`99.6612%`** |
| `#13` (`B10_010_010_210`) | Apéndice técnico 4 (AT4) - Indicadores de disponibilidad, seguridad y nivel de servicio | `B10` | `20` (`6+14`) | `7` | `15` | `33` | **`54`** | `52` | `12.042` | **`99.6612%`** |
| `#14` (`A50_015_005_025`) | Segregador físico y confinamiento de ciclorruta y carril exclusivo no motorizado | `A50` | `20` (`9+11`) | `10` | `12` | `40` | **`54`** | `52` | `11.417` | **`99.6612%`** |
| `#15` (`A30_035_010_015`) | Estación de peaje | `A30` | `16` (`4+12`) | `5` | `12` | `39` | **`52`** | `50` | `10.917` | **`99.6735%`** |
| **Mean (316 Anchor Nodes)** | Intertabularly Coupled Anchor Subgraph | `A10–B50` | **`5.02`** | `3.44` | `2.60` | `7.68` | **`12.76`** | `11.75` | `3.311` | **`99.9152%`** |
| **Mean (All 16,232 C2 Nodes)** | Complete SITI Layer 2 Topological Graph | `A10–B50` | `0.0977` | `1.05` | `0.06` | `0.15` | **`1.24`** | `0.2288` | `2.152` | **`99.9862%`** |

---

## D.6 Shift-Left OpenBIM/GIS Authoring Kits (`9` Kits) and Retrospective Evolution of $\Phi_{\text{eff}}$ Across the 5 CAS Lineage Stages (`Table D.5`)

### Table D.5 (Panel A): Cryptographic Audit of the 9 Shift-Left OpenBIM and GIS Authoring Kits

| Kit ID | Suite | Target Authoring Tool / Standard | Verified Files | Total Size (Bytes) | Composite `SHA-256` Prefix | Covered SITI Classes / Psets | Prevented Wave 2 Cold-Ingestion Failures (`unsupported` / `partial`) | $\Phi_{\text{eff}}^{\text{(Shift-Left)}}$ (\%) |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| `KIT-BIM-01` | `Kits_BIM` | **Autodesk Revit (Assembly Codes, Classification DB & Shared Parameters)** | `9` | `20,048,329` | `50d5a6663bed42de...` | `16,230 classes + 4,088 shared params` | Prevents 1 binary RVT unsupported + 15 unclassified family partial receipts | **`100.00%`** |
| `KIT-BIM-02` | `Kits_BIM` | **Graphisoft ArchiCAD (XML Classification Systems A10–A50 / B10–B50 & Properties)** | `9` | `51,406,216` | `97873c17c67196fc...` | `16,230 classes (4,686 A + 11,544 B)` | Prevents 12 partial BIM exports with A/B axis conflation | **`100.00%`** |
| `KIT-BIM-03` | `Kits_BIM` | **Autodesk Civil 3D (EPSG:9377 Survey Point, Corridor DXF & Intermodal Contracts)** | `5` | `2,708,029` | `b148d1c100ffd24b...` | `4,686 physical classes + EPSG:9377 CRS` | Prevents 10 partial DXF corridor alignments & local coordinate drift | **`100.00%`** |
| `KIT-BIM-04` | `Kits_BIM` | **buildingSMART IFC 4.3 (ISO 16739-1:2024 732 Psets + 117 Qtos = 849 Sets)** | `6` | `10,156,059` | `98b0790e2ac38056...` | `849 sets (732 Pset + 117 Qto, 4,088 props)` | Prevents 26 mute IFC unsupported + 27 partial IFC receipts | **`100.00%`** |
| `KIT-BIM-05` | `Kits_BIM` | **Blender Headless CLI / OpenUSD (Bimodal 64-bit EPSG:9377 Anchor + 32-bit Local ENU Affine Exchange)** | `3` | `44,071` | `bbb4a1ea45dcfd75...` | `5,011 bimodal 64-bit EPSG:9377 + 32-bit local ENU instances + OpenUSD` | Prevents float32 vertex jitter & untracked 3D mesh exports | **`100.00%`** |
| `KIT-GIS-06` | `Kits_GIS` | **Esri ArcGIS Pro (Python Toolbox .pyt, XML Workspace, Arcade Rules & Contingent Values)** | `8` | `8,571,406` | `a6befdb1ce363145...` | `16,230 coded domain values + Arcade CWA` | Prevents 42 uncoded GIS feature tables & domain drift | **`100.00%`** |
| `KIT-GIS-07` | `Kits_GIS` | **QGIS 3.x Official Template (GeoPackage MAGNA 9377, QML Form & QLR Layers)** | `5` | `18,539,994` | `de7900a8905835d4...` | `13 GPKG tables (16,230 classes + 2,892 SKOS)` | Prevents 21 unstructured TXT + 1 corrupt CSV + 56 partial CSVs | **`100.00%`** |
| `KIT-GIS-08` | `Kits_GIS` | **PostgreSQL / PostGIS Spatial Relational Schema (EPSG:9377 WKB & Intermodal Contracts)** | `4` | `9,687,776` | `34409bd7f1de2868...` | `226,322 EPSG:9377 WKB geometries + SRID checks` | Prevents 24 partial SQL dumps lacking explicit SRID/codigo_siti | **`100.00%`** |
| `KIT-GIS-09` | `Kits_GIS` | **ET GeoWizards / CAD-to-GIS Topological Cleaning & Value Mapping Dictionary** | `3` | `2,902,109` | `c3001a8a01de278a...` | `16,230 XML mapped values + OGC WKT CRS` | Prevents 15 partial CAD-to-GIS polygon/polyline topology gaps | **`100.00%`** |
| **TOTAL (9 Kits)** | **BIM (5) + GIS (4)** | **Complete Shift-Left Ecosystem (`siti_production_corpus/`)** | **`51`** (`52` refs) | **`124,060,870`** | `f8d93f7313919ca2...` | **`16,230` classes + `849` Psets/Qtos** | **Prevents `49/49` `unsupported` (`100%`) & `174/174` `partial` (`100%`)** | **`100.00%`** |

### Table D.5 (Panel B): Retrospective Evolution of $\Phi_{\text{eff}}$ Across the 5 CAS Lineage Stages

| Lineage Stage | Publication / Revision ID | Active C2 Intertabular Edges | Active Recipes | Queries Reconstructed Without Orphanage ($n/50$) | Query Completion Rate (\%) | Mean Reconstruction Latency (ms) | $\Phi_{\text{eff}}^{\text{(Query-Time vs M1)}}$ (\%) | $\Phi_{\text{eff}}^{\text{(Query-Time vs M2)}}$ (\%) | $\Phi_{\text{eff}}^{\text{(Markov-Isolation)}}$ (\%) | $\Phi_{\text{eff}}^{\text{(Shift-Left-Kits)}}$ (\%) | Composite $\Phi_{\text{eff}}$ (\%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 0 (Stage S0 initial baseline)** | `Pre-CAS Baseline (15,982 classes, 0 C2 edges)` | `0` | `0/13` | `12/50` | **`24.00%`** | `6.790` | `54.60%` | `18.00%` | `0.0000%` | `22.22%` | **`16.53%`** |
| **Stage 1 (CAS 1: Railway)** | `340ed01141b7448e8d6157bd05aab5e2` | `0` | `4/13` | `17/50` | **`34.00%`** | `4.472` | `70.10%` | `46.00%` | `0.0000%` | `55.56%` | **`35.23%`** |
| **Stage 2 (CAS 2: Stage S2)** | `9a3cc6d9a341e551b95fecf286948fb2` | `344` | `8/13` | `34/50` | **`68.00%`** | `1.728` | `88.45%` | `79.14%` | `99.1205%` | `77.78%` | **`80.15%`** |
| **Stage 3 (CAS 3: Stage S3)** | `55e94d32a7f24ee70684c7c1b01de82d` | `793` | `13/13` | `50/50` | **`100.00%`** | `0.804` | `94.63%` | `90.29%` | `99.9152%` | `88.89%` | **`94.43%`** |
| **Stage 4 (CAS 4: Stage S4)** | `b6bd01f850790ad22d399b95545f73d2` | `793` | `13/13` | `50/50` | **`100.00%`** | `0.705` | `95.29%` | `91.49%` | `99.9152%` | `100.00%` | **`96.58%`** |

---
