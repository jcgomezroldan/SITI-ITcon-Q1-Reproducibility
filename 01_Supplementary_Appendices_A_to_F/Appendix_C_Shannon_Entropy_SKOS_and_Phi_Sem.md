# Supplementary Appendix C: Conditional Shannon Classification Entropy Collapse ($H(C \mid T)$), Pentalingual W3C SKOS Lexical Normalization ($2,892$ Terms), Deterministic Disambiguation of `A50_045`, OWL 2 DL Existential Pruning ($814$ Restrictions), and W3C SHACL Closed-World Discrimination ($\Phi_{\text{sem}}$)

**Manuscript Title:** *Orthogonal Ontology Factorization for Semantic Interoperability in Transport Infrastructure* (`ORTHOGONAL ONTOLOGY FACTORIZATION FOR SEMANTIC INTEROPERABILITY IN TRANSPORT INFRASTRUCTURE`)  
**Authors:** Juan C. Gómez (Corresponding Author; PhD candidate, Doctoral program in Technology Innovation Management, Universidad de los Andes, and National Infrastructure Agency (ANI), Bogotá, Colombia, `jc.gomez1988@uniandes.edu.co`), Rodrigo F. Herrera (Associate professor, School of Civil Engineering, Pontificia Universidad Católica de Valparaíso, Valparaíso, Chile, `rodrigo.herrera@pucv.cl`), Karen M. Castañeda (Assistant professor, School of Civil Engineering, Pontificia Universidad Católica de Valparaíso, Valparaíso, Chile, `karen.castaneda@pucv.cl`), and Juan F. Correal (Full professor, Department of Civil and Environmental Engineering, Universidad de los Andes, Bogotá, Colombia, `jcorreal@uniandes.edu.co`)  
**Reference:** Gómez, J. C., Herrera, R. F., Castañeda, K. M., & Correal, J. F. (2027). Orthogonal ontology factorization for semantic interoperability in transport infrastructure. *Journal of Information Technology in Construction (ITcon)*, 32, 1-X. https://doi.org/10.36680/j.itcon.2027.[added by editor]  
**Journal Target:** *Journal of Information Technology in Construction (ITcon)* — Second Submission (Comprehensive Empirical & Mathematical Audit Across the 5 CAS Lineage Stages)  
**Active Semantic Release Audited (CAS Stage 4 / Gate 3):** `b6bd01f850790ad22d399b95545f73d2` (`Stage S3/S4 (CAS b6bd01f850790ad22d399b95545f73d2)`, evolved from `55e94d32a7f24ee70684c7c1b01de82d`, `9a3cc6d9a341e551b95fecf286948fb2`, and `340ed01141b7448e8d6157bd05aab5e2`)  
**Reproducibility & Automated Manuscript-to-Corpus Table Synchronization Protocol:** Strict read-only forensic execution (`os.O_RDONLY`, `0` production bytes modified). Every analytical cell in `Table C.1` through `Table C.5` is programmatically formatted and injected directly from the live DuckDB/SciPy data outputs (`seed = 20261102`, $B = 10,000$ Bootstrap resamples).

---

## C.1. Mathematical Formulation of Dimension 2 ($\Phi_{\text{sem}}$) and Its Three Complementary Sub-Metrics

Within the global **Semantic Interoperability Index ($\text{SII} = w_1 \, \Phi_{\text{ont}} + w_2 \, \Phi_{\text{sem}} + w_3 \, \Phi_{\text{eff}}$)**, the second orthogonal dimension ($\Phi_{\text{sem}}$) evaluates how the three-layer architecture disambiguates lexical polysemy, intra-tabular code collisions, and normative engineering violations across the **5 Evolutionary Stages (`Stage 0` to `Stage 4`)**:

1. **Primary Information-Theoretic Sub-Metric — Conditional Shannon Classification Entropy Collapse ($\Phi_{\text{sem}}^{\text{(Shannon-Collapse)}}$):**
   $$\Phi_{\text{sem}}^{\text{(Shannon-Collapse)}}(s) = \left(1 - \frac{H_{\text{obs}, s}(C \mid T)}{H_{\max}}\right) \times 100\%, \qquad H_{\text{obs}, s}(C \mid T) = -\sum_{t \in \mathcal{T}} P(t) \sum_{c \in \mathcal{C}_s(t)} P_s(c \mid t) \log_2 P_s(c \mid t)$$
   - **Stage S0 (initial baseline) Longitudinal Reference Horizon:** $H_{\max}^{\text{(ref)}} = 3.4800\text{ bits}$ ($2^{3.48} \approx 11.16$ effective competing classes in uncontrolled legacy nomenclature).
   - **Exact Empirical Maximum Candidate Pool Horizon:** $H_{\max}^{\text{(emp)}} = \log_2 |\mathcal{C}_{\text{cand, max}}| = \log_2(11) = 3.4594\text{ bits}$ ($11$ competing candidate classes in `Stage 0` prior to $\text{Language A} \perp \text{Language B}$ decoupling).
   - **Realistic Irreducible Polymorphic Residual Entropy in `Stage 4` ($S_4$):** Because civil infrastructure terminology includes genuinely polymorphic cross-level concepts (`A30` spatial zone vs. `A40` functional system vs. `A50` technical component—e.g., *calzada*, *drenaje*, *separador*, *luminaria*, *centro de control operacional*) whose disambiguation prior to specifying the target query granularity level retains a non-zero posterior uncertainty, $H_{S_4}(C \mid T)$ converges to an empirical residual mean of **$0.1578\text{ bits}$** ($\text{SD} = 0.0249\text{ bits}$, range $[0.1099, 0.2144]\text{ bits}$) across the $N = 47$ itemized asset partitions (**$0.1613\text{ bits}$** across the $N = 50$ master concessions), yielding **$\Phi_{\text{sem}}^{\text{(Shannon-Collapse)}}(S_4) = 95.47\%$** (**$95.37\%$** across $N = 50$).

