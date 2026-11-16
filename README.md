[[https://zenodo.org/badge/DOI/10.5281/zenodo.24290225.svg]](https://doi.org/10.5281/zenodo.24290225)
[[https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg]](https://creativecommons.org/licenses/by/4.0/)

**Permanent Archival Record (Zenodo):** https://doi.org/10.5281/zenodo.24290225  
**Release Binary Archive:** SITI_ITcon_Q1_Reproducibility_Package.zip (164 files; 57,545,939 bytes; SHA-256: 4a1177f65c0930842963ac351dbdec1fcef80126588f252e187e3db751ee2443)

# SITI Three-Layer Reproducibility Package — *ITcon* Vol. 32 (2027)

**Article Title:** *Orthogonal Ontology Factorization for Semantic Interoperability in Transport Infrastructure*  
**Authors:** Juan C. Gómez (Corresponding Author: `jc.gomez1988@uniandes.edu.co`), Rodrigo F. Herrera, Karen M. Castañeda, and Juan F. Correal  
**Journal:** *Journal of Information Technology in Construction (ITcon)*, Vol. 32 (2027)  
**Active Content-Addressable Semantic (CAS) Release:** `b6bd01f850790ad22d399b95545f73d2` (Stage S4)  
**License:** Creative Commons Attribution 4.0 International (`CC BY 4.0`)

## 1. Unified Folder Hierarchy (High Cognitive Clarity for Peer Review)

Unzipping `SITI_ITcon_Q1_Reproducibility_Package.zip` yields a clean, self-contained seven-folder hierarchy matching **Section 2**, **Section 3**, **Appendix A**, and **Table 8** of the manuscript:

1. `01_Supplementary_Appendices_A_to_F/` — Unified Supplementary Volume (`.docx`, `.pdf`, `.md`, `.tex`) and standalone Markdown files for **Supplementary Appendices A through F** (Table 8 Rows 1–7).
2. `02_Manuscript_Figures_Tables_and_Bibliography/` — All **9 publication figures** at lossless `300.0 DPI` (`.png` + Type-42 vector `.pdf`), all **8 manuscript tables** (`.csv`, `.md`, `.tex` booktabs), and the **107 APA 7th edition verified references** (`References_107_Verified_APA7.bib`).
3. `03_Layer1_C1_Semantic_Core_OWL_SKOS_SHACL/` — Native SITI Layer 1 (`C1`) semantic artifacts under CAS `b6bd01f8`: `manifest.json`, the `10` canonical taxonomic CSV tables (`A10`–`A50` in Language A: `4,686` classes; `B10`–`B50` in Language B: `11,544` classes = `16,230` active unique classes), isomorphic `OWL 2 DL` ontologies (`.ttl` / `.owl`, `438,194` triples), pentalingual `W3C SKOS` lexicon (`2,892` terms), `104` closed-world `W3C SHACL` shapes, `849` `ISO 16739-1:2024` property/quantity sets, and deterministic compiler `capa1_build_siti_ontology.py` (Table 8 Row 8).
4. `04_Layer2_C2_Property_Graph_and_13_Recipes/` — Native SITI Layer 2 (`C2`) topological Labeled Property Graph (`16,232` `UUIDv5` nodes, `793` inter-tabular edges, `316` Markov blanket anchors) and `13` compositional assembly recipes (`REC-A-01`..`REC-B-06`) in JSON and `openCypher` (Table 8 Row 9).
5. `05_Layer3_C3_Columnar_Lakehouse_and_Geodesy/` — SITI Layer 3 (`C3`) Apache Parquet analytical stores (`226,324` national assets, `8`-column operational SoA slice, `2,715,888`-row `UUIDv7` Unboxed EAV telemetry store, `5,011` local `ENU`/`OpenUSD` instances, `18,112` differential confrontation matrix units, `526` decoupled `INVIAS` APU items, `603` cold-CDE ingestion ledger, and `2` `SHA-256` PII-pseudonymized public tables under Colombian Law 1581/2012) (Table 8 Rows 10–14).
6. `06_Verification_Scripts_and_Checkpoints/` — All `13` read-only (`os.O_RDONLY`) Python verification, benchmark, and `300 DPI` plotting scripts (`wave1_...py` through `wave7_...py` + `generate_figures_300dpi.py`) and all `7` cryptographic JSON checkpoints (`wave1_checkpoint.json` through `wave7_ablation_checkpoint.json`, Table 8 Rows 1–7).
7. `07_Empirical_Results_Datasets_Waves_1_to_7/` — All `56` empirical output datasets (`.csv`, `.parquet`, `.json`) organized cleanly into `Wave_1_...` through `Wave_7_...` subfolders.

> **Note on Native Colombian SITI Identifiers (`03_`, `04_`, `05_`):** Official institutional container filenames and schema columns in Layers 1–3 preserve their exact Spanish SITI regulatory identifiers so that all cryptographic `SHA-256` digests in `manifest.json` (`bda830878ebd24c1`) and **Table 8** remain bit-identical to the national production repository. Full English translations of every SITI filename, table prefix, edge type, and Parquet column are provided in `DATA_DICTIONARY_AND_SITI_SCHEMA_GUIDE.md`.

## 2. Quickstart Verification Commands

To verify cryptographic `SHA-256` integrity across the entire unpacked directory on macOS or Linux:

```bash
shasum -a 256 -c SHA256SUMS.txt
```

Reference benchmark workstation: Apple MacBook Pro (`M4 Pro`, `arm64`, `12` cores, `24.0 GB` unified RAM, macOS `27.2`), Python `3.14.6`, `DuckDB 1.5.5`, `PyArrow 23.0.1`, `SQLite 3.53.2`, `RDFLib 7.6.0`, `pySHACL`, `SciPy`, and `NumPy`.
