# English Data Dictionary & Schema Guide for Native SITI Containers (Layers C1, C2, and C3)

To preserve bit-exact cryptographic `SHA-256` parity with the sealed Content-Addressable Semantic (`CAS`) bundle `b6bd01f850790ad22d399b95545f73d2` (`manifest.json` digest `bda830878ebd24c1...`) and **Table 8** of the manuscript, official institutional files in folders `03_`, `04_`, and `05_` retain their canonical Colombian SITI filenames and column identifiers. This guide provides a complete 1:1 English reference for international reviewers.

## 1. Layer 1 (`03_Layer1_C1_Semantic_Core_OWL_SKOS_SHACL/`)

| Canonical SITI Filename | English Description & Architectural Role | Cardinality | Table 8 SHA-256 Prefix |
| :--- | :--- | :--- | :--- |
| `manifest.json` | Active Stage S4 CAS bundle cryptographic manifest (`b6bd01f850790ad22d399b95545f73d2`) | 1 manifest | `bda830878ebd24c1` |
| `capa1_taxonomia_A10.csv` .. `A50.csv` | **Language A** intrinsic physical-spatial hierarchy (`A10` Complexes, `A20` Functional Systems, `A30` Technical Zones [where `A30_035_005_040` *Calzada SITI* = single traffic lane], `A40` Structural Elements, `A50` Sub-elements/Components) | 4,686 active classes | `30bcc7e239fb7e73` (JSON) / `3cb2e801e9b45f91` (mf) |
| `capa1_taxonomia_B10.csv` .. `B50.csv` | **Language B** extrinsic management & telemetry hierarchy (`B10` Project Lifecycle Phases, `B20` Institutional Actors, `B30` Equipment/Machinery/Vehicles, `B40` Materials/Activities/APU Rubrics, `B50` Operational Indicators/Sensors/Context) | 11,544 active classes | (included in 10-CSV digest above) |
| `capa1_siti_ontology.ttl` / `.owl` | Isomorphic `OWL 2 DL` TBox serialization (`814` `owl:Restriction` axioms, `157` `owl:ObjectProperty` predicates) | 438,194 RDF triples | `ab454d4bbb77e48b` / `3b0bd72a3923bb8a` |
| `capa1_lexico_versionado.json` | Versioned pentalingual `W3C SKOS` lexical ring (`ES`, `EN`, `FR`, `PT`, `DE`) | 2,892 reviewed terms | `bef5d58bbbc0b81f` |
| `capa1_shacl_shapes.ttl` | Closed-world `W3C SHACL` validation shapes (`1,229` triples; `F1 = 100.0%` on `240` bipolar cases) | 104 `sh:NodeShape`s | `21b210c7a69fa221` |
| `capa1_iso16739_psets.json` | `ISO 16739-1:2024` (`IFC 4.3`) aligned property and quantity sets | 849 Pset/Qto specs | `ad16ade0ba47e6e5` |
| `capa1_build_siti_ontology.py` | Deterministic `C1` compiler generating `.ttl`, `.owl`, SKOS, and SHACL from the 10 CSVs | Python compiler | Verified in `manifest.json` |

## 2. Layer 2 (`04_Layer2_C2_Property_Graph_and_13_Recipes/`)

| Canonical SITI Filename | English Description & Architectural Role | Cardinality | Table 8 SHA-256 Prefix |
| :--- | :--- | :--- | :--- |
| `capa2_catalogo_lpg.json` | Complete Labeled Property Graph (`LPG`) node & directed adjacency catalog (`:SUBCLASE_DE` = `:SUBCLASS_OF` taxonomic hierarchy; `793` inter-tabular edges across `316` Markov blanket anchors) | 16,232 `UUIDv5` nodes | `c097ff89d55b3a4c` |
| `capa2_siti_lpg_schema.cypher` | Core `Neo4j` / `openCypher` uniqueness constraints and index schema | Schema DDL | `4816dba0042f8440` |
| `capa2_relaciones_intertabulares_puerta1.cypher` | Materialized `openCypher` statements for all `793` inter-tabular `C2` edges | 793 directed edges | `f5795b4501a25b78` (verified) |
| `capa2_recetas_ensamblaje_intertabular.json` | Formal specification of all `13` compositional multi-hop lifecycle assembly recipes (`REC-A-01`..`REC-A-07`, `REC-B-01`..`REC-B-06`) | 13 recipes | `d3020c3b6447c188` (verified) |

## 3. Layer 3 (`05_Layer3_C3_Columnar_Lakehouse_and_Geodesy/`) — Key Parquet Column Glossary

| Native SITI Column Name | English Meaning | Data Type & Governance Role |
| :--- | :--- | :--- |
| `codigo_siti` | SITI taxonomic class code (e.g., `A30_035_005_040`) | Primary semantic join key (`Sigma_C1 -> Pi_C3`) |
| `tabla_siti` | Taxonomic table identifier (`A10`–`A50`, `B10`–`B50`) | Partition / predicate pushdown column |
| `nombre_clase` / `nombre_activo` | Canonical SITI class label / asset record name | UTF-8 descriptive label |
| `tabla_origen_ani` / `capa_origen` | Source `ANI` GIS feature layer (`21` layers) | Provenance & spatial stratum key |
| `proyecto_id` / `codigo_corredor` | Concession / master project identifier (`50` projects) | Corridor aggregation key (Panel `B50`) |
| `unidad_funcional` | Contractual Functional Unit (`UF`) | Concession handover delivery unit |
| `material_normalizado` / `material_inferido` | Normalized / inferred engineering material | Decoupled `B40` material facet |
| `estado_operativo` | Operational lifecycle status | Asset condition state |
| `longitud_metros` / `area_m2` | Geodesic length (`m`) / surface area (`m^2`) | Scalar physical quantities in `SoA` |
| `centroide_x_9377`, `centroide_y_9377` | `EPSG:9377` (`MAGNA-SIRGAS / Origen Nacional`) centroid (`m`) | 64-bit projected coordinates |
| `categoria_tarifa` | Electronic toll / `WIM` vehicle axle tariff category | `OETR` traffic & `ESAL` load stratum |
| `nit` | Corporate taxpayer identification number | Masked via `ANON_NIT_<SHA256[:12]>` in public sample |
| `cedula_catastral`, `folio_matricula`, `propietario_titular` | Cadastral parcel ID, land-registry folio, registered landowner | Masked via deterministic `SHA-256` in public sample |
