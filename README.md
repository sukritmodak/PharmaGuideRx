# PharmaGuideRx

**Personalized Pharmacogenomics, Explained.**

PharmaGuideRx is an educational and research-oriented pharmacogenomics decision-support prototype. It demonstrates how pharmacogene, medication, and phenotype information can be connected to transparent, rule-based interpretations.

> **Important:** This is a research/educational prototype. It is not a medical device and must not be used as a substitute for a qualified clinician, validated laboratory, or current CPIC/DPWG/FDA guidance.

## Features
- Interactive Streamlit web application
- Patient profile and medication selection
- Pharmacogene and phenotype selection
- Explainable local gene-drug rules
- Transparent phenotype → interpretation → potential action pathway
- Evidence/source notes in the interface
- Demonstration pharmacogenomics dataset
- No API keys required for the demo
- GitHub Actions Python syntax check

## Demonstration examples
- CYP2C19 → Clopidogrel
- CYP2D6 → Codeine
- TPMT → Thiopurines
- DPYD → Fluoropyrimidines
- SLCO1B1 → Simvastatin

The examples are simplified for software demonstration. Clinical recommendations must be verified against current authoritative guidance and patient-specific clinical information.

## Run locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app/main.py
```

## Project structure

```text
PharmaGuideRx/
├── app/
│   ├── main.py
│   └── rules.py
├── data/
│   └── gene_drug_demo.json
├── .github/
│   └── workflows/
│       └── syntax-check.yml
├── .gitignore
├── .env.example
├── LICENSE
├── PROJECT_STATUS.md
├── README.md
└── requirements.txt
```

## Future development
Potential next stages include validated CPIC/DPWG guideline ingestion, VCF and star-allele support, evidence/version provenance, FHIR/EHR interoperability, authentication, audit logging, clinical validation, and regulatory review.

## License
MIT License.
