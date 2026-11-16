# Supplementary Appendix B: Orthogonal Language Factorization ($\text{Language A} \perp \text{Language B}$), Combinatorial Compression ($112.35\times$), and Multi-Domain Evaluation of Ontological Binding Integrity ($\Phi_{\text{ont}}$)

**Manuscript Title:** *Orthogonal Ontology Factorization for Semantic Interoperability in Transport Infrastructure* (`ORTHOGONAL ONTOLOGY FACTORIZATION FOR SEMANTIC INTEROPERABILITY IN TRANSPORT INFRASTRUCTURE`)  
**Authors:** Juan C. Gómez (Corresponding Author; PhD candidate, Doctoral program in Technology Innovation Management, Universidad de los Andes, and National Infrastructure Agency (ANI), Bogotá, Colombia, `jc.gomez1988@uniandes.edu.co`), Rodrigo F. Herrera (Associate professor, School of Civil Engineering, Pontificia Universidad Católica de Valparaíso, Valparaíso, Chile, `rodrigo.herrera@pucv.cl`), Karen M. Castañeda (Assistant professor, School of Civil Engineering, Pontificia Universidad Católica de Valparaíso, Valparaíso, Chile, `karen.castaneda@pucv.cl`), and Juan F. Correal (Full professor, Department of Civil and Environmental Engineering, Universidad de los Andes, Bogotá, Colombia, `jcorreal@uniandes.edu.co`)  
**Reference:** Gómez, J. C., Herrera, R. F., Castañeda, K. M., & Correal, J. F. (2027). Orthogonal ontology factorization for semantic interoperability in transport infrastructure. *Journal of Information Technology in Construction (ITcon)*, 32, 1-X. https://doi.org/10.36680/j.itcon.2027.[added by editor]  
**Journal Target:** *Journal of Information Technology in Construction (ITcon)* — Special / Regular Issue on Semantic Interoperability and Digital Twins in Civil Infrastructure  
**Active Semantic Release Audited (CAS Stage 4 / Gate 3):** `b6bd01f850790ad22d399b95545f73d2` (`Stage S3/S4 (CAS b6bd01f850790ad22d399b95545f73d2)`, `manifest_sha256: bda830878ebd24c1f6a190a0431b86a3602a4f246f9c71616bdab3ac0d6bf2d0`)  
**Reproducibility Protocol:** Read-only forensic audit (`os.O_RDONLY`) over `16,230` active unique ontology classes in Layer 1 (`C1`), `793` deduplicated intertabular edges and `13` assembly recipes in Layer 2 (`C2`), and `2,510,964` analytical records across `726` Apache Parquet tables in Layer 3 (`C3`).

---

## B.1. Formal Mathematical Distinction Between $\Phi_{\text{ont}}$ and the Global Composite Index ($\text{SII}$)

To prevent conflation between taxonomic coverage and full semantic interoperability across the project lifecycle, the **Semantic Interoperability Index ($\text{SII}$)** is formulated as a weighted three-dimensional convex combination:

$$\text{SII} = w_1 \, \Phi_{\text{ont}} + w_2 \, \Phi_{\text{sem}} + w_3 \, \Phi_{\text{eff}}, \quad \text{subject to } \sum_{k=1}^{3} w_k = 1, \; w_k > 0$$

where:
1. **$\Phi_{\text{ont}} \in [0, 100\%]$ (Ontological & Relational Binding Integrity — evaluated in this Appendix B):** Measures the structural absence of orphan class codes in `C3`, the lossless relational decomposability of composite engineering records via `C2`, and the cold-start structural grounding of heterogeneous deliverables.
2. **$\Phi_{\text{sem}} \in [0, 100\%]$ (Axiomatic, Lexical & Constraint Preservation Integrity — evaluated in Appendix C / Wave 3):** Measures OWL 2 DL reasoning consistency ($814$ existential restrictions, $157$ object properties), SKOS lexical coverage ($2,892$ expressions across $814$ classes), and SHACL closed-world conformance ($104$ `sh:NodeShape` constraints).
3. **$\Phi_{\text{eff}} \in [0, 100\%]$ (Computational, Geodesic & Cross-Tool Exchange Efficiency — evaluated in Appendix D / Wave 4):** Measures query-time graph traversal latency, bimodal 64-bit EPSG:9377 anchor + 32-bit local ENU offset spatial precision, and native round-trip fidelity across BIM/GIS authoring kits (`Kits_BIM` and `Kits_GIS`).

Within Dimension 1 ($\Phi_{\text{ont}}$), we define three rigorous, non-overlapping sub-metrics:

$$\Phi_{\text{ont}}^{\text{(Taxonomic-Asset)}} = \frac{1}{|R_{\text{inv}}|} \sum_{r \in R_{\text{inv}}} \mathbb{I}\!\left(\text{code}(r) \in \mathcal{C}_1^{\text{active}}\right) \times 100\%$$

$$\Phi_{\text{ont}}^{\text{(Relational-AB)}} = \left\{\Phi_{\text{ont}}^{\text{(Doc-Matrix-18112)}} = \frac{|U_{\text{reconciled}}|}{|U_{\text{total}}|}, \quad \Phi_{\text{ont}}^{\text{(Relational-C2-793)}} = \frac{|P_{\text{ESTADO\_4}}^{\text{reconstructed}}| + |R_{\text{APU}}^{\text{reconstructed}}|}{|P_{\text{ESTADO\_4}}^{\text{total}}| + |R_{\text{APU}}^{\text{total}}|}\right\} \times 100\%$$