2. **Formal Logic Sub-Metric — OWL 2 DL TBox Consistency ($\Phi_{\text{sem}}^{\text{(OWL2DL-TBox-Consistency)}}$):** Evaluates over `capa1_siti_ontology.ttl` (`438,194` RDF triples, isomorphic with `.owl`) the formal consistency of the `16,230` active unique classes, `814` `owl:Restriction` axioms (`806` `owl:someValuesFrom` + `8` `owl:allValuesFrom`), `157` `owl:ObjectProperty` declarations, and `45` pairwise table disjointness constraints ($\binom{10}{2} = 45$), confirming `0` cycles, `0` unsatisfiable classes, and `0` $\text{Language A} \cap \text{Language B}$ leaks (**$\Phi_{\text{sem}}^{\text{(OWL2DL-TBox-Consistency)}} = 100.00\%$**).

3. **Closed-World Validation Sub-Metric — W3C SHACL Discrimination ($\Phi_{\text{sem}}^{\text{(SHACL-CWA-Discrimination)}}$):** Evaluates live over `capa1_shacl_shapes.ttl` (`1,229` triples, **`104` `sh:NodeShape`**, **`109` `sh:property` constraints** + `1` `sh:sparql` constraint) the bipolar discrimination between compliant Layer 3 engineering records (`0` false alarms, `FPR = 0.00%`) and synthetic/adversarial engineering anomalies (`TPR = 100.00%`), achieving **$\Phi_{\text{sem}}^{\text{(SHACL-CWA-Discrimination)}} = 100.00\%$**.

---

## C.2. Table C.1: Pentalingual W3C SKOS Lexicon Distribution Across 10 SITI Tables and 5 Languages ($2,892$ Terms) and Deterministic Disambiguation of `A50_045` ($179/346$ Classes)

### Table C.1: Pentalingual SKOS Lexicon Distribution ($2,892$ Expressions Across $814$ Enriched Classes and $10$ Tables A10–B50) and Conditional Shannon Entropy Collapse ($H_{\text{S0}} \to H_{\text{S4}}$)

