# Supplementary Appendix F: Unified Longitudinal Trajectory of the Semantic Interoperability Index (SII), Dirichlet Simplex Sensitivity ($B = 10,000$), Three-Layer Ablation, and Concession Handover Archetypes

**Manuscript Title:** *Orthogonal Ontology Factorization for Semantic Interoperability in Transport Infrastructure* (`ORTHOGONAL ONTOLOGY FACTORIZATION FOR SEMANTIC INTEROPERABILITY IN TRANSPORT INFRASTRUCTURE`)  
**Authors:** Juan C. Gómez (Corresponding Author; PhD candidate, Doctoral program in Technology Innovation Management, Universidad de los Andes, and National Infrastructure Agency (ANI), Bogotá, Colombia, `jc.gomez1988@uniandes.edu.co`), Rodrigo F. Herrera (Associate professor, School of Civil Engineering, Pontificia Universidad Católica de Valparaíso, Valparaíso, Chile, `rodrigo.herrera@pucv.cl`), Karen M. Castañeda (Assistant professor, School of Civil Engineering, Pontificia Universidad Católica de Valparaíso, Valparaíso, Chile, `karen.castaneda@pucv.cl`), and Juan F. Correal (Full professor, Department of Civil and Environmental Engineering, Universidad de los Andes, Bogotá, Colombia, `jcorreal@uniandes.edu.co`)  
**Reference:** Gómez, J. C., Herrera, R. F., Castañeda, K. M., & Correal, J. F. (2027). Orthogonal ontology factorization for semantic interoperability in transport infrastructure. *Journal of Information Technology in Construction (ITcon)*, 32, 1-X. https://doi.org/10.36680/j.itcon.2027.[added by editor]  
**Target Journal:** *Journal of Information Technology in Construction (ITcon)* — Q1 Peer-Reviewed Resubmission  
**Active SITI CAS Semantic Publication:** `b6bd01f850790ad22d399b95545f73d2` (`Stage S4`)  
**Execution Timestamp (UTC):** `2026-11-03T00:20:52.235489+00:00`  
**Forensic Verification Protocol:** Strict `os.O_RDONLY` ingestion across Waves 1–6 (`0` bytes modified in `siti_production_corpus/`, `bundles/`, `Kits_BIM/`, `Kits_GIS/`, and all 9 primary source libraries), deterministic Abstract Syntax Tree (AST) live bipolar verification (`4/4` compliant methods, `36` live engine calls, `0` static JSON reads), and 100% programmatic Stage 5 (Automated Manuscript-to-Corpus Table Synchronization) synchronization across `Appendix_A..F` and `Table_1..8`.

---

## F.1 Mathematical Reconciliation of the Semantic Interoperability Index (SII) and Formal Algebraic Reconstruction Operator

In `Stage S0 (initial baseline)`, a terminological conflation between single-subset taxonomic coverage (`48.20%` over the initial `47,768`-row pilot road table: `23,024` linked vs. `24,744` orphans) and multi-dimensional interoperability caused an apparent contradiction between `Table 2` and `Table 5`. In this resubmission, every dimension and denominator is formally separated and evaluated longitudinally across the **5 real Content-Addressable Storage (CAS) lineage stages** (`Stage S0 (initial baseline)` through `Stage 4: CAS b6bd01f8`):

$$\text{SII}_s(\mathbf{w}) = w_1 \Phi_{\text{ont}, s} + w_2 \Phi_{\text{sem}, s} + w_3 \Phi_{\text{eff}, s}, \qquad \mathbf{w} = (w_1, w_2, w_3) \in \Delta^2 = \{ \mathbf{w} \in \mathbb{R}_+^3 : w_1 + w_2 + w_3 = 1 \}$$

Rather than hard-wiring operational attributes and geometric meshes into a monolithic class hierarchy, SITI evaluates cross-domain lifecycle queries at runtime through the **Three-Layer Algebraic Reconstruction Operator**:

$$\mathcal{R}_Q = \Pi_{C3} \circ \Gamma_{C2} \circ \Sigma_{C1}$$

where:
1. $\Sigma_{C1}$ (*Intensional Semantic & Closed-World Operator* on `C1`): maps multilingual input terms via `2,892` SKOS expressions (`134` colliding `A50_045` stems / `179` secondary occurrences disambiguated via `__occN`, with `8` explicit `SKOS` notes) onto `16,230` orthogonal classes (`4,686` `Language A` $\perp$ `11,544` `Language B`), enforcing `814` `OWL 2 DL` existential restrictions and `104` `W3C SHACL` Closed-World shapes (`PAR_B50_0001..0100`).
2. $\Gamma_{C2}$ (*Bounded Topological Traversal Operator* on `C2`): expands inter-tabular relationships across `793` deduplicated edges (`13` canonical assembly recipes `REC-A-01..07`, `REC-B-01..06`, `0` intra-tabular meronymy) strictly confined within the target node's Markov Blanket $\partial\mathcal{M}(u)$ (mean `12.76` nodes, `99.92%` graph isolation).
3. $\Pi_{C3}$ (*Columnar SoA & Selective Late Spatial Projection Operator* on `C3`): projects operational attributes from `siti_ani_activos_principales.parquet` (`18.48 MB` ZSTD / `0.22 MB` 8-column `SoA`) and bitemporal `UUIDv7` `Unboxed EAV` vectors (`ROW_NUMBER()` windowing, `0` mutable `is_active` flags), materializing `EPSG:9377 WKB` or bimodal 64-bit `EPSG:9377` anchor + 32-bit local `ENU` / `OpenUSD` geometries (`455.88 MB`) *only* for records satisfying spatial predicates.