$$\Phi_{\text{ont}}^{\text{(Cold-Ingestion)}} = \left\{\Phi_{\text{ont}}^{\text{(Cold-Open-554)}} = \frac{|D_{\text{complete}}| + |D_{\text{partial}}|}{|D_{\text{open}}|}, \quad \Phi_{\text{ont}}^{\text{(Cold-Raw-603)}} = \frac{|D_{\text{complete}}| + |D_{\text{partial}}|}{|D_{\text{raw}}|}\right\} \times 100\%$$

---

## B.2. Theorem of Orthogonal Factorization ($\text{Language A} \perp \text{Language B}$) and Combinatorial Compression ($112.35\times$)

**Theorem B.1 (Orthogonal Decoupling vs. Monolithic Pre-Coordination):**  
Let $\mathcal{A} = \bigsqcup_{i=1}^{5} A_{10i}$ denote the vocabulary of **Language A** (physical, spatial, and functional infrastructure entities, with $|\mathcal{A}| = 4,686$ active unique classes: $|A10|=1,278$, $|A20|=351$, $|A30|=361$, $|A40|=913$, $|A50|=1,783$), and let $\mathcal{B} = \bigsqcup_{j=1}^{5} B_{10j}$ denote the vocabulary of **Language B** (documentary, institutional, material/resource, lifecycle activity, and governance/cost facets, with $|\mathcal{B}| = 11,544$ active unique classes: $|B10|=635$, $|B20|=5,253$, $|B30|=870$, $|B40|=4,048$, $|B50|=738$), such that $\mathcal{A} \cap \mathcal{B} = \emptyset$.

1. **Bipartite Pre-Coordination Explosion:** Any monolithic classification scheme that pre-coordinates physical assets with operational/material attributes requires a worst-case Cartesian state space of:
   $$|\Omega_{\text{mono}}^{(2)}| = |\mathcal{A}| \times |\mathcal{B}| = 4,686 \times 11,544 = 54,095,184 \text{ classes}$$
   whereas the orthogonal factorization $\text{Language A} \perp \text{Language B}$ requires only $|\mathcal{A}| + |\mathcal{B}| = 16,230$ classes in `C1` plus $|E_{C2}| = 793$ reusable intertabular edges in `C2` ($17,023$ total constructs), achieving a **$3,333.04\times$** taxonomic reduction in `C1` (**$3,177.77\times$** including `C2`).

2. **Tetradimensional 5D Cost-Item (`APU`) Explosion:** Pre-coordinating 5D unit-price items across physical asset ($A$), construction activity ($B40$), material/equipment ($B30$), and cost/specification parameter ($B50$) yields:
   $$|\Omega_{\text{mono}}^{(4)}| = |\mathcal{A}| \times |B40| \times |B30| \times |B50| = 4,686 \times 4,048 \times 870 \times 738 = 12,179,189,911,680 \approx 1.2179 \times 10^{13}$$
   compared to the additive subset $|\mathcal{A}| + |B40| + |B30| + |B50| = 10,342$ classes ($17,023$ total in `C1 + C2`), representing a **$7.1546 \times 10^{8}\times$** state-space reduction (and **$2.3865 \times 10^{15}\times$** over the full 6-tuple space $|\mathcal{A}| \times \prod_{j=1}^{5} |B_{10j}| = 4.0626 \times 10^{19}$).

3. **Empirical Documentary Rupture ($73.06\%$) and Layer 2 Compression ($112.35\times$):** Across the $N = 18,112$ documentary units audited in `siti_matriz_confrontacion_diferencial_ab.parquet` (`1,754` source files across `10` institutional libraries), a rigid 1-to-1 monolithic classifier captures only `ESTADO_1` (`4,230` units = `23.35%`) or `ESTADO_1 + ESTADO_2` (`4,880` units = `26.94%`), suffering a **`73.06%` (`13,232` units) semantic rupture** at handover. Specifically, `11,137` units (`61.49%`, `ESTADO_4`) are multi-table composite propositions that induce $11,137 \times 8 = \mathbf{89,096}$ implicit directed intertabular pairs (`89,480` total evidence occurrences), which compress losslessly onto the **`793` deduplicated edges of `C2`** (`98` `A->A`, `282` `A<->B`, `413` `Bx<->By`, with `0` intra-tabular meronymy violations):
   $$\mathcal{K}_{C2} = \frac{89,096}{793} = \mathbf{112.3531\times} \approx \mathbf{112.35\times}$$

---

## B.3. Table B.1: Differential Confrontation Matrix ($N = 18,112$) Across 10 Primary Libraries and 5 Reconciliation States

### Table B.1: Differential Confrontation Matrix ($N = 18,112$) Across 10 Institutional Libraries and 5 Reconciliation States

