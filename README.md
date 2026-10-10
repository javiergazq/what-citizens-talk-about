# What Citizens Talk About

## Analysis code and reproducibility materials

This repository contains the analysis code, lexical resources, and reproducibility materials for the study:

> **What Citizens Talk About: Lexical Entity Detection and Negative Review Burden in Online Reviews of a Public Healthcare System**

**Authors:** Javier Gazquez-Garcia, Mª Mar Martinez-Lentisco, Sonia Martinez-Castro, Francisco José Sanchez-Laguna, Carlos Luis Sánchez-Bocanegra

The study analyzes unsolicited Google Maps reviews of publicly funded primary care and hospital facilities in the Andalusian Health Service (*Servicio Andaluz de Salud*), Spain.

The analytical approach identifies service entities and explicit discourse markers using a transparent lexical instrument, quantifies the concentration of negatively rated feedback through **negative review burden**, compares primary and hospital care, and evaluates the detection instrument against manual annotation.

---

## Study at a glance

| Characteristic | Value |
|---|---:|
| Initial review extraction | 66,606 reviews |
| Initial facility sampling frame | 922 facilities |
| Final analytical corpus | **47,589 reviews** |
| Facilities in the analytical corpus | **812** |
| Service entities | **6** |
| Lexical discourse markers | **7** |
| Manual validation sample | **400 reviews** |
| Facility-clustered bootstrap | **2,000 replicates** |

The final lexicon was fixed before manual validation and was not subsequently modified. Validation therefore evaluates the prespecified detection instrument rather than an instrument adapted to the validation results.

---

## Data provenance

The analytical corpus is the same as that defined in the companion longitudinal study of public perception of the Andalusian public health system.

The original sampling frame comprised **922 publicly funded health care facilities** identified from the official directory of the Andalusian Health Service (*Servicio Andaluz de Salud*), Spain. Google Maps reviews associated with these facilities were retrieved through an automated data-collection pipeline.

The initial extraction yielded **66,606 reviews**. After filtering for valid star ratings, free-text content, minimum text length, and language, the final analytical corpus used in this study comprised:

- **47,589 textual reviews**
- **812 health care facilities**

The complete facility-identification, review-collection, and initial corpus-construction procedure is described in the companion study:

> Gazquez-Garcia J, Sánchez-Bocanegra CL, Fernández-Llatas C.  
> *Public Perception of Health Care Before, During, and After COVID-19: A Longitudinal Analysis of Online Reviews.*  
> Gazquez-Garcia J, Sánchez-Bocanegra CL, Fernandez-Llatas C. Public Perception of Health Care Before, During, and After COVID-19: Longitudinal Analysis of Online Reviews. J Med Internet Res 2026;28:e96824. doi: 10.2196/96824

This repository starts from the resulting local review-level dataset (`data/Merged.csv`) and does **not** reproduce the original Google Maps data-collection process.

---

## Main analytical components

The repository contains the analyses underlying the manuscript:

- detection of six service entities;
- detection of seven complaint and praise discourse markers;
- comparison of entity salience between primary and hospital care;
- estimation of **negative review burden**;
- analysis of burden across facility types;
- sentiment-stratified logistic regression of discourse markers;
- facility-clustered bootstrap confidence intervals;
- manual validation using complementary sampling frames;
- inter-rater reliability assessment;
- trigger-level validation analyses;
- sensitivity analyses for temporal restriction, lexical specification, duplicate records, and temporal periods.

---

## Negative review burden

For entity \(e\), negative review burden is defined as:

\[
B_e =
P(E_e = 1)
\times
P(Y = \mathrm{negative} \mid E_e = 1)
=
P(E_e = 1,\ Y = \mathrm{negative})
\]

where \(E_e = 1\) indicates that entity \(e\) is mentioned.

Negative review burden therefore represents the proportion of all reviews that both mention a given entity and receive a negative review-level star rating.

It is used as a transparent descriptive prioritization measure. It should **not** be interpreted as:

- entity-specific sentiment;
- a direct measure of dissatisfaction with that entity;
- a measure of health care quality;
- a psychometric or composite score.

---

## Repository contents

| File | Description |
|---|---|
| `Paper2_analysis.ipynb` | Main analysis notebook. Reproduces corpus verification, lexical analyses, tables, figures, sensitivity analyses, and multimedia appendices. Validation-specific outputs additionally require the restricted annotation files described below. |
| `paper2_lexicon.py` | Original and final lexical specifications, disambiguation rules, and entity and discourse-marker detection functions. |
| `requirements.txt` | Python package versions used for the analysis. |
| `.gitignore` | Prevents accidental inclusion of review-level data, restricted annotation files, and generated outputs. |
| `LICENSE` | MIT License covering the analysis code and lexical resources. |

The notebook is distributed without stored cell outputs to avoid inadvertent disclosure of review-level textual content.

---

## Notebook workflow

| Section | Analysis | Manuscript output |
|---|---|---|
| 1 | Canonical corpus construction and verification | Methods |
| 2 | Detection using the final lexicon | Methods |
| 3 | Pre-validation lexical audit and comparison of original and final lexicons | Methods |
| 4 | Validation sampling frames | Methods |
| 5 | Precision, recall, F1, and inter-rater agreement | Validation analyses* |
| 6 | Sensitivity to exact duplicate records | Sensitivity analyses |
| 7 | Negative review burden and facility-type analyses | Table 1, Figures 1-2 |
| 8 | Lexical discourse-marker analyses | Table 2 |
| 9 | Multimedia appendices | Multimedia Appendices 1-4 |
| 10 | Detailed validation outputs | Table 3, Multimedia Appendix 5* |

\* Requires restricted manual-annotation data.

---

## Multimedia Appendices

The analysis notebook generates five supplementary analytical appendices:

| Appendix | Content |
|---|---|
| **Multimedia Appendix 1** | Complete entity and lexical-marker dictionaries, phrase lists, disambiguation rules, and documentation of the original and final lexicons |
| **Multimedia Appendix 2** | Manual annotation guide used for validation |
| **Multimedia Appendix 3** | Negative review burden by facility type, facility classification mapping, and detailed results for outpatient consultation centers |
| **Multimedia Appendix 4** | Sensitivity analyses |
| **Multimedia Appendix 5** | Detailed validation analyses, alternative estimators, and trigger-level performance |

The completed STROBE reporting checklist is provided separately with the manuscript as **Multimedia Appendix 6**.

---

## Reproducing the analysis

### Software environment

The analyses were conducted using **Python 3.13.5**.

Install the required packages from the repository root:

```bash
pip install -r requirements.txt