> **Columnar Benchmark Timing Note:** All wide sparse `AoS` baselines (`E1a`: `11,565` columns; `E1b`: `759` columns) in `Appendix E` reflect live block-partitioned `time.perf_counter_ns()` executions (`15` scan iterations plus `5` temporal reconciliation iterations per batch $N \in \{1,000 \dots 226,324\}$).

---

## F.2 Consolidated 5-Stage Longitudinal Trajectory Across Four Evaluation Regimes (`V1–V4`, `Table F.1`)

To preclude any ambiguity regarding metric selection, `Table F.1` reports four explicit regimes:
- **`V1` (`Strict Primary Empirical SII — Baseline vs. M1 Monolithic RDF`, Canonical Manuscript Metric):** combines $\Phi_{\text{ont}}^{\text{(Core-3)}}$ (`23.85% -> 100.00%`), $\Phi_{\text{sem}}^{\text{(Panel A47 Shannon)}}$ (`17.02% -> 95.47%`, retaining irreducible engineering polymorphism $H = 0.1578\text{ bits}$), and $\Phi_{\text{eff}}^{\text{(vs. M1)}}$ (`13.10% -> 95.29%` effective penalized by query orphanage; `54.60% -> 95.29%` conditional on completed queries). Under equal weights $[1/3,1/3,1/3]$, canonical `V1` rises from **`17.99%` in `Stage 0` to `96.92%` in `Stage 4`** (`+78.93 pp`; design weights `[0.35,0.35,0.30]`: `18.23% -> 97.00%`).
- **`V2` (`Strict Primary Empirical SII — Baseline vs. M2 Row-SQL`):** benchmarks $\Phi_{\text{eff}}$ against indexed relational AoS tables (`91.49%` in `Stage 4`), yielding **`95.65%`** (`95.86%` design).
- **`V3` (`Cold-Ingestion Inclusive SII — Raw 603 CDE Receipts`):** replaces $\Phi_{\text{ont}}^{\text{(Core-3)}}$ with $\Phi_{\text{ont}}^{\text{(All-4 Raw 603)}} = 97.97\%$, explicitly penalizing the `49` legacy proprietary/unstructured files (`26` Pset-less B-Rep IFCs, `21` free-text `.txt`, `1` closed `.rvt`, `1` corrupted `.csv`) received without Shift-Left authoring kits, yielding **`96.24%`**.
- **`V4` (`Comprehensive Multi-Submetric Composite SII`):** averages all submetrics per dimension ($\Phi_{\text{ont}} = 100.00\%$, $\Phi_{\text{sem}} = 98.49\%$, $\Phi_{\text{eff}} = 96.58\%$), reaching **`98.36%`**.

Across both national cohorts, the paired jump $\Delta\text{SII}(S_0 \to S_4)$ is statistically overwhelming: **`+77.11 pp`** across the `N = 47` itemized asset partitions (Wilcoxon $W = 0.0, Z = 5.968, p = 1.421e-14$, Hedges' $g = 54.64$) and **`+77.53 pp`** across the `N = 50` master concessions ($W = 0.0, Z = 6.154, p = 1.776e-15$, Hedges' $g = 39.21$).

### Table F.1 (Panel A): Macro Longitudinal Trajectory (`V1–V4`)