| Source Library / Repository | Source Files | Total Units ($N$) | `ESTADO_1` (Exact 1:1) | `ESTADO_2` (SKOS Lexical) | `ESTADO_3` (Param./Topol.) | `ESTADO_4` (Composite $A \perp B$) | `ESTADO_5` (New C1 Class) | Monolithic 1:1 Capture (`E1`) | Monolithic + SKOS (`E1+E2`) | Monolithic Rupture (`E3..E5`) | Implicit `ESTADO_4` Pairs ($8 \times E_4$) | SITI `C1+C2` Reconciliation |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `historico_y_desarrollo` | 1,565 | 7,293 | 1,114 | 0 | 1,287 | 4,892 | 0 | 15.27% | 15.27% | 84.73% (6,179) | 39,136 | **100.00%** |
| `docs` | 65 | 4,628 | 132 | 7 | 246 | 4,235 | 8 | 2.85% | 3.00% | 97.00% (4,489) | 33,880 | **100.00%** |
| `Biblioteca_tecnica_INVIAS` | 12 | 2,275 | 533 | 399 | 206 | 1,031 | 106 | 23.43% | 40.97% | 59.03% (1,343) | 8,248 | **100.00%** |
| `Documentos concesion` | 34 | 2,150 | 1,519 | 108 | 11 | 434 | 78 | 70.65% | 75.67% | 24.33% (523) | 3,472 | **100.00%** |
| `Biblioteca_tecnica_ANI` | 33 | 723 | 487 | 29 | 40 | 145 | 22 | 67.36% | 71.37% | 28.63% (207) | 1,160 | **100.00%** |
| `Biblioteca_ontologias_transporte` | 25 | 562 | 117 | 55 | 41 | 342 | 7 | 20.82% | 30.60% | 69.40% (390) | 2,736 | **100.00%** |
| `Power BI - planeacion ANI` | 6 | 382 | 321 | 0 | 22 | 39 | 0 | 84.03% | 84.03% | 15.97% (61) | 312 | **100.00%** |
| `otros documentos` | 4 | 42 | 0 | 30 | 0 | 4 | 8 | 0.00% | 71.43% | 28.57% (12) | 32 | **100.00%** |
| `siti_production_corpus` | 5 | 29 | 2 | 18 | 1 | 0 | 8 | 6.90% | 68.97% | 31.03% (9) | 0 | **100.00%** |
| `Biblioteca_tecnica_PMI` | 5 | 28 | 5 | 4 | 1 | 15 | 3 | 17.86% | 32.14% | 67.86% (19) | 120 | **100.00%** |
| **Total Audited Corpus (`10` Libraries)** | **1,754** | **18,112** | **4,230 (23.35%)** | **650 (3.59%)** | **1,855 (10.24%)** | **11,137 (61.49%)** | **240 (1.33%)** | **23.35%** | **26.94%** | **73.06% (13,232)** | **89,096** | **100.00% (18,112)** |

---

## B.4. Table B.2: Tetradimensional 5D Unit-Price (`APU`) Decoupling ($526$ National Items $\times 140$ Regional Books $= 73,640$ Rows)

### Table B.2: Tetradimensional 5D Unit-Price (`APU`) Decoupling ($526$ National Items $\times 140$ Regional Books $= 73,640$ Regional Compositions)