| SITI Table / Hierarchy | Active Unique Classes (`C1`) | Classes with SKOS (`814`) | `skos:prefLabel` (`es`) | `es` (`alt/idx`) | `en` (`trans.`) | `fr` (`trans.`) | `pt` (`trans.`) | `de` (`trans.`) | Total SKOS Reviewed (`2,892`) | Total Lexical Forms (`pref+alt`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `A10` (Infrastructure complexes & networks) | 1,278 | 13 | 1,278 | 14 | 8 | 1 | 0 | 0 | 23 | 1,301 |
| `A20` (Modal functional transport systems) | 351 | 31 | 351 | 32 | 16 | 3 | 0 | 0 | 51 | 402 |
| `A30` (Transport spatial zones & corridors) | 361 | 32 | 361 | 40 | 25 | 11 | 1 | 1 | 78 | 439 |
| `A40` (Constructive systems & elements) | 913 | 266 | 913 | 260 | 260 | 250 | 242 | 242 | 1,254 | 2,167 |
| `A50` (Technical components & devices) | 1,783 | 172 | 1,783 | 174 | 162 | 142 | 134 | 133 | 745 | 2,528 |
| `B10` (Lifecycle phases, contracts & documents) | 635 | 50 | 635 | 51 | 27 | 14 | 0 | 0 | 92 | 727 |
| `B20` (Institutional actors, roles & entities) | 5,253 | 41 | 5,253 | 35 | 19 | 12 | 0 | 0 | 66 | 5,319 |
| `B30` (Construction resources, materials & equipment) | 870 | 55 | 870 | 65 | 26 | 13 | 0 | 0 | 104 | 974 |
| `B40` (Lifecycle construction & O&M activities) | 4,048 | 48 | 4,048 | 228 | 25 | 13 | 0 | 0 | 266 | 4,314 |
| `B50` (Technical properties, costs & KPIs) | 738 | 106 | 738 | 96 | 71 | 26 | 10 | 10 | 213 | 951 |
| **Total `C1` (`10` Tables)** | **16,230** | **814** | **16,230** | **995** | **639** | **485** | **387** | **386** | **2,892** | **19,122** |
| **Sub-Hierarchy `A50_045` (Water & Drainage)** | **346** (`167` raw + `179` `__occN`) | **33** | **346** | **31** | **28** | **27** | **26** | **26** | **138** | **`0` PK Collisions (`100%` Disambiguated)** |

---

## C.3. Table C.2: Conditional Shannon Entropy $H(C \mid T)$ and $\Phi_{\text{sem}}$ Evolution Across the 5 CAS Lineage Stages by SITI Table ($N=10$), Documentary Library ($N=10$), and SKOS Language ($N=5$)

| Stratum / Panel Unit | Evaluated Items / Units | $H_{S_0}(C\mid T)$ (`bits`) | $H_{S_1}(C\mid T)$ (`bits`) | $H_{S_2}(C\mid T)$ (`bits`) | $H_{S_3}(C\mid T)$ (`bits`) | $H_{S_4}(C\mid T)$ (`bits`) | $\Phi_{\text{sem}}(S_0)$ (`%`) | $\Phi_{\text{sem}}(S_1)$ (`%`) | $\Phi_{\text{sem}}(S_2)$ (`%`) | $\Phi_{\text{sem}}(S_3)$ (`%`) | $\Phi_{\text{sem}}(S_4)$ (`%`, $H_{\max}=3.48$) | $\Phi_{\text{sem}}^{\text{(emp)}}(S_4)$ (`%`, $\log_2 11$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Panel C: By Canonical SITI Ontology Table (N = 10 Tables, 16,230 Active Unique Classes)** | | | | | | | | | | | | |
| `A10` (Infrastructure complexes & networks) | 1,278 | 2.8277 | 1.8267 | 0.8571 | 0.2431 | 0.1895 | 18.74% | 47.51% | 75.37% | 93.01% | **94.55%** | 94.52% |
| `A20` (Modal functional transport systems) | 351 | 2.8155 | 1.8061 | 0.8545 | 0.2442 | 0.1840 | 19.09% | 48.10% | 75.45% | 92.98% | **94.71%** | 94.68% |
| `A30` (Transport spatial zones & corridors) | 361 | 2.8531 | 1.8554 | 0.8742 | 0.2487 | 0.1924 | 18.01% | 46.68% | 74.88% | 92.85% | **94.47%** | 94.44% |
| `A40` (Constructive systems & elements) | 913 | 2.8883 | 1.9029 | 0.8974 | 0.2557 | 0.1997 | 17.00% | 45.32% | 74.21% | 92.65% | **94.26%** | 94.23% |
| `A50` (Technical components & devices) | 1,783 | 2.8808 | 1.9010 | 0.8601 | 0.2459 | 0.1901 | 17.22% | 45.37% | 75.29% | 92.93% | **94.54%** | 94.50% |
| `B10` (Lifecycle phases, contracts & documents) | 635 | 2.8589 | 1.7977 | 0.8627 | 0.2457 | 0.1807 | 17.85% | 48.34% | 75.21% | 92.94% | **94.81%** | 94.78% |
| `B20` (Institutional actors, roles & entities) | 5,253 | 2.8444 | 1.8520 | 0.9327 | 0.2645 | 0.2030 | 18.27% | 46.78% | 73.20% | 92.40% | **94.17%** | 94.13% |
| `B30` (Construction resources, materials & equipment) | 870 | 2.8567 | 1.8022 | 0.8584 | 0.2442 | 0.1809 | 17.91% | 48.21% | 75.33% | 92.98% | **94.80%** | 94.77% |
| `B40` (Lifecycle construction & O&M activities) | 4,048 | 2.7974 | 1.8574 | 1.0322 | 0.2952 | 0.2345 | 19.61% | 46.63% | 70.34% | 91.52% | **93.26%** | 93.22% |
| `B50` (Technical properties, costs & KPIs) | 738 | 2.8714 | 1.8232 | 0.8773 | 0.2496 | 0.1843 | 17.49% | 47.61% | 74.79% | 92.83% | **94.70%** | 94.67% |
| **Panel C Mean (10 Canonical Tables, 16,230 Active Classes)** | **16,230** | **2.8494** | **1.8425** | **0.8906** | **0.2537** | **0.1939** | **18.12%** | **47.06%** | **74.41%** | **92.71%** | **94.43%** | **94.39%** |
| **Panel D: By Documentary Repository in Confrontation Matrix (N = 10 Libraries, 18,112 Units)** | | | | | | | | | | | | |
| `historico_y_desarrollo` (Repository historico_y_desarrollo) | 7,293 | 3.1333 | 2.0443 | 0.8887 | 0.3055 | 0.2053 | 9.96% | 41.25% | 74.46% | 91.22% | **94.10%** | 94.07% |
| `docs` (Repository docs) | 4,628 | 3.3119 | 2.1903 | 0.9524 | 0.3180 | 0.2189 | 4.83% | 37.06% | 72.63% | 90.86% | **93.71%** | 93.67% |
| `Biblioteca_tecnica_INVIAS` (Repository Biblioteca_tecnica_INVIAS) | 2,275 | 2.9825 | 1.9170 | 0.7800 | 0.2881 | 0.1853 | 14.30% | 44.91% | 77.59% | 91.72% | **94.67%** | 94.64% |
| `Documentos concesion` (Repository Documentos concesion) | 2,150 | 2.5265 | 1.3762 | 0.5943 | 0.2543 | 0.1511 | 27.40% | 60.45% | 82.92% | 92.69% | **95.66%** | 95.63% |
| `Biblioteca_tecnica_ANI` (Repository Biblioteca_tecnica_ANI) | 723 | 2.5539 | 1.4175 | 0.6138 | 0.2573 | 0.1542 | 26.61% | 59.27% | 82.36% | 92.61% | **95.57%** | 95.54% |
| `Biblioteca_ontologias_transporte` (Repository Biblioteca_ontologias_transporte) | 562 | 3.0560 | 1.9585 | 0.8219 | 0.2953 | 0.1939 | 12.19% | 43.72% | 76.38% | 91.52% | **94.43%** | 94.40% |
| `Power BI - planeacion ANI` (Repository Power BI - planeacion ANI) | 382 | 2.3836 | 1.2212 | 0.5422 | 0.2440 | 0.1409 | 31.50% | 64.91% | 84.42% | 92.99% | **95.95%** | 95.93% |
| `otros documentos` (Repository otros documentos) | 42 | 3.0164 | 2.1035 | 0.6844 | 0.2748 | 0.1670 | 13.32% | 39.55% | 80.33% | 92.10% | **95.20%** | 95.17% |
| `siti_production_corpus` (Repository siti_production_corpus) | 29 | 2.9610 | 2.0548 | 0.7006 | 0.2762 | 0.1684 | 14.91% | 40.95% | 79.87% | 92.06% | **95.16%** | 95.13% |
| `Biblioteca_tecnica_PMI` (Repository Biblioteca_tecnica_PMI) | 28 | 3.0705 | 1.9978 | 0.8295 | 0.2966 | 0.1945 | 11.77% | 42.59% | 76.16% | 91.48% | **94.41%** | 94.38% |
| **Panel D Mean (10 Repositories, 18,112 Documentary Units)** | **18,112** | **2.8996** | **1.8281** | **0.7408** | **0.2810** | **0.1779** | **16.68%** | **47.47%** | **78.71%** | **91.93%** | **94.89%** | **94.86%** |
| **Panel E: By W3C SKOS Lexical Language (N = 5 Languages, 2,892 Reviewed Expressions)** | | | | | | | | | | | | |
| `SKOS_ES` (Spanish (reviewed aliases & variants)) | 995 | 2.7988 | 1.7480 | 0.7898 | 0.2204 | 0.1565 | 19.57% | 49.77% | 77.30% | 93.67% | **95.50%** | 95.48% |
| `SKOS_EN` (English (IFC/AASHTO technical translations)) | 639 | 2.7627 | 1.6981 | 0.7537 | 0.2082 | 0.1424 | 20.61% | 51.20% | 78.34% | 94.02% | **95.91%** | 95.88% |
| `SKOS_FR` (French (PIARC/AFNOR technical translations)) | 485 | 2.7561 | 1.7138 | 0.7633 | 0.2111 | 0.1456 | 20.80% | 50.75% | 78.07% | 93.93% | **95.82%** | 95.79% |
| `SKOS_PT` (Portuguese (DNIT/ABNT technical translations)) | 387 | 2.7239 | 1.6693 | 0.7310 | 0.2008 | 0.1329 | 21.73% | 52.03% | 78.99% | 94.23% | **96.18%** | 96.16% |
| `SKOS_DE` (German (FGSV/DIN technical translations)) | 386 | 2.7241 | 1.6695 | 0.7312 | 0.2009 | 0.1329 | 21.72% | 52.03% | 78.99% | 94.23% | **96.18%** | 96.16% |
| **Panel E Mean (5 W3C SKOS Languages, 2,892 Expressions)** | **2,892** | **2.7531** | **1.6997** | **0.7538** | **0.2083** | **0.1421** | **20.89%** | **51.16%** | **78.34%** | **94.02%** | **95.92%** | **95.89%** |

---

## C.4. Table C.3: Concession-Level Conditional Entropy Collapse Across 47 Itemized Asset Partitions and 50 Master Concessions ($S_0 \to S_4$)

### Table C.3: Itemized Longitudinal Trajectory of Conditional Shannon Entropy $H(C \mid T)$ and $\Phi_{\text{sem}}$ Across All $N = 47$ Empirical Asset Partitions ($226,324$ National Assets)

| Panel / ID | Concession Name / Partition Scope | Stage / Mode | Assets ($N_{\text{inv}}$) | Functional Layers | $H_{S_0}(C\mid T)$ (`bits`) | $H_{S_1}(C\mid T)$ (`bits`) | $H_{S_2}(C\mid T)$ (`bits`) | $H_{S_3}(C\mid T)$ (`bits`) | $H_{S_4}(C\mid T)$ (`bits`) | $\Delta H_{S_0\to S_4}$ (`bits`) | $\Phi_{\text{sem}}(S_0)$ (`%`) | $\Phi_{\text{sem}}(S_4)$ (`%`, $H_{\max}=3.48$) | $\Phi_{\text{sem}}^{\text{(emp)}}(S_4)$ (`%`, $\log_2 11$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `M-001` | IP - Accesos Norte a Bogotá | Construcción / Carretero | 604 | 5 | 2.8185 | 1.6101 | 0.7550 | 0.2067 | 0.1329 | 2.6856 | 19.01% | **96.18%** | 96.16% |
| `M-002` | IP - Antioquia - Bolívar | Construcción / Carretero | 16,096 | 15 | 2.9035 | 1.7396 | 0.8232 | 0.2432 | 0.1626 | 2.7410 | 16.56% | **95.33%** | 95.30% |
| `M-003` | Autopista Conexión Pacífico 1 | Construcción / Carretero | 8,481 | 17 | 2.8791 | 1.6898 | 0.7936 | 0.2230 | 0.1459 | 2.7332 | 17.27% | **95.81%** | 95.78% |
| `M-004` | Autopista Conexión Pacífico 2 | Operación y Mantenimiento / Carretero | 4,356 | 15 | 2.9896 | 1.9485 | 0.8308 | 0.2371 | 0.1760 | 2.8136 | 14.09% | **94.94%** | 94.91% |
| `M-005` | Autopista Conexión Pacífico 3 | Operación y Mantenimiento / Carretero | 1,193 | 3 | 2.8174 | 1.6123 | 0.7626 | 0.2061 | 0.1310 | 2.6865 | 19.04% | **96.24%** | 96.21% |
| `M-006` | Autopista al Mar 1 | Operación y Mantenimiento / Carretero | 855 | 3 | 2.7998 | 1.5928 | 0.7453 | 0.2036 | 0.1270 | 2.6728 | 19.55% | **96.35%** | 96.33% |
| `M-007` | Autopista al Mar 2 | Construcción / Carretero | 973 | 3 | 2.8397 | 1.6950 | 0.7664 | 0.2184 | 0.1464 | 2.6933 | 18.40% | **95.79%** | 95.77% |
| `M-008` | Autopista al Río Magdalena 2 | Construcción / Carretero | 1,311 | 8 | 2.9554 | 1.9232 | 0.7926 | 0.2289 | 0.1714 | 2.7840 | 15.08% | **95.08%** | 95.05% |
| `M-009` | Autopista Conexión Norte | Operación y Mantenimiento / Carretero | 7,200 | 17 | 2.9187 | 1.7900 | 0.8194 | 0.2469 | 0.1636 | 2.7550 | 16.13% | **95.30%** | 95.27% |
| `M-010` | Bucaramanga - Barrancabermeja - Yondó | Construcción / Carretero | 8,485 | 17 | 2.9362 | 1.8124 | 0.8284 | 0.2497 | 0.1787 | 2.7575 | 15.63% | **94.86%** | 94.83% |
| `M-011` | Cartagena - Barranquilla y Circunvalar de la Prosperidad | Operación y Mantenimiento / Carretero | 12,707 | 11 | 2.9393 | 1.7853 | 0.8557 | 0.2514 | 0.1740 | 2.7653 | 15.54% | **95.00%** | 94.97% |
| `M-013` | Pamplona - Cúcuta | Operación y Mantenimiento / Carretero | 7,810 | 15 | 2.9088 | 1.7385 | 0.8107 | 0.2387 | 0.1621 | 2.7467 | 16.41% | **95.34%** | 95.31% |
| `M-014` | Honda - Puerto Salgar - Girardot | Operación y Mantenimiento / Carretero | 670 | 3 | 2.8051 | 1.5993 | 0.7366 | 0.2027 | 0.1265 | 2.6786 | 19.39% | **96.36%** | 96.34% |
| `M-015` | IP - Cambao Manizales | Construcción / Carretero | 803 | 3 | 2.7957 | 1.5917 | 0.7331 | 0.1959 | 0.1253 | 2.6704 | 19.66% | **96.40%** | 96.38% |
| `M-016` | IP - Chirajara - Fundadores | Operación y Mantenimiento / Carretero | 458 | 6 | 2.8824 | 1.7635 | 0.8513 | 0.2540 | 0.1709 | 2.7115 | 17.17% | **95.09%** | 95.06% |
| `M-018` | Mulaló - Loboguerrero | Preconstrucción / Carretero | 1,987 | 14 | 2.9011 | 1.7822 | 0.8337 | 0.2531 | 0.1745 | 2.7266 | 16.64% | **94.99%** | 94.96% |
| `M-019` | IP Neiva - Espinal - Girardot. | Operación y Mantenimiento / Carretero | 0 | 0 | 3.0906 | 1.9911 | 0.9432 | 0.2747 | 0.1725 | 2.9182 | 11.19% | **95.04%** | 95.02% |
| `M-020` | Rumichaca - Pasto | Operación y Mantenimiento / Carretero | 10,417 | 14 | 2.8890 | 1.7504 | 0.8161 | 0.2352 | 0.1644 | 2.7247 | 16.98% | **95.28%** | 95.25% |
| `M-021` | Perimetral de Oriente de Cundinamarca | Operación y Mantenimiento / Carretero | 9,764 | 13 | 2.9292 | 1.8232 | 0.8263 | 0.2412 | 0.1699 | 2.7594 | 15.83% | **95.12%** | 95.09% |
| `M-022` | Puerta de Hierro - Palmar de Varela y Carreto - Cruz del Viso | Operación y Mantenimiento / Carretero | 5,658 | 14 | 2.9402 | 1.8113 | 0.8276 | 0.2493 | 0.1772 | 2.7630 | 15.51% | **94.91%** | 94.88% |
| `M-023` | Santana - Mocoa - Neiva | Construcción / Carretero | 1,700 | 3 | 2.8237 | 1.6164 | 0.7557 | 0.2049 | 0.1319 | 2.6918 | 18.86% | **96.21%** | 96.19% |
| `M-024` | Popayán - Santander de Quilichao | Construcción / Carretero | 665 | 3 | 2.8199 | 1.6021 | 0.7499 | 0.2007 | 0.1338 | 2.6861 | 18.97% | **96.15%** | 96.13% |
| `M-025` | Transversal del Sisga | Operación y Mantenimiento / Carretero | 8,556 | 13 | 2.9176 | 1.7730 | 0.8372 | 0.2527 | 0.1671 | 2.7505 | 16.16% | **95.20%** | 95.17% |
| `M-026` | IP - Ampliación a tercer carril doble calzada Bogotá - Girardot | Construcción / Carretero | 10,152 | 13 | 2.8430 | 1.6275 | 0.7672 | 0.2215 | 0.1448 | 2.6982 | 18.30% | **95.84%** | 95.81% |
| `M-028` | IP - Vías del Nus | Operación y Mantenimiento / Carretero | 16,330 | 17 | 2.9875 | 1.9636 | 0.8444 | 0.2443 | 0.1808 | 2.8067 | 14.15% | **94.81%** | 94.77% |
| `M-029` | Villavicencio - Yopal | Construcción / Carretero | 1,154 | 3 | 2.8244 | 1.6082 | 0.7544 | 0.1978 | 0.1324 | 2.6920 | 18.84% | **96.20%** | 96.17% |
| `M-030` | IP - GICA | Operación y Mantenimiento / Carretero | 1,739 | 14 | 2.8906 | 1.7275 | 0.8024 | 0.2334 | 0.1523 | 2.7382 | 16.94% | **95.62%** | 95.60% |
| `M-032` | Desarrollo Vial Armenia - Pereira - Manizales. | Operación y mantenimiento / Carretero | 3,681 | 12 | 2.8630 | 1.6418 | 0.7899 | 0.2285 | 0.1441 | 2.7189 | 17.73% | **95.86%** | 95.83% |
| `M-033` | Santafé de Bogotá (Puente el Cortijo)  - Siberia - La Punta - El Vino - La Vega - Villeta | Operación y mantenimiento / Carretero | 7,310 | 14 | 2.9020 | 1.7626 | 0.8132 | 0.2364 | 0.1610 | 2.7410 | 16.61% | **95.37%** | 95.35% |
| `M-037` | Desarrollo vial del Oriente de Medellin DEVIMED | Operación y mantenimiento / Carretero | 1,393 | 3 | 2.8166 | 1.6070 | 0.7678 | 0.2089 | 0.1299 | 2.6867 | 19.06% | **96.27%** | 96.24% |
| `M-039` | Malla Vial del Meta | Construcción / Carretero | 987 | 3 | 2.8462 | 1.6806 | 0.7716 | 0.2121 | 0.1470 | 2.6993 | 18.21% | **95.78%** | 95.75% |
| `M-040` | Neiva - Espinal - Girardot | Construcción / Carretero | 1,029 | 3 | 2.8334 | 1.6140 | 0.7579 | 0.1997 | 0.1333 | 2.7001 | 18.58% | **96.17%** | 96.15% |
| `M-041` | Santa Marta - Riohacha - Paraguachón | Operación y mantenimiento / Carretero | 851 | 3 | 2.8229 | 1.6113 | 0.7477 | 0.2044 | 0.1289 | 2.6941 | 18.88% | **96.30%** | 96.27% |
| `M-045` | Briceño - Tunja - Sogamoso | Operación y mantenimiento / Carretero | 8,333 | 15 | 2.9934 | 1.9892 | 0.8786 | 0.2677 | 0.2047 | 2.7887 | 13.98% | **94.12%** | 94.08% |
| `M-046` | Cordoba Sucre | Operación y Mantenimiento / Carretero | 0 | 0 | 3.0823 | 1.9930 | 0.9452 | 0.2768 | 0.1675 | 2.9148 | 11.43% | **95.19%** | 95.16% |
| `M-052` | Ruta del Sol - Sector 3 | Construcción / Carretero | 3,052 | 3 | 2.8511 | 1.6248 | 0.7800 | 0.2178 | 0.1371 | 2.7140 | 18.07% | **96.06%** | 96.04% |
| `M-153` | Nueva Malla vial del Valle accesos Cali y Palmira. | Construcción / Carretero | 2,325 | 3 | 2.8804 | 1.6465 | 0.7982 | 0.2239 | 0.1415 | 2.7388 | 17.23% | **95.93%** | 95.91% |
| `M-154` | ALO Sur - Avenida Longitudinal de Occidente | Preconstrucción / Carretero | 235 | 4 | 2.9028 | 1.7209 | 0.8240 | 0.2381 | 0.1615 | 2.7413 | 16.59% | **95.36%** | 95.33% |
| `M-155` | Troncal del Magdalena "Puerto Salgar - Barrancabermeja" C1 | Construcción / Carretero | 18,949 | 15 | 3.0202 | 1.9434 | 0.8393 | 0.2463 | 0.1839 | 2.8363 | 13.21% | **94.71%** | 94.68% |
| `M-156` | Troncal del Magdalena "Sabana de Torres - Curumaní C2 | Construcción / Carretero | 1,886 | 4 | 2.8912 | 1.6534 | 0.7948 | 0.2208 | 0.1424 | 2.7487 | 16.92% | **95.91%** | 95.88% |
| `M-157` | Accesos Norte Fase II | Preconstrucción / Carretero | 2,689 | 13 | 2.9817 | 1.8315 | 0.8614 | 0.2595 | 0.1791 | 2.8025 | 14.32% | **94.85%** | 94.82% |
| `M-158` | APP Buga – Buenaventura | Construcción / Carretero | 13,887 | 15 | 3.0005 | 1.9736 | 0.8629 | 0.2645 | 0.2027 | 2.7978 | 13.78% | **94.18%** | 94.14% |
| `M-162` | IP Aeropuerto De Suroccidente - Aeropuerto Alfonso Bonilla Aragón | Estructuración / Aeroportuario | 5 | 4 | 2.9807 | 1.9829 | 0.8964 | 0.2702 | 0.2096 | 2.7710 | 14.35% | **93.98%** | 93.94% |
| `M-165` | APP Dorada - Chiriguana | Estructuración / Ferreo | 6 | 1 | 2.8664 | 1.8809 | 0.8907 | 0.2552 | 0.1983 | 2.6681 | 17.63% | **94.30%** | 94.27% |
| `M-167` | Bucaramanga - Pamplona | Reversión / Carretero | 0 | 0 | 3.1358 | 2.0158 | 0.9710 | 0.2837 | 0.1783 | 2.9574 | 9.89% | **94.88%** | 94.84% |
| `M-169` | IP Conexión Centro | Estructuración / Carretero | 0 | 0 | 3.1282 | 2.0192 | 0.9760 | 0.2854 | 0.1751 | 2.9531 | 10.11% | **94.97%** | 94.94% |
| `M-174` | APP Sogamoso – Aguazul – Mani - Yucao | Estructuración / Carretero | 0 | 0 | 3.1369 | 2.0267 | 0.9724 | 0.2842 | 0.1778 | 2.9590 | 9.86% | **94.89%** | 94.86% |
| `M-183` | APP Villeta - Guaduas- El Korán | Estructuración / Carretero | 0 | 0 | 3.1458 | 2.0272 | 0.9685 | 0.2858 | 0.1815 | 2.9642 | 9.60% | **94.78%** | 94.75% |
| `M-184` | IP Autopistas del Caribe, corredor de carga Cartagena - Barranquilla | Preconstrucción / Carretero | 9,445 | 15 | 2.9454 | 1.7180 | 0.8428 | 0.2584 | 0.1666 | 2.7788 | 15.36% | **95.21%** | 95.18% |
| `M-187` | IP Campo De Vuelo Aeropuerto El Dorado - Bogotá Dc | Estructuración / Aeroportuario | 10 | 5 | 3.0015 | 2.0071 | 0.9050 | 0.2761 | 0.2144 | 2.7871 | 13.75% | **93.84%** | 93.80% |
| `P-000` | Partición heredada ID 0 (Proyecto ANI 0) | Partición histórica (Contrato §2.8) | 3,861 | 8 | 2.7575 | 1.5634 | 0.7586 | 0.2154 | 0.1405 | 2.6170 | 20.76% | **95.96%** | 95.94% |
| `P-017` | Partición heredada ID 17 (Proyecto ANI 17) | Partición histórica (Contrato §2.8) | 6,137 | 13 | 2.8251 | 1.6689 | 0.7941 | 0.2278 | 0.1546 | 2.6705 | 18.82% | **95.56%** | 95.53% |
| `P-049` | Partición heredada ID 49 (Proyecto ANI 49) | Partición histórica (Contrato §2.8) | 129 | 1 | 2.7887 | 1.5878 | 0.6922 | 0.1762 | 0.1099 | 2.6789 | 19.86% | **96.84%** | 96.82% |
| **MEAN-A47** | **Panel A Mean (47 Itemized Asset Partitions, SD in Text)** | **47 Partitions** | **226,324** | **21** | **2.8878** | **1.7380** | **0.8040** | **0.2308** | **0.1578** | **2.7300** | **17.02%** | **95.47%** | **95.44%** |
| **MEAN-B50** | **Panel B Mean (50 Master Concessions in siti_ani_proyectos)** | **50 Concessions** | **216,197** | **21** | **2.9215** | **1.7788** | **0.8264** | **0.2384** | **0.1613** | **2.7602** | **16.05%** | **95.37%** | **95.34%** |

---

## C.5. Table C.4: Non-Parametric Wilcoxon Signed-Rank Tests, Effect Sizes (Cohen's $d$, Hedges' $g$, Rosenthal's $r$, $r_{rb}$), and $B=10,000$ Bootstrap 95% Confidence Intervals

### Table C.4: Non-Parametric Paired Wilcoxon Signed-Rank Tests, Effect Sizes, and $B = 10,000$ Bootstrap 95% BCa Confidence Intervals Across 4 Empirical Panels

| Empirical Panel ($N$) | Stage Transition | Mean $\Delta H$ (`bits`) | 95% CI $\Delta H$ (Percentile / BCa, $B=10,000$) | Mean $\Delta \Phi_{\text{sem}}$ (`pp`) | 95% CI $\Delta \Phi_{\text{sem}}$ (Percentile / BCa) | Wilcoxon $W$ | Standardized $Z$ | Two-Sided $p$-Value | One-Sided $p$-Value | Cohen's $d$ | Hedges' $g$ | Rosenthal's $r$ | Rank-Biserial $r_{rb}$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Panel A (N=47 Asset Partitions)** | `S0 -> S1` | `-1.1498` | `[-1.1696, -1.1285] / [-1.1685, -1.1271]` | `+33.04` | `[32.43, 33.61] / [32.39, 33.58]` | `0.0` | `5.9683` | `1.42e-14` | `7.11e-15` | `15.66` | `15.41` | `0.8706` | `1.0000` |
| **Panel A (N=47 Asset Partitions)** | `S1 -> S2` | `-0.9341` | `[-0.9614, -0.9085] / [-0.9635, -0.9103]` | `+26.84` | `[26.11, 27.63] / [26.16, 27.69]` | `0.0` | `5.9683` | `1.42e-14` | `7.11e-15` | `10.05` | `9.88` | `0.8706` | `1.0000` |
| **Panel A (N=47 Asset Partitions)** | `S2 -> S4` | `-0.6462` | `[-0.6532, -0.6392] / [-0.6529, -0.6390]` | `+18.57` | `[18.37, 18.77] / [18.36, 18.76]` | `0.0` | `5.9683` | `1.42e-14` | `7.11e-15` | `26.01` | `25.59` | `0.8706` | `1.0000` |
| **Panel A (N=47 Asset Partitions)** | `S0 -> S4` | `-2.7300` | `[-2.7439, -2.7169] / [-2.7443, -2.7171]` | `+78.45` | `[78.07, 78.85] / [78.08, 78.86]` | `0.0` | `5.9683` | `1.42e-14` | `7.11e-15` | `57.72` | `56.77` | `0.8706` | `1.0000` |
| **Panel B (N=50 Master Concessions)** | `S0 -> S1` | `-1.1427` | `[-1.1615, -1.1224] / [-1.1606, -1.1213]` | `+32.84` | `[32.25, 33.38] / [32.22, 33.35]` | `0.0` | `6.1540` | `1.78e-15` | `8.88e-16` | `15.93` | `15.69` | `0.8703` | `1.0000` |
| **Panel B (N=50 Master Concessions)** | `S1 -> S2` | `-0.9524` | `[-0.9796, -0.9268] / [-0.9805, -0.9280]` | `+27.37` | `[26.63, 28.15] / [26.67, 28.18]` | `0.0` | `6.1540` | `1.78e-15` | `8.88e-16` | `10.06` | `9.91` | `0.8703` | `1.0000` |
| **Panel B (N=50 Master Concessions)** | `S2 -> S4` | `-0.6651` | `[-0.6793, -0.6520] / [-0.6816, -0.6533]` | `+19.11` | `[18.74, 19.52] / [18.77, 19.59]` | `0.0` | `6.1540` | `1.78e-15` | `8.88e-16` | `13.14` | `12.93` | `0.8703` | `1.0000` |
| **Panel B (N=50 Master Concessions)** | `S0 -> S4` | `-2.7602` | `[-2.7834, -2.7392] / [-2.7855, -2.7409]` | `+79.32` | `[78.71, 79.98] / [78.76, 80.04]` | `0.0` | `6.1540` | `1.78e-15` | `8.88e-16` | `34.34` | `33.81` | `0.8703` | `1.0000` |
| **Panel C (N=10 SITI Tables A10–B50)** | `S0 -> S1` | `-1.0070` | `[-1.0290, -0.9852] / [-1.0292, -0.9853]` | `+28.94` | `[28.31, 29.57] / [28.31, 29.57]` | `0.0` | `2.8031` | `1.95e-03` | `9.77e-04` | `26.56` | `24.29` | `0.8864` | `1.0000` |
| **Panel C (N=10 SITI Tables A10–B50)** | `S1 -> S2` | `-0.9518` | `[-0.9834, -0.9159] / [-0.9802, -0.9113]` | `+27.35` | `[26.32, 28.26] / [26.19, 28.17]` | `0.0` | `2.8031` | `1.95e-03` | `9.77e-04` | `16.63` | `15.21` | `0.8864` | `1.0000` |
| **Panel C (N=10 SITI Tables A10–B50)** | `S2 -> S4` | `-0.6967` | `[-0.7241, -0.6778] / [-0.7361, -0.6806]` | `+20.02` | `[19.48, 20.81] / [19.56, 21.15]` | `0.0` | `2.8031` | `1.95e-03` | `9.77e-04` | `17.45` | `15.95` | `0.8864` | `1.0000` |
| **Panel C (N=10 SITI Tables A10–B50)** | `S0 -> S4` | `-2.6555` | `[-2.6759, -2.6302] / [-2.6732, -2.6245]` | `+76.31` | `[75.58, 76.89] / [75.42, 76.82]` | `0.0` | `2.8031` | `1.95e-03` | `9.77e-04` | `67.46` | `61.68` | `0.8864` | `1.0000` |
| **Panel D (N=10 Documentary Libraries)** | `S0 -> S1` | `-1.0714` | `[-1.1204, -1.0144] / [-1.1142, -1.0030]` | `+30.79` | `[29.15, 32.20] / [28.82, 32.02]` | `0.0` | `2.8031` | `1.95e-03` | `9.77e-04` | `11.76` | `10.75` | `0.8864` | `1.0000` |
| **Panel D (N=10 Documentary Libraries)** | `S1 -> S2` | `-1.0873` | `[-1.2276, -0.9354] / [-1.2200, -0.9242]` | `+31.24` | `[26.88, 35.28] / [26.56, 35.06]` | `0.0` | `2.8031` | `1.95e-03` | `9.77e-04` | `4.36` | `3.98` | `0.8864` | `1.0000` |
| **Panel D (N=10 Documentary Libraries)** | `S2 -> S4` | `-0.5628` | `[-0.6253, -0.4983] / [-0.6259, -0.4995]` | `+16.17` | `[14.32, 17.97] / [14.35, 17.99]` | `0.0` | `2.8031` | `1.95e-03` | `9.77e-04` | `5.13` | `4.69` | `0.8864` | `1.0000` |
| **Panel D (N=10 Documentary Libraries)** | `S0 -> S4` | `-2.7216` | `[-2.8749, -2.5496] / [-2.8621, -2.5301]` | `+78.21` | `[73.26, 82.61] / [72.70, 82.25]` | `0.0` | `2.8031` | `1.95e-03` | `9.77e-04` | `9.73` | `8.90` | `0.8864` | `1.0000` |

---

## C.6. Table C.5: OWL 2 DL Existential Restriction Pruning ($814$ Restrictions, $157$ ObjectProperties) and W3C SHACL Closed-World Discrimination ($104$ NodeShapes, $109$ `sh:property`)

### Table C.5: OWL 2 DL Existential Restriction Pruning ($814$ Restrictions, $157$ ObjectProperties) and W3C SHACL Closed-World Discrimination ($104$ NodeShapes, $109$ `sh:property`)

| Formal Semantic Verification Layer & Category | Target Scope (`Domain -> Range` / Shape Target) | Active Construct Count | Triples / Constraints Evaluated | Compliant Batch Violations (`FPR`) | Adversarial / Anomaly Batch Detections (`TPR`) | Pruning / Discrimination Efficacy |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Panel A: OWL 2 DL TBox Axiomatic & Restriction Pruning (capa1_siti_ontology.ttl)** | **16,230 Active Classes / 438,194 Triples** | **814** | **157 ObjectProps + 45 Disjointness** | **0 Unsatisfiable (0.00%)** | **100.00% Invalid A/B Pruned** | **100.00%** |
| 1. Existential Physical Composition (owl:someValuesFrom) | `A10 -> A20 -> A30 -> A40 -> A50 (DAG)` | 98 | 65 ObjectProps (0 Intra-Tabular Ax->Ax) | 0 Cycles / 0 False Blocks | 98/98 Certified DAG Links | **100.00%** |
| 2. Cross-Language Coupling Restrictions (owl:someValuesFrom) | `Language A (A10..A50) <-> Language B (B10..B50)` | 282 | 25 Cross-Language ObjectProps | 0 A cap B Leaks (0.00%) | 282/282 A<->B Couplings | **100.00%** |
| 3. Intertabular Governance & 5D APU Restrictions (owl:someValuesFrom) | `Bx <-> By (B40->B30: 94, B20->B10: 93, B10->B50: 78)` | 413 | 55 Governance ObjectProps | 0 Orphan Facets (0.00%) | 413/413 Bx<->By Governance Links | **100.00%** |
| 4. Canonical Multi-Hop Assembly Recipes (owl:someValuesFrom) | `REC-A-01..07 (7) + REC-B-01..06 (6)` | 13 | 13 Dedicated Recipe ObjectProps | 0 Broken Chains (0.00%) | 13/13 Multi-Hop Chains Verified | **100.00%** |
| 5. Modal Domain Closure Restrictions (owl:allValuesFrom) | `A20_005..040 -> A30_005..040 (siti:tieneAreaModal)` | 8 | 8 Transport Modes (Road, Rail, Air, River...) | 0 Cross-Mode Leaks (0.00%) | 8/8 Modal Closures Enforced | **100.00%** |
| **Panel B: W3C SHACL Closed-World Assumption Discrimination (capa1_shacl_shapes.ttl)** | **104 sh:NodeShape / 1,229 RDF Triples** | **104** | **109 sh:property + 1 sh:sparql** | **0/120 False Alarms (FPR = 0.00%)** | **120/120 Detected (TPR = 100.00%)** | **100.00%** |
| 6. Core Contractual, DAG, Smart Escrow 85/15 & TPM 2.0 Shapes | `A10..A50 (EPSG:9377, UUIDv5) & B10_010_040_0050` | 4 | 9 sh:property + 1 sh:sparql (Ax->Ax block) | 0/30 Compliant Blocked (0.00%) | 30/30 CRS/DAG/Escrow Violations Caught | **100.00%** |
| 7. Parametric Engineering Threshold Shapes (Shape_PAR_B50_0001..0100) | `IRI <= 2.5, Retro >= 150, Asphalt >= 5 cm, Rail 914 mm I <= 50 mm` | 100 | 100 sh:property (min/maxInclusive, pattern) | 0/90 Compliant Blocked (0.00%) | 90/90 Engineering Anomalies Caught | **100.00%** |

---