| Stage & CAS Release | $\Phi_{\text{ont}}^{\text{(Core-3)}}$ (\%) | $\Phi_{\text{ont}}^{\text{(Raw-603)}}$ (\%) | $\Phi_{\text{sem}}^{\text{(Panel A47)}}$ (\%) | $\Phi_{\text{sem}}^{\text{(Comp.)}}$ (\%) | Query Compl. (\%) | $\Phi_{\text{eff}}^{\text{(Eff. M1)}}$ (\%) | $\Phi_{\text{eff}}^{\text{(Cond. M1)}}$ (\%) | `V1` Canonical Equal / Design (\%) | `V1-Cond` Equal (\%) | `V2` vs. SQL Equal (\%) | `V3` Raw-603 Equal (\%) | `V4` Composite Equal (\%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 0 (Stage S0 initial baseline)** | `23.85%` | `17.89%` | `17.02%` | `5.67%` | `24.0%` | `13.10%` | `54.60%` | **`17.99%` / `18.23%`** | `31.82%` | `15.06%` | `16.00%` | `15.35%` |
| **Stage 1 (CAS 340ed011 — Railway)** | `42.30%` | `31.72%` | `50.06%` | `16.69%` | `48.0%` | `31.11%` | `64.81%` | **`41.16%` / `41.66%`** | `52.39%` | `38.15%` | `37.63%` | `31.41%` |
| **Stage 2 (CAS 9a3cc6d9 — Stage S2)** | `81.05%` | `60.79%` | `76.90%` | `39.72%` | `82.0%` | `67.62%` | `82.46%` | **`75.19%` / `75.57%`** | `80.14%` | `74.28%` | `68.44%` | `66.97%` |
| **Stage 3 (CAS 55e94d32 — Stage S3)** | `100.00%` | `97.97%` | `93.37%` | `97.79%` | `100.0%` | `94.15%` | `94.15%` | **`95.84%` / `95.92%`** | `95.84%` | `94.55%` | `95.16%` | `97.41%` |
| **Stage 4 (CAS b6bd01f8 — Stage S4)** | `100.00%` | `97.97%` | `95.47%` | `98.49%` | `100.0%` | `95.29%` | `95.29%` | **`96.92%` / `97.00%`** | `96.92%` | `95.65%` | `96.24%` | `98.36%` |

### Table F.1 (Panel B): Paired Non-Parametric & Bootstrap Inference Across `N = 47` Partitions and `N = 50` Concessions

| Empirical Cohort | Units $N$ | Transition | Mean $\text{SII}_{\text{start}}$ (\%) | Mean $\text{SII}_{\text{end}}$ (\%) | Mean $\Delta\text{SII}$ (pp) | Bootstrap 95\% CI ($B=10,000$, pp) | Wilcoxon $W$ | Wilcoxon $Z$ | Two-Sided $p$-Value | Cohen's $d$ / Hedges' $g$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Panel A (Itemized Partitions)** | `47` | `S0 -> S1` | `19.15%` | `40.03%` | **`+20.87`** | `[20.47, 21.32]` | `0.0` | `5.968` | `1.421e-14` | `13.91 / 13.69` |
| **Panel A (Itemized Partitions)** | `47` | `S1 -> S2` | `40.03%` | `74.09%` | **`+34.07`** | `[33.85, 34.34]` | `0.0` | `5.968` | `1.421e-14` | `39.53 / 38.88` |
| **Panel A (Itemized Partitions)** | `47` | `S2 -> S3` | `74.09%` | `95.18%` | **`+21.09`** | `[20.76, 21.40]` | `0.0` | `5.968` | `1.421e-14` | `18.60 / 18.30` |
| **Panel A (Itemized Partitions)** | `47` | `S3 -> S4` | `95.18%` | `96.26%` | **`+1.08`** | `[1.06, 1.10]` | `0.0` | `5.968` | `1.421e-14` | `13.94 / 13.71` |
| **Panel A (Itemized Partitions)** | `47` | `S0 -> S4` | `19.15%` | `96.26%` | **`+77.11`** | `[76.76, 77.55]` | `0.0` | `5.968` | `1.421e-14` | `55.55 / 54.64` |
| **Panel B (Master Concessions)** | `50` | `S0 -> S1` | `18.73%` | `39.50%` | **`+20.77`** | `[20.42, 21.17]` | `0.0` | `6.154` | `1.776e-15` | `15.14 / 14.90` |
| **Panel B (Master Concessions)** | `50` | `S1 -> S2` | `39.50%` | `73.75%` | **`+34.25`** | `[34.03, 34.52]` | `0.0` | `6.154` | `1.776e-15` | `38.48 / 37.88` |
| **Panel B (Master Concessions)** | `50` | `S2 -> S3` | `73.75%` | `95.14%` | **`+21.39`** | `[21.01, 21.80]` | `0.0` | `6.154` | `1.776e-15` | `14.99 / 14.76` |
| **Panel B (Master Concessions)** | `50` | `S3 -> S4` | `95.14%` | `96.26%` | **`+1.12`** | `[1.08, 1.16]` | `0.0` | `6.154` | `1.776e-15` | `8.71 / 8.57` |
| **Panel B (Master Concessions)** | `50` | `S0 -> S4` | `18.73%` | `96.26%` | **`+77.53`** | `[77.04, 78.11]` | `0.0` | `6.154` | `1.776e-15` | `39.82 / 39.21` |

---

## F.3 Dirichlet Simplex Monte Carlo Sensitivity ($B = 10,000$) and Boundary Vertex Evaluation (`Table F.2`)

To prove that SITI's longitudinal improvement is not an artifact of ad-hoc indicator weights, $B = 10,000$ weight vectors $\mathbf{w} \sim \text{Dirichlet}(1,1,1)$ (`seed = 20261102`) plus a deterministic $5,151$-point simplex lattice were evaluated across all regimes. Over the interior of $\Delta^2$, strict monotonic stage dominance $\text{SII}(S_4) > \text{SII}(S_3) > \text{SII}(S_2) > \text{SII}(S_1) > \text{SII}(S_0)$ holds on **`10000 / 10000` (`100.00%`, $p < 10^{-15}$)** of draws across every variant (`V1–V4`). Even at the extreme degenerate vertex $\mathbf{w} = (1,0,0)$ (pure ontological binding, ignoring semantics and efficiency), $\text{SII}(S_4) = \text{SII}(S_3) = 100.00\% > 81.05\% > 42.30\% > 23.85\%$.

### Table F.2 (Panel A): Dirichlet Monte Carlo ($B = 10,000$) and Deterministic Lattice Summary

| SII Variant Regime | Stage | Dirichlet Mean ± SD (\%) | Median (\%) | 95\% Credible Interval $[p_{2.5}, p_{97.5}]$ (\%) | Simplex Absolute $[\min, \max]$ (\%) | Grid Mean ($5,151$ pts, \%) | Rank Dominance $P(S_4 > S_3 > S_2 > S_1 > S_0)$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `V1_EFFECTIVE` | **S0** | `18.00 ± 2.21` | `17.80` | `[14.14, 22.54]` | `[13.10, 23.85]` | `17.99` | `—` |
| `V1_EFFECTIVE` | **S1** | `41.18 ± 3.89` | `41.46` | `[33.46, 48.18]` | `[31.11, 50.06]` | `41.16` | `—` |
| `V1_EFFECTIVE` | **S2** | `75.21 ± 2.80` | `75.56` | `[69.36, 79.88]` | `[67.62, 81.05]` | `75.19` | `—` |
| `V1_EFFECTIVE` | **S3** | `95.84 ± 1.48` | `95.59` | `[93.73, 99.05]` | `[93.37, 100.00]` | `95.84` | `—` |
| `V1_EFFECTIVE` | **S4** | `96.92 ± 1.09` | `96.73` | `[95.43, 99.30]` | `[95.29, 100.00]` | `96.92` | `100.00% (10,000/10,000)` |
| `V1_CONDITIONAL` | **S0** | `31.77 ± 8.16` | `30.41` | `[19.48, 49.13]` | `[17.02, 54.60]` | `31.82` | `—` |
| `V1_CONDITIONAL` | **S1** | `52.36 ± 4.65` | `51.88` | `[44.35, 61.96]` | `[42.30, 64.81]` | `52.39` | `—` |
| `V1_CONDITIONAL` | **S2** | `80.13 ± 1.19` | `80.28` | `[77.64, 82.01]` | `[76.90, 82.46]` | `80.14` | `—` |
| `V1_CONDITIONAL` | **S3** | `95.84 ± 1.48` | `95.59` | `[93.73, 99.05]` | `[93.37, 100.00]` | `95.84` | `—` |
| `V1_CONDITIONAL` | **S4** | `96.92 ± 1.09` | `96.73` | `[95.43, 99.30]` | `[95.29, 100.00]` | `96.92` | `100.00% (10,000/10,000)` |
| `V2_SQL` | **S0** | `15.09 ± 4.03` | `15.49` | `[6.78, 22.06]` | `[4.32, 23.85]` | `15.06` | `—` |
| `V2_SQL` | **S1** | `38.18 ± 5.89` | `38.98` | `[25.90, 47.78]` | `[22.08, 50.06]` | `38.15` | `—` |
| `V2_SQL` | **S2** | `74.30 ± 3.41` | `74.81` | `[67.05, 79.76]` | `[64.89, 81.05]` | `74.28` | `—` |
| `V2_SQL` | **S3** | `94.56 ± 2.02` | `94.35` | `[91.17, 98.77]` | `[90.29, 100.00]` | `94.55` | `—` |
| `V2_SQL` | **S4** | `95.66 ± 1.73` | `95.61` | `[92.41, 99.05]` | `[91.49, 100.00]` | `95.65` | `100.00% (10,000/10,000)` |
| `V3_RAW603` | **S0** | `16.01 ± 1.04` | `16.18` | `[13.78, 17.57]` | `[13.10, 17.89]` | `16.00` | `—` |
| `V3_RAW603` | **S1** | `37.65 ± 4.41` | `36.92` | `[31.65, 47.15]` | `[31.11, 50.06]` | `37.63` | `—` |
| `V3_RAW603` | **S2** | `68.44 ± 3.31` | `68.27` | `[62.47, 74.96]` | `[60.79, 76.90]` | `68.44` | `—` |
| `V3_RAW603` | **S3** | `95.16 ± 1.00` | `95.00` | `[93.67, 97.32]` | `[93.37, 97.97]` | `95.16` | `—` |
| `V3_RAW603` | **S4** | `96.24 ± 0.61` | `96.14` | `[95.40, 97.58]` | `[95.29, 97.97]` | `96.24` | `100.00% (10,000/10,000)` |
| `V4_COMPOSITE` | **S0** | `15.35 ± 3.75` | `15.59` | `[7.90, 22.00]` | `[5.67, 23.85]` | `15.35` | `—` |
| `V4_COMPOSITE` | **S1** | `31.40 ± 5.42` | `32.07` | `[20.11, 40.14]` | `[16.69, 42.30]` | `31.41` | `—` |
| `V4_COMPOSITE` | **S2** | `66.94 ± 9.68` | `68.56` | `[46.08, 80.06]` | `[39.72, 81.05]` | `66.97` | `—` |
| `V4_COMPOSITE` | **S3** | `97.41 ± 1.14` | `97.50` | `[95.11, 99.45]` | `[94.43, 100.00]` | `97.41` | `—` |
| `V4_COMPOSITE` | **S4** | `98.36 ± 0.70` | `98.39` | `[96.98, 99.65]` | `[96.58, 100.00]` | `98.36` | `100.00% (10,000/10,000)` |

### Table F.2 (Panel B): Exact Simplex Vertices and Notable Weight Schemes

| Simplex Weight Vector $(w_1, w_2, w_3)$ | Regime Role | `V1` $S_0$ (\%) | `V1` $S_1$ (\%) | `V1` $S_2$ (\%) | `V1` $S_3$ (\%) | `V1` $S_4$ (\%) | $\Delta(S_0 \to S_4)$ (pp) | `V3` Raw-603 $S_4$ (\%) | `V4` Comp. $S_4$ (\%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `(1/3, 1/3, 1/3)` | Canonical Equal-Weight Centroid | `17.99` | `41.16` | `75.19` | `95.84` | **`96.92`** | **`+78.93`** | `96.24` | `98.36` |
| `(0.35, 0.35, 0.30)` | SITI Institutional Design Weights | `18.23` | `41.66` | `75.57` | `95.92` | **`97.00`** | **`+78.76`** | `96.29` | `98.44` |
| `(1.00, 0.00, 0.00)` | Pure Ontological Binding Vertex | `23.85` | `42.30` | `81.05` | `100.00` | **`100.00`** | **`+76.15`** | `97.97` | `100.00` |
| `(0.00, 1.00, 0.00)` | Pure Semantic Disambiguation Vertex | `17.02` | `50.06` | `76.90` | `93.37` | **`95.47`** | **`+78.45`** | `95.47` | `98.49` |
| `(0.00, 0.00, 1.00)` | Pure Query-Time Efficiency Vertex | `13.10` | `31.11` | `67.62` | `94.15` | **`95.29`** | **`+82.18`** | `95.29` | `96.58` |
| `(0.50, 0.25, 0.25)` | Ontology-Dominant Interior Regime | `19.46` | `41.44` | `76.65` | `96.88` | **`97.69`** | **`+78.23`** | `96.67` | `98.77` |
| `(0.25, 0.50, 0.25)` | Semantics-Dominant Interior Regime | `17.75` | `43.38` | `75.62` | `95.22` | **`96.55`** | **`+78.81`** | `96.05` | `98.39` |
| `(0.25, 0.25, 0.50)` | Efficiency-Dominant Interior Regime | `16.77` | `38.64` | `73.30` | `95.42` | **`96.51`** | **`+79.74`** | `96.00` | `97.91` |

---

## F.4 Layer-by-Layer and Component-Wise Architectural Ablation Study (`Abl-1` to `Abl-6`, `Table F.3`)

### Table F.3: Layer-by-Layer and Component-Wise Architectural Ablation Study (Abl-1 to Abl-6)

| Configuration ID | Removed Architectural Mechanism | $\Phi_{\text{ont}}$ (\%) | $\Phi_{\text{sem}}$ (\%) | $\Phi_{\text{eff}}$ (\%) | $\text{SII}_{\text{equal}}$ (\%) | $\Delta\text{SII}_{\text{equal}}$ (pp) | $\text{SII}_{\text{design}}$ (\%) | Empirical Failure / Degradation Mechanism |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **STAGE4_FULL** | None (Full SITI Stage 4 Three-Layer Closure — CAS b6bd01f8) | `100.00%` | `95.47%` | `95.29%` | **`96.92%`** | `0.00` | `97.00%` | All 3 layers active: A ⊥ B decoupling, 2,892 SKOS + __occN, 104 SHACL shapes, 793 C2 edges, SoA + Unboxed EAV, 9 Kits |
| **Abl-1** | Without Language A ⊥ Language B Orthogonal Decoupling (Monolithic Pre-Coordinated Classes) | `74.45%` | `68.42%` | `78.15%` | **`73.67%`** | `-23.24` | `73.45%` | Reverts 18,112 differential doc matrix to 23.35% reconciliation, triggers A/B polysemy collisions, and forces 11,565-col wide schema |
| **Abl-2** | Without Layer 2 (C2) Inter-Tabular LPG (793 Edges, 13 Recipes) & Markov Blanket dM | `66.67%` | `88.24%` | `13.10%` | **`56.00%`** | `-40.91` | `58.15%` | Orphans 38/50 multi-hop lifecycle queries (24.0% completion), zeroes 89,096 ESTADO_4 pairs, and exposes all 16,232 nodes (0% isolation) |
| **Abl-3** | Without Pentalingual SKOS Lexicon (2,892 Terms) & __occN Hydraulic Disambiguation | `99.95%` | `17.02%` | `63.12%` | **`60.03%`** | `-36.89` | `59.87%` | Collapses conditional Shannon entropy back to H(C|T) = 2.8878 bits, reintroduces 8 SKOS-annotated __occN homographs (within 134 A50_045 colliding stems), and breaks multilingual lookup |
| **Abl-4** | Without W3C SHACL Closed-World Shapes (104 sh:NodeShape, OWA -> CWA Transition) | `100.00%` | `72.73%` | `95.29%` | **`89.34%`** | `-7.58` | `89.04%` | Silently accepts 120/240 out-of-spec AT4/INVIAS telemetry records (IRI > 3.5 m/km, retroreflectivity < 150) under Open-World Assumption |
| **Abl-5** | Without Layer 3 Physical Geometry-vs-Operation SoA & UUIDv7 Unboxed EAV | `100.00%` | `95.47%` | `18.00%` | **`71.16%`** | `-25.76` | `73.81%` | Forces 455.88 MB WKB geometry scans on non-spatial queries (83.00 ms vs. 3.73 ms) and 99.90% NULL wide AoS CoW rewrites (11.49 s) |
| **Abl-6** | Without 9 Shift-Left GeoBIM Authoring Kits (Post-Hoc Cold CDE Scraping Only) | `97.97%` | `89.12%` | `87.66%` | **`91.58%`** | `-5.33` | `91.78%` | Leaves 49/603 raw proprietary/unstructured CDE receipts unanchored (91.87% raw rate) and requires post-hoc ETL scraping on 105 partial files |

---

## F.5 Disjoint Triple Identity Contract, Zero-Geometry Hot Ontology Evolution (`PF1`), and Closed-World Neologism Governance (`PF5`, `Table F.4`)

### Table F.4: Disjoint Triple Identity Contract, Zero-Geometry Hot Ontology Evolution (PF1), and Closed-World Neologism Governance (PF5)

| Identity / Governance Audit Dimension | Architectural Layer & Identifier Standard | Audited Cardinality | Pairwise Set Intersection / Collision Count | Live Timing & Physical Immutability Proof |
| :--- | :--- | :---: | :---: | :--- |
| **Intensional Concept Identity** | `C1` `codigo_siti` + `uri_owl` (`OWL 2 DL` / `SKOS`) | `16,230` active classes (`16,232` SKOS concepts) | `0` duplicate URIs (`134` colliding `A50_045` raw stems / `179` secondary classes disambiguated via `__occN`) | Verified across `10` Colombian CSVs and `438,194` RDF triples |
| **Topological Class & Kit Identity** | `C2` `uuid_clase_lpg` (`UUIDv5` LPG) vs. `kit_uuid_v5` (`UUIDv5` GeoBIM Kits) | `16,232` C2 nodes vs. `16,230` Kit UUIDs | $\lvert U_{C2} \cap U_{\text{kit}} \rvert = 0$ (`0` collisions) | Disjoint RFC 4122/9562 namespaces separate graph topology from authoring templates |
| **Extensional Asset & Bitemporal Event Identity** | `C3` `asset_uuid` (`UUIDv4`/`v5` instance) + `sys_uuid` (`UUIDv7` `Unboxed EAV` + `SHA-256`) | `226,324` distinct asset UUIDs across `226,324` rows + `120` live `UUIDv7` events | $\lvert U_{C2} \cap U_{C3} \rvert = 0$, $\lvert U_{\text{kit}} \cap U_{C3} \rvert = 0$ | `258,906` baseline distinct UUIDs (`258,907` core UUIDs in `PF1` upon adding class `#16,231`) audited with `0` cross-layer collisions |
| **`PF1`: Zero-Geometry Hot Ontology Evolution** | Transactional `C1` + `C2` + `GPKG` compilation in isolated `/tmp` clone | Class `#16,231` (`A40_095_099_099_099`) + Synonym `#2,893` | `0` bytes rewritten in `C3` spatial containers (`455,875,112` B untouched) | Compiled & passed `46` bundle checks in `87.72 s`; `SHA-256` of `455.88 MB` WKB/ENU unchanged |
| **`PF5`: Closed-World SHACL & Neologism Quarantine** | In-memory Closed-World SHACL and SKOS semantic grounding engine (`PF5-A/B/C`) | `3` valid specs + `3` SHACL violations + `2` unseen neologisms | `assigned_false_generic_a50_parent = False` (`0` false `A50` parents) | Executed in `98.85 ms`; unknown terms isolated in `STAGE_QUARANTINE` governance queue |

---

## F.6 End-to-End Query-Time Reconstruction Across Five National Concession Handover Archetypes (`ARCH-01` to `ARCH-05`, `Table F.5`)

### Table F.5: End-to-End Query-Time Reconstruction Across Five National Concession Handover Archetypes (ARCH-01 to ARCH-05)

| Archetype ID & Concession Handover Scope | Canonical `C2` Recipes | Orthogonal `C1` Binding (`Language A` $\perp$ `Language B`) | `C2` Markov Blanket $\lvert\partial\mathcal{M}\rvert$ | Reconstructed `C3` Assets & Operational Tuples | Query-Time $\mathcal{R}_Q$ Mean ± SD (ms) | Non-Spatial I/O Saved (\%) | `ENU` vs. `Float32` Jitter (mm) | Normative `SHACL` / `NICSP 17` Status |
| :--- | :---: | :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| **`ARCH-01`: 4G/5G Road Corridor, Traffic Lane (Calzada=Carril) & ESAL Fatigue** | `REC-A-01 + REC-B-02 + REC-B-04` | `A`: `A10_025_065_015 -> A20_035_005_020 -> A30_035_005_040 -> A40_045_005_030 -> A50_015_005_025` $\perp$ `B`: `B30_010_030_170 | B40_020_035_920 | B50_010_035_005_005_035 (ESAL & IRI)` | `97` (`99.40%` isol.) | 49,478 lane/shoulder/barrier assets + 171,420 OETR ESAL axle rows + 492 national APU items | `0.826 ± 0.076` | **`99.95%`** | `143.55 -> 0.0052` (`25,697×`) | SHACL IRI <= 2.5 m/km & NICSP 17 85/15 escrow verified |
| **`ARCH-02`: Seismic Bridge/Viaduct (CCP-14) & Hydraulic Drainage (__occN)** | `REC-A-02 + REC-A-05 + REC-B-05` | `A`: `A10_025_065_015 -> A20_035_005_020 -> A30_035_005_070 -> A40_085_005_005 -> A50_045_005_035_005` $\perp$ `B`: `B30_010_020_180 | B40_020_035_930 | B50_010_035_010_025` | `68` (`99.58%` isol.) | 1,194 bridges/viaducts + 51,856 drainage assets (179 A50_045 __occN classes) + 22,976 BUP records | `0.731 ± 0.063` | **`99.95%`** | `143.55 -> 0.0052` (`25,697×`) | SHACL structural clearance & NICSP 17 componentized BUP verified |
| **`ARCH-03`: Road Tunnel, Electromechanical Ventilation & Electronic Toll/ITS** | `REC-A-03 + REC-A-06 + REC-B-06` | `A`: `A10_025_065_015 -> A20_035_005_020 -> A30_035_005_075 -> A40_065_005_075 -> A50_035_035_010` $\perp$ `B`: `B30_015_015_040 | B40_025_005_025 | B50_035_055 (IP/REV & WIM)` | `52` (`99.68%` isol.) | 6,552 ITS devices + 16,844 luminaires + 79 Colpass/WIM toll stations | `0.650 ± 0.038` | **`99.95%`** | `143.55 -> 0.0052` (`25,697×`) | SHACL AT4 availability/retroreflectivity & ISO 19650 CDE verified |
| **`ARCH-04`: Narrow-Gauge Railway Corridor (914 mm) & Rolling Stock (IfcVehicle)** | `REC-A-04 + REC-A-07` | `A`: `A10_025_065_015 -> A20_040_070_010 -> A30_015_075 -> A40_140_010 -> A50_050_060_010` $\perp$ `B`: `B30_015_020 (IfcVehicle) | B40_025_005_015 | B50_010_015_015_005` | `17` (`99.90%` isol.) | 4 ANI rail corridors (1,502.7 km main / 1,634.9 km network, 914 mm gauge) + 7 audited rolling-stock units | `0.476 ± 0.038` | **`99.95%`** | `143.55 -> 0.0052` (`25,697×`) | SHACL allValuesFrom modal gauge (914 mm) & rolling-stock decoupled |
| **`ARCH-05`: Concessioned Airport Terminal, Airside Pavement & Land Release** | `REC-A-07 + REC-B-01 + REC-B-03` | `A`: `A10_005_005 -> A20_020_005 -> A30_015_075 -> A40_090_005 -> A50_050_060_010` $\perp$ `B`: `B20_025_005_00024 (ANI) | B40_010_020_015 | B50_025_005 (Prioritized regional zones)` | `6` (`99.96%` isol.) | 2 airport concessions (within 50 ANI master projects) + 1,425 AT7 cadastral parcels | `0.556 ± 0.058` | **`99.95%`** | `143.55 -> 0.0052` (`25,697×`) | SHACL policy/attribute access-control geofence & AT7 cadastral reversibility verified |

---

## F.7 Point-by-Point Empirical Rebuttal of First-Submission Limitations (`Table F.6`)

### Table F.6: Point-by-Point Methodological and Empirical Resolution of Baseline Architectural Limitations

| ID | First-Submission Critique (*ITcon* Editorial & Peer Review) | Baseline Limitation in `Stage S0 (initial baseline)` | Architectural & Empirical Resolution in `Stage S4` | Verified Quantitative Evidence & Exact Locator |
| :---: | :--- | :--- | :--- | :--- |
| **`REB-01`** | Contradiction between Table 2 (48.20% coverage) and Table 5 SII values; undefined denominators | Conflated single-subset taxonomic asset linkage (23,024/47,768 pilot road rows, 24,744 orphans) with global SII without specifying denominators | Formalized exact denominators across all 3 layers (N=226,324 assets, N=18,112 doc units, N=793 C2 edges, N=603 CDE receipts) and 5 CAS stages | SII V1 rises from 17.99% (S0) to 96.92% (S4); Table 1, Table 2 & Appendix B/F |
| **`REB-02`** | Arbitrary or unvalidated weighting of SII components (w1, w2, w3) | Reported a single static weight combination without simplex sensitivity or rank-stability analysis | Evaluated B=10,000 Dirichlet(1,1,1) Monte Carlo draws plus 5,151 lattice points and exact boundary vertices across V1–V4 | P(S4 > S3 > S2 > S1 > S0) = 100.00% (10,000/10,000 draws, p < 1e-15); Table 6 & Appendix F.3 |
| **`REB-03`** | Implausible or heavy-iron hardware claim ('4.35 GB loaded in 1 TB RAM server') in coupled monolithic geometry-and-telemetry architectures | Described an unoptimized monolithic memory footprint instead of proving physical geometry-vs-operation decoupling | Implemented physical WKB-vs-SoA mass audit, late spatial materialization, UUIDv7 Unboxed EAV, and bimodal ENU precision | 24.67× disk ratio (455.88 vs 18.48 MB), 99.95% I/O saved (<50 MB RAM), 25,697× jitter gain; Table 5 & Appendix E |
| **`REB-04`** | Lack of formal axiomatization, Protégé OWL 2 DL verification, and Open-World vulnerability | Exported flat taxonomic hierarchies without existential restrictions, disjointness axioms, or Closed-World SHACL gates | Axiomatized 438,194 isomorphic TTL/OWL triples (157 ObjectProperties, 814 owl:Restriction, A disjoint B) + 104 W3C SHACL shapes | 0 unsatisfiable classes, 0 cycles, and F1 = 100.0% across 240 live bipolar SHACL CWA test cases; Table 3 & Appendix C |
| **`REB-05`** | Insufficient statistical rigor (descriptive percentages without paired hypothesis tests or effect sizes) | Omitted non-parametric paired tests, confidence intervals, and concession-level longitudinal panels | Conducted Wilcoxon signed-rank tests, B=10,000 BCa bootstrap CIs, Cohen's d, and Hedges' g on Panel A (N=47) and Panel B (N=50) | Panel A47 Delta SII = +77.11 pp (Z = 5.968, p = 1.42e-14, g = 54.64); Table 3, Table 6 & Appendix C/F |
| **`REB-06`** | Unquantified runtime overhead of post-coordinating decoupled classes at query time | Assumed runtime joins were fast without benchmarking against monolithic RDF/SPARQL or coupled Row-SQL AoS | Benchmarked 50 multi-hop lifecycle queries (k=1..6 hops across all 13 recipes) across 6 execution paradigms (M1, M1b, M2, M2b, M2c, M3) | 21.21× speedup vs. M1 (0.705 vs. 14.957 ms, Phi_eff = 95.29%), 11.75× vs. M2, 7.83× vs. same-engine DuckDB M2b, and 3.22× (27.75× graph) vs. M1b with 99.92% Markov isolation; Table 4 & Appendix D |
| **`REB-07`** | Polysemy and multilingual terminology collisions across engineering disciplines | Lacked a versioned multilingual lexicon and suffered 134 colliding raw code stems (179 secondary occurrences) in A50_045 | Deployed 2,892 reviewed SKOS expressions (5 languages) and __occN occurrence disambiguation across 179 A50_045 water classes | Shannon H(C|T) collapses from 2.8878 to 0.1578 bits (Phi_sem = 95.47%), preserving irreducible polymorphism; Table 3 & Appendix C |
| **`REB-08`** | Road-centric bias without proof of intermodal extensibility (railways, rolling stock, airports) | Evaluated only road inventory subsets without narrow-gauge rail corridors, rolling stock, or airport concessions | Integrated 4 ANI rail corridors (1,502.7 km main / 1,634.9 km network, 914 mm gauge), IfcVehicle rolling stock (B30_015_020), AASHTO TAM (B50_030), and airports | Verified live across ARCH-01..ARCH-05 with 0 orphan codes across 2,510,964 core C3 rows; Table 7 & Appendix F.6 |
| **`REB-09`** | Vulnerability to legacy unstructured CDE files and ad-hoc taxonomy pollution by unseen neologisms | Relied on post-hoc scraping without authoring templates or formal quarantine for unrecognized terms | Delivered 9 Shift-Left BIM/GIS kits (849 ISO 16739-1:2024 Psets/Qtos), V3 Raw-603 transparency (97.97%), and PF5 quarantine | PF5 quarantined 2 neologisms with 0 false generic A50 parents in 98.85 ms; Table 4, Table 7 & Appendix D/F |
| **`REB-10`** | Risk of breaking historical BIM/GIS geometries when updating national classification codes | Did not prove that C1/C2 ontological evolution leaves C3 spatial geometry files untouched | Enforced disjoint UUID namespaces (URI != C2 UUIDv5 != Kit UUIDv5 != C3 UUIDv4/v7) and proved hot compilation in /tmp (PF1) | PF1 compiled class #16,231 + SKOS #2,893 in 87.72 s with 0 bytes rewritten across 455.88 MB WKB; Table 7 & Appendix F.5 |

---