| Facet Dimension & SITI Code / Chapter | Canonical Description (English / Spanish Reference) | Subchapters | National Items | Regional Rows ($\times 140$) | Share (`%`) | Min Regional Price (`COP`) | Mean of Regional Means (`COP`) | Max Regional Price (`COP`) | $\Phi_{\text{ont}}^{\text{(APU)}}$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Panel A. By INVIAS Construction Chapter (`8` Groups, `110` Subchapters)** | **Total National 5D Catalog (`REC-B-02`)** | **110** | **526** | **73,640** | **100.00%** | **0.00** | **948,413.04** | **97,399,077.83** | **100.00%** |
| `Cap. 600` | Structures, bridges, structural steels/concretes & drainage (*Cap. 600 — Estructuras, puentes, aceros, concretos estructurales y drenaje*) | 31 | 157 | 21,980 | 29.85% | 0.00 | 1,466,584.82 | 26,202,912.17 | 100.00% |
| `Cap. 400` | Asphalt pavements, tack/prime coats, mixes & hydraulic concrete (*Cap. 400 — Pavimentos asfálticos, riegos, mezclas y concreto hidráulico*) | 25 | 103 | 14,420 | 19.58% | 1,835.94 | 223,354.11 | 3,405,948.94 | 100.00% |
| `Cap. 200` | Earthworks, excavations, embankments & rockfills (*Cap. 200 — Explanaciones, excavaciones, terraplenes y pedraplenes*) | 16 | 94 | 13,160 | 17.87% | 305.73 | 459,800.30 | 12,503,392.58 | 100.00% |
| `Cap. 800` | Environmental works, sodding, tree planting & bioengineering (*Cap. 800 — Obras ambientales, empradización, arborización y bioingeniería*) | 9 | 62 | 8,680 | 11.79% | 1,191.26 | 1,272,319.48 | 97,399,077.83 | 100.00% |
| `Cap. 300` | Subgrades, granular subbases/bases & stabilized layers (*Cap. 300 — Afirmados, subbases y bases granulares y estabilizadas*) | 10 | 56 | 7,840 | 10.65% | 582.46 | 110,374.45 | 907,298.37 | 100.00% |
| `Cap. 700` | Road signage, metal guardrails, lighting & ITS (*Cap. 700 — Señalización vial, defensas metálicas, iluminación e ITS*) | 14 | 40 | 5,600 | 7.60% | 1,869.58 | 2,845,374.41 | 45,706,588.58 | 100.00% |
| `Cap. 500` | Portland cement concrete pavements & joints (*Cap. 500 — Pavimentos de concreto hidráulico y juntas*) | 4 | 8 | 1,120 | 1.52% | 548.64 | 437,145.43 | 1,841,014.12 | 100.00% |
| `Cap. 900` | Material hauling, overhaul transport & miscellaneous (*Cap. 900 — Transporte de materiales, acarreos y varios*) | 1 | 6 | 840 | 1.14% | 708.32 | 1,303.58 | 5,644.95 | 100.00% |
| **Panel B. By Intervened Physical Asset Class (`Language A`, `9` Active Classes)** | **Zero Material Contamination in `A10–A50`** | **---** | **526** | **73,640** | **100.00%** | **0.00** | **948,413.04** | **97,399,077.83** | **100.00%** |
| `A30_035_005_040` | Calzada o carril vehicular | --- | 356 | 49,840 | 67.68% | 0.00 | 1,196,466.78 | 97,399,077.83 | 100.00% |
| `A40_045_005_030` | Sistema de pavimento o calzada flexible | --- | 105 | 14,700 | 19.96% | 1,835.94 | 162,744.91 | 3,405,948.94 | 100.00% |
| `A50_015_005_025` | Segregador físico y confinamiento de ciclorruta y carril exclusivo no motorizado | --- | 33 | 4,620 | 6.27% | 1,869.58 | 1,039,399.88 | 15,220,950.90 | 100.00% |
| `A40_055_005` | Sistemas de pesaje según la modalidad de operación | --- | 17 | 2,380 | 3.23% | 16,792.21 | 267,743.96 | 2,906,650.81 | 100.00% |
| `A40_085_005_010` | Subestructura | --- | 10 | 1,400 | 1.90% | 46,932.71 | 1,416,869.02 | 4,349,128.93 | 100.00% |
| `A40_085_005_005` | Superestructura | --- | 2 | 280 | 0.38% | 50,060.82 | 833,848.36 | 1,593,743.87 | 100.00% |
| `A40_140_010` | Circuito de vía de audiofrecuencia sin juntas | --- | 1 | 140 | 0.19% | 8,670.31 | 9,980.13 | 14,175.33 | 100.00% |
| `A40_045_005_035` | Sistema de pavimento o calzada fotocatalítico | --- | 1 | 140 | 0.19% | 67,909.83 | 107,704.59 | 195,547.33 | 100.00% |
| `A50_040_045_055` | Dispositivo de apoyo sísmico y aislador de superestructura de puente | --- | 1 | 140 | 0.19% | 819,197.84 | 1,028,951.97 | 1,059,699.40 | 100.00% |
| **Panel C1. By Construction Activity Class (`Table B40`, `11` Active Classes)** | **Lifecycle Work Activity Facet** | **---** | **526** | **73,640** | **100.00%** | **0.00** | **948,413.04** | **97,399,077.83** | **100.00%** |
| `B40_020_035_930` | Actividades de estructuras de concreto, acero, cimentaciones profundas y puentes (Capítulo 600 INVIAS) | --- | 118 | 16,520 | 22.43% | 0.00 | 1,354,917.23 | 26,202,912.17 | 100.00% |
| `B40_020_035_920` | Actividades de riegos bituminosos y capas de pavimentos asfálticos (Capítulo 400 INVIAS) | --- | 103 | 14,420 | 19.58% | 1,835.94 | 223,354.11 | 3,405,948.94 | 100.00% |
| `B40_020_035_910` | Actividades de explanación, excavación de cortes y conformación de terraplenes (Capítulo 200 INVIAS) | --- | 73 | 10,220 | 13.88% | 582.14 | 301,314.65 | 3,850,758.77 | 100.00% |
| `B40_020_035_945` | Actividades de obras complementarias, bioingeniería, geotecnia y transporte de materiales (Capítulos 800 y 900 INVIAS) | --- | 68 | 9,520 | 12.93% | 708.32 | 1,160,171.02 | 97,399,077.83 | 100.00% |
| `B40_020_035_915` | Actividades de afirmados, subbases y bases granulares y estabilizadas (Capítulo 300 INVIAS) | --- | 56 | 7,840 | 10.65% | 582.46 | 110,374.45 | 907,298.37 | 100.00% |
| `B40_020_035_935` | Actividades de obras de drenaje vial, subdrenaje, alcantarillas y contención (Capítulo 600 INVIAS) | --- | 39 | 5,460 | 7.41% | 5,719.80 | 1,804,450.86 | 20,324,246.51 | 100.00% |
| `B40_020_035_940` | Actividades de señalización vial, demarcación horizontal, defensas e iluminación (Capítulo 700 INVIAS) | --- | 38 | 5,320 | 7.22% | 1,869.58 | 2,956,455.88 | 45,706,588.58 | 100.00% |
| `B40_020_035_905` | Actividades preliminares, desmonte, limpieza y demoliciones en carreteras (Capítulo 200 INVIAS) | --- | 21 | 2,940 | 3.99% | 305.73 | 1,010,726.62 | 12,503,392.58 | 100.00% |
| `B40_020_035_925` | Actividades de pavimentos de concreto hidráulico y elementos prefabricados (Capítulo 500 INVIAS) | --- | 8 | 1,120 | 1.52% | 548.64 | 437,145.43 | 1,841,014.12 | 100.00% |
| `B40_020_035_730_4` | Poda de la parte aérea de árboles tipo I | --- | 1 | 140 | 0.19% | 533,797.96 | 533,990.35 | 534,984.18 | 100.00% |
| `B40_020_035_731_1` | Poda de la parte aérea de árboles tipo II | --- | 1 | 140 | 0.19% | 925,880.63 | 935,662.82 | 956,971.87 | 100.00% |
| **Panel C2. By Resource / Material Class (`Table B30`, `10` Active Classes)** | **Decoupled Material & Input Facet** | **---** | **526** | **73,640** | **100.00%** | **0.00** | **948,413.04** | **97,399,077.83** | **100.00%** |
| `B30_010_005_175` | Agregado pétreo seleccionado y triturado para afirmado, subbase y base granular (Clases A, B y C) | --- | 315 | 44,100 | 59.89% | 0.00 | 1,124,457.53 | 97,399,077.83 | 100.00% |
| `B30_010_020_180` | Concreto hidráulico estructural por clase de resistencia a compresión (Clases A a G — Artículo 630 INVIAS) | --- | 87 | 12,180 | 16.54% | 548.64 | 791,900.64 | 26,202,912.17 | 100.00% |
| `B30_010_030_175` | Emulsión asfáltica catiónica convencional y modificada con polímeros (Artículos 411 y 415 INVIAS) | --- | 38 | 5,320 | 7.22% | 1,835.94 | 15,473.41 | 873,455.72 | 100.00% |
| `B30_010_030_170` | Cemento asfáltico modificado con polímeros elastoméricos SBS o grano de caucho reciclado (GCR) | --- | 28 | 3,920 | 5.32% | 83,059.36 | 390,172.15 | 2,106,855.84 | 100.00% |
| `B30_010_040_180` | Torón de acero de baja relajación de siete alambres para preesfuerzo y tirantes | --- | 22 | 3,080 | 4.18% | 1,324.50 | 2,813,701.38 | 20,324,246.51 | 100.00% |
| `B30_010_025_150` | Geotextil tejido y no tejido para separación, filtración y estabilización de subrasantes (Artículo 231 INVIAS) | --- | 19 | 2,660 | 3.61% | 5,018.59 | 28,241.06 | 147,563.36 | 100.00% |
| `B30_010_050_155` | Recubrimiento termoplástico y plástico en frío con microesferas retrorreflectivas | --- | 7 | 980 | 1.33% | 1,044.86 | 22,875.14 | 170,298.06 | 100.00% |
| `B30_010_025_155` | Geocompuesto planar de subdrenaje con núcleo polimérico tridimensional y filtro geotextil (Artículo 673 INVIAS) | --- | 6 | 840 | 1.14% | 5,719.80 | 73,539.62 | 630,499.23 | 100.00% |
| `B30_010_065_160` | Compuesto elastomérico de policloropreno (neopreno) vulcanizado con láminas de acero para apoyos y sellos | --- | 3 | 420 | 0.57% | 53,043.09 | 401,205.40 | 1,059,699.40 | 100.00% |
| `B30_010_040_175` | Acero perlítico de alta dureza tratado térmicamente en cabeza para rieles y desvíos | --- | 1 | 140 | 0.19% | 8,670.31 | 9,980.13 | 14,175.33 | 100.00% |

---

## B.5. Table B.3: Multi-Domain Audit of Ontological Binding Integrity ($\Phi_{\text{ont}}$) Across the $2,510,964$ Records of Layer 3 (`C3`), Including the 21 ANI Functional Layers, 17 IFC 4.3 Classes, and 50 Concessions

### Table B.3A: Exhaustive Per-Layer Taxonomic Binding Audit Across 21 ANI Functional Layers and 17 IFC 4.3 Entities ($N = 226,324$ National Assets)

| # | ANI Functional Layer (`tabla_origen_ani`) | Modal SITI Table | Primary SITI Code & Class Name (`Language A`) | ISO 16739-1:2024 (`IFC 4.3`) Entity | Modal `PredefinedType` | Evaluated Assets | Linked to `C1` | Orphans | Concessions | Share (`%`) | $\Phi_{\text{ont}}^{\text{(Taxonomic)}}$ |
| :---: | :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `senal_vertical` | `A50` | `A50_015_010_020` — Vertical traffic signs | `IfcSign` | `TRAFFIC_SIGN` | 87,639 | 87,639 | 0 | 24 | 38.7228% | **100.00%** |
| 2 | `cuneta` | `A50` | `A50_045_005_015` — Surface drainage gutters & ditches | `IfcDitch` | `GUTTER` | 33,801 | 33,801 | 0 | 23 | 14.9348% | **100.00%** |
| 3 | `berma` | `A50` | `A50_015_005_015` — Road shoulders & widenings | `IfcKerb` | `SHOULDER` | 22,420 | 22,420 | 0 | 41 | 9.9062% | **100.00%** |
| 4 | `drenajes` | `A40` | `A40_090_015_030` — Cross-drainage culverts & box culverts | `IfcPipeSegment` | `CULVERT` | 18,055 | 18,055 | 0 | 20 | 7.9775% | **100.00%** |
| 5 | `luminarias` | `A50` | `A50_030_015_040` — Roadway luminaires (`16,843`) + `A40_050` airfield (`1`) | `IfcLightFixture` | `STREETLIGHT` | 16,844 | 16,844 | 0 | 23 | 7.4424% | **100.00%** |
| 6 | `defensa_vial` | `A50` | `A50_015_005_010` — Vehicular crash barriers & guardrails | `IfcImpactProtectionDevice` | `CRASHBARRIER` | 16,348 | 16,348 | 0 | 22 | 7.2233% | **100.00%** |
| 7 | `calzada` | `A50` | `A50_015_005_005` — Roadway pavement courses (`10,704`) + `A50_015_010` (`6`) | `IfcCourse` | `ROADWAY` | 10,710 | 10,710 | 0 | 43 | 4.7322% | **100.00%** |
| 8 | `dispositivo_its` | `A40` | `A40_060_010` — Intelligent Transport Systems (ITS) & telemetry | `IfcSensor` | `TELEMETRY` | 6,552 | 6,552 | 0 | 23 | 2.8950% | **100.00%** |
| 9 | `separador` | `A30` | `A30_035_005_065` — Roadway medians (`6,148`, `IfcRoadPart`) + `A50_015_010` (`1`) | `IfcRoadPart` | `MEDIAN` | 6,149 | 6,149 | 0 | 42 | 2.7169% | **100.00%** |
| 10 | `muro` | `A40` | `A40_090_020` — Earth-retaining wall systems | `IfcRetainingWall` | `RETAININGWALL` | 2,744 | 2,744 | 0 | 19 | 1.2124% | **100.00%** |
| 11 | `talud` | `A40` | `A40_090_010_010` — Slope stabilization & geotechnical cuts | `IfcEarthworksCut` | `SLOPE` | 2,074 | 2,074 | 0 | 3 | 0.9164% | **100.00%** |
| 12 | `predio` | `A10` | `A10_025_040` — Cadastral right-of-way parcels | `IfcSpatialZone` | `LAND_PARCEL` | 1,425 | 1,425 | 0 | 3 | 0.6296% | **100.00%** |
| 13 | `puente` | `A30` | `A30_035_010_045` — Highway bridges, overpasses & viaducts | `IfcBridge` | `BRIDGE` | 1,194 | 1,194 | 0 | 27 | 0.5276% | **100.00%** |
| 14 | `ciclorruta` | `A50` | `A50_015_005_025` — Dedicated cycleways & non-motorized lanes | `IfcCourse` | `CYCLEWAY` | 98 | 98 | 0 | 7 | 0.0433% | **100.00%** |
| 15 | `estacion_peaje` | `A30` | `A30_035_010_015` — Toll collection plazas | `IfcFacility` | `TOLL_PLAZA` | 79 | 79 | 0 | 23 | 0.0349% | **100.00%** |
| 16 | `estacion_pesaje` | `A30` | `A30_035_010_020` — Truck weighing & load-control stations | `IfcFacility` | `WEIGH_STATION` | 63 | 63 | 0 | 21 | 0.0278% | **100.00%** |
| 17 | `tunel` | `A30` | `A30_035_010_060` — Road tunnels & underground works | `IfcTunnel` | `TUNNEL` | 62 | 62 | 0 | 11 | 0.0274% | **100.00%** |
| 18 | `cco` | `A40` | `A40_025_005` — Operational Control Centers (`27`), `A20_015_060` (`6`, `IfcRailway`), `A20_010` (`1`) | `IfcBuilding` | `OPERATIONS_CENTER` | 34 | 34 | 0 | 22 | 0.0150% | **100.00%** |
| 19 | `zona_servicio` | `A30` | `A30_035_010_025` — Roadside service areas & rest bays | `IfcFacility` | `SERVICE_AREA` | 27 | 27 | 0 | 18 | 0.0119% | **100.00%** |
| 20 | `aeropuerto_terminal` | `A20` | `A20_010` — Air transport passenger/cargo terminal complexes | `IfcBuilding` | `TERMINAL` | 4 | 4 | 0 | 2 | 0.0018% | **100.00%** |
| 21 | `aeropuerto_torre` | `A40` | `A40_010` — Air traffic control tower facilities | `IfcBuilding` | `CONTROL_TOWER` | 2 | 2 | 0 | 2 | 0.0009% | **100.00%** |
| **Total** | **21 Functional Layers** | **`A10..A50`** | **`A10`: 1,425 \| `A20`: 11 \| `A30`: 7,573 \| `A40`: 29,455 \| `A50`: 187,860** | **17 `IFC 4.3` Classes** | **22 Types** | **226,324** | **226,324** | **0** | **47 Part. / 50 Conc.** | **100.0000%** | **100.00%** |

### Table B.3B: Complete Multi-Domain Synthesis Across All $2,510,964$ Analytical Records in Layer 3

| Layer 3 (`C3`) Analytical Domain | Parquet Tables | Evaluated Rows | Linked SITI Codes / UUIDs | Orphan Codes in Prod. | Layer 2 (`C2`) Assembly Recipes & Edges | Domain $\Phi_{\text{ont}}$ |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| **01. ANI National Concession Assets (`47` itemized partitions / `50` master concessions)** | 5 | 226,409 | 226,409 | 0 | `REC-A-01..07`, `REC-B-01..06` | **100.00%** |
| **02. Bimodal Spatial Inventory (`226,342` Geodesic `WKB` + `5,011` Bimodal 64-bit `EPSG:9377` + 32-bit Local `ENU` + Cadastre)** | 3 | 457,687 | 457,684 prod. (+3 mapped legacy) | 0 | `REC-A-01`, `REC-B-03` (`100%` 1:1 UUID match) | **100.00%** |
| **03. Railway & Intermodal Domain (`4` corridors in `914 mm` / `1,573.6 km`, `AT4`, `IfcVehicle`)** | 4 | 32 | 32 (`38` transversal A/B codes) | 0 | `REC-A-04` (`B30_015_020` + `B50_030` AASHTO TAM) | **100.00%** |
| **04. OETR Toll Plazas, Traffic & Revenue (`125` active / `162` historical, `2014–2026`)** | 40 | 377,084 | 377,084 | 0 | `REC-A-06`, `REC-B-04` (`A30_035_010_015`) | **100.00%** |
| **05. Confrontation Matrix (`18,112`), 5D APU (`73,640` regional), & Grounding Ledger (`603`)** | 4 | 92,881 | 92,881 | 0 | `793` C2 edges (`112.35×` compression) + `REC-B-02` | **100.00%** |
| **06. Cold-Start Ingestion Extracted Parquet Tables (`576` extraction + `62` confirmation)** | 638 | 32,983 | 32,983 (`554/554` open; `49` closed) | 0 | `REC-A-01`, `REC-A-02`, `REC-A-04`, `REC-B-04` | **100.00%** (open) / **91.87%** (raw) |
| **07. ANI Strategic Planning PBIX (`15` tables, `15,153` rows) & Municipal Territorial Equity (`1,122` mun.)** | 23 | 50,903 | 50,903 (`170` prioritized, `344` conflict-recovery, `173` border) | 0 | `REC-B-01`, `B50_025_005..015` | **100.00%** |
| **08. National & International Geospatial Harvester (*God's Eye*, `8` layers + consolidated)** | 9 | 1,272,985 | 1,272,985 (`EPSG:4326 <-> 9377 <-> ENU`) | 0 | `REC-A-01..07` | **100.00%** |
| **Total Core Layer 3 (`C3`) Analytical Lakehouse Audited** | **726** | **2,510,964** | **2,510,964** | **0** | **`793` Edges + `13` Canonical Recipes** | **100.00%** |

> **Forensic Note on the 50 Master Concessions (`siti_ani_proyectos.parquet`):** Among the `50` master concessions, `44` match `siti_ani_activos_principales.parquet` directly by `project_id` (`216,197` assets), while `3` legacy partition IDs (`0`: `3,861` assets; `17`: `6,137` assets; `49`: `129` assets; total `10,127` assets) are preserved unmerged in compliance with Contract §2.8, yielding `47` itemized partitions (`226,324` assets). The `6` master project headers without direct itemized rows correspond to `3` concessions in the `Estructuración` phase with `0.0%` physical construction progress (`ID 169` *IP Conexión Centro*, `ID 174` *APP Sogamoso–Aguazul–Maní–Yucao*, `ID 183` *APP Villeta–Guaduas–El Korán*), `1` contract in `Reversión` (`ID 167` *Bucaramanga–Pamplona*), `1` duplicate SECOP header pending legal reconciliation (`ID 19` *IP Neiva–Espinal–Girardot.*, sharing pseudonymized tax identifier `ANON_NIT_80FC3071C65A` (`SHA-256` prefix of internal `nit`) with active `ID 40` which holds `1,029` assets), and `1` header (`ID 46` *Córdoba–Sucre*) whose inventory is preserved under legacy partition IDs.

---

## B.6. Table B.4: Cold-Start Documentary Ingestion Audit ($603$ Receipts vs. $638$ Extracted Parquet Tables / $32,983$ Rows)

### Table B.4: Cold-Start Documentary Ingestion Audit Across $603$ Heterogeneous File Receipts and $638$ Extracted Parquet Tables

| Detected Format | Total Receipts (`603`) | `complete_structural` | `partial` (Structurable) | `unsupported` (Closed / Free-Text) | Open Structurable Universe (`554`) | $\Phi_{\text{ont}}^{\text{(Cold-Open)}}$ | $\Phi_{\text{ont}}^{\text{(Cold-Raw)}}$ | Parquet Tables in `C3` (`638`) | Parquet Split (`extraccion` + `confirmacion`) | Extracted Parquet Rows (`32,983`) | Unique Ledger Records (`16,785`) | Anchored `C1` (`B10` / `A`), `C2` Recipe & `C3` SHACL Shape |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`csv`** | 442 | 328 (74.21%) | 113 (25.57%) | 1 (0.23%) | 441 | **100.00%** | 99.77% | 475 | 441 + 34 | 897 | 794 | `B10_010_015_005` / `A30_035_005_040` / `REC-B-04` / `Shape_PAR_B50_0008` |
| **`ifc`** | 53 | 0 (0.00%) | 27 (50.94%) | 26 (49.06%) | 27 | **100.00%** | 50.94% | 33 | 27 + 6 | 60 | 60 | `B10_025_10_005` / `A40_045_005_030` / `REC-A-01` / `Shape_PAR_B50_0007` |
| **`markdown`** | 24 | 24 (100.00%) | 0 (0.00%) | 0 (0.00%) | 24 | **100.00%** | 100.00% | 24 | 24 + 0 | 219 | 219 | `B10_010_015_005` / `A30_035_005_040` / `REC-B-04` / `Shape_PAR_B50_0008` |
| **`sql_dump`** | 24 | 0 (0.00%) | 24 (100.00%) | 0 (0.00%) | 24 | **100.00%** | 100.00% | 24 | 24 + 0 | 84 | 84 | `B10_010_015_005` / `A30_035_005_040` / `REC-B-04` / `Shape_PAR_B50_0008` |
| **`txt`** | 21 | 0 (0.00%) | 0 (0.00%) | 21 (100.00%) | 0 | N/A (Free text) | 0.00% | 21 | 21 + 0 | 0 | 0 | `B10_010_015_005` / `A30_035_010_015` / `REC-A-04` (0-row schema skeleton) |
| **`sqlite`** | 16 | 16 (100.00%) | 0 (0.00%) | 0 (0.00%) | 16 | **100.00%** | 100.00% | 16 | 16 + 0 | 137 | 137 | `B10_010_015_005` / `A30_035_005_040` / `REC-B-04` / `Shape_PAR_B50_0008` |
| **`dxf`** | 10 | 0 (0.00%) | 10 (100.00%) | 0 (0.00%) | 10 | **100.00%** | 100.00% | 20 | 10 + 10 | 400 | 200 | `B30_005_005` / `A30_035_005_040` / `REC-A-01` / `Shape_PAR_B50_0002` |
| **`landxml`** | 9 | 9 (100.00%) | 0 (0.00%) | 0 (0.00%) | 9 | **100.00%** | 100.00% | 18 | 9 + 9 | 54 | 27 | `B10_025_10_005` / `A30_035_005_040` / `REC-A-01` / `Shape_PAR_B50_0004` |
| **`pbix_prepared`** | 3 | 3 (100.00%) | 0 (0.00%) | 0 (0.00%) | 3 | **100.00%** | 100.00% | 6 | 3 + 3 | 31,132 | 15,566 | `B10_010_015_005` / `A30_035_005_040` / `REC-B-04` / `Shape_PAR_B50_0008` |
| **`rvt`** | 1 | 0 (0.00%) | 0 (0.00%) | 1 (100.00%) | 0 | N/A (Closed OLE2) | 0.00% | 1 | 1 + 0 | 0 | 0 | `B10_025_10_005` / `A40_085_005_005` / `REC-A-02` (Closed Revit binary) |
| **Total Audited** | **603** | **380 (63.02%)** | **174 (28.86%)** | **49 (8.13%)** | **554** | **100.00% (554/554)** | **91.87% (554/603)** | **638** | **576 + 62** | **32,983** | **16,785** | **`100.00%` Grounding Over Open/Structurable Formats** |

---

## B.7. Table B.5: Retrospective Evolution of $\Phi_{\text{ont}}$ Sub-Metrics Across the 5 CAS Lineage Stages (`Stage 0` to `Stage 4`)

### Table B.5: Retrospective Evolution of $\Phi_{\text{ont}}$ Sub-Metrics Across the 5 CAS Lineage Stages (Stage S0 to Stage S4)

| Evolutionary Lineage Stage | CAS Revision ID & Semantic Version | Active `C1` Classes ($\|A\| + \|B\|$) | `OWL 2 DL` Restr. / `SHACL` Shapes | `C2` Edges / Recipes | Evaluated / Linked Assets (`Orphans`) | $\Phi_{\text{ont}}^{\text{(Taxonomic-Asset)}}$ (Batch / Norm. `226,324`) | $\Phi_{\text{ont}}^{\text{(Doc-Matrix-18112)}}$ (Reconciled Units) | $\Phi_{\text{ont}}^{\text{(Relational-C2-793)}}$ (`ESTADO_4` + `APU`) | $\Phi_{\text{ont}}^{\text{(Cold-Ingestion)}}$ (`554` Open / `603` Raw) | $\Phi_{\text{ont}}^{\text{(Composite-Core3)}}$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 0** (First *ITcon* Submission Baseline) | `preliminary_monolithic_submission` (`2026-08`) | 15,822 (`4,620 + 11,202`) | 0 / 0 | 0 / 0 | `47,768 / 23,024` (`24,744` orphans) | **48.20%** (`10.17%`) | **23.35%** (`4,230 / 18,112`) | **0.00%** (`0 / 793`) | **0.00%** / **0.00%** | **23.85%** *(Stage S0 initial baseline prelim. SII: 55.8%)* |
| **Stage 1** (`CAS 1` — Pre-Gate 1, Railway + TAM) | `340ed01141b7448e8d6157bd05aab5e2` (`2026-10-15`) | 15,990 (`4,620 + 11,370`) | 8 / 4 | 0 / 0 | `226,324 / 226,226` (`98` orphans `A50_015_005_025`) | **99.9567%** (`99.9567%`) | **26.94%** (`4,880 / 18,112`) | **0.00%** (`0 / 793`) | **0.00%** / **0.00%** | **42.30%** |
| **Stage 2** (`CAS 2` — Gate 2 Promotion) | `9a3cc6d9a341e551b95fecf286948fb2` (`2026-10-24`) | 16,190 (`4,666 + 11,524`) | 8 / 100 | 344 / 0 | `226,324 / 226,324` (`0` orphans) | **100.00%** (`100.00%`) | **99.78%** (`18,072 / 18,112`) | **43.38%** (`344 / 793` edges) | **0.00%** / **0.00%** | **81.05%** |
| **Stage 3** (`CAS 3` — Gate 2.5 OWL 2 DL Axiomatized) | `55e94d32a7f24ee70684c7c1b01de82d` (`2026-10-25`) | 16,230 (`4,686 + 11,544`) | 814 / 104 | 793 / 13 | `226,324 / 226,324` (`0` orphans) | **100.00%** (`100.00%`) | **100.00%** (`18,112 / 18,112`) | **100.00%** (`89,096` + `73,640`) | **100.00%** / **91.87%** | **100.00%** |
| **Stage 4** (`CAS 4` — Gate 3 Active Production) | `b6bd01f850790ad22d399b95545f73d2` (`2026-10-25`) | 16,230 (`4,686 + 11,544`) | 814 / 104 | 793 / 13 | `226,324 / 226,324` (`0` orphans) | **100.00%** (`100.00%`) | **100.00%** (`18,112 / 18,112`) | **100.00%** (`89,096` + `73,640`) | **100.00%** / **91.87%** | **100.00%** |

---